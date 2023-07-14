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