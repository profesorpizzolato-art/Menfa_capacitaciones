from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    rol = Column(String(20), default='alumno')
    progresos = relationship("Progreso", back_populates="usuario")

class Recurso(Base):
    __tablename__ = 'recursos'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    tipo = Column(String(50)) 
    url = Column(Text, nullable=False)
    categoria = Column(String(100))
    progresos = relationship("Progreso", back_populates="recurso")

class Progreso(Base):
    __tablename__ = 'progreso'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    recurso_id = Column(Integer, ForeignKey('recursos.id'))
    completado = Column(Integer, default=0)
    ruta_programa = Column(String(255))
    usuario = relationship("Usuario", back_populates="progresos")
    recurso = relationship("Recurso", back_populates="progresos")
