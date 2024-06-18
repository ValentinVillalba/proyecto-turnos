document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_turnos_usuario')
        .then(response => response.json())
        .then(data => {
            console.log('Data:', data); // Verifica los datos recibidos
            const tbody = document.querySelector('#tabla-turnos');
            console.log('Tbody:', tbody); // Verifica el tbody seleccionado
            data.forEach(turno => {
                const row = document.createElement('tr');

                const fechaCell = document.createElement('td');
                fechaCell.textContent = turno.fecha;
                row.appendChild(fechaCell);

                const horaCell = document.createElement('td');
                horaCell.textContent = turno.hora;
                row.appendChild(horaCell);

                const estadoCell = document.createElement('td');
                estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Vencido";
                row.appendChild(estadoCell);

                const accionesCell = document.createElement('td');
                accionesCell.textContent = ''; // Columna vacía por ahora
                row.appendChild(accionesCell);

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));
});
