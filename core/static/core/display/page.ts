import { fetchJsonFromBackend, getCookie } from '../standard/utils';
import { addSuccessMessage, addErrorMessage, clearMessages } from '../standard/message';


function applyClassesForFlightStatus(cell, status) {
    cell.classList.remove('flight-delayed', 'flight-boarding', 'flight-last-call');
    if (status === 'Delayed') {
        cell.classList.add('flight-delayed');
    }
    else if (status === 'Boarding') {
        cell.classList.add('flight-boarding');
    }
    else if (status === 'Final Call') {
        cell.classList.add('flight-last-call');
    }
}

function updateFlightRow(row, flight){
    const cells = row.getElementsByTagName('td');
    // Cells are the following columns:
    // Flight, Candy, Destination, Departing At, Gate, Available Seats, Status
    const newData = [flight.id, flight.candy, flight.destination, flight.scheduled_departure,
                     flight.gate, flight.available_seats, flight.status];
    for (let i = 0; i < cells.length; i++) {
        if (i < 3 || i === 4) {
            continue;
        }
        else {
            cells[i].textContent = newData[i];
            if (i === 3 || i === 6) {
                applyClassesForFlightStatus(cells[i], flight.status);
            }
        }
    }
}

function createNewFlightRow(table, flight){
    console.log("Adding new flight row");
}

function updateFlightsDisplay() {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        fetchJsonFromBackend(
            csrftoken,
            '/display/',
            {},
            (response) => {
                const flightsList = response['flights'];
                flightsList.forEach((flight) => {
                    const flightRow = document.getElementById(`flight-${flight.id}`);
                    if (flightRow) {
                        updateFlightRow(flightRow, flight);
                    }
                    else {
                        const flightsTable = document.getElementById('flights-table');
                        createNewFlightRow(flightsTable, flight);
                    }
                });
            },
            (error) => {
                console.error(error);
            }
        );
    }
}

setInterval(updateFlightsDisplay, 1000);
