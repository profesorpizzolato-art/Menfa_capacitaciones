from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# AQUÍ ESTABA EL ERROR: Debe decir 'models' (sin la o)
from models import Base 

engine = create_engine('sqlite:///menfa_datos.db', connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def inicializar_sistema():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        import streamlit as st
        st.error(f"Error DB: {e}")

if __name__ == "__main__":
    inicializar_sistema()
