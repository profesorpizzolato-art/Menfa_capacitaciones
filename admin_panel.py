import streamlit as st
from models import Usuario, Recurso

def admin_module():
    st.title("⚙️ Panel de Administración CRM")
    
    tab1, tab2 = st.tabs(["Gestionar Alumnos", "Cargar Material"])
    
    with tab1:
        st.subheader("Registrar Nuevo Alumno")
        with st.form("nuevo_usuario"):
            nombre = st.text_input("Nombre Completo")
            email = st.text_input("Email")
            pw = st.text_input("Contraseña Provisional")
            rol = st.selectbox("Rol", ["alumno", "admin"])
            if st.form_submit_button("Crear Usuario"):
                st.success(f"Usuario {nombre} creado con éxito.")
                # Aquí iría el session.add(Usuario(...))

    with tab2:
        st.subheader("Subir Material a la Biblioteca")
        with st.form("nuevo_recurso"):
            titulo = st.text_input("Título del Material")
            tipo = st.selectbox("Tipo", ["PDF", "Video", "Simulador"])
            url = st.text_input("URL (Drive/YouTube)")
            cat = st.text_input("Categoría (ej: Perforación)")
            if st.form_submit_button("Publicar"):
                st.success("Material publicado en la plataforma.")
