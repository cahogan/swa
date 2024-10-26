export function addMessage(message, level) {
    const messageBox = document.getElementById('dynamic-messages');
    const messageElement = document.createElement('li');
    messageElement.className = `alert alert-${level}`;
    messageElement.textContent = message;
    messageBox?.appendChild(messageElement);
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

export function addSuccessMessage(message) {
    addMessage(message, 'success');
}

export function addErrorMessage(message) {
    addMessage(message, 'error');
}
