from datetime import date, time, timedelta
from functools import wraps
from flask import jsonify, render_template, request, redirect, url_for, flash, session
from app.models import create_connection, close_connection
from app import app

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
                flash('No tienes acceso a esta página.')
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
        cursor.execute("SELECT * FROM turnos")
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])

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

            # Verificar el rol y redirigir según el rol
            if user['rol'] == 'secretaria':
                return redirect(url_for('secretaria_dashboard'))
            elif user['rol'] == 'cliente':
                return redirect(url_for('cliente_dashboard'))
        else:
            flash('Usuario o password incorrecta, ingrese los datos nuevamente')
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