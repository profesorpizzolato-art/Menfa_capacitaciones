import streamlit as st
from models import Usuario

def login(session):
    st.title("⚒️ Ingreso - MENFA Capacitaciones")
    
    with st.form("login_form"):
        email = st.text_input("Correo Electrónico")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            usuario = session.query(Usuario).filter_by(email=email, password=password).first()
            if usuario:
                st.session_state['autenticado'] = True
                st.session_state['usuario_id'] = usuario.id
                st.session_state['nombre'] = usuario.nombre
                st.session_state['rol'] = usuario.rol
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

def logout():
    st.session_state['autenticado'] = False
    st.rerun()
