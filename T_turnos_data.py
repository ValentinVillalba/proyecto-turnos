from datetime import date, time
from app import app, db
from app.models import Turnos

#Este es un archivo para insertar datos de prueba en la tabla de turnos.

def insert_data():
    with app.app_context():
        turnos = [
            Turnos(fecha=date(2024, 6, 5), hora=time(9, 0), estado=True, id_paciente=1),
            Turnos(fecha=date(2024, 6, 5), hora=time(10, 0), estado=True, id_paciente=2),
            Turnos(fecha=date(2024, 6, 5), hora=time(11, 0), estado=True, id_paciente=3),
            Turnos(fecha=date(2024, 6, 6), hora=time(9, 0), estado=True, id_paciente=4),
            Turnos(fecha=date(2024, 6, 6), hora=time(10, 0), estado=True, id_paciente=5)
        ]
        
        print("TURNOS INSERTADOS CORRECTAMENTE")
        db.session.bulk_save_objects(turnos)
        db.session.commit()

if __name__ == '__main__':
    insert_data()
