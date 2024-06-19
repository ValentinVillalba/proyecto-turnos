document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_turnos_usuario')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos');
            if (data[0] == undefined) {
                console.log("No hay turnos");
            }
            else{
                document.getElementById('obra-social-slot').innerHTML = data[0].obra_soc;
            }
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
                if (new Date(turno.fecha) < new Date()) {
                    estadoCell.textContent = "Vencido";
                }
                else{
                    estadoCell.textContent = "Pendiente"
                }
                row.appendChild(estadoCell);

                const dniCell = document.createElement('td');
                dniCell.textContent = turno.dni;
                row.appendChild(dniCell);

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching turnos:', error));
});
