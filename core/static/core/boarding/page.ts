import { fetchJsonFromBackend, getCookie } from '../standard/utils';
import { addSuccessMessage, addErrorMessage, clearMessages } from '../standard/message';


function markTicketAsBoardedInTable(ticketId: number) {
    const ticketRow = document.getElementById(`ticket-${ticketId}`);
    const BOARDED_COLUMN_INDEX = 2;
    if (ticketRow) {
            ticketRow.getElementsByTagName('td')[BOARDED_COLUMN_INDEX].textContent = '✅';
    }
}

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
                            clearMessages();
                            addSuccessMessage('Ticket boarded');
                            markTicketAsBoardedInTable(ticketId);
                        } else {
                            clearMessages();
                            addErrorMessage(`Failed to board: ${response.messages}`);
                        }
                    },
                    (error) => {
                        clearMessages();
                        alert('Failed to board');
                        addErrorMessage(`Failed to board: ${error}`);
                    }
                );
                setTimeout(() => {
                    boardingInput.disabled = false;
                    boardingInput.value = '';
                    boardingInput.focus();
                }, 500);
            }
        });
    }
}

hookupTicketBoardingForm()
