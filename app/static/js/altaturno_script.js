document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('newPatientForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        fetch('/agregar_paciente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.message === 'Paciente agregado correctamente') {
                alert('Paciente agregado correctamente');
                form.reset();
            } else {
                console.error('Error al agregar paciente:', result.message);
            }
        })
        .catch(error => console.error('Error en la solicitud de agregar paciente:', error));
    });

    const dateInput = document.getElementById('appointmentDate');
    const timeSelect = document.getElementById('appointmentTime');

    fetch('/get_all_turnos_pendientes')
        .then(response => response.json())
        .then(turnos => {
            const datepicker = new Pikaday({
                field: dateInput,
                format: 'DD/MM/YYYY',
                i18n: {
                    previousMonth: 'Mes anterior',
                    nextMonth: 'Próximo mes',
                    months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                    weekdays: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
                    weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
                },
                firstDay: 1,
                minDate: new Date(),
                onSelect: function(date) {
                    const formattedDate = date.toISOString().split('T')[0];
                    updateAvailableTimes(formattedDate, turnos);
                    dateInput.value = date.toLocaleDateString('es-ES');
                }
            });
        })
        .catch(error => console.error('Error obteniendo las fechas:', error));

    function updateAvailableTimes(selectedDate, turnos) {
        const selectedTurnos = turnos.filter(turno => turno.fecha === selectedDate);
        const takenTimes = selectedTurnos.map(turno => turno.hora);
        const allTimes = [
            "9:00:00", "9:30:00", "10:00:00", "10:30:00",
            "11:00:00", "11:30:00", "12:00:00", "12:30:00", "13:00:00", "13:30:00",
            "14:00:00", "14:30:00", "15:00:00", "15:30:00", "16:00:00", "16:30:00", "17:00:00"
        ];

        timeSelect.innerHTML = '';

        allTimes.forEach(time => {
            if (!takenTimes.includes(time)) {
                const option = document.createElement('option');
                option.value = time;
                option.textContent = time;
                timeSelect.appendChild(option);
            }
        });
    }

    var dniArray = [];

    fetch('/get_pacientes')
    .then(response => response.json())
    .then(pacientes => {
        pacientes.forEach(paciente => {
            dniArray.push(paciente.dni);
        });
    })

    document.getElementById('dni').addEventListener('input', function() {
        var dni = parseInt(this.value);
        if (!isNaN(dni) && dni.toString().length === 8) {
            if (!dniArray.includes(dni)) {
                document.getElementById('dniError').style.display = 'block';
                document.getElementById('asignarTurno').disabled = true;
                document.getElementById('asignarTurno').classList.add('btn-disabled');
            } else {
                document.getElementById('dniError').style.display = 'none';
                document.getElementById('asignarTurno').disabled = false;
                document.getElementById('asignarTurno').classList.remove('btn-disabled');
            }
        } else {
            document.getElementById('dniError').style.display = 'block';
            document.getElementById('asignarTurno').disabled = true;
            document.getElementById('asignarTurno').classList.add('btn-disabled');
        }
    });

    const appointmentForm = document.getElementById('appointmentForm');
    appointmentForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const appointmentFormData = new FormData(appointmentForm);
        const dataAppointment = Object.fromEntries(appointmentFormData.entries());

        dataAppointment.dni = parseInt(dataAppointment.dni);
        const [day, month, year] = dataAppointment.appointmentDate.split('/');
        dataAppointment.appointmentDate = `${year}-${month}-${day}`;
        const selectedTime = document.getElementById('appointmentTime').value;
        dataAppointment.appointmentTime = `${selectedTime}`;

        fetch('/asignar_turno', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataAppointment)
        })
        .then(response => response.json())
        .then(result => {
            if (result.message === 'Turno asignado correctamente') {
                alert('Turno asignado correctamente');
                appointmentForm.reset();
            } else {
                console.error('Error al asignar turno:', result.message);
            }
        })
        .catch(error => console.error('Error en la solicitud de asignar turno:', error));
    });
});