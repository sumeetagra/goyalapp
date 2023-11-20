from . import __version__ as app_version

app_name = "goyalapp"
app_title = "Goyal App"
app_publisher = "Go4all Technologies Pvt Ltd"
app_description = "Personalised App for Goyal Group"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@goyalironsteel.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/goyalapp/css/goyalapp.css"
# app_include_js = "/assets/goyalapp/js/goyalapp.js"

# include js, css files in header of web template
web_include_css = "/assets/goyalapp/css/goyalapp.css"
# web_include_js = "/assets/goyalapp/js/goyalapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "goyalapp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }
has_website_permission = {
	"Sales Order": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Quotation": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Sales Invoice": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Supplier Quotation": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Purchase Order": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Purchase Invoice": "goyalapp.controllers.goyalwebsite.has_website_permission",
	"Material Request": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Delivery Note": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Issue": "erpnext.support.doctype.issue.issue.has_website_permission",
	"Timesheet": "erpnext.controllers.website_list_for_contact.has_website_permission",
}
# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "goyalapp.utils.jinja_methods",
# 	"filters": "goyalapp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "goyalapp.install.before_install"
# after_install = "goyalapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "goyalapp.uninstall.before_uninstall"
# after_uninstall = "goyalapp.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "goyalapp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"goyalapp.tasks.all"
# 	],
# 	"daily": [
# 		"goyalapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"goyalapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"goyalapp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"goyalapp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "goyalapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "goyalapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "goyalapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"goyalapp.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
