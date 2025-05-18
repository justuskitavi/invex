document.addEventListener("DOMContentLoaded", function () {
    const resendBtn = document.getElementById("resend-btn");
    const timerSpan = document.getElementById("timer");
  
    let seconds = 60;
    const countdown = setInterval(() => {
      seconds--;
      timerSpan.textContent = seconds;
  
      if (seconds <= 0) {
        clearInterval(countdown);
        resendBtn.style.display = "inline-block";
        document.getElementById("countdown-text").style.display = "none";
      }
    }, 1000);
  });
    