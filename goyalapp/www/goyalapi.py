# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import frappe
from frappe import _
from frappe.model.document import Document, get_controller
from frappe.utils import cint, quoted, flt, has_common
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
def get(
	doctype, txt=None, limit_start=0, fields=None, cmd=None, limit=20, **kwargs
):
	"""Returns processed HTML page for a standard listing."""
	limit_start = cint(limit_start)

	if frappe.is_table(doctype):
		frappe.throw(_("Child DocTypes are not allowed"), title=_("Invalid DocType"))

	if not txt and frappe.form_dict.search:
		txt = frappe.form_dict.search
		del frappe.form_dict["search"]

	controller = get_controller(doctype)
	meta = frappe.get_meta(doctype)

	if frappe.local.form_dict.get("fields"):
		fields = frappe.local.form_dict["fields"] = json.loads(frappe.local.form_dict["fields"])

	# set limit of records for frappe.get_list
	frappe.local.form_dict.setdefault(
		"limit_page_length",
		frappe.local.form_dict.limit or frappe.local.form_dict.limit_page_length or 20,
	)

	if frappe.local.form_dict.cmd:
		del frappe.local.form_dict["cmd"]

	_get_list = get_transaction_list

	kwargs = dict(
		doctype=doctype,
		fields=fields,
		txt=txt,
		filters=None,
		limit_start=limit_start,
		limit_page_length=limit,
		order_by="modified desc",
	)

	raw_result = _get_list(**kwargs)
	return raw_result

def get_transaction_list(
	doctype,
	fields,
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

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers, post_process

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else 1

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = ("Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype)
		# find party for this contact
		customers, suppliers = get_customers_suppliers(parties_doctype, user)
# 		parties = customers or suppliers

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

	"""Get List of transactions like Invoices, Orders"""
	from frappe.www.list import get_list

	data = 	get_list(
		doctype,
		txt,
		filters=filters,
		fields="name",
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		ignore_permissions=False,
		order_by="modified desc",
	)

	return data

def SI_transaction_list(parties_doctype, doctype, customers, limit_start, limit_page_length):
	data = frappe.db.get_list('tabSales Invoice')

	return data