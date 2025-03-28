# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
import frappe.www.list
from frappe import _

no_cache = 1

def get_context(context):
	if frappe.session.user != "Guest":
		context.current_user = frappe.get_doc("User", frappe.session.user)
	context.show_sidebar = False
	context.full_width = True
	context.only_static = False	