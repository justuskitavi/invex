// users/static/users/js/edit_product.js

function promptEdit(shopID, productID) {
    const password = prompt("Please enter your password to edit the product:");
    if (!password) return;

    fetch(`/shop/${shopID}/edit-product/${productID}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = document.createElement('div');
            modal.innerHTML = data.form_html;
            modal.id = 'editProductModal';
            document.body.appendChild(modal);

            const form = document.getElementById('editProductForm');
            if (form) {
                form.addEventListener('submit', function (e) {
                    e.preventDefault();
                    const formData = new FormData(form);

                    fetch(`/shop/${shopID}/edit-product/${productID}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: formData
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            alert('Product updated successfully.');
                            window.location.reload();
                        } else {
                            alert(data.error || 'Failed to update product.');
                        }
                    })
                    .catch(err => {
                        console.error('Update error', err);
                        alert('An error occurred while updating.');
                    });
                });
            }
        } else {
            alert(data.error || 'Failed to load edit form.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to edit the product.');
    });
}

function closeEditModal() {
    const modal = document.getElementById('editProductModal');
    if (modal) modal.remove();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
