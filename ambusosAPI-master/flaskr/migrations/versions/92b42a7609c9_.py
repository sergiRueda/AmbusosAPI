"""empty message

Revision ID: 92b42a7609c9
Revises: 
Create Date: 2024-12-06 17:01:45.644027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b42a7609c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospitales',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('direccion', sa.String(length=200), nullable=False),
    sa.Column('capacidad_atencion', sa.Integer(), nullable=False),
    sa.Column('categoria', sa.Enum('General', 'Especializado', 'Clínica', 'Emergencias'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.Enum('ADMINISTRADOR', 'CONDUCTOR', 'ENFERMERO', 'PARAMEDICO', name='rolesenum'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('ambulancia',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('placa', sa.String(length=10), nullable=False),
    sa.Column('categoria_ambulancia', sa.Enum('BASICA', 'MEDICALIZADA', 'UTIM', name='categoriaambulanciaenum'), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitales.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('placa')
    )
    op.create_table('personal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('contrasena_hash', sa.String(length=255), nullable=False),
    sa.Column('personal_rol', sa.Enum('ADMINISTRADOR', 'CONDUCTOR', 'ENFERMERO', 'PARAMEDICO', name='rolesenum'), nullable=True),
    sa.ForeignKeyConstraint(['personal_rol'], ['roles.nombre'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('asignacion_ambulancia',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_persona', sa.Integer(), nullable=False),
    sa.Column('id_ambulancia', sa.Integer(), nullable=False),
    sa.Column('fecha_asignacion', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_ambulancia'], ['ambulancia.id'], ),
    sa.ForeignKeyConstraint(['id_persona'], ['personal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('formularioaccidente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('apellido', sa.String(length=50), nullable=False),
    sa.Column('numero_documento', sa.String(length=255), nullable=True),
    sa.Column('genero', sa.Enum('MASCULINO', 'FEMENINO', 'OTRO', name='generoenum'), nullable=False),
    sa.Column('seguro_medico', sa.String(length=100), nullable=True),
    sa.Column('reporte_accidente', sa.Text(), nullable=False),
    sa.Column('fecha_reporte', sa.DateTime(), nullable=False),
    sa.Column('ubicacion', sa.String(length=255), nullable=True),
    sa.Column('EPS', sa.String(length=100), nullable=False),
    sa.Column('estado', sa.Enum('LEVE', 'MODERADO', 'GRAVE', 'CRITICO', name='estadoaccidenteenum'), nullable=False),
    sa.Column('ambulancia_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ambulancia_id'], ['ambulancia.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reporte_viajes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ambulancia_asignada', sa.Integer(), nullable=False),
    sa.Column('tiempo', sa.Time(), nullable=False),
    sa.Column('paciente', sa.String(length=50), nullable=True),
    sa.Column('punto_i', sa.String(length=100), nullable=True),
    sa.Column('punto_f', sa.String(length=100), nullable=True),
    sa.Column('accidente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accidente_id'], ['formularioaccidente.id'], ),
    sa.ForeignKeyConstraint(['ambulancia_asignada'], ['ambulancia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reporte_viajes')
    op.drop_table('formularioaccidente')
    op.drop_table('asignacion_ambulancia')
    op.drop_table('personal')
    op.drop_table('ambulancia')
    op.drop_table('roles')
    op.drop_table('hospitales')
    # ### end Alembic commands ###