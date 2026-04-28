from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol = Column(String(20)) # 'admin' o 'alumno'

class Programa(Base):
    __tablename__ = 'programas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    ruta_programa = Column(String(255))

class Material(Base): # Asegurate de que se llame Material, NO Recurso
    __tablename__ = 'materiales'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    link = Column(String(255))
    categoria = Column(String(50))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
