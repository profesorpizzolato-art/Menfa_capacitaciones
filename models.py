from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol = Column(String(20))  # 'admin' o 'alumno'

class Programa(Base):
    __tablename__ = 'programas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    ruta_programa = Column(String(255)) # Para el PDF del programa

class Material(Base): # <--- ACÁ ESTABA EL ERROR (Antes era Recurso)
    __tablename__ = 'materiales'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(150))
    categoria = Column(String(50))
    link = Column(String(255))

class Pregunta(Base):
    __tablename__ = 'preguntas'
    id = Column(Integer, primary_key=True)
    programa_id = Column(Integer, ForeignKey('programas.id'))
    enunciado = Column(Text)
    opcion_a = Column(String(255))
    opcion_b = Column(String(255))
    opcion_c = Column(String(255))
    correcta = Column(String(1)) # 'A', 'B' o 'C'

class ExamenResultado(Base):
    __tablename__ = 'resultados'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    programa_id = Column(Integer, ForeignKey('programas.id'))
    nota = Column(Float)
