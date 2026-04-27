import streamlit as st
from models import Usuario, Recurso

def admin_module():
    st.title("⚙️ Panel de Administración - MENFA")
    
    tab1, tab2, tab3 = st.tabs(["Registrar Alumno", "Cargar Material", "Lista de Usuarios"])
    
    # Obtener sesión de base de datos desde el estado de streamlit
    from database_manager import Session
    session = Session()

    with tab1:
        st.subheader("Alta de Nuevo Alumno")
        with st.form("nuevo_usuario"):
            nombre = st.text_input("Nombre y Apellido Completo")
            email = st.text_input("Correo Electrónico")
            rol = st.selectbox("Rol", ["alumno", "admin"])
            
            submit = st.form_submit_button("Generar Credenciales y Crear")
            
            if submit:
                if nombre and email:
                    # Lógica de contraseña automática: Apellido + 2026
                    apellido = nombre.split()[-1].lower() if " " in nombre else "menfa"
                    password_auto = f"{apellido}2026"
                    
                    nuevo_usuario = Usuario(
                        nombre=nombre,
                        email=email,
                        password=password_auto,
                        rol=rol
                    )
                    
                    try:
                        session.add(nuevo_usuario)
                        session.commit()
                        st.success(f"✅ Usuario creado con éxito.")
                        st.info(f"🔑 Contraseña provisoria: **{password_auto}**")
                        st.warning("Informale al alumno que use su apellido en minúsculas seguido de 2026.")
                    except Exception as e:
                        st.error(f"Error: El email ya está registrado.")
                else:
                    st.warning("Por favor, completá nombre y email.")

    with tab2:
        st.subheader("Subir Material a la Biblioteca")
        with st.form("nuevo_recurso"):
            titulo = st.text_input("Título del Material (ej: Guía de Well Control)")
            tipo = st.selectbox("Tipo", ["PDF", "Video", "Simulador"])
            url = st.text_input("URL (Google Drive / YouTube)")
            cat = st.selectbox("Categoría", ["Perforación", "Producción", "Well Control", "Seguridad"])
            
            if st.form_submit_button("Publicar Recurso"):
                nuevo_res = Recurso(titulo=titulo, tipo=tipo, url=url, categoria=cat)
                session.add(nuevo_res)
                session.commit()
                st.success(f"📚 '{titulo}' ya está disponible en la biblioteca.")

    with tab3:
        st.subheader("Alumnos Registrados")
        usuarios = session.query(Usuario).all()
        for u in usuarios:
            st.text(f"👤 {u.nombre} - 📧 {u.email} - 🛡️ {u.rol}")

    session.close()
