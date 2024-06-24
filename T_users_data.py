from app import app, db
from app.models import Usuarios

#Este es un archivo para insertar usuarios de prueba en la tabla de usuarios.
#USAR ESTE ARCHIVO SOLAMENTE UNA VEZ!!! Comentar usuario "admin" si se necesita usar de nuevo.

def insert_users():
    with app.app_context():
        users = [
            Usuarios(nombre_usuario='admin', password='admin123', rol='secretaria'),

            # Usuarios de prueba para las obras sociales
           # Usuarios(nombre_usuario='facturista', password='factu123', rol='facturista'),
            Usuarios(nombre_usuario='osde', password='osde123', rol='cliente', obra_soc='OSDE'),
            Usuarios(nombre_usuario='ioma', password='ioma123', rol='cliente', obra_soc='IOMA'),
            Usuarios(nombre_usuario='osecac', password='osecac123', rol='cliente', obra_soc='OSECAC')
           ]
        
        print("USUARIOS INSERTADOS CORRECTAMENTE")
        db.session.bulk_save_objects(users)
        db.session.commit()

if __name__ == '__main__':
    insert_users()
