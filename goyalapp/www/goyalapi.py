# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import frappe
from frappe import _
from frappe.model.document import Document, get_controller
from frappe.utils import cint, quoted
from frappe.utils.user import is_website_user
from frappe.website.path_resolver import resolve_path

no_cache = 1


def get_context(context, **dict_params):
	"""Returns context for a list standard list page.
	Will also update `get_list_context` from the doctype module file"""
	frappe.local.form_dict.update(dict_params)
	doctype = frappe.local.form_dict.doctype
	context.parents = [{"route": "me", "title": _("My Account")}]
	context.meta = frappe.get_meta(doctype)
	context.update(get_list_context(context, doctype) or {})
	context.doctype = doctype
	context.txt = frappe.local.form_dict.txt
	context.update(get(**frappe.local.form_dict))


@frappe.whitelist(allow_guest=True)
def get(doctype, txt=None, fields=None, filters=None, limit_start=0, limit=20, pathname=None, web_form_name=None, **kwargs):
	"""Returns processed HTML page for a standard listing."""
	limit_start = cint(limit_start)

	if frappe.is_table(doctype):
		frappe.throw(_("Child DocTypes are not allowed"), title=_("Invalid DocType"))

	if fields:
		fields = json.loads(fields)

	if not txt and frappe.form_dict.search:
		txt = frappe.form_dict.search
		del frappe.form_dict["search"]

	controller = get_controller(doctype)
	meta = frappe.get_meta(doctype)

	list_context = get_list_context(frappe._dict(), doctype, web_form_name)
	list_context.title_field = getattr(controller, "website", {}).get(
		"page_title_field", meta.title_field or "name"
	)

	if list_context.filters:
		filters.update(list_context.filters)

	_get_list = get_transaction_list

	kwargs = dict(
		doctype=doctype,
		txt=txt,
		filters=filters,
		limit_start=limit_start,
		limit_page_length=limit,
		order_by=list_context.order_by or "modified desc",
	)

	# allow guest if flag is set
	if not list_context.get_list and (list_context.allow_guest or meta.allow_guest_to_view):
		kwargs["ignore_permissions"] = True

	raw_result = _get_list(**kwargs)

	# list context to be used if called as rendered list
	frappe.flags.list_context = list_context

	return {
		"raw_result": raw_result,
		"SG": kwargs,
		"SG1": filters,
	}

def get_transaction_list(
	doctype,
	txt=None,
	filters=None,
	limit_start=0,
	limit_page_length=20,
	order_by="modified",
	custom=False,
):
	user = frappe.session.user
	ignore_permissions = False

	if not filters:
		filters = {}

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else 1
		return filters

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = (
			"Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
		)
		# find party for this contact
		customers, suppliers = get_customers_suppliers(parties_doctype, user)

		if customers:
			if doctype == "Quotation":
				filters["quotation_to"] = "Customer"
				filters["party_name"] = ["in", customers]
			else:
				filters["customer"] = ["in", customers]
		elif suppliers:
			filters["supplier"] = ["in", suppliers]
		elif not custom:
			return []

		if doctype == "Request for Quotation":
			parties = customers or suppliers
			return rfq_transaction_list(parties_doctype, doctype, parties, limit_start, limit_page_length)

		# Since customers and supplier do not have direct access to internal doctypes
		ignore_permissions = True

		if not customers and not suppliers and custom:
			ignore_permissions = False
			filters = {}

	transactions = get_list_for_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="modified desc",
	)

	if custom:
		return transactions

	return post_process(doctype, transactions)

def get_list_for_transactions(
	doctype,
	txt,
	filters,
	limit_start,
	limit_page_length=20,
	ignore_permissions=False,
	fields=None,
	order_by=None,
):
	"""Get List of transactions like Invoices, Orders"""
	from frappe.www.list import get_list

	meta = frappe.get_meta(doctype)
	data = []
	or_filters = []

	for d in get_list(
		doctype,
		txt,
		filters=filters,
		fields="name",
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		ignore_permissions=ignore_permissions,
		order_by="modified desc",
	):
		data.append(d)

	if txt:
		if meta.get_field("items"):
			if meta.get_field("items").options:
				child_doctype = meta.get_field("items").options
				for item in frappe.get_all(child_doctype, {"item_name": ["like", "%" + txt + "%"]}):
					child = frappe.get_doc(child_doctype, item.name)
					or_filters.append([doctype, "name", "=", child.parent])

	if or_filters:
		for r in frappe.get_list(
			doctype,
			fields=fields,
			filters=filters,
			or_filters=or_filters,
			limit_start=limit_start,
			limit_page_length=limit_page_length,
			ignore_permissions=ignore_permissions,
			order_by=order_by,
		):
			data.append(r)

	return data

def prepare_filters(doctype, controller, kwargs):
	for key in kwargs.keys():
		try:
			kwargs[key] = json.loads(kwargs[key])
		except ValueError:
			pass
	filters = frappe._dict(kwargs)
	return filters.items()

	meta = frappe.get_meta(doctype)

	if hasattr(controller, "website") and controller.website.get("condition_field"):
		filters[controller.website["condition_field"]] = 1

	if filters.pathname:
		# resolve additional filters from path
		resolve_path(filters.pathname)
		for key, val in frappe.local.form_dict.items():
			if key not in filters and key != "flags":
				filters[key] = val

	# filter the filters to include valid fields only
	for fieldname, val in list(filters.items()):
		if not meta.has_field(fieldname):
			del filters[fieldname]

	return filters


def post_process(doctype, data):
	result = []
	for d in data:
		doc = frappe.get_doc(doctype, d.name)

		doc.status_percent = 0
		doc.status_display = []

		if doc.get("per_billed"):
			doc.status_percent += flt(doc.per_billed)
			doc.status_display.append(
				_("Billed") if doc.per_billed == 100 else _("{0}% Billed").format(doc.per_billed)
			)

		if doc.get("per_delivered"):
			doc.status_percent += flt(doc.per_delivered)
			doc.status_display.append(
				_("Delivered") if doc.per_delivered == 100 else _("{0}% Delivered").format(doc.per_delivered)
			)

		if hasattr(doc, "set_indicator"):
			doc.set_indicator()

		doc.status_display = ", ".join(doc.status_display)
		doc.items_preview = ", ".join(d.item_name for d in doc.items if d.item_name)
		result.append(doc)

	return result


def get_customers_suppliers(doctype, user):
	customers = []
	suppliers = []
	meta = frappe.get_meta(doctype)

	customer_field_name = get_customer_field_name(doctype)

	has_customer_field = meta.has_field(customer_field_name)
	has_supplier_field = meta.has_field("supplier")

	if has_common(["Supplier", "Customer"], frappe.get_roles(user)):
		suppliers = get_parents_for_user("Supplier")
		customers = get_parents_for_user("Customer")
	elif frappe.has_permission(doctype, "read", user=user):
		customer_list = frappe.get_list("Customer")
		customers = suppliers = [customer.name for customer in customer_list]

	return customers if has_customer_field else None, suppliers if has_supplier_field else None


def get_parents_for_user(parenttype: str) -> list[str]:
	portal_user = frappe.qb.DocType("Portal User")

	return (
		frappe.qb.from_(portal_user)
		.select(portal_user.parent)
		.where(portal_user.user == frappe.session.user)
		.where(portal_user.parenttype == parenttype)
	).run(pluck="name")


def has_website_permission(doc, ptype, user, verbose=False):
	doctype = doc.doctype
	customers, suppliers = get_customers_suppliers(doctype, user)
	if customers:
		return frappe.db.exists(doctype, get_customer_filter(doc, customers))
	elif suppliers:
		fieldname = "suppliers" if doctype == "Request for Quotation" else "supplier"
		return frappe.db.exists(doctype, {"name": doc.name, fieldname: ["in", suppliers]})
	else:
		return False

def get_list_context(context, doctype, web_form_name=None):
	from frappe.modules import load_doctype_module
	from frappe.website.doctype.web_form.web_form import get_web_form_module

	list_context = context or frappe._dict()
	meta = frappe.get_meta(doctype)

	def update_context_from_module(module, list_context):
		# call the user defined method `get_list_context`
		# from the python module
		if hasattr(module, "get_list_context"):
			out = frappe._dict(module.get_list_context(list_context) or {})
			if out:
				list_context = out
		return list_context

	# get context from the doctype module
	if not meta.custom:
		# custom doctypes don't have modules
		module = load_doctype_module(doctype)
		list_context = update_context_from_module(module, list_context)

	# get context for custom webform
	if meta.custom and web_form_name:
		webform_list_contexts = frappe.get_hooks("webform_list_context")
		if webform_list_contexts:
			out = frappe._dict(frappe.get_attr(webform_list_contexts[0])(meta.module) or {})
			if out:
				list_context = out

	# get context from web form module
	if web_form_name:
		web_form = frappe.get_doc("Web Form", web_form_name)
		list_context = update_context_from_module(get_web_form_module(web_form), list_context)

	# get path from '/templates/' folder of the doctype
	if not meta.custom and not list_context.row_template:
		list_context.row_template = meta.get_row_template()

	if not meta.custom and not list_context.list_template:
		list_context.template = meta.get_list_template() or "www/list.html"

	return list_context


def get_list(
	doctype,
	txt,
	filters,
	limit_start,
	limit_page_length=20,
	ignore_permissions=False,
	fields=None,
	order_by=None,
):
	meta = frappe.get_meta(doctype)
	if not filters:
		filters = []

	if not fields:
		fields = "distinct *"

	or_filters = []

	if txt:
		if meta.search_fields:
			for f in meta.get_search_fields():
				if f == "name" or meta.get_field(f).fieldtype in ("Data", "Text", "Small Text", "Text Editor"):
					or_filters.append([doctype, f, "like", "%" + txt + "%"])
		else:
			if isinstance(filters, dict):
				filters["name"] = ("like", "%" + txt + "%")
			else:
				filters.append([doctype, "name", "like", "%" + txt + "%"])

	return frappe.get_list(
		doctype,
		fields=fields,
		filters=filters,
		or_filters=or_filters,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		ignore_permissions=ignore_permissions,
		order_by=order_by,
	)