import frappe
from frappe import _


def get_context(context):
	context.doc = frappe.get_all(
		"Sales Invoice",
		fields=["name","customer","customer_name"],
		filters={},
	)
