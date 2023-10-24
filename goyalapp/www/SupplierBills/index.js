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
    date_picker.disabled = true;
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

async function get_time_slots(date, timezone) {
    let slots = (await frappe.call({
        method: 'erpnext.www.book_appointment.index.get_appointment_slots',
        args: {
            date: date,
            timezone: timezone
        }
    })).message;
    return slots;
}

async function update_time_slots(selected_date, selected_timezone) {
    let timeslot_container = document.getElementById('timeslot-container');
    window.slots = await get_time_slots(selected_date, selected_timezone);
    clear_time_slots();
    if (window.slots.length <= 0) {
        let message_div = document.createElement('p');
        message_div.innerHTML = __("There are no slots available on this date");
        timeslot_container.appendChild(message_div);
        return
    }
    window.slots.forEach((slot, index) => {
        // Get and append timeslot div
        let timeslot_div = get_timeslot_div_layout(slot)
        timeslot_container.appendChild(timeslot_div);
    });
    set_default_timeslot();
}

function get_timeslot_div_layout(timeslot) {
    let start_time = new Date(timeslot.time)
    let timeslot_div = document.createElement('div');
    timeslot_div.classList.add('time-slot');
    if (!timeslot.availability) {
        timeslot_div.classList.add('unavailable')
    }
    timeslot_div.innerHTML = get_slot_layout(start_time);
    timeslot_div.id = timeslot.time.substring(11, 19);
    timeslot_div.addEventListener('click', select_time);
    return timeslot_div
}

function clear_time_slots() {
    // Clear any existing divs in timeslot container
    let timeslot_container = document.getElementById('timeslot-container');
    while (timeslot_container.firstChild) {
        timeslot_container.removeChild(timeslot_container.firstChild);
    }
}

function get_slot_layout(time) {
    return `<span style="font-size: 1.2em;">${__("Sg is HERE") }</span><br><span class="text-muted small">${__("to") } ${__("Sg is HERE") }</span>`;
}

function select_time() {
    if (this.classList.contains('unavailable')) {
        return;
    }
    let selected_element = document.getElementsByClassName('selected');
    if (!(selected_element.length > 0)) {
        this.classList.add('selected');
        show_next_button();
        return;
    }
    selected_element = selected_element[0]
    window.selected_time = this.id;
    selected_element.classList.remove('selected');
    this.classList.add('selected');
    show_next_button();
}

function set_default_timeslot() {
    let timeslots = document.getElementsByClassName('time-slot')
    // Can't use a forEach here since, we need to break the loop after a timeslot is selected
    for (let i = 0; i < timeslots.length; i++) {
        const timeslot = timeslots[i];
        if (!timeslot.classList.contains('unavailable')) {
            timeslot.classList.add('selected');
            break;
        }
    }
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
    let timeslot_container = document.getElementById('timeslot-container');
    let message_div = document.createElement('div');
    message_div.innerHTML = listdata1.result;
    timeslot_container.appendChild(message_div);
}

function get_form_data() {
    let contact = {};
    let inputs = ['name', 'skype', 'number', 'notes', 'email'];
    inputs.forEach((id) => contact[id] = document.getElementById(`customer_${id}`).value)
    return contact
}