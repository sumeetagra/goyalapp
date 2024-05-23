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
def GetSupplierBills(doctype, StartDate, EndDate):

	if StartDate > EndDate:
		frappe.throw(_("Start Date shall be before the End Date."))

	return {
		"result": "SG is Here!",
		"Start Date": StartDate,
		"End Date": EndDate,
	}

	"""Update password for the current user.

	Args:
	        new_password (str): New password.
	        logout_all_sessions (int, optional): If set to 1, all other sessions will be logged out. Defaults to 0.
	        key (str, optional): Password reset key. Defaults to None.
	        old_password (str, optional): Old password. Defaults to None.
	"""

	if len(new_password) > MAX_PASSWORD_SIZE:
		frappe.throw(_("Password size exceeded the maximum allowed size."))

	result = test_password_strength(new_password)
	feedback = result.get("feedback", None)

	if feedback and not feedback.get("password_policy_validation_passed", False):
		handle_password_test_fail(feedback)

	res = _get_user_for_update_password(key, old_password)
	if res.get("message"):
		frappe.local.response.http_status_code = 410
		return res["message"]
	else:
		user = res["user"]

	logout_all_sessions = cint(logout_all_sessions) or frappe.db.get_single_value(
		"System Settings", "logout_on_password_reset"
	)
	_update_password(user, new_password, logout_all_sessions=cint(logout_all_sessions))

	user_doc, redirect_url = reset_user_data(user)

	# get redirect url from cache
	redirect_to = frappe.cache.hget("redirect_after_login", user)
	if redirect_to:
		redirect_url = redirect_to
		frappe.cache.hdel("redirect_after_login", user)

	frappe.local.login_manager.login_as(user)

	frappe.db.set_value("User", user, "last_password_reset_date", today())
	frappe.db.set_value("User", user, "reset_password_key", "")

	if user_doc.user_type == "System User":
		return "/app"
	else:
		return redirect_url or "/"



@frappe.whitelist(allow_guest=True)
def get(doctype, StartDate, EndDate, txt=None, limit_start=0, fields=None, cmd=None, limit=20, **kwargs):
	return {
		"result": "SG is Here!",
	}

	"""Returns processed HTML page for a standard listing."""
	limit_start = cint(limit_start)

	if frappe.is_table(doctype):
		frappe.throw(_("Child DocTypes are not allowed"), title=_("Invalid DocType"))

	if not txt and frappe.form_dict.search:
		txt = frappe.form_dict.search
		del frappe.form_dict["search"]

	controller = get_controller(doctype)
	meta = frappe.get_meta(doctype)

	filters = prepare_filters(doctype, controller, kwargs)

	_get_list = get_transaction_list

	kwargs = dict(
		doctype=doctype,
		txt=txt,
		filters=filters,
		limit_start=limit_start,
		limit_page_length=limit,
		order_by="name",
	)

	limit_start = cint(limit_start)
	raw_result = _get_list(**kwargs)
	show_more = len(raw_result) > limit
	if show_more:
		raw_result = raw_result[:-1]

	if not raw_result:
		return {"result": []}

	from frappe.utils.response import json_handler

	return {
		"raw_result": json.dumps(raw_result, default=json_handler),
		"result": raw_result,
	}

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


def prepare_filters(doctype, controller, kwargs):
	for key in kwargs.keys():
		try:
			kwargs[key] = json.loads(kwargs[key])
		except ValueError:
			pass
	filters = frappe._dict(kwargs)

	return filters	