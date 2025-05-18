document.addEventListener('DOMContentLoaded', () => {
  // Helper function to get CSRF token cookie
  window.getCookie = function(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (const c of cookies) {
        const cTrim = c.trim();
        if (cTrim.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cTrim.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  let currentShopID = null;
  let currentProductID = null;

  window.promptAdd = function(shopID, productID) {
    currentShopID = shopID;
    currentProductID = productID;

    const modal = new bootstrap.Modal(document.getElementById('addStockModal'));
    document.getElementById('modalShopID').value = shopID;
    document.getElementById('modalProductID').value = productID;
    modal.show();
  };

  document.getElementById('addStockForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!currentShopID || !currentProductID) return;

    const password = document.getElementById('stockPassword').value;
    const quantity = document.getElementById('stockQuantity').value;

    fetch(`/shop/${currentShopID}/add-stock/${currentProductID}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ password, quantity })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Stock added successfully!');
        window.location.reload();
      } else {
        alert(data.error);
      }
    })
    .catch(err => {
      console.error('Add stock error', err);
      alert('An error occurred.');
    });
  });

  window.promptSell = function(shopID, productID) {
    currentShopID = shopID;
    currentProductID = productID;

    const modal = new bootstrap.Modal(document.getElementById('sellProductModal'));
    document.getElementById('sellShopID').value = shopID;
    document.getElementById('sellProductID').value = productID;
    modal.show();
  };

  document.getElementById('sellProductForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!currentShopID || !currentProductID) return;

    const quantity = document.getElementById('sellQuantity').value;

    fetch(`/shop/${currentShopID}/sell-product/${currentProductID}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ quantity })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Product sold successfully!');
        window.location.reload();
      } else {
        alert(data.error);
      }
    })
    .catch(err => {
      console.error('Sell product error', err);
      alert('An error occurred.');
    });
  });

  window.promptEdit = function(shopID, productID) {
    currentShopID = shopID;
    currentProductID = productID;

    const modal = new bootstrap.Modal(document.getElementById('editPasswordModal'));
    modal.show();
  };

  const editPasswordForm = document.getElementById('editPasswordModal');  
  if (editPasswordForm) {
    editPasswordForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!currentShopID || !currentProductID) return;

      const password = document.getElementById('passwordInput').value;
      

      fetch(`/shop/${currentShopID}/edit-product/${currentProductID}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          
          document.getElementById('editModalBody').innerHTML = data.form_html;

          const modalEl = document.getElementById('editProductModal');
          const modal = new bootstrap.Modal(modalEl);
          modal.show();

          const editForm = document.getElementById('editProductForm');
          if (editForm) {
            editForm.addEventListener('submit', (e) => {
              e.preventDefault();
              const formData = new FormData(editForm);

              fetch(`/shop/${currentShopID}/edit-product/${currentProductID}/`, {
                method: 'POST',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
              })
              .then(res => res.json())
              .then(data => {
                if (data.success) {
                  alert('Product updated successfully!');
                  window.location.reload();
                } else {
                  alert(data.error);
                }
              })
              .catch(() => alert('Something went wrong.'));
            });
          }

          bootstrap.Modal.getInstance(document.getElementById('editPasswordModal')).hide();
        } else {
          alert(data.error || 'Authentication failed.');
        }
      })
      .catch(() => alert('Error verifying password.'));
    });
  }

  window.promptDelete = function(shopID, productID) {
    const password = prompt('Enter your password to delete this product:');
    if (!password) return;

    const confirmed = confirm('Are you sure you want to delete this product?');
    if (!confirmed) return;

    fetch(`/shop/${shopID}/delete-product/${productID}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ password })      
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Product deleted successfully!');
        window.location.reload();
      } else {
        alert(data.error);
      }
    })
    .catch(err => {
      console.error('Delete error', err);
      alert('An error occurred.');
    });
  };
});
