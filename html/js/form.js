jQuery(function () {
    var date = new Date();
    var minDate = new Date()
    minDate.setDate(date.getDate() - 1);

    var datepicker = $('#arrivalDate');
    if (datepicker.length > 0) {
        datepicker.datepicker({
            //format: "dd/mm/yyyy",
            format: "yyyy-mm-dd",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
            minDate: minDate
        }).on("change", function (e) {
            hideClientData();
            removeAvailableRooms();
        });
        //datepicker.val(moment(date).format('DD/MM/YYYY'))
        datepicker.val(moment(date).format('YYYY-MM-DD'))
    }
});

jQuery(function () {
    var date = new Date();
    date.setDate(date.getDate() + 1);
    var minDate = new Date()
    minDate.setDate(date.getDate() - 1);
    var datepicker = $('#departureDate');

    if (datepicker.length > 0) {
        datepicker.datepicker({
            //format: "dd/mm/yyyy",
            format: "yyyy-mm-dd",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
            minDate: minDate
        }).on("change", function (e) {
            hideClientData();
            removeAvailableRooms();
        });
        //datepicker.val(moment(date).format('DD/MM/YYYY'))
        datepicker.val(moment(date).format('YYYY-MM-DD'))
    }
});

// -----------------------------------------------------------------------------

function checkAvailability() {
    if (checkDateOrder()) {
        getAvailableRooms()
    } else {
        alert("Wrong dates!")
    }
}

function getAvailableRooms() {
    let arrivalInput = $("#arrivalDate").val();
    let departureInput = $("#departureDate").val();

    /*var arrivalDate = moment(arrivalInput, "DD/MM/YYYY");
    arrivalDate = arrivalDate.toDate();
    arrivalDate = moment(arrivalDate).format('YYYY-MM-DD')
    var departureDate = moment(departureInput, "DD/MM/YYYY");
    departureDate = departureDate.toDate();
    departureDate = moment(departureDate).format('YYYY-MM-DD')*/

    var arrivalDate = arrivalInput
    var departureDate = departureInput
    

    let url = "/api/available_rooms/" + arrivalDate + "/" + departureDate
    var answear

    try {
        let res = fetch(url).then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Something went wrong');
            }
        }).then((data) => {
            //console.log(data)
            var theDiv = document.getElementById("roomsAvailable");
            theDiv.innerHTML = "";
            answer = data.number

            // b
            var b_element = document.createElement("b");
            b_element.appendChild(
                document.createTextNode("Choose from available rooms:")
            )
            theDiv.appendChild(b_element);

            // break line
            var break_line = document.createElement("br");
            theDiv.appendChild(break_line);

            // info
            var row = document.createElement("div");
            row.classList.add('form-group');
            row.classList.add('row');

            var label = document.createElement("label");
            label.classList.add('col-sm-4');
            label.classList.add("col-form-label");
            label.htmlFor = 'numberOfRooms'
            label.appendChild(
                document.createTextNode('Double Room: ')
            )
            var double_room = document.createElement("select");
            double_room.classList.add('form-control');
            double_room.classList.add('col-sm-3');
            double_room.setAttribute('name', 'numberOfRooms')
            double_room.id = 'numberOfRooms';
            for (let i = 0; i <= answer.toString(); i++) {
                var opt = document.createElement('option');
                opt.value = i.toString();
                opt.innerHTML = i.toString();
                double_room.appendChild(opt);
            }
            double_room.onchange = function () {
                hideClientData()
            }
            row.appendChild(label);
            row.appendChild(double_room);
            theDiv.appendChild(row);

            // button
            var button = document.createElement("button");
            button.appendChild(
                document.createTextNode("Next")
            )
            button.classList.add("btn");
            button.classList.add("btn-primary");
            button.classList.add("confirm-button");
            button.onclick = function (event) {
                showClientData()
            }
            button.setAttribute('type', 'button')
            theDiv.appendChild(button)

            // empty row
            var empty_row = document.createElement("div");
            empty_row.classList.add('empty-row');
            theDiv.appendChild(empty_row);
        }).catch((error) => {
            console.log(error)
            var theDiv = document.getElementById("roomsAvailable");
            theDiv.innerHTML = error.toString();
        });
    } catch (error) {
        console.log(error);
        var theDiv = document.getElementById("roomsAvailable");
        theDiv.innerHTML = error.toString();
    }
}

function checkDateOrder() {
    var arrivalInput = $("#arrivalDate").val();
    var departureInput = $("#departureDate").val();

    if (arrivalInput == "" || departureInput == "") {
        return false
    }

    if (!validateDates()) {
        return false;
    }

    var arrivalDate = moment(arrivalInput, 'YYYY-MM-DD');
    arrivalDate = arrivalDate.toDate();
    var departureDate = moment(departureInput, 'YYYY-MM-DD');
    departureDate = departureDate.toDate();
    if (arrivalDate >= departureDate) {
        return false
    } else {
        return true
    }
}

function validateDates() {
    var arrivalInput = $("#arrivalDate").val();
    var departureInput = $("#departureDate").val();

    if (!moment(arrivalInput, 'YYYY-MM-DD').isValid()) {
        //console.log(moment(arrivalInput, "DD/MM/YYYY").isValid())
        return false;
    }

    if (!moment(departureInput, 'YYYY-MM-DD').isValid()) {
        return false;
    }

    return true;

}

function showClientData() {
    if ($("#numberOfRooms").val() == 0) {
        alert("Choose rooms!")
    } else {
        var x = document.getElementById("clientData");
        if (x.style.display === "none") {
            x.style.display = "block";
        }
    }
}

function hideClientData() {
    var x = document.getElementById("clientData");
    x.style.display = "none";
}

function removeAvailableRooms() {
    var theDiv = document.getElementById("roomsAvailable");
    theDiv.innerHTML = ""
}

function validateForm() {
    let arrivalDate = $("#arrivalDate").val();
    let departureDate = $("#departureDate").val();

    if (arrivalDate == "" || departureDate == "") {
        return false;
    }

    if (!validateDates()) {
        return false;
    }

    if ($("#numberOfRooms").val() == "0") {
        return false;
    }

    function check(id, regex) {
        return regex.test($(id).val());
    }

    function isEmpty(id) {
        let x = $(id).val();
        return x == "";
    }

    var regex_email = /\S+@\S+\.\S+/;
    if (isEmpty("#email") && !check("#email", regex_email)) {
        return false;
    }
    var regex_phone = /^\+(?:[0-9] ?){6,14}[0-9]$/;
    if (!isEmpty("#phoneNumber") && !check("#phoneNumber", regex_phone)) {
        return false;
    }

    var regex_start_uppercase = /^[A-Z]/;
    if (!isEmpty("#name") && !check("#name", regex_start_uppercase)) {
        return false;
    }
    if (!isEmpty("#surname") && !check("#surname", regex_start_uppercase)) {
        return false;
    }
    if (!isEmpty("#street") && !check("#street", regex_start_uppercase)) {
        return false;
    }
    if (!isEmpty("#city") && !check("#city", regex_start_uppercase)) {
        return false;
    }
    if (!isEmpty("#country") && !check("#country", regex_start_uppercase)) {
        return false;
    }
    
    return true;
}

function validateFormAndAlert() {
    if (validateForm()) {
        return true;
    } else {
        alert("Check form!")
        return false;
    }
}
