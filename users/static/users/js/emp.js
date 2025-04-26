function confirmFire(employeeId){
    if (confirm("Are you sure you want to fire this employee?")){
        const password = prompt("Please enter your password to confirm:");
        if (password) {
            fetch(`/employees/${employeeId}/fire/`, {
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
                    alert("Employee fired successfully.");
                    window.location.reload();    
                }
                else {
                    alert(data.error || "Failed to fire employee.");
                }
            })
            .catch(error => {
                console.error('Error firing employee:', error);
                alert("Something went wrong.");
            });
        }
    }
}

function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}