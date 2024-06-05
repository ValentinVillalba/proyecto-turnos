document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_data_turnos')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos tbody');
            data.forEach(turno => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${turno.id_turno}</td>
                    <td>${turno.fecha}</td>
                    <td>${turno.hora}</td>
                    <td>${turno.estado}</td>
                    <td>${turno.id_paciente}</td>
                `;
                tbody.appendChild(row);
            });
        });
});