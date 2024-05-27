document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_data_turnos')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos tbody');
            data.forEach(turno => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${turno.id}</td>
                    <td>${turno.nombre}</td>
                `;
                tbody.appendChild(row);
            });
        });
});