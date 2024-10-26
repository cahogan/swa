import { fetchJsonFromBackend, getCookie } from '../standard/utils';

function hookupTicketBoardingForm() {
    const boardingInput = document.getElementById('boarding-input') as HTMLInputElement;
    console.log('Boarding input:', boardingInput);
}

hookupTicketBoardingForm()
