jQuery(function () {
    var date = new Date();
    var minDate = new Date()
    minDate.setDate(date.getDate() - 1);

    var datepicker = $('#arrivalDate');
    if (datepicker.length > 0) {
        datepicker.datepicker({
            format: "dd/mm/yyyy",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
            minDate: minDate
        });
        //datepicker.attr("placeholder", moment(date).format('DD/MM/YYYY'));
        datepicker.val(moment(date).format('DD/MM/YYYY'))
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
            format: "dd/mm/yyyy",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
            minDate: minDate
        });
        //datepicker.attr("placeholder", moment(date).format('DD/MM/YYYY'));
        datepicker.val(moment(date).format('DD/MM/YYYY'))
    }
});

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

    var arrivalDate = moment(arrivalInput, "DD/MM/YYYY");
    arrivalDate = arrivalDate.toDate();
    arrivalDate = moment(arrivalDate).format('YYYY-MM-DD')
    var departureDate = moment(departureInput, "DD/MM/YYYY");
    departureDate = departureDate.toDate();
    departureDate = moment(departureDate).format('YYYY-MM-DD')

    let url = "/api/available_rooms/" + arrivalDate + "/" + departureDate
    var answear

    try {
        let res = fetch(url).then((response) => {return response.json()}).then((data) => {
            //console.log(data)
            var theDiv = document.getElementById("roomsAvailable");
            answear = data.number
            theDiv.innerHTML = "<b>Choose from available rooms:</b>"
            theDiv.innerHTML += " <br> "
            theDiv.innerHTML += 'Double Room: <input type="number", id="numberOfRooms" name="numberOfRooms", min="0", max="' + answear.toString() + '">'
            theDiv.innerHTML += " <br> "
            theDiv.innerHTML += "<button onclick=\"showClientData()\" class=\"btn btn-primary\" type='button'>Next</button> "; ""
         })
        

    } catch (error) {
        console.log(error);
    }   
}

function checkDateOrder() {
    var arrivalInput = $("#arrivalDate").val();
    var departureInput = $("#departureDate").val();

    if (arrivalInput == "" || departureInput == "") {
        return false
    }

    var arrivalDate = moment(arrivalInput, "DD/MM/YYYY");
    arrivalDate = arrivalDate.toDate();
    var departureDate = moment(departureInput, "DD/MM/YYYY");
    departureDate = departureDate.toDate();
    if (arrivalDate >= departureDate) {
        return false
    } else {
        return true
    }

}

function showClientData() {
    var x = document.getElementById("clientData");
    if (x.style.display === "none") {
        x.style.display = "block";
    } //else {
    //    x.style.display = "none";
    //}
}

function submitFunction() {

}

function validateForm() {

}
