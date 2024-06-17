document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_turnos_usuario')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#tabla-turnos');
            data.forEach(turno => {
                const row = document.createElement('li');
                row.innerHTML = `
                    Fecha: ${turno.fecha}
                    <br>
                    Hora:${turno.hora}
                    <br>
                    Estado: ${turno.estado == 1 ? "Pendiente" : ""} ${turno.estado == 0 ? "Vencido" : ""}
                `;
                tbody.appendChild(row);
            });
        });
});