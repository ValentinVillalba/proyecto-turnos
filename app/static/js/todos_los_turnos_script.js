document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_data_turnos')
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

            const pacienteCell = document.createElement('td');
            pacienteCell.textContent = turno.dni;
            row.appendChild(pacienteCell);

            const estadoCell = document.createElement('td');
            if(turno.estado == 1 && new Date(turno.fecha) < new Date()){
                estadoCell.textContent = "Vencido";
            }
            else{
                estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Cancelado";
            }
            row.appendChild(estadoCell);

            tbody.appendChild(row);
        });
    })
});