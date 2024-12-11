from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
# Inicialización de la base de datos
db = SQLAlchemy()

# Definición de los enums
class RolesEnum(enum.Enum):
    SUPERADMIN = "Super Administrador"
    ADMINISTRADOR = "Administrador"
    CONDUCTOR = "Conductor"
    ENFERMERO = "Enfermero"
    PARAMEDICO = "Paramédico"
    
class CategoriaAmbulanciaEnum(enum.Enum):
    BASICA = "Básica"
    MEDICALIZADA = "Medicalizada"
    UTIM = "UTIM"

class GeneroEnum(enum.Enum):
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "Otro"

class EstadoEnum(enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class EstadoAccidenteEnum(enum.Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"
    CRITICO = "critico"
    
    
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Enum(RolesEnum), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre.value
        }


class Personal(db.Model):
    __tablename__ = 'personal'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    
    # Cambiado de String a Enum para que coincida con roles.nombre
    personal_rol = db.Column(db.Enum(RolesEnum), db.ForeignKey('roles.nombre'), nullable=True)  # Clave foránea al nombre de Roles

    # Relaciones
    rol = db.relationship('Roles', backref='personal', uselist=False)  # Relación con Roles

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible.")

    @contrasena.setter
    def contrasena(self, password):
        if not password:
            raise ValueError("La contraseña no puede estar vacía.")
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol.nombre if self.rol else None  # Devuelve el nombre del rol, no el ID
        }
# Modelos de la base de datos
# Modelo de Hospitales
class Hospitales(db.Model):
    __tablename__ = 'hospitales'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=False)
    capacidad_atencion = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.Enum('General', 'Especializado', 'Clínica', 'Emergencias'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "capacidad_atencion": self.capacidad_atencion,
            "categoria": self.categoria
        }



class Ambulancia(db.Model):
    __tablename__ = 'ambulancia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    categoria_ambulancia = db.Column(db.Enum(CategoriaAmbulanciaEnum), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitales.id', ondelete='SET NULL'))

    def to_dict(self):
        return {
            "id": self.id,
            "placa": self.placa,
            "categoria_ambulancia": self.categoria_ambulancia.value,
            "hospital_id": self.hospital_id
        }
        


class AsignacionAmbulancia(db.Model):
    __tablename__ = 'asignacion_ambulancia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personal_id = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    ambulancia_id = db.Column(db.Integer, db.ForeignKey('ambulancia.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Relaciones
    persona = db.relationship('Personal', backref='asignaciones', lazy='joined')
    ambulancia = db.relationship('Ambulancia', backref='asignaciones', lazy='joined')

    # Restricción única para asegurar que un rol no se repita en la misma ambulancia
    __table_args__ = (
        db.UniqueConstraint('ambulancia_id', 'personal_id', name='unique_ambulancia_personal'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "personal_id": self.personal_id,
            "ambulancia_id": self.ambulancia_id,  # Asegúrate de que este campo esté correctamente incluido
            "fecha_asignacion": self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            "ambulancia": self.ambulancia.to_dict() if self.ambulancia else None  # Incluir la ambulancia asociada
        }




class FormularioAccidente(db.Model):
    __tablename__ = 'formularioaccidente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    numero_documento = db.Column(db.String(255))
    genero = db.Column(db.String(10), nullable=False)
    seguro_medico = db.Column(db.String(100))
    reporte_accidente = db.Column(db.Text, nullable=False)
    fecha_reporte = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    ubicacion = db.Column(db.String(255))
    EPS = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    ambulancia_id = db.Column(db.Integer, db.ForeignKey('ambulancia.id', ondelete='SET NULL'))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "numero_documento": self.numero_documento,
            "genero": self.genero,
            "seguro_medico": self.seguro_medico,
            "reporte_accidente": self.reporte_accidente,
            "fecha_reporte": self.fecha_reporte.isoformat() if self.fecha_reporte else None,
            "ubicacion": self.ubicacion,
            "EPS": self.EPS,
            "estado": self.estado,
            "ambulancia_id": self.ambulancia_id
        }

class ReporteViajes(db.Model):
    __tablename__ = 'reporte_viajes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
 
    tiempo = db.Column(db.Time, nullable=False)
  
    punto_i = db.Column(db.String(100), nullable=True)  # Ya no es clave foránea, solo un campo de ubicación
    punto_f = db.Column(db.String(100), nullable=True)
    accidente_id = db.Column(db.Integer, db.ForeignKey('formularioaccidente.id'), nullable=True)

    # Relación explícita con la tabla FormularioAccidente
    accidente = db.relationship('FormularioAccidente', backref=db.backref('reportes_viajes', lazy=True), foreign_keys=[accidente_id])

    def to_dict(self):
        return {
            "id": self.id,
            "ambulancia_id": self.ambulancia_asignada,  # Renombrado a 'ambulancia_id' para ser más claro
            "tiempo": str(self.tiempo) if self.tiempo else None,
            "paciente": self.paciente,
            "punto_i": self.punto_i,
            "punto_f": self.punto_f,
            "accidente_id": self.accidente_id  # Asegúrate de incluirlo aquí
        }