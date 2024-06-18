document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_turnos_usuario')
        .then(response => response.json())
        .then(data => {
            console.log('Data:', data);
            const tbody = document.querySelector('#tabla-turnos');
            console.log('Tbody:', tbody);
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
                const cancelarButton = document.createElement('button');
                cancelarButton.textContent = 'Cancelar';
                cancelarButton.className = 'btn btn-danger btn-sm';
                cancelarButton.addEventListener('click', () => {
                    cancelarTurno(turno.id, row);
                });
                accionesCell.appendChild(cancelarButton);
                row.appendChild(accionesCell);

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));
});

function cancelarTurno(id, row) {
    fetch(`/cancelar_turno/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ estado: 'Cancelado' })
    })
    .then(response => {
        if (response.ok) {
            // Actualizar la fila en la tabla
            row.querySelector('td:nth-child(3)').textContent = 'Cancelado';
        } else {
            console.error('Error cancelando el turno');
        }
    })
    .catch(error => console.error('Error en la solicitud de cancelación:', error));
}

/* Nota:
Asegurarse de que el endpoint /cancelar_turno/<id> esté implementado en el servidor para manejar la cancelación del turno y actualizar el estado del turno a "Cancelado" en la base de datos.
La función cancelarTurno hace una solicitud POST al servidor con el ID del turno a cancelar y actualiza el estado del turno a "Cancelado".*/