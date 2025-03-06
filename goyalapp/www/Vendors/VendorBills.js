frappe.ready(async () => {
//	alert("SG IS HERE2");
	initialise_select_date();
});

async function initialise_select_date() {
	setup_date_picker();
	hide_next_button();
}

function setup_date_picker() {
	let date_picker = document.getElementById("open-date");
	let date_picker1 = document.getElementById("close-date");
	date_picker1.disabled = true;
	let today = new Date("04/01/2024");
	let today1 = new Date();
	today.setDate(today.getDate() + 1);
	date_picker.min = today.toISOString().substr(0, 10);
	today1.setDate(today1.getDate() + 0);
	date_picker.max = today1.toISOString().substr(0, 10);
}

function hide_next_button() {
	let next_button = document.getElementById("details-button");
	next_button.disabled = true;
	next_button.onclick = () => frappe.msgprint(__("Please select a date and time"));
}

function show_datepicker_2() {
	let date_picker = document.getElementById("open-date").value;
	let date_picker1 = document.getElementById("close-date");
	let today = new Date(date_picker);
	let today1 = new Date();
	today.setDate(today.getDate() + 0);
	date_picker1.min = today.toISOString().substr(0, 10);
	today1.setDate(today1.getDate() + 0);
	date_picker1.max = today1.toISOString().substr(0, 10);
	date_picker1.disabled = false;
}

function show_next_button() {
	let startdate = document.getElementById("open-date").value;
	let enddate = document.getElementById("close-date").value;
	if (startdate > enddate) {
		frappe.show_alert(__("Invalid Dates Selected"));
		alert("Invalid Dates Selected");
		document.getElementById("close-date").value = "";
		let next_button = document.getElementById("details-button");
		next_button.disabled = true;
		return;
	} else
	{
		let next_button = document.getElementById("details-button");
		next_button.disabled = false;
		next_button.onclick = setup_details_page;	
	}
}

function setup_details_page() {
	let date_picker = document.getElementById("open-date").value;
	let date_picker1 = document.getElementById("close-date").value;
	let startdate = new Date(date_picker);
	let enddate = new Date(date_picker1);
	let next_button = document.getElementById("details-button");
	let differencetime = days_between(enddate.getTime(), startdate.getTime());
	if (differencetime > 3) {
		alert("Difference Between Start Date and End Date cannot be greater than 3 Days");
		document.getElementById("close-date").value = "";
		next_button.disabled = true;
		return;
	} else
	{
		next_button.disabled = true;
		let result_wrapper = $(".result");
		let content = "";
		$(content).appendTo(result_wrapper);
		let appointment = frappe.call({
			method: "goyalapp.www.goyalapi.GetSupplierBills",
			args: {
				StartDate: date_picker,
				EndDate: date_picker1,
				doctype: 'Purchase Invoice',
			},
			callback: (response) => {
				let data = response.message.DataResponse;
				if (data.length > 0) {
					for (let i = 0; i < data.length; i++) {
						const rowdata = data[i];
						alert(JSON.stringify(rowdata));
						let content = `<tr class='resultcontent'><td class='table-sr'>${i+1}</td><td class='table-sr'>${rowdata.posting_date}</td><td class='table-sr'>${rowdata.name}</td><td class='table-sr'>${rowdata.supplier}</td><td class='table-sr'>${rowdata.supplier_name}</td><td class='table-sr'>${rowdata.vehicle_no}</td><td class='table-sr'>${rowdata.total_qty}</td><td class='table-sr'>${rowdata.total}</td><td class='table-sr'>${rowdata.total_taxes_and_charges}</td><td class='table-sr'>${rowdata.rounded_total}</td><td class='table-sr'>${rowdata.status}</td></tr>`;
						$(content).appendTo(result_wrapper);
					}
				} else {
					frappe.show_alert(__("No Data Found!"));
					next_button.disabled = false;
				}
			},
		error: (err) => {
			frappe.show_alert(__("Something went wrong please try again"));
			button.disabled = false;
			next_button.disabled = false;
		},
		});
	}
}

function days_between(date1, date2) {
    // The number of milliseconds in one day
    const ONE_DAY = 1000 * 60 * 60 * 24;

    // Calculate the difference in milliseconds
    const differenceMs = Math.abs(date1 - date2);

    // Convert back to days and return
    return Math.round(differenceMs / ONE_DAY);
}

