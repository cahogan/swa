// Taken from an example in the Django documentation
export function getCookie(name) {
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

export function fetchJsonFromBackend(
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
