function consultarTurnos() {
    console.log('Botón Consultar clicado'); // Añade un log para verificar que el evento está siendo capturado

    const fechaDesdeInput = document.getElementById('fecha-desde');
    const fechaHastaInput = document.getElementById('fecha-hasta');
    const tableContainer = document.querySelector('.table-container');
    const tbody = document.querySelector('#tabla-turnos');

    const fechaDesde = fechaDesdeInput.value;
    const fechaHasta = fechaHastaInput.value;

    if (fechaDesde && fechaHasta) {
        console.log('Fecha desde:', fechaDesde, 'Fecha hasta:', fechaHasta); // Log de las fechas

        fetch(`/get_data_turnos_facturista?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`)
            .then(response => {
                console.log('Fetch realizado');
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data); // Log de los datos recibidos

                tbody.innerHTML = ''; // Limpiar la tabla antes de insertar los nuevos datos

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
                    if (turno.estado == 1 && new Date(turno.fecha) < new Date()) {
                        estadoCell.textContent = "Vencido";
                    } else {
                        estadoCell.textContent = turno.estado == 1 ? "Pendiente" : "Cancelado";
                    }
                    row.appendChild(estadoCell);

                    tbody.appendChild(row);
                });

                tableContainer.style.display = 'block'; // Mostrar la tabla
            })
            .catch(error => console.error('Error fetching turnos:', error));
    } else {
        alert('Por favor, selecciona ambas fechas.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM cargado'); // Verificar que el DOM está cargado
});
