document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.page-wrapper');
    if (!wrapper) return;

    // Fade in effect on page load
    wrapper.classList.add('fade-in');

    // Fade out effect on link navigation
    const links = document.querySelectorAll('a[href]:not([target="_blank"])');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Skip empty or anchor-only links
            if (!href || href.startsWith('#') || this.classList.contains('no-fade')) return;

            // Prevent immediate navigation
            e.preventDefault();

            // Trigger fade out
            wrapper.classList.remove('fade-in');
            wrapper.style.opacity = '0';

            // Wait for the transition to complete
            setTimeout(() => {
                window.location.href = href;
            }, 300); // match CSS transition duration
        });
    });
});
