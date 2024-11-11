from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

USER_DB = 'root'
PASS_DB = ''
URL_DB = 'localhost'
NAME_DB = 'flask_sqlalchemy'
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)



class cargos(db.Model):
    id = db.column(db.integer, primary_key=True)
    cargo = db.column(db.String(250))
    
    
    def __init__(self, id, cargo):
        self.id = id
        self.cargo = cargo
        
    def json(self):
        return {'id': self.id, 'cargo': self.cargo}
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class ambulancia(db. model):
    id = db.column(db.integer, primary_key=True)
    placa = db.column(db.String(250))
    categoria_ambulancia = db.column(db.String(250))
    
    def __init__(self, id, placa, categoria_ambulancia):
        self.id = id
        self.placa = placa
        self.categoria_ambulancia = categoria_ambulancia
    
    def json(self):
        return {'id': self.id, 'placa': self.placa, 'categoria_ambulancia': self.categoria_ambulancia }
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    
class asignacionambulancia(db. model):
    id = db.column(db.integer, primary_key=True)
    ambulancia = db.column(db.String(250))
    personal = db.column(db.String(250))
    cargo = db.column(db.String(250))
    
    def __init__(self, id, ambulancia, personal, cargo):
        self.id = id
        self.ambulancia = ambulancia
        self.personal = personal
        self.cargo = cargo
        
    def json(self):
        return {'id': self.id, 'ambulancia': self.ambulancia, 'personal': self.personal, 'cargo': self.cargo}
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    

class rol(db. model):
    id = db.column(db.integer, primary_key=True)
    nombre = db.column(db.ENUM)
    
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
    
    def json(self):
        return {'id': self.id, 'nombre': self.nombre}
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    
class personal(db. model):
    id = db.column(db.integer, primary_key=True)
    nombre = db.column(db.String(250))
    apellido = db.column(db.String(250))
    numero_documento = db.column(db.String(250))
    estado = db.column(db.String(250))
    correo = db.column(db.String(250))
    contraseña = db.column(db.String(250))
    rol_id = db.column(db.String(250))
      
    def __init__(self, id, nombre, apellido, numero_documento, estado, correo, contraseña, rol_id):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.numero_documento = numero_documento
        self.estado = estado
        self.correo = correo
        self.contraseña = contraseña
        self.rol_id = rol_id
        
    def json(self):
        return{'id': self.id, 'nombre': self.nombre, 'apellido': self.apellido, 'numero_documento': self.numero_documento, 'estado': self.estado, 'correo': self.correo, 'contraseña': self.contraseña, 'rol_id': self.rol_id}
     
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    


class Hospitales(db.Model):
    __tablename__ = 'hospitales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    capacidad_atencion = db.Column(db.Integer)
    categoria = db.Column(db.Enum('basica', 'medicalizada', 'utim'))  # Ajustar según los valores específicos de categoría

    def __init__(self, nombre, direccion, capacidad_atencion, categoria):
        self.nombre = nombre
        self.direccion = direccion
        self.capacidad_atencion = capacidad_atencion
        self.categoria = categoria

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'capacidad_atencion': self.capacidad_atencion,
            'categoria': self.categoria
        }

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class ReporteViajes(db.Model):
    __tablename__ = 'reporte_viajes'
    id = db.Column(db.Integer, primary_key=True)
    ambulancia_asignada = db.Column(db.Integer)
    tiempo = db.Column(db.Time)
    paciente = db.Column(db.String(50))
    punto_i = db.Column(db.String(100))  # punto inicial
    punto_f = db.Column(db.String(100))  # punto final

    def __init__(self, ambulancia_asignada, tiempo, paciente, punto_i, punto_f):
        self.ambulancia_asignada = ambulancia_asignada
        self.tiempo = tiempo
        self.paciente = paciente
        self.punto_i = punto_i
        self.punto_f = punto_f

    def json(self):
        return {
            'id': self.id,
            'ambulancia_asignada': self.ambulancia_asignada,
            'tiempo': self.tiempo,
            'paciente': self.paciente,
            'punto_i': self.punto_i,
            'punto_f': self.punto_f
        }

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class FormularioAccidente(db.Model):
    __tablename__ = 'formularioaccidente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    numero_documento = db.Column(db.String(25))
    genero = db.Column(db.Enum('M', 'F', 'Otro'))  # Ajustar los valores según se necesite
    seguro_medico = db.Column(db.String(100))
    reporte_accidente = db.Column(db.Text)
    fecha_reporte = db.Column(db.TIMESTAMP)
    ubicacion = db.Column(db.String(255))

    def __init__(self, nombre, apellido, numero_documento, genero, seguro_medico, reporte_accidente, fecha_reporte, ubicacion):
        self.nombre = nombre
        self.apellido = apellido
        self.numero_documento = numero_documento
        self.genero = genero
        self.seguro_medico = seguro_medico
        self.reporte_accidente = reporte_accidente
        self.fecha_reporte = fecha_reporte
        self.ubicacion = ubicacion

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'numero_documento': self.numero_documento,
            'genero': self.genero,
            'seguro_medico': self.seguro_medico,
            'reporte_accidente': self.reporte_accidente,
            'fecha_reporte': self.fecha_reporte,
            'ubicacion': self.ubicacion
        }

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    
    
          
        
      