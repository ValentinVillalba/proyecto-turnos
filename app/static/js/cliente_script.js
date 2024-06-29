document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_turnos_dia_cliente')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos');
            tbody.innerHTML = ''; // Limpiar la tabla antes de llenarla con nuevos datos
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

                const pacienteCell = document.createElement('td');
                pacienteCell.textContent = turno.dni;
                row.appendChild(pacienteCell);

                const nombreCell = document.createElement('td');
                nombreCell.textContent = turno.nombre;
                nombreCell.classList.add('nowrap');
                row.appendChild(nombreCell);

                const obrasocialCell = document.createElement('td');
                    obrasocialCell.textContent = turno.obra_soc;
                    obrasocialCell.classList.add('nowrap');
                    row.appendChild(obrasocialCell);

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

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));
});
