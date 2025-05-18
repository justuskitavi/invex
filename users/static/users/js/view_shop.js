window.getCookie = function(name) {
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
};

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

// Function to open the modal and set the shopID
function promptViewShopPassword(shopID) {
  document.getElementById('viewShopID').value = shopID;
  const modal = new bootstrap.Modal(document.getElementById('viewShopPasswordModal'));
  modal.show();
}

// Handle form submission for password verification
document.getElementById('viewShopPasswordForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const password = document.getElementById('viewShopPasswordInput').value;
  const shopID = document.getElementById('viewShopID').value;
  
  fetch(`/shop/${shopID}/verify-password/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // assuming you have this helper
    },
    body: JSON.stringify({ password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Close modal
      const modalEl = document.getElementById('viewShopPasswordModal');
      const modal = bootstrap.Modal.getInstance(modalEl);
      modal.hide();
      console.log('shopID:', shopID);
      
      const redirectUrl = `/shop/${shopID}/`;
      window.location.href = redirectUrl;

    } 
    else {
      alert('Incorrect password');
    }
  })
  .catch(err => {
    console.error('Error verifying password:', err);
    alert('An error occurred. Please try again.');
  });
});

function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}