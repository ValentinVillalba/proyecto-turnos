from app import app, db
from app.models import Usuarios

#Este es un archivo para insertar usuarios de prueba en la tabla de usuarios.

def insert_users():
    with app.app_context():
        users = [
            Usuarios(nombre_usuario='admin', password='admin123', rol='secretaria', id_paciente=1),
            #TODO: Cambiar cliente por OBRA SOCIAL
            Usuarios(nombre_usuario='cliente', password='cliente123', rol='cliente', id_paciente=2)
        ]
        
        print("USUARIOS INSERTADOS CORRECTAMENTE")
        db.session.bulk_save_objects(users)
        db.session.commit()

if __name__ == '__main__':
    insert_users()
