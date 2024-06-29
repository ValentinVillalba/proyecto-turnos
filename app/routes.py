from datetime import date, time, datetime, timedelta
from functools import wraps
from flask import jsonify, render_template, request, redirect, url_for, flash, session
from app.models import Pacientes, create_connection, close_connection
from app import app, db

app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Serializar los datos de la base de datos
def serialize_data(rows):
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (timedelta, date, time)):
                row[key] = str(value)
    return rows

# Decoradores para el control de acceso
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicie sesión primero.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('Acceso denegado.')
                return redirect(url_for('logout'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# RUTAS

# Ruta para obtener todos los datos de la tabla turnos para la secretaria
@app.route('/get_data_turnos')
@login_required
@role_required('secretaria')
def get_data_turnos_secretaria():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM turnos JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente")
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])


# Ruta para obtener los turnos del usuario logueado
@app.route('/get_turnos_usuario')
@login_required
@role_required('cliente')
def get_turnos_usuario():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM turnos JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente WHERE pacientes.obra_soc = %s"
        cursor.execute(query, (session['obra_soc'],))
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])

# Ruta para ver turnos pendientes del usuario unicamente
@app.route('/get_turnos_pendientes')
@login_required
@role_required('cliente')
def get_turnos_pendientes():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM turnos JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente WHERE pacientes.obra_soc = %s AND turnos.estado = 1"
        cursor.execute(query, (session['obra_soc'],))
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])

# Ruta para ver todos los turnos pendientes
@app.route('/get_all_turnos_pendientes')
@login_required
@role_required('secretaria')
def get_all_turnos_pendientes():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM turnos WHERE estado = 1 AND asistencia=0 AND fecha >= CURDATE() ORDER BY fecha ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])

# Ruta para cancelar turnos
@app.route('/cancelar_turno', methods=['POST'])
@login_required
def cancelar_turno():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            id_turno = request.json['id_turno']
            query = "UPDATE turnos SET estado = 0 WHERE id_turno = %s"
            cursor.execute(query, (id_turno,))
            connection.commit()
            close_connection(connection)
            return jsonify({'message': 'Turno cancelado correctamente'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error al cancelar el turno'})
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'})

# Ruta para cancelar los turnos vencidos
@app.route('/cancelar_turnos_vencidos', methods=['POST'])
@login_required
@role_required('secretaria')
def cancelar_turnos_vencidos():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = "UPDATE turnos SET estado = 0 WHERE fecha < CURDATE() AND estado = 1"
            cursor.execute(query)
            connection.commit()
            close_connection(connection)
            return jsonify({'message': 'Turnos vencidos cancelados correctamente'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error al cancelar los turnos vencidos'})
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'})

# Index login
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        close_connection(connection)

        if user:
            # Guardar usuario en sesión
            session['username'] = user['nombre_usuario']
            session['role'] = user['rol']
            session['obra_soc'] = user['obra_soc']

            # Verificar el rol y redirigir según el rol
            if user['rol'] == 'secretaria':
                return redirect(url_for('secretaria_dashboard'))
            elif user['rol'] == 'cliente':
                return redirect(url_for('cliente_dashboard'))
            elif user['rol'] == 'facturista':
                return redirect(url_for('facturista_dashboard'))
        else:
            flash('Usuario o contraseña incorrecta, ingrese los datos nuevamente')
            return redirect(url_for('login'))
    else:
        return jsonify([])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/secretaria_dashboard')
@login_required
@role_required('secretaria')
def secretaria_dashboard():
    return render_template('secretaria_dashboard.html')

@app.route('/facturista_dashboard')
@login_required
@role_required('facturista')
def facturista_dashboard():
    return render_template('facturista_dashboard.html')

@app.route('/cliente_dashboard')
@login_required
def cliente_dashboard():
    return render_template('cliente_dashboard.html')

@app.route('/modifpacientes')
@login_required
def modifpacientes():
    return render_template('modifpacientes.html')

@app.route('/altaturno')
@login_required
def altaturno():
    return render_template('altaturno.html')

@app.route('/mis_turnos')
def mis_turnos():
    # Suponiendo que tienes la lógica para obtener el rol del usuario en la sesión
    user_role = session.get('role')  # O cualquier otra lógica que uses para obtener el rol
    return render_template('mis_turnos.html', user_role=user_role)

@app.route('/asistencia')
@login_required
@role_required('secretaria')
def asistencia():
    return render_template('asistencia.html')

@app.route('/cancelar_turnos')
@login_required
@role_required('cliente')
def cancelar_turnos():
    return render_template('cancelar_turno.html')

@app.route('/cancelar_turnos_admin')
@login_required
@role_required('secretaria')
def cancelar_turnos_admin():
    return render_template('cancelar_turno_admin.html')

@app.route('/todos_los_turnos')
@login_required
@role_required('secretaria')
def todos_los_turnos():
    return render_template('todos_los_turnos.html')

@app.route('/f_todos_los_turnos')
@login_required
@role_required('facturista')
def f_todos_los_turnos():
    return render_template('f_todos_los_turnos.html')

@app.route('/agregar_paciente', methods=['POST'])
@login_required
@role_required('secretaria')
def add_patient():
    data = request.json
    nombre = data.get('newPatientName')
    dni = data.get('newDni')
    fecha_nac = datetime.strptime(data.get('newBirthdate'), '%Y-%m-%d').date()
    obra_soc = data.get('newObraSocial').lower()
    telefono = data.get('newPhone')
    email = data.get('newEmail')
    direccion = data.get('newAddress')
    
    nuevo_paciente = Pacientes(
        nombre=nombre,
        dni=dni,
        fecha_nac=fecha_nac,
        obra_soc=obra_soc,
        telefono=telefono,
        email=email,
        direccion=direccion
    )
    
    db.session.add(nuevo_paciente)
    db.session.commit()
    
    return jsonify({'message': 'Paciente agregado correctamente'})

@app.route('/get_pacientes')
@login_required
@role_required('secretaria')
def get_pacientes():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM pacientes"
        cursor.execute(query)
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])

@app.route('/asignar_turno', methods=['POST'])
@login_required
@role_required('secretaria')
def asignar_turno():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            dni = request.json['dni']
            fecha = request.json['appointmentDate']
            hora = request.json['appointmentTime']
            
            cursor.execute("SELECT id_paciente FROM pacientes WHERE dni = %s", (dni,))
            result = cursor.fetchone()
            if result is None:
                return jsonify({'message': 'DNI no encontrado'})

            id_paciente = result['id_paciente']

            query = "INSERT INTO turnos (fecha, hora, estado, asistencia, id_paciente) VALUES (%s, %s, 1, 0, %s)"
            cursor.execute(query, (fecha, hora, id_paciente))
            connection.commit()
            close_connection(connection)
            return jsonify({'message': 'Turno asignado correctamente'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error al asignar el turno'})
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'})

# Ruta para obtener datos del paciente
@app.route('/get_paciente', methods=['GET'])
@login_required
@role_required('secretaria')
def get_paciente():
    dni = request.args.get('dni')
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM pacientes WHERE dni = %s"
        cursor.execute(query, (dni,))
        paciente = cursor.fetchone()
        close_connection(connection)
        if paciente:
            paciente = serialize_data([paciente])[0]
            return jsonify(paciente)
        else:
            return jsonify(None)
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'}), 500


#Ruta para actualizar datos del paciente
@app.route('/update_paciente', methods=['POST'])
@login_required
@role_required('secretaria')
def update_paciente():
    data = request.form
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
                UPDATE pacientes 
                SET nombre=%s, fecha_nac=%s, obra_soc=%s, telefono=%s, email=%s, direccion=%s 
                WHERE id_paciente=%s
            """
            cursor.execute(query, (data['patientName'], data['birthdate'], data['socialSecurity'], data['phone'], data['email'], data['address'], data['id_paciente']))
            connection.commit()
            close_connection(connection)
            return jsonify({'success': True})
        except Exception as e:
            print(f"Error: {e}")
            close_connection(connection)
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'}), 500


# Ruta para obtener todos los datos de la tabla turnos para el facturista con filtros opcionales
@app.route('/get_data_turnos_facturista')
@login_required
@role_required('facturista')
def get_data_turnos_facturista():
    obra_social = request.args.get('obraSocial')
    fecha_desde = request.args.get('fechaDesde')
    fecha_hasta = request.args.get('fechaHasta')

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT turnos.*, pacientes.*
            FROM turnos
            JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente
            WHERE 1=1
        """

        params = []
        if obra_social:
            query += " AND pacientes.obra_soc = %s"
            params.append(obra_social)
        if fecha_desde:
            query += " AND turnos.fecha >= %s"
            params.append(fecha_desde)
        if fecha_hasta:
            query += " AND turnos.fecha <= %s"
            params.append(fecha_hasta)

        query += " ORDER BY turnos.fecha ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])
# Ruta vieja para obtener todos los datos de la tabla turnos para el facturista
#@app.route('/get_data_turnos_facturista')
#@login_required
#@role_required('facturista')
#def get_data_turnos_facturista():
#    connection = create_connection()
#    if connection:
#        cursor = connection.cursor(dictionary=True)
#        cursor.execute("SELECT * FROM turnos JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente")
#        rows = cursor.fetchall()
#        close_connection(connection)
#        rows = serialize_data(rows)
#        return jsonify(rows)
#    else:
#        return jsonify([])

@app.route('/get_turnos_by_dni', methods=['GET'])
@login_required
@role_required('secretaria')
def get_turnos_by_dni():
    dni = request.args.get('dni')
    if not dni:
        return jsonify({'error': 'DNI es requerido'}), 400

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT t.id_turno, t.fecha, t.hora, t.estado, t.asistencia, p.dni
                FROM turnos t
                JOIN pacientes p ON t.id_paciente = p.id_paciente
                WHERE p.dni = %s
            """
            cursor.execute(query, (dni,))
            rows = cursor.fetchall()
            close_connection(connection)
            
            if rows:
                rows = serialize_data(rows)
                return jsonify({'turnos': rows}), 200
            else:
                return jsonify({'error': 'No se encontraron turnos para este paciente'}), 404
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Error al obtener los turnos'}), 500
    else:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

@app.route('/update_asistencia', methods=['POST'])
@login_required
@role_required('secretaria')
def update_asistencia():
    data = request.get_json()
    id_turno = data.get('id_turno')
    if not id_turno:
        return jsonify({'error': 'ID del turno es requerido'}), 400

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = "UPDATE turnos SET asistencia = %s WHERE id_turno = %s"
            cursor.execute(query, (True, id_turno))
            connection.commit()
            close_connection(connection)
            return jsonify({'message': 'Asistencia actualizada correctamente'}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Error al actualizar la asistencia'}), 500
    else:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500
    
@app.route('/get_turnos_dia_cliente')
@login_required
def get_turnos_dia_cliente():
    fecha_actual = date.today()
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT turnos.fecha, turnos.hora, pacientes.dni, pacientes.nombre, pacientes.obra_soc, turnos.estado
                FROM turnos
                JOIN pacientes ON turnos.id_paciente = pacientes.id_paciente
                WHERE turnos.fecha = %s
                ORDER BY turnos.hora ASC
            """
            cursor.execute(query, (fecha_actual,))
            rows = cursor.fetchall()
            close_connection(connection)
            rows = serialize_data(rows)
            return jsonify(rows)
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error al obtener los turnos del día'}), 500
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'}), 500
