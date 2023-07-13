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
def get(
	doctype, txt=None, limit_start=0, filters=None, cmd=None, limit=20, web_form_name=None, **kwargs
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

	list_context = get_list_context(frappe._dict(), doctype, web_form_name)
	list_context.title_field = getattr(controller, "website", {}).get(
		"page_title_field", meta.title_field or "name"
	)

	if list_context.filters:
		filters.update(list_context.filters)

	_get_list = list_context.get_list or get_list

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

