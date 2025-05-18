document.addEventListener('DOMContentLoaded', () => {
  // Initialize Bootstrap modal
  const passwordModalEl = document.getElementById('passwordModal');
  const passwordModal = new bootstrap.Modal(passwordModalEl);
  const passwordInput = document.getElementById('passwordInputModal');

  let targetUrl = '';

  // Handle links that require password
  document.querySelectorAll('.secure-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      targetUrl = link.dataset.targetUrl;
      passwordInput.value = '';
      passwordModal.show();
      passwordInput.focus();
    });
  });

  // Handle Cancel button inside modal
  const cancelBtn = document.getElementById('cancelBtn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      passwordModal.hide();
    });
  }

  // Handle Verify button
  const verifyBtn = document.getElementById('verifyPasswordBtn');
  if (verifyBtn) {
    verifyBtn.addEventListener('click', () => {
      const password = passwordInput.value.trim();
      if (!password) {
        alert('Please enter your password.');
        return;
      }
      verifyPassword(password);
    });
  }

  function verifyPassword(password) {
    fetch(`/verify-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({ password: password }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Password correct, redirect
        window.location.href = targetUrl;
      } else {
        alert('Incorrect password. Please try again.');
      }
    })
    .catch(() => {
      alert('Error verifying password.');
    })
    .finally(() => {
      passwordModal.hide();
    });
  }

  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let c of cookies) {
        c = c.trim();
        if (c.startsWith('csrftoken=')) {
          cookieValue = c.substring('csrftoken='.length);
          break;
        }
      }
    }
    return cookieValue;
  }
});