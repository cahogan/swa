import { fetchJsonFromBackend, getCookie } from '../standard/utils';

function hookupPrintBoardingPassButton() {
    const printButton = document.getElementById('print-boarding-pass-button');
    const csrftoken = getCookie('csrftoken');
    if (printButton && csrftoken) {
        printButton.addEventListener('click', () => {
            const ticketId = printButton.getAttribute('data-ticket-id');
            fetchJsonFromBackend(
                csrftoken,
                `/ticket/${ticketId}/print/`,
                { ticket_id: ticketId },
                (response) => {
                    if (response.success) {
                        console.log('Boarding pass printed');
                    } else {
                        alert('Failed to print boarding pass');
                    }
                },
                (error) => {
                    alert('Failed to print boarding pass');
                }
            );
        });
    }
}

hookupPrintBoardingPassButton()
