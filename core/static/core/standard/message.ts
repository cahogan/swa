export function addMessage(message, level, timeout = -1) {
    const messageBox = document.getElementById('dynamic-messages');
    const messageElement = document.createElement('li');
    messageElement.className = `alert alert-${level}`;
    messageElement.textContent = message;
    messageBox?.appendChild(messageElement);
    if (timeout > 0) {
        setTimeout(() => {
            messageElement.remove();
        }, timeout);
    }
}

export function addSuccessMessage(message) {
    addMessage(message, 'success');
}

export function addErrorMessage(message) {
    addMessage(message, 'error');
}

export function clearMessages() {
    const messageBox = document.getElementById('dynamic-messages');
    if (messageBox) {
        messageBox.innerHTML = '';
    }
}
