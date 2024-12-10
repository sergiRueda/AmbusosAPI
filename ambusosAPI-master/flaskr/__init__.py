from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .modelos.modelo import db 
from .vistas.vistas import (
    VistaAmbulancias,
    VistaFormularioAccidente,
    VistaSignin, 
    VistalogIn,
    VistaReporteViajes,
    VistaPersonal,
    VistaHospitales,
    VistaAsignacionAmbulancia,# Importamos la nueva vista
)

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuración de la base de datos MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ambu'
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
    api.add_resource(VistaAsignacionAmbulancia, '/asignacion')
    api.add_resource(VistaAmbulancias, '/ambulancias')
    api.add_resource(VistaFormularioAccidente, '/accidentes')
    api.add_resource(VistaReporteViajes, '/reportes')
    api.add_resource(VistaPersonal, '/personal')
    api.add_resource(VistaHospitales, '/hospitales')  # Agregamos la nueva ruta para hospitales

    # Rutas de login y sign-in
    api.add_resource(VistaSignin, '/signin')  # Registro de usuario (Sign-Up)
    api.add_resource(VistalogIn, '/login')    # Ingreso de usuario (Log-In)
    
    return app
