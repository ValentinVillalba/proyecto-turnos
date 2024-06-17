from datetime import date, time, timedelta
from flask import jsonify, render_template, render_template, request, redirect, url_for, flash
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

#RUTAS

# Ruta para obtener todos los datos de la tabla turnos en el front-end
@app.route('/get_data_turnos')
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

@app.route('/secretaria_dashboard')
def secretaria_dashboard():
    return render_template('secretaria_dashboard.html')

@app.route('/cliente_dashboard')
def cliente_dashboard():
    return render_template('cliente_dashboard.html')