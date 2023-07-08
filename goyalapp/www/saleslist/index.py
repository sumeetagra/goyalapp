import frappe
from frappe import _


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_all(
		"Sales Invoice",
		fields=["name", "customer"],
		filters={},
	)
	context.body_class="hold-transition skin-blue sidebar-mini"
