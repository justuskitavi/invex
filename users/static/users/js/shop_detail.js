window.promptSell = function (shopID, productID) {
    const quantity = prompt('Enter quantity to sell:');
    if (!quantity || isNaN(quantity)) {
        alert('Quantity must be a number');
        return;
    }

    fetch(`/shop/${shopID}/sell-product/${productID}/`, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ quantity: quantity })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Sale successful!');
                window.location.reload();
            } 
            else {
                alert(data.error);
            }
    })
            .catch(error => {
                console.error('Sell product error',error);  
                alert('An error occurred.');              
            });
};

//add stock function
window.promptAdd = function (shopID, productID) {
    const password = prompt('Enter password to add stock:');
    if (!password) return;

    const quantity = prompt('Enter quantity to add:');
    if (!quantity || isNaN(quantity)) {
        alert('Quantity must be a number');
        return;
    }

    fetch(`/shop/${shopID}/add-stock/${productID}/`, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ password: password, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Stock added successfully!');
            window.location.reload();
        } 
        else {
            alert(data.error);
        }
    })

    .catch(error => {
        console.error('Add stock error',error);  
        alert('An error occurred while adding stock.');              
    });
};

window.promptDelete = function (shopID, productID) {
    const password = prompt('Enter your password to delete this product:');
    if (!password) return;

    const confirmed = confirm('Are you sure you want to permanently delete this product?');
    if (!confirmed) return;

    fetch(`/shop/${shopID}/delete-product/${productID}/`, {
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
            alert('Product deleted successfully.');
            window.location.reload();
        } else {
            alert(data.error || 'Could not delete product.');
        }
    })
    .catch(error => {
        console.error('Delete product error', error);
        alert('An error occurred while deleting the product.');
    });
};


//Utility function to get CSRF token from cookies
function getCSRFToken(){
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}


// Closing the DOMContentLoaded event listener




    
