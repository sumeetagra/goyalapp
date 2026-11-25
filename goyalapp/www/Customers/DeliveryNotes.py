import frappe
def get_context(context):
 context.users = frappe.get_list("User", fields=["first_name", "last_name"])