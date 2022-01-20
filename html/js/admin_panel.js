var lastArrivalValue = new Date();
lastArrivalValue.setHours(0,0,0,0);
var lastDepartureValue = new Date();
lastDepartureValue.setDate(lastDepartureValue.getDate() + 1)
lastDepartureValue.setHours(0,0,0,0);

jQuery(function () {
    // this script creates arrivalDate date picker
    var date = new Date();
    var minDate = new Date()
    minDate.setDate(date.getDate() - 1);

    var datepicker = $('#arrivalDate');
    if (datepicker.length > 0) {
        datepicker.datepicker({
            format: "dd/mm/yyyy",
            //format: "yyyy-mm-dd",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
        }).on("change", function (e) {

            hide_elements()

            let arrivalInput = $("#arrivalDate").val();
            let departureInput = $("#departureDate").val();
            var arrivalDate = moment(arrivalInput, 'DD/MM/YYYY').toDate()
            var departureDate = moment(departureInput, 'DD/MM/YYYY').toDate()

            if((lastArrivalValue - arrivalDate) != 0){
                if(departureDate <= arrivalDate) {
                    var newDep = moment(arrivalInput, 'DD/MM/YYYY').add(1, 'days').format('DD/MM/YYYY');
                    $("#departureDate").val(newDep);
                    lastDepartureValue = moment(arrivalInput, 'DD/MM/YYYY').add(1, 'days').toDate()
                }
                lastArrivalValue = arrivalDate;
              }
        });
        datepicker.val(moment(date).format('DD/MM/YYYY'))
        //datepicker.val(moment(date).format('YYYY-MM-DD'))
    }
});

jQuery(function () {
    // this script creates departurelDate date picker
    var date = new Date();
    date.setDate(date.getDate() + 1);
    var minDate = new Date()
    minDate.setDate(date.getDate() - 1);
    var datepicker = $('#departureDate');

    if (datepicker.length > 0) {
        datepicker.datepicker({
            format: "dd/mm/yyyy",
            //format: "yyyy-mm-dd",
            startDate: '+1d',
            autoclose: true,
            uiLibrary: 'bootstrap4',
            disableDates:  function (date) {
                let arrivalInput = $("#arrivalDate").val();
                var arrivalDatePlus1 = moment(arrivalInput, 'DD/MM/YYYY').add(1, 'days').toDate()
                if (date < arrivalDatePlus1) {
                    return false;
                } else {
                    return true;
                }
            }
        }).on("change", function (e) {

            hide_elements()

            let arrivalInput = $("#arrivalDate").val();
            let departureInput = $("#departureDate").val();
            var arrivalDate = moment(arrivalInput, 'DD/MM/YYYY').toDate()
            var departureDate = moment(departureInput, 'DD/MM/YYYY').toDate()

            if((lastDepartureValue - departureDate) != 0){
                lastDepartureValue = departureDate;
              }
        });
        datepicker.val(moment(date).format('DD/MM/YYYY'))
        //datepicker.val(moment(date).format('YYYY-MM-DD'))
    }
}); 

// this script sets js functions to html elements
window.onload = function() {
    document.getElementById('showDataButton').onclick = showData
}


// -----------------------------------------------------------------------------

function hide_elements(){
    var theDiv = document.getElementById("table_div");
    theDiv.innerHTML = "";

    hide_chars()
}

function hide_chars() {
    var pieChart = document.getElementById("pieChartDiv");
    pieChart.innerHTML = "";

    var barChart = document.getElementById("barChartDiv");
    barChart.innerHTML = "";
}

function changeDateFormatFromDisplayToSend(d) {
    // changes date format from DD/MM/YYYY to YYYY-MM-DD
    return moment(d, 'DD/MM/YYYY').format('YYYY-MM-DD');
}


function showData() {
    // this function connects to API 
    // and processes available rooms data 
    // and creates html elements in form

    if(!validateDates){
        return
    }

    let arrivalInput = $("#arrivalDate").val();
    let departureInput = $("#departureDate").val();

    var arrivalDate = changeDateFormatFromDisplayToSend(arrivalInput) //arrivalInput
    var departureDate = changeDateFormatFromDisplayToSend(departureInput) //departureInput


    let url = "/admin/reservations/" + arrivalDate + "/" + departureDate

    try {
        let res = fetch(url).then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Something went wrong');
            }
        }).then((data) => {
            var theDiv = document.getElementById("table_div");
            theDiv.innerHTML = "";

            var pieChart = document.getElementById("pieChartDiv");
            pieChart.innerHTML = "";

            theDiv.innerHTML = data.html_table;

            var t = document.getElementById("table");
            t.classList.add('table')
            t.classList.remove('dataframe')
            t.classList.add('table-striped')
            t.classList.add('table-bordered')
            t.classList.add('table-sm')

            t.setAttribute('cellspacing', '0');
            t.setAttribute('width', '100%');

            t.removeAttribute('border');

            $(document).ready(function () {
                $('#table').DataTable({
                    "scrollX": true,
                    "lengthMenu": [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]]
                });
                $('.dataTables_length').addClass('bs-select');
            });

            //if all not zero
            JSC.chart('pieChartDiv', {
                legend_visible: false,
                title_position: 'center',
                defaultSeries_type: 'pieDonut',
                title_label_text: 'Rooms available',
                series: [
                  {
                    name: 'rooms',
                    palette: ['#00FF00', '#FF0000'],
                    points: [
                      { name: 'Available', y: 5 },
                      { name: 'Not available', y: 10 }
                    ]
                  }
                ]
              });

              JSC.chart('barChartDiv', { 
                legend_visible: false,
                defaultSeries_type: 'column', 
                title_position: 'center',
                title_label_text: 'Reservation type', 
                yAxis: { label_text: 'Number' }, 
                xAxis_label_text: 'Room type', 
                series: [ 
                  { 
                    name: 'all reserved', 
                    id: 's1', 
                    points: [ 
                      { x: 'Single room', y: 0 }, 
                      { x: 'Double room', y: 1 }, 
                      { x: 'Family room', y: 5 }
                    ] 
                  }
                ] 
              }); 

            
        }).catch((error) => {
            console.log(error)
            var theDiv = document.getElementById("table_div");
            theDiv.innerHTML = error.toString();
            theDiv.innerHTML += ' Try to log out and log in.'
            hide_chars()
        });
    } catch (error) {
        console.log(error);
        var theDiv = document.getElementById("table_div");
        theDiv.innerHTML = error.toString();
        theDiv.innerHTML += ' Try to log out and log in.'
        hide_chars()
    }
}

function validateDates() {
    // this function validates date format
    var arrivalInput = $("#arrivalDate").val();
    var departureInput = $("#departureDate").val();

    if (!moment(arrivalInput, "DD/MM/YYYY").isValid()) {
        return false;
    }

    if (!moment(departureInput, "DD/MM/YYYY").isValid()) {
        return false;
    }

    return true;

}


