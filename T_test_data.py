from app import app, db
from app.models import *

#Este es un archivo para insertar datos de prueba en la tabla de turnos.

def insert_data():
    with app.app_context():
        turnos = [
            Turnos(nombre='Juan', edad=18),
            Turnos(nombre='Carlos', edad=30),
            Turnos(nombre='Ana', edad=25),
            Turnos(nombre='Luis', edad=22),
            Turnos(nombre='Marta', edad=27)
        ]
        
        print("DATOS INSERTADOS CORRECTAMENTE")
        db.session.bulk_save_objects(turnos)
        db.session.commit()

if __name__ == '__main__':
    insert_data()
