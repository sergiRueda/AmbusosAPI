from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from flask_cors import CORS
from .modelos.modelo import db
from .modelos.modelo import db,Personal
from .modelos.modelo import RolesEnum
from .vistas.vistas import (
    VistaAmbulancias,
    VistaFormularioAccidente,
    VistaSignin,
    VistalogIn,
    VistaReporteViajes,
    VistaPersonal,
    VistaHospitales,
    VistaAsignacionAmbulancia
)

def create_app(config_name='default'):
    app = Flask(__name__)


    # Configuración de la base de datos MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/julio'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos y migración
    db.init_app(app)
    migrate = Migrate(app, db)  # Inicializa Flask-Migrate

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambia esto por una clave más segura
    jwt = JWTManager(app)  # Inicializa JWT para autenticar las peticiones

    # Habilita CORS para permitir solicitudes de otros dominios
    CORS(app)

    # Configuración de la API RESTful
    api = Api(app)

    # Definición de rutas para las vistas
    api.add_resource(VistaFormularioAccidente, '/accidentes', '/accidentes/<int:id>')
    api.add_resource(VistaPersonal, '/personal', '/personal/<int:id>')
    api.add_resource(VistaAmbulancias, '/ambulancias', '/ambulancias/<int:id>')
    api.add_resource(VistaHospitales, '/hospitales', '/hospitales/<int:id>')
    api.add_resource(VistaAsignacionAmbulancia, '/asignacion', '/asignacion/<int:id>')
    api.add_resource(VistaReporteViajes, '/reportes', '/reportes/<int:id>')

    # Rutas de login y sign-in
    api.add_resource(VistaSignin, '/signin')  # Registro de usuario (Sign-Up)
    api.add_resource(VistalogIn, '/login')    # Ingreso de usuario (Log-In)

    
    # Crear el rol SUPERADMIN y usuario inicial al iniciar la aplicación
    with app.app_context():
        crear_rol_superadmin()
        crear_usuario_superadmin()

    return app

def crear_rol_superadmin():
    """Crea el rol SUPERADMIN si no existe en la base de datos."""
    from .modelos.modelo import Roles
    if not Roles.query.filter_by(nombre=RolesEnum.SUPERADMIN).first():
        superadmin_role = Roles(nombre=RolesEnum.SUPERADMIN)
        db.session.add(superadmin_role)
        db.session.commit()

def crear_usuario_superadmin():
    """Crea un usuario SUPERADMIN si no existe en la base de datos."""
    if not Personal.query.filter_by(email="superadmin@example.com").first():
        superadmin_user = Personal(
            nombre="Superadmin",
            email="superadmin@example.com",
            contrasena_hash=generate_password_hash("securepassword"),  # Cambia por una contraseña más segura
            personal_rol=RolesEnum.SUPERADMIN
        )
        db.session.add(superadmin_user)
        db.session.commit()