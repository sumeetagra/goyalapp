import frappe
from frappe import _


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_all(
		"Sales Invoice",
		start=0, page_length=20,
		fields=["name", "customer"],
		filters={},
	)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	context.body_class="hold-transition skin-blue sidebar-mini"
