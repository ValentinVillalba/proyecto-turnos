from app import app, db
from app.models import Turnos
from sqlalchemy import text

#Este archivo sirve para ELIMINAR COMPLETAMENTE todos los datos de la tabla de turnos.

def clear_data():
    with app.app_context():
        db.session.query(Turnos).delete()
        query = text("ALTER TABLE Turnos AUTO_INCREMENT = 1")
        db.session.execute(query)
        db.session.commit()
        print("TODOS LOS DATOS DE LA TABLA FUERON BORRADOS")

if __name__ == '__main__':
    clear_data()
