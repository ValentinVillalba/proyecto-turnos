from datetime import date, datetime, time, timedelta
from functools import wraps
from flask import jsonify, render_template, request, redirect, url_for, flash, session
from app.models import Pacientes, create_connection, close_connection
from app import app, db

app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

#Serializar los datos de la base de datos
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

#RUTAS

# Ruta para obtener todos los datos de la tabla turnos en el front-end
@app.route('/get_data_turnos')
@login_required #Recordar agregar este decorador siempre a todas las rutas, excepto login y logout
@role_required('secretaria') #Recordar agregar este decorador a las rutas que son SOLO para secretaria
def get_data():
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
def get_data_usuario():
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
        query = "SELECT * FROM turnos WHERE estado = 1"
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

@app.route('/cliente_dashboard')
@login_required
def cliente_dashboard():
    return render_template('cliente_dashboard.html')

@app.route('/altaturno')
@login_required
def altaturno():
    return render_template('altaturno.html')

@app.route('/mis_turnos')
@login_required
@role_required('cliente')
def mis_turnos():
    return render_template('mis_turnos.html')


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

            query = "INSERT INTO turnos (fecha, hora, estado, id_paciente) VALUES (%s, %s, 1, %s)"
            cursor.execute(query, (fecha, hora, id_paciente))
            connection.commit()
            close_connection(connection)
            return jsonify({'message': 'Turno asignado correctamente'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Error al asignar el turno'})
    else:
        return jsonify({'message': 'Error al conectar a la base de datos'})