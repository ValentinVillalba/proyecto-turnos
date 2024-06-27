document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('turnoForm');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const dni = document.getElementById('dniInput').value;

        if (!dni) {
            alert('Por favor, ingrese el DNI.');
            return;
        }

        try {
            const response = await fetch(`/get_turnos_by_dni?dni=${dni}`);
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            const turnos = data.turnos;
            const today = new Date().toISOString().split('T')[0];

            for (let turno of turnos) {
                if (turno.fecha === today) {
                    const updateResponse = await fetch('/update_asistencia', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ id_turno: turno.id_turno })
                    });

                    if (!updateResponse.ok) {
                        throw new Error('Error en la respuesta del servidor');
                    }

                    const updateData = await updateResponse.json();

                    if (updateData.message) {
                        alert(updateData.message);
                    } else {
                        alert(updateData.error);
                    }
                    return;
                }
            }

            alert('No hay turnos para la fecha actual.');

        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al procesar la solicitud.');
        }
    });
});
