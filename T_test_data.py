from app import app, db
from app.models import TablaTurnos

#Este es un archivo para insertar datos de prueba en la tabla de turnos.

def insert_data():
    with app.app_context():
        turnos = [
            TablaTurnos(nombre='Juan'),
            TablaTurnos(nombre='Carlos'),
            TablaTurnos(nombre='Ana'),
            TablaTurnos(nombre='Luis'),
            TablaTurnos(nombre='Marta')
        ]
        
        print("DATOS INSERTADOS CORRECTAMENTE")
        db.session.bulk_save_objects(turnos)
        db.session.commit()

if __name__ == '__main__':
    insert_data()
