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
  
  window.promptAdd = function(shopID, productID) {
    const modal = new bootstrap.Modal(document.getElementById('addStockModal'));
    document.getElementById('modalShopID').value = shopID;
    document.getElementById('modalProductID').value = productID;
    modal.show();
  };
  
  document.getElementById('addStockForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const shopID = document.getElementById('modalShopID').value;
    const productID = document.getElementById('modalProductID').value;
    const password = document.getElementById('stockPassword').value;
    const quantity = document.getElementById('stockQuantity').value;
  
    fetch(`/shop/${shopID}/add-stock/${productID}/`, {
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
    const modal = new bootstrap.Modal(document.getElementById('sellProductModal'));
    document.getElementById('sellShopID').value = shopID;
    document.getElementById('sellProductID').value = productID;
    modal.show();
  };
  
  document.getElementById('sellProductForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const shopID = document.getElementById('sellShopID').value;
    const productID = document.getElementById('sellProductID').value;
    const quantity = document.getElementById('sellQuantity').value;
  
    fetch(`/shop/${shopID}/sell-product/${productID}/`, {
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
    const password = prompt('Enter your password to edit this product:');
    if (!password) return;
  
    fetch(`/shop/${shopID}/edit-product/${productID}/`, {
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
        document.getElementById('editModalBody').innerHTML = data.form_html;
        const modal = new bootstrap.Modal(document.getElementById('editProductModal'));
        modal.show();
  
        document.getElementById('editProductForm')?.addEventListener('submit', function (e) {
          e.preventDefault();
          const formData = new FormData(this);
          fetch(`/shop/${shopID}/edit-product/${productID}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
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
          .catch(err => {
            console.error('Edit error', err);
            alert('Something went wrong.');
          });
        });
  
      } else {
        alert(data.error || 'Authentication failed.');
      }
    })
    .catch(err => {
      console.error('Edit fetch error', err);
      alert('An error occurred.');
    });
  };
  
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
  