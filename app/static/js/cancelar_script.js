document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_turnos_pendientes')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos');
            data.forEach(turno => {

                // No muestra turnos vencidos
                if (new Date(turno.fecha) < new Date()) {
                    return;
                }

                const row = document.createElement('tr');

                const fechaCell = document.createElement('td');
                const fechaUTC = new Date(turno.fecha + 'T00:00:00Z');
                let day = fechaUTC.getUTCDate();
                let month = fechaUTC.getUTCMonth() + 1;
                let year = fechaUTC.getUTCFullYear();
                
                fechaCell.textContent = `${day}/${month}/${year}`;
                row.appendChild(fechaCell);

                const horaCell = document.createElement('td');
                horaCell.textContent = turno.hora;
                row.appendChild(horaCell);

                const estadoCell = document.createElement('td');
                estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Cancelado";
                row.appendChild(estadoCell);

                const accionesCell = document.createElement('td');
                const cancelarButton = document.createElement('button');
                cancelarButton.textContent = 'Cancelar';
                cancelarButton.className = 'btn btn-danger btn-sm';
                cancelarButton.addEventListener('click', () => {
                    turnoIdToCancel = turno.id_turno;
                    rowToUpdate = row;
                    var myModal = new bootstrap.Modal(document.getElementById('cancelModal'), {
                        keyboard: false
                    })
                    myModal.show();
                });
                accionesCell.appendChild(cancelarButton);
                row.appendChild(accionesCell);

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));

        document.getElementById('confirmCancel').addEventListener('click', function() {
            cancelarTurno(turnoIdToCancel, rowToUpdate);
            var myModalEl = document.getElementById('cancelModal');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
        });
});

function cancelarTurno(id, row) {
    fetch(`/cancelar_turno`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_turno: id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Turno cancelado correctamente') {
            row.querySelector('td:nth-child(3)').textContent = 'Cancelado';
            row.querySelector('td:nth-child(4)').textContent = '';
        } else {
            console.error('Error cancelando el turno:', data.message);
        }
    })
    .catch(error => console.error('Error en la solicitud de cancelación:', error));
}