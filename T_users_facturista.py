from app import app, db
from app.models import Usuarios

def insert_user_facturista():
    with app.app_context():
        # Verificar si ya existe un usuario con el rol 'facturista'
        existing_user = Usuarios.query.filter_by(rol='facturista').first()
        if existing_user:
            print("Ya existe un usuario con el rol de facturista.")
        else:
            # Crear un nuevo usuario con rol 'facturista'
            new_user = Usuarios(nombre_usuario='facturista', password='factu123', rol='facturista')
            db.session.add(new_user)
            db.session.commit()
            print("Usuario facturista insertado correctamente.")

if __name__ == '__main__':
    insert_user_facturista()
