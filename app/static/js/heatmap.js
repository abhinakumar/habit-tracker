document.addEventListener('DOMContentLoaded', function () {
    const dataEl = document.getElementById('heatmap-data');
    const container = document.getElementById('heatmap');
    if (!dataEl || !container) return;

    const data = JSON.parse(dataEl.textContent);

    data.forEach(function (entry) {
        const cell = document.createElement('div');
        cell.className = 'heatmap-cell' + (entry.checked_in ? ' checked' : '');
        cell.title = entry.date + (entry.checked_in ? ' — checked in' : ' — no check-in');
        container.appendChild(cell);
    });
});
