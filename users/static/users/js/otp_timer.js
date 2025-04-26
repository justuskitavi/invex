// otp_timer.js

document.addEventListener("DOMContentLoaded", function () {
    let timeLeft = 60;
    const countdownEl = document.getElementById("countdown");
    const resendBtn = document.getElementById("resend-btn");
    const timerEl = document.getElementById("timer");

    const timer = setInterval(() => {
        timeLeft--;
        countdownEl.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);
            timerEl.style.display = "none";
            resendBtn.style.display = "inline-block";
        }
    }, 1000);
});
