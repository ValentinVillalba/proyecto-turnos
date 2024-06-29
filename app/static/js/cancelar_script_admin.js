document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('boton-vencidos').setAttribute('disabled', 'disabled');

    fetch('/get_all_turnos_pendientes')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos');
            data.forEach(turno => {
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
                
                let fechaTurnoDate = new Date(turno.fecha + 'T00:00:00-03:00');

            let partesHora = turno.hora.split(':');
            let hora = parseInt(partesHora[0], 10);
            let minutos = parseInt(partesHora[1], 10);

            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);

            const esHoy = fechaTurnoDate.getTime() === hoy.getTime();

            if (turno.asistencia == 1) {
                estadoCell.textContent = "Asistió";
            } 
            else if (fechaTurnoDate < hoy) {
                estadoCell.textContent = "Vencido";
            } 
            else if (esHoy) {
                const ahora = new Date();
                if (turno.estado == 1 && (hora < ahora.getHours() || (hora === ahora.getHours() && minutos < ahora.getMinutes()))) {
                    estadoCell.textContent = "Vencido";
                }
                else {
                    estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Cancelado";
                }
            } 
            else {
                estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Cancelado";
            }

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

                // if (new Date(turno.fecha) < new Date()) {
                //     document.getElementById('boton-vencidos').removeAttribute('disabled');
                // }
                
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));

        document.getElementById('confirmCancel').addEventListener('click', function() {
            cancelarTurno(turnoIdToCancel, rowToUpdate);
            var myModalEl = document.getElementById('cancelModal');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
        });

        // document.getElementById('confirmCancelAll').addEventListener('click', function() {
        //     cancelarTurnosVencidos();
        //     var myModalEl = document.getElementById('cancelAllModal');
        //     var modal = bootstrap.Modal.getInstance(myModalEl)
        //     modal.hide();
        // });
});

// function abrirModalCancelarTodos() {
//     var myModal = new bootstrap.Modal(document.getElementById('cancelAllModal'), {
//         keyboard: false
//     })
//     myModal.show();
// }

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

// function cancelarTurnosVencidos(){
//     fetch(`/cancelar_turnos_vencidos`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message === 'Turnos vencidos cancelados correctamente') {
//             console.log('Turnos cancelados correctamente');
//             window.location.reload();
//         } else {
//             console.error('Error cancelando los turnos:', data.message);
//         }
//     })
//     .catch(error => console.error('Error en la solicitud de cancelación:', error));
// }