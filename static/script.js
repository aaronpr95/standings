document.addEventListener('DOMContentLoaded', function() {
    // Get the elements for the toggle button and the table
    const toggleViewLink = document.getElementById('toggleView');
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
    });
});