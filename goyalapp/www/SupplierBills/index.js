frappe.ready(async () => {
    initialise_select_date();
})

async function initialise_select_date() {
    setup_start_datepicker();
    hide_fetch_button();
    hide_end_date();
}

function setup_start_datepicker() {
    let date_picker = document.getElementById('start-date');
    let today = new Date();
    let timediff = '15';
    date_picker.max = today.toISOString().substr(0, 10);
    today.setDate(today.getDate() - timediff);
    date_picker.min = today.toISOString().substr(0, 10);
}

function hide_fetch_button() {
    let next_button = document.getElementById('fetch-button');
    next_button.disabled = true;
}

function hide_end_date() {
    let date_picker = document.getElementById('stop-date');
    let dataTable = document.getElementById('ctl00_ContentPlaceHolder1_tr_data');
    date_picker.disabled = true;
    dataTable.style.display = 'none';

}

function show_end_date() {
    let date_picker = document.getElementById('stop-date');
    date_picker.disabled = false;
    let today = new Date();
    let timediff = '15';
    date_picker.max = today.toISOString().substr(0, 10);
    today.setDate(today.getDate() - timediff);
    date_picker.min = today.toISOString().substr(0, 10);
}

function show_fetch_button() {
    let next_button = document.getElementById('fetch-button');
    next_button.disabled = false;
}

function show_next_button() {
    let next_button = document.getElementById('next-button');
    next_button.disabled = false;
    next_button.onclick = setup_details_page;
}

function on_start_date_select() {
    let date_picker = document.getElementById('start-date');
    if (date_picker.value === '') {
        hide_fetch_button();
        frappe.throw(__('Please select a date'));
    }
    show_end_date();
    window.selected_date = date_picker.value;
}

function on_end_date_select() {
    let date_picker3 = document.getElementById('stop-date');
    if (date_picker3.value === '') {
        hide_fetch_button();
        frappe.throw(__('Please select a date'));
    }
    show_fetch_button();
    window.selected_date = date_picker3.value;
}

function get_timeslot_div_layout(timeslot) {
    let timeslot_div = document.createElement('tr');
    timeslot_div.classList.add('tab_content')
    timeslot_div.classList.add('odd')
    timeslot_div.innerHTML = get_slot_layout(timeslot);
    timeslot_div.id = timeslot.name;
    return timeslot_div
}

function get_slot_layout(time) {
    let DocName = time.name;
    let SupplierCode = time.supplier;
    let SupplierNm = time.supplier_name;
    let SupplierDoc = time.bill_no;
    let SupplierDt = time.bill_date;
    let TotalQty = time.total_qty;
    let incoterm = time.incoterm;
    let SupplierBs = time.base_total;
    let SupplierTx = time.total_taxes_and_charges;
    let SupplierTl = time.rounded_total;
    let SupplierOs = time.outstanding_amount;    
    return `<tr class="tab_content odd">
    <td>${DocName}</td>
    <td>${SupplierCode}</td>
    <td>${SupplierNm}</td>
    <td>${SupplierDoc}
    <br>${SupplierDt}</td>
    <td>${TotalQty}</td>
    <td>${incoterm}</td>
    <td>${SupplierBs}</td>
    <td>${SupplierTx}</td>
    <td>${SupplierTl}</td>
    <td>${SupplierOs}</td>
    </tr>`;
}


function navigate_to_page(page_number) {
    let page1 = document.getElementById('select-date-time');
    let page2 = document.getElementById('enter-details');
    switch (page_number) {
        case 1:
            page1.style.display = 'block';
            page2.style.display = 'none';
            break;
        case 2:
            page1.style.display = 'none';
            page2.style.display = 'block';
            break;
        default:
            break;
    }
}

function setup_details_page() {
    let next_button = document.getElementById('fetch-button');

    navigate_to_page(2)
    let date_container = document.getElementsByClassName('date-span')[0];
    let time_container = document.getElementsByClassName('time-span')[0];
    setup_search_params();
    date_container.innerHTML = moment(window.selected_date).format("MMM Do YYYY");
    time_container.innerHTML = moment(window.selected_time, "HH:mm:ss").format("LT");
}

function setup_search_params() {
    let search_params = new URLSearchParams(window.location.search);
    let customer_name = search_params.get("name")
    let customer_email = search_params.get("email")
    let detail = search_params.get("details")
    if (customer_name) {
        let name_input = document.getElementById("customer_name");
        name_input.value = customer_name;
        name_input.disabled = true;
    }
    if(customer_email) {
        let email_input = document.getElementById("customer_email");
        email_input.value = customer_email;
        email_input.disabled = true;
    }
    if(detail) {
        let detail_input = document.getElementById("customer_notes");
        detail_input.value = detail;
        detail_input.disabled = true;
    }
}

async function get_list_data(date, timezone) {
    let listingdata = (await frappe.call({
        method: 'goyalapp.www.goyalapi.get',
        args: {
            doctype: date
        }
    })).message;
    return listingdata;
}


async function submit() {
    let button = document.getElementById('fetch-button');
    button.disabled = true;
    let listDoctype = 'Purchase Invoice';
    let listDoctype1 = 'Purchase Invoice';
    window.listdata1 = await get_list_data(listDoctype, listDoctype1);
    let timeslot_container = document.getElementById('slot-container');
    let dataTable = document.getElementById('ctl00_ContentPlaceHolder1_tr_data');
    dataTable.style.display = 'block';
    let timeslot_div = document.createElement('tbody');
    window.listdata1.result.forEach(slot => {
        // Get and append timeslot div
        let timeslot_div = get_timeslot_div_layout(slot)
        timeslot_container.appendChild(timeslot_div);
    });


}

function get_form_data() {
    let contact = {};
    let inputs = ['name', 'skype', 'number', 'notes', 'email'];
    inputs.forEach((id) => contact[id] = document.getElementById(`customer_${id}`).value)
    return contact
}