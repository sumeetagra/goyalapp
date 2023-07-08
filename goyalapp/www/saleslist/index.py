import frappe
from frappe import _


def get_context(context):
	context.doc = frappe.get_doc('Sales Invoice')
	console.log(doc.name)
    return context