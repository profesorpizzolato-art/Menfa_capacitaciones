import streamlit as st
import os
from database_manager import Session
from models import Programa, Usuario, Material

def admin_module():
    st.title("⚙️ Panel de Administración - MENFA")
    session = Session()

    if not os.path.exists("archivos_programas"):
        os.makedirs("archivos_programas")

    tab_alumnos, tab_programas, tab_materiales = st.tabs([
        "👥 Gestión de Alumnos", 
        "📄 Programas (PDF/Docs)", 
        "📚 Material de Estudio"
    ])
with tab_alumnos:
        st.subheader("👤 Registro de Nuevos Alumnos")
        
        with st.form("registro_alumno"):
            nombre_alumno = st.text_input("Nombre Completo")
            email_alumno = st.text_input("Email del Alumno (será su usuario)")
            pass_alumno = st.text_input("Contraseña Temporal", type="password")
            
            if st.form_submit_button("Registrar Alumno"):
                if nombre_alumno and email_alumno and pass_alumno:
                    # Verificamos si ya existe
                    existe = session.query(Usuario).filter_by(email=email_alumno).first()
                    if existe:
                        st.error("Este email ya está registrado.")
                    else:
                        nuevo_u = Usuario(
                            nombre=nombre_alumno, 
                            email=email_alumno, 
                            password=pass_alumno, 
                            rol='alumno' # <--- Importante: rol alumno
                        )
                        session.add(nuevo_u)
                        session.commit()
                        st.success(f"✅ Alumno {nombre_alumno} registrado con éxito.")
                else:
                    st.warning("Completá todos los campos.")

        st.write("---")
        st.subheader("📋 Lista de Alumnos Registrados")
        usuarios = session.query(Usuario).filter_by(rol='alumno').all()
        for u in usuarios:
            st.text(f"• {u.nombre} ({u.email})")

    with tab_programas:
        st.subheader("Gestión de Programas Oficiales")

        # SECCIÓN 1: CREAR EL NOMBRE DEL PROGRAMA
        with st.expander("➕ Crear Nuevo Nombre de Programa (Hacé clic aquí)"):
            with st.form("crear_prog_form"):
                nuevo_nombre = st.text_input("Nombre del Programa (ej: Recorredor de Campo)")
                nueva_desc = st.text_area("Descripción breve")
                if st.form_submit_button("Guardar Programa"):
                    if nuevo_nombre:
                        nuevo_p = Programa(nombre=nuevo_nombre, descripcion=nueva_desc)
                        session.add(nuevo_p)
                        session.commit()
                        st.success(f"¡Programa '{nuevo_nombre}' creado!")
                        st.rerun()

        st.write("---")

        # SECCIÓN 2: SUBIR EL ARCHIVO
        programas = session.query(Programa).all()
        nombres_prog = {p.nombre: p.id for p in programas}

        if nombres_prog:
            st.write("### Subir Archivo PDF/Word")
            prog_sel = st.selectbox("Seleccioná el curso para el archivo", list(nombres_prog.keys()))
            archivo = st.file_uploader("Arrastrá el archivo aquí", type=['pdf', 'docx', 'doc', 'pptx'])
            
            if st.button("Vincular Archivo"):
                if archivo:
                    ruta = os.path.join("archivos_programas", archivo.name)
                    with open(ruta, "wb") as f:
                        f.write(archivo.getbuffer())
                    
                    prog_db = session.query(Programa).filter_by(id=nombres_prog[prog_sel]).first()
                    prog_db.ruta_programa = ruta
                    session.commit()
                    st.success(f"✅ Archivo '{archivo.name}' vinculado con éxito.")
                else:
                    st.error("Seleccioná un archivo.")
        else:
            st.warning("⚠️ No hay programas creados. Usá el botón de arriba (+) para empezar.")

    with tab_materiales:
        st.subheader("Subir material adicional")
        st.info("Espacio para subir links de videos o guías técnicas.")

    session.close()
