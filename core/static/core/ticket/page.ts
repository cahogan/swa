function getCookie(name) {
    let cookieValue = '';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fetchJsonFromBackend(
    csrftoken: string,
    fetchUrl: string,
    data: object,
    callback: Function,
    errorCallback?: Function,
  ) {
    fetch(fetchUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
        credentials: 'same-origin',
      })
      .then((response) => response.json())
      .then((responseJson) => callback(responseJson))
      .catch((error) => {
        if (errorCallback) {
          errorCallback(error)
        } else {
          console.error(error)
        }
      })
  }

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
