# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import frappe
from frappe import _
from frappe.modules.utils import get_module_app
from frappe.model.document import Document, get_controller
from frappe.utils import cint, quoted, flt, has_common
from frappe.utils.user import is_website_user
from frappe.website.path_resolver import resolve_path


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
def GetSupplierBills(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if StartDate == '':
		frappe.throw(_("Please Enter Start Date."))

	if EndDate == '':
		frappe.throw(_("Please Enter End Date."))

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	if not filters:
		filters = {}

	filters["status"] = ["!=", "Cancelled"]

	filters["is_return"] = 0

	filters["posting_date"] = ["between", [StartDate, EndDate]]

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
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

	transactions = get_list_SG_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	return {
		"DataResponse": transactions
	}


@frappe.whitelist(allow_guest=True)
def GetCustomerBills(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if StartDate == '':
		return []

	if EndDate == '':
		frappe.throw(_("Please Enter End Date."))

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	if not filters:
		filters = {}

	filters["status"] = ["!=", "Cancelled"]

	filters["is_return"] = 0

	filters["posting_date"] = ["between", [StartDate, EndDate]]

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
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

	transactions = get_list_SG_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	return {
		"DataResponse": transactions
	}


@frappe.whitelist(allow_guest=True)
def GetCreditNotes(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if StartDate == '':
		frappe.throw(_("Please Enter Start Date."))

	if EndDate == '':
		frappe.throw(_("Please Enter End Date."))

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	if not filters:
		filters = {}

	filters["status"] = ["!=", "Cancelled"]

	filters["is_return"] = 1

	filters["posting_date"] = ["between", [StartDate, EndDate]]

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
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

	transactions = get_list_SG_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	return {
		"DataResponse": transactions
	}


@frappe.whitelist(allow_guest=True)
def GetDeliveryNotes(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if StartDate == '':
		frappe.throw(_("Please Enter Start Date."))

	if EndDate == '':
		frappe.throw(_("Please Enter End Date."))

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	if not filters:
		filters = {}

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else 1

	filters["posting_date"] = ["between", [StartDate, EndDate]]

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
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

	transactions = get_list_SG_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	return {
		"DataResponse": transactions
	}


@frappe.whitelist(allow_guest=True)
def GetUserLoggedDetails(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if not filters:
		filters = {}

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	doctype = "User"

	return {
		"User": user,
		"Doctype": parties,
		"customers": customers,
		"suppliers": suppliers,
		"Website": is_website_user(),
	}


@frappe.whitelist(allow_guest=True)
def GetPurchaseReceipts(doctype, StartDate, EndDate, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="creation", custom=False):

	user = frappe.session.user
	ignore_permissions = False

	if StartDate == '':
		frappe.throw(_("Please Enter Start Date."))

	if EndDate == '':
		frappe.throw(_("Please Enter End Date."))

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	if not filters:
		filters = {}

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else 1

	filters["posting_date"] = ["between", [StartDate, EndDate]]

	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
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

	transactions = get_list_SG_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	return {
		"DataResponse": transactions
	}


def get_list_SG_transactions(
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

	data = []
	if doctype in ["Purchase Invoice", "Purchase Receipt"]:
		fields = ["name", "posting_date", "supplier", "supplier_name", "total_qty", "total", "total_taxes_and_charges", "rounded_total", "outstanding_amount", "incoterm", "vehicle_no", "status"]
	elif doctype in ["Sales Invoice", "Delivery Note"]:
		fields = ["name", "posting_date", "customer", "customer_name", "total_qty", "total", "total_taxes_and_charges", "rounded_total", "outstanding_amount", "incoterm", "vehicle_no", "status"]
	else:
		fields = ["name"]

	or_filters = []

	for d in get_list(
		doctype,
		txt,
		filters=filters,
		fields=fields,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	):
		data.append(d)

	return data


def get_transaction_list(doctype,txt=None,filters=None,limit_start=0,limit_page_length=20,order_by="name",custom=False,):
	user = frappe.session.user
	ignore_permissions = False

	if not filters:
		filters = {}

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else 1

	"""Get List of transactions for custom doctypes"""
	from erpnext.controllers.website_list_for_contact import get_customers_suppliers, get_list_for_transactions, post_process

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
		fields="*",
		ignore_permissions=ignore_permissions,
		order_by="name",
	)


	if custom:
		return transactions

	return post_process(doctype, transactions)