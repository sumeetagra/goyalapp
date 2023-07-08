import frappe
from frappe import _


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_doc(doctype='Sales Invoice')

	context.enabled_checkout = frappe.get_doc("E Commerce Settings").enable_checkout

	if not frappe.has_website_permission(context.doc):
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

	context.available_loyalty_points = 0.0
	if context.doc.get("customer"):
		# check for the loyalty program of the customer
		customer_loyalty_program = frappe.db.get_value(
			"Customer", context.doc.customer, "loyalty_program"
		)

		if customer_loyalty_program:
			from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
				get_loyalty_program_details_with_points,
			)

			loyalty_program_details = get_loyalty_program_details_with_points(
				context.doc.customer, customer_loyalty_program
			)
			context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

	context.show_pay_button = frappe.db.get_single_value("Buying Settings", "show_pay_button")
	context.show_make_pi_button = False
	if context.doc.get("supplier"):
		# show Make Purchase Invoice button based on permission
		context.show_make_pi_button = frappe.has_permission("Purchase Invoice", "create")
