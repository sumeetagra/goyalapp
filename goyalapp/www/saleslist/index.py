import frappe
from frappe import _


def get_context(context):
	context.doc = frappe.get_all(
		"Sales Invoice",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)

	console.log(doc.name)