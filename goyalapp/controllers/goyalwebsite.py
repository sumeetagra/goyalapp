# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import copy
import json

import frappe
from frappe import _
from frappe.utils import cstr, flt, has_common
from frappe.modules.utils import get_module_app
from frappe.utils.user import is_website_user



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



def get_customer_filter(doc, customers):
	doctype = doc.doctype
	filters = frappe._dict()
	filters.name = doc.name
	filters[get_customer_field_name(doctype)] = ["in", customers]
	if doctype == "Quotation":
		filters.quotation_to = "Customer"
	return filters

