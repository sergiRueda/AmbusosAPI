from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .modelo import RolesEnum, CategoriaAmbulanciaEnum, GeneroEnum, EstadoAccidenteEnum
from .modelo import AsignacionAmbulancia, Roles, Ambulancia, Personal, FormularioAccidente, ReporteViajes, Hospitales

class RolesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True

class AmbulanciaSchema(SQLAlchemyAutoSchema):
    categoria_ambulancia = fields.Str()  # Serializar el valor del Enum como un string

    class Meta:
        model = Ambulancia
        include_relationships = True
        load_instance = True


class PersonalSchema(SQLAlchemyAutoSchema):
    # Serializa el nombre del rol directamente
    personal_rol = fields.String(attribute="rol.nombre", dump_only=True)  # Aquí es donde cambia el ID por el nombre

    class Meta:
        model = Personal
        load_instance = True  # Esto permite la deserialización para crear o actualizar instancias
        include_relationships = True  # Incluir relaciones (por ejemplo, el rol)

    @validates('personal_rol')
    def validate_personal_rol(self, value):
        # Validar que el valor del rol esté dentro de los miembros del RolesEnum
        if value not in RolesEnum.__members__:
            raise ValidationError("El valor del rol no es válido. Debe ser uno de: " + ", ".join(RolesEnum.__members__.keys()))

class FormularioAccidenteSchema(SQLAlchemyAutoSchema):
    genero = fields.Str()  # Serializa el valor de GeneroEnum como un string
    estado = fields.Str()  # Serializa el valor de EstadoAccidenteEnum como un string

    class Meta:
        model = FormularioAccidente
        include_relationships = True
        load_instance = True


class ReporteViajesSchema(SQLAlchemyAutoSchema):
    accidente = fields.Nested(FormularioAccidenteSchema)  # Relación con FormularioAccidente

    class Meta:
        model = ReporteViajes
        include_relationships = True
        load_instance = True


# Esquema de HospitalSchema para serialización
class HospitalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hospitales
        include_relationships = True
        load_instance = True


class AsignacionAmbulanciaSchema(SQLAlchemyAutoSchema):
    persona = fields.Nested('PersonalSchema')  # Relación con Personal
    ambulancia = fields.Nested('AmbulanciaSchema')  # Relación con Ambulancia

    # Aquí no necesitas serializar el rol directamente, solo accedes al nombre del rol
    rol_persona = fields.String(attribute="persona.rol.nombre", dump_only=True)  # Mostrar el rol de la persona sin permitir modificarlo

    class Meta:
        model = AsignacionAmbulancia
        include_relationships = True
        load_instance = True

    # Validación para asegurar que no se modifique el rol en la asignación
    def validate_rol(self, value):
        raise ValidationError("El rol no puede ser modificado en esta asignación.")
