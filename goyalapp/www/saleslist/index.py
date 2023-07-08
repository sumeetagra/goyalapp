import frappe
from frappe import _


def get_context(context):
	context.doc = frappe.get_all(
		"Sales Invoice",
		fields=["name", "customer"],
		filters={},
	)
	context.body_class="hold-transition skin-blue sidebar-mini"
