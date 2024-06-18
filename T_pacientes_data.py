from datetime import date
from app import app, db
from app.models import Pacientes

#Este es un archivo para insertar datos de prueba en la tabla de pacientes.

def insert_data():
    with app.app_context():
        pacientes = [
            Pacientes(nombre='Juan', dni=12345678, fecha_nac=date(2000, 1, 1), obra_soc='IOMA', telefono='123456789', email='juan@example.com', direccion='Calle 1'),
            Pacientes(nombre='Carlos', dni=23456789, fecha_nac=date(1990, 2, 2), obra_soc='OSDE', telefono='987654321', email='carlos@example.com', direccion='Calle 2'),
            Pacientes(nombre='Ana', dni=34567890, fecha_nac=date(1985, 3, 3), obra_soc='OSDE', telefono='567890123', email='ana@example.com', direccion='Calle 3'),
            Pacientes(nombre='Luis', dni=45678901, fecha_nac=date(1975, 4, 4), obra_soc='IOMA', telefono='789012345', email='luis@example.com', direccion='Calle 4'),
            Pacientes(nombre='Marta', dni=56789012, fecha_nac=date(1965, 5, 5), obra_soc='OSECAC', telefono='345678901', email='marta@example.com', direccion='Calle 5')
        ]
        
        db.session.bulk_save_objects(pacientes)
        db.session.commit()
        print("PACIENTES INSERTADOS CORRECTAMENTE")

if __name__ == '__main__':
    insert_data()
