frappe.ready(async () => {
	initialise_select_date();
});

async function initialise_select_date() {
	setup_date_picker();
	hide_next_button();
}

function setup_date_picker() {
	let date_picker = document.getElementById("open-date");
	let today = new Date();
	date_picker.min = today.toISOString().substr(0, 10);
	today.setDate(today.getDate() + 5);
	date_picker.max = today.toISOString().substr(0, 10);
}

function hide_next_button() {
	let next_button = document.getElementById("details-button");
	next_button.disabled = true;
	next_button.onclick = () => frappe.msgprint(__("Please select a date and time"));
}