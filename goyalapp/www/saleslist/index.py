import frappe
from frappe import _


def get_context(context):
	context.doc = frappe.get_all(
		"Sales Invoice",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={},
	)

	console.log(doc.name)