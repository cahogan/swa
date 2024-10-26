import { fetchJsonFromBackend, getCookie } from '../standard/utils';
import { addSuccessMessage, addErrorMessage } from '../standard/message';


function hookupTicketBoardingForm() {
    const boardingInput = document.getElementById('boarding-input') as HTMLInputElement;
    const flightId = boardingInput.getAttribute('data-flight-id');
    const csrftoken = getCookie('csrftoken');
    if (boardingInput && csrftoken) {
        boardingInput.addEventListener('input', () => {
            const scanComponents = boardingInput.value.split('-')
            if (scanComponents.length > 4) {
                const ticketId = parseInt(scanComponents[0])
                boardingInput.disabled = true;
                fetchJsonFromBackend(
                    csrftoken,
                    `/boarding/${flightId}/`,
                    { ticket_id: ticketId },
                    (response) => {
                        if (response.success) {
                            addSuccessMessage('Ticket boarded');
                        } else {
                            addErrorMessage(`Failed to board: ${response.messages}`);
                        }
                    },
                    (error) => {
                        alert('Failed to board');
                        addErrorMessage(`Failed to board: ${error}`);
                    }
                );
                boardingInput.disabled = false;
                boardingInput.value = '';
            }
        });
    }
}

hookupTicketBoardingForm()
