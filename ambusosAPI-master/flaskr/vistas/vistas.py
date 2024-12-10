from flask import request
from flask_restful import Resource
from ..modelos import db,AsignacionAmbulancia,AsignacionAmbulanciaSchema, Roles, RolesSchema, Ambulancia, Personal, FormularioAccidente, ReporteViajes, AmbulanciaSchema, PersonalSchema, FormularioAccidenteSchema, ReporteViajesSchema, Hospitales, HospitalSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
# Esquemas para serializar los datos
asignacion_ambulancia_schema = AsignacionAmbulanciaSchema()
asignaciones_ambulancia_schema = AsignacionAmbulanciaSchema(many=True)
hospital_schema = HospitalSchema()
hospitales_schema = HospitalSchema(many=True)
ambulancia_schema = AmbulanciaSchema()
ambulancias_schema = AmbulanciaSchema(many=True)
personal_schema = PersonalSchema()
personales_schema = PersonalSchema(many=True)
formulario_accidente_schema = FormularioAccidenteSchema()
formulario_accidente_schema = FormularioAccidenteSchema(many=True)
reporte_viajes_schema = ReporteViajesSchema()
reportes_viajes_schema = ReporteViajesSchema(many=True)



import logging

from flask import request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

class VistaSignin(Resource):
    def post(self):
        # Obtener los datos enviados en el cuerpo de la solicitud
        nombre_Personal = request.json.get("nombre")
        email_Personal = request.json.get("email")
        contrasena_Personal = request.json.get("contrasena")
        rol_nombre = request.json.get("rol")  # Obtener el nombre del rol, no el ID

        # Verificar que todos los campos necesarios estén presentes
        if not nombre_Personal or not email_Personal or not contrasena_Personal:
            return {"mensaje": "Nombre, email y contraseña son obligatorios."}, 400
        
        # Comprobar si el nombre ya está registrado
        if Personal.query.filter_by(nombre=nombre_Personal).first():
            logging.error(f"El nombre de usuario {nombre_Personal} ya está registrado.")
            return {"mensaje": "El nombre de usuario ya está registrado"}, 409
        
        # Comprobar si el correo electrónico ya está registrado
        if Personal.query.filter_by(email=email_Personal).first():
            logging.error(f"El correo electrónico {email_Personal} ya está registrado.")
            return {"mensaje": "El correo electrónico ya está registrado"}, 409

        # Validar si el nombre del rol existe en la tabla Roles
        if rol_nombre:
            rol = Roles.query.filter_by(nombre=rol_nombre).first()  # Buscar por nombre de rol
            if not rol:
                return {"mensaje": f"El rol '{rol_nombre}' no existe."}, 404
        else:
            rol = None  # Si no se pasa un rol, lo dejamos como None

        # Crear el nuevo usuario
        try:
            nuevo_Personal = Personal(
                nombre=nombre_Personal, 
                email=email_Personal,
                personal_rol=rol_nombre,  # Asignar el nombre del rol encontrado
            )
            nuevo_Personal.contrasena = contrasena_Personal  # Esto llamará al setter que hace el hash
        except ValueError as e:
            logging.error(f"Error al crear la contraseña: {e}")
            return {"mensaje": str(e)}, 400

        # Agregar el nuevo usuario a la base de datos
        db.session.add(nuevo_Personal)

        try:
            db.session.commit()
        except IntegrityError as e:
            logging.error(f"Error al crear el usuario: {e}")
            db.session.rollback()
            return {"mensaje": "Error al crear el usuario. Intenta nuevamente."}, 500

        # Retornar una respuesta exitosa
        return {"mensaje": "Usuario creado exitosamente. Ahora puede iniciar sesión."}, 201


class VistalogIn(Resource):
    def post(self):
        nombre = request.json.get("nombre")
        contrasena = request.json.get("contrasena")
        usuario = Personal.query.filter_by(nombre=nombre).first()
        if usuario and usuario.verificar_contrasena(contrasena):
            token_de_acceso = create_access_token(identity=nombre)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}, 200
        return {"mensaje": "Usuario o contraseña incorrectos"}, 401
class VistaPersonal(Resource):
    
    def get(self):
        """Obtener todos los registros de personal"""
        personales = Personal.query.all()
        return personales_schema.dump(personales), 200

    def post(self):
        """Crear un nuevo personal"""
        # Obtener el rol de la solicitud, si existe
        rol_nombre = request.json.get('rol', None)
        rol = Roles.query.filter_by(nombre=rol_nombre).first() if rol_nombre else None
        
        # Crear nuevo objeto Personal
        nuevo_personal = Personal(
            nombre=request.json['nombre'],
            email=request.json['email'],
            contrasena=request.json['contrasena'],
            personal_rol=rol.nombre if rol else None  # Asignar el rol por nombre
        )
        
        # Añadir y guardar en la base de datos
        db.session.add(nuevo_personal)
        db.session.commit()

        return personal_schema.dump(nuevo_personal), 201

    def put(self, id):
        """Actualizar un personal existente"""
        personal = Personal.query.get(id)
        
        if not personal:
            return {"mensaje": "Usuario no encontrado."}, 404

        # Actualizar los datos del personal
        personal.nombre = request.json.get('nombre', personal.nombre)
        personal.email = request.json.get('email', personal.email)
        
        # Actualizar el rol, si se ha enviado uno en la solicitud
        rol_nombre = request.json.get('rol', None)
        if rol_nombre:
            rol = Roles.query.filter_by(nombre=rol_nombre).first()
            personal.personal_rol = rol.nombre if rol else None
        
        # Guardar los cambios en la base de datos
        db.session.commit()

        return personal_schema.dump(personal), 200

    def delete(self, id):
        """Eliminar un personal por su ID"""
        personal = Personal.query.get(id)
        
        if not personal:
            return {"mensaje": "Usuario no encontrado."}, 404

        # Eliminar de la base de datos
        db.session.delete(personal)
        db.session.commit()

        return {"mensaje": "Usuario eliminado."}, 204
class VistaAmbulancias(Resource):
    def get(self):
        return ambulancias_schema.dump(Ambulancia.query.all()), 200

    def post(self):
        nueva_ambulancia = Ambulancia(
            placa=request.json['placa'],
            categoria_ambulancia=request.json['categoria_ambulancia'],
            hospital_id=request.json.get('hospital_id')
        )
        db.session.add(nueva_ambulancia)
        db.session.commit()
        return ambulancia_schema.dump(nueva_ambulancia), 201

    def put(self, id):
        ambulancia = Ambulancia.query.get(id)
        if not ambulancia:
            return {"mensaje": "Ambulancia no encontrada."}, 404

        ambulancia.placa = request.json.get('placa', ambulancia.placa)
        ambulancia.categoria_ambulancia = request.json.get('categoria_ambulancia', ambulancia.categoria_ambulancia)
        db.session.commit()
        return ambulancia_schema.dump(ambulancia), 200

    def delete(self, id):
        ambulancia = Ambulancia.query.get(id)
        if not ambulancia:
            return {"mensaje": "Ambulancia no encontrada."}, 404

        db.session.delete(ambulancia)
        db.session.commit()
        return {"mensaje": "Ambulancia eliminada."}, 204


# Vista para gestionar los formularios de accidente
class VistaFormularioAccidente(Resource):
    def get(self):
        return formulario_accidente_schema.dump(FormularioAccidente.query.all()), 200

    def post(self):
        nuevo_formulario = FormularioAccidente(
            descripcion=request.json['descripcion'],
            fecha=request.json['fecha'],
            ambulancia_id=request.json.get('ambulancia_id')
        )
        db.session.add(nuevo_formulario)
        db.session.commit()
        return formulario_accidente_schema.dump(nuevo_formulario), 201

    def put(self, id):
        formulario = FormularioAccidente.query.get(id)
        if not formulario:
            return {"mensaje": "Formulario no encontrado."}, 404

        formulario.descripcion = request.json.get('descripcion', formulario.descripcion)
        db.session.commit()
        return formulario_accidente_schema.dump(formulario), 200

    def delete(self, id):
        formulario = FormularioAccidente.query.get(id)
        if not formulario:
            return {"mensaje": "Formulario no encontrado."}, 404

        db.session.delete(formulario)
        db.session.commit()
        return {"mensaje": "Formulario eliminado."}, 204


# Vista para gestionar los reportes de viajes
class VistaReporteViajes(Resource):
    def get(self):
        reportes = ReporteViajes.query.all()
        return reportes_viajes_schema.dump(reportes), 200

    def post(self):
        nuevo_reporte = ReporteViajes(
            destino=request.json['destino'],
            fecha=request.json['fecha'],
            ambulancia_id=request.json.get('ambulancia_id')
        )
        db.session.add(nuevo_reporte)
        db.session.commit()
        return reporte_viajes_schema.dump(nuevo_reporte), 201

    def put(self, id):
        reporte = ReporteViajes.query.get(id)
        if not reporte:
            return {"mensaje": "Reporte no encontrado."}, 404

        reporte.destino = request.json.get('destino', reporte.destino)
        reporte.fecha = request.json.get('fecha', reporte.fecha)
        reporte.ambulancia_id = request.json.get('ambulancia_id', reporte.ambulancia_id)
        db.session.commit()
        return reporte_viajes_schema.dump(reporte), 200

    def delete(self, id):
        reporte = ReporteViajes.query.get(id)
        if not reporte:
            return {"mensaje": "Reporte no encontrado."}, 404

        db.session.delete(reporte)
        db.session.commit()
        return {"mensaje": "Reporte eliminado."}, 204
# Vista para gestionar los hospitales
class VistaHospitales(Resource):
    def get(self):
        """Obtiene todos los hospitales."""
        hospitales = Hospitales.query.all()
        return hospitales_schema.dump(hospitales), 200

    def post(self):
        """Crea un nuevo hospital."""
        # Obtén los datos del cuerpo de la solicitud
        nuevo_hospital = Hospitales(
            nombre=request.json['nombre'],
            direccion=request.json['direccion'],
            capacidad_atencion=request.json['capacidad_atencion'],
            categoria=request.json['categoria']
        )
        
        db.session.add(nuevo_hospital)
        db.session.commit()
        return hospital_schema.dump(nuevo_hospital), 201

    def put(self, id):
        """Actualiza los datos de un hospital."""
        hospital = Hospitales.query.get(id)
        if not hospital:
            return {"mensaje": "Hospital no encontrado."}, 404
        
        hospital.nombre = request.json.get('nombre', hospital.nombre)
        hospital.direccion = request.json.get('direccion', hospital.direccion)
        hospital.capacidad_atencion = request.json.get('capacidad_atencion', hospital.capacidad_atencion)
        hospital.categoria = request.json.get('categoria', hospital.categoria)
        
        db.session.commit()
        return hospital_schema.dump(hospital), 200

    def delete(self, id):
        """Elimina un hospital."""
        hospital = Hospitales.query.get(id)
        if not hospital:
            return {"mensaje": "Hospital no encontrado."}, 404

        db.session.delete(hospital)
        db.session.commit()
        return {"mensaje": "Hospital eliminado."}, 204
    
class VistaAsignacionAmbulancia(Resource):
    def get(self):
        """Obtener todas las asignaciones de ambulancia."""
        asignaciones = AsignacionAmbulancia.query.all()
        return asignaciones_ambulancia_schema.dump(asignaciones), 200

    def post(self):
        """Crear una nueva asignación de ambulancia."""
        # Obtener los datos del cuerpo de la solicitud
        id_persona = request.json.get('id_persona')
        id_ambulancia = request.json.get('id_ambulancia')

        # Verificar que los datos sean válidos
        if not id_persona or not id_ambulancia:
            return {"mensaje": "Se deben proporcionar 'id_persona' y 'id_ambulancia'."}, 400
        
        # Crear una nueva asignación de ambulancia
        nueva_asignacion = AsignacionAmbulancia(
            id_persona=id_persona,
            id_ambulancia=id_ambulancia
        )

        # Guardar en la base de datos
        db.session.add(nueva_asignacion)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {"mensaje": "Error al crear la asignación. Intenta nuevamente."}, 500

        # Devolver la asignación creada
        return asignacion_ambulancia_schema.dump(nueva_asignacion), 201

    def put(self, id):
        """Actualizar una asignación de ambulancia existente."""
        asignacion = AsignacionAmbulancia.query.get(id)
        if not asignacion:
            return {"mensaje": "Asignación no encontrada."}, 404

        # Actualizar los datos de la asignación
        id_persona = request.json.get('id_persona', asignacion.id_persona)
        id_ambulancia = request.json.get('id_ambulancia', asignacion.id_ambulancia)

        # Actualizar los campos
        asignacion.id_persona = id_persona
        asignacion.id_ambulancia = id_ambulancia
        db.session.commit()

        return asignacion_ambulancia_schema.dump(asignacion), 200

    def delete(self, id):
        """Eliminar una asignación de ambulancia."""
        asignacion = AsignacionAmbulancia.query.get(id)
        if not asignacion:
            return {"mensaje": "Asignación no encontrada."}, 404

        db.session.delete(asignacion)
        db.session.commit()

        return {"mensaje": "Asignación eliminada."}, 204
