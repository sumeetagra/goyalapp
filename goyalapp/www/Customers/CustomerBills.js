frappe.ready(async () => {
	initialise_select_date();
});

async function initialise_select_date() {
	setup_date_picker();
	hide_next_button();
}

function setup_date_picker() {
	let date_picker = document.getElementById("appointment-date");
	let today = new Date();
	date_picker.min = today.toISOString().substr(0, 10);
	today.setDate(today.getDate() + window.appointment_settings.advance_booking_days);
	date_picker.max = today.toISOString().substr(0, 10);
}

function hide_next_button() {
	let next_button = document.getElementById("next-button");
	next_button.disabled = true;
	next_button.onclick = () => frappe.msgprint(__("Please select a date and time"));
}