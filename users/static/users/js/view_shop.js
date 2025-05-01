function shutdownShop(shopID) {
    const password = prompt("Enter your password to shut down this shop:");
    if (!password) return;

    const confirmDelete = confirm("This action cannot be undone. Are you sure you want to delete this shop?");
    if (!confirmDelete) return;

    fetch(`/shop/${shopID}/delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Shop successfully deleted.');
            window.location.reload();
        } else {
            alert(data.error || 'Failed to delete shop.');
        }
    })
    .catch(error => {
        console.error('Error deleting shop:', error);
        alert('A server error occurred.');
    });
}

function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}
