# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import datetime
import json
import zoneinfo

import frappe
import frappe.www.list
from frappe import _
from frappe.utils.data import get_system_timezone
from frappe.utils import date_diff

no_cache = 1


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

	context.current_user = frappe.get_doc("User", frappe.session.user)
	context.show_sidebar = True
	context.full_width = True