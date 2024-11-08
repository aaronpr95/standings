document.addEventListener('DOMContentLoaded', function() {
    // Get the elements for the toggle button and the table
    const toggleViewLink = document.getElementById('toggleView');
    const tableContainer = document.querySelector('.table-responsive-sm');
    const table = document.querySelector('table');
    const hiddenCells = document.querySelectorAll('td.hidden');
    const hiddenHeaders = document.querySelectorAll('th.hidden');
    const rows = document.querySelectorAll("tbody tr");

    rows.forEach(row => {
        const bgColor = window.getComputedStyle(row).backgroundColor;
        const stickyCols = row.querySelectorAll(".sticky-col, .sticky-right");
        stickyCols.forEach(col => {
            col.style.backgroundColor = bgColor;
        });
    });

    // Function to animate scroll
    function animateScroll(element, to, duration) {
        const start = element.scrollLeft;
        const change = to - start;
        const increment = 20;
        let currentTime = 0;

        const animate = function() {
            currentTime += increment;
            const val = Math.easeInOutQuad(currentTime, start, change, duration);
            element.scrollLeft = val;
            if (currentTime < duration) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }

    // Easing function for smooth scroll
    Math.easeInOutQuad = function(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    };

    // Add an event listener for the toggle button
    toggleViewLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior

        // Toggle between the compact and full modes by adding/removing classes
        table.classList.toggle('short-mode');
        table.classList.toggle('full-mode');

        // Toggle the visibility of hidden cells and headers
        hiddenCells.forEach(cell => cell.classList.toggle('hidden'));
        hiddenHeaders.forEach(header => header.classList.toggle('hidden'));

        // Change the link text based on the current mode
        toggleViewLink.textContent = table.classList.contains('short-mode') 
            ? 'Ver Detalles'  // If short mode is active, show 'Ver Detalles'
            : 'Ver Menos';     // If full mode is active, show 'Ver Menos'

        // Scroll the table container to the right
        if (table.classList.contains('full-mode')) {
            animateScroll(tableContainer, 100, 600);
        } else {
            animateScroll(tableContainer, 0, 600);
        }
    });
});