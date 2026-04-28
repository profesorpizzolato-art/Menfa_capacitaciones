import streamlit as st
import os
from database_manager import Session
from models import Programa, Usuario, Material # Importaciones correctas

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
    
    # ... resto del código que te pasé antes ...
    with tab_alumnos:
        st.subheader("Registro de nuevos alumnos")
        # Aquí va tu código actual de registro de alumnos...

   with tab_programas:
        st.subheader("Gestión de Programas Oficiales")

        # --- SECCIÓN 1: CREAR EL NOMBRE DEL PROGRAMA ---
        with st.expander("➕ Crear Nuevo Nombre de Programa (Hacé clic aquí)"):
            with st.form("crear_prog_form"):
                nuevo_nombre = st.text_input("Nombre del Programa (ej: Recorredor de Campo)")
                nueva_desc = st.text_area("Descripción breve")
                if st.form_submit_button("Guardar Programa"):
                    if nuevo_nombre:
                        nuevo_p = Programa(nombre=nuevo_nombre, descripcion=nueva_desc)
                        session.add(nuevo_p)
                        session.commit()
                        st.success(f"¡Programa '{nuevo_nombre}' creado! Ahora podés subir el archivo abajo.")
                        st.rerun() # Esto actualiza la lista automáticamente

        st.write("---")

        # --- SECCIÓN 2: SUBIR EL ARCHIVO ---
        programas = session.query(Programa).all()
        nombres_prog = {p.nombre: p.id for p in programas}

        if nombres_prog:
            st.write("### Subir Archivo PDF/Word")
            prog_seleccionado = st.selectbox("Seleccioná el curso para asociar el archivo", list(nombres_prog.keys()))
            archivo = st.file_uploader("Arrastrá el archivo del programa aquí", type=['pdf', 'docx', 'doc', 'pptx'])
            
            if st.button("Vincular Archivo al Programa"):
                if archivo:
                    ruta = os.path.join("archivos_programas", archivo.name)
                    with open(ruta, "wb") as f:
                        f.write(archivo.getbuffer())
                    
                    programa_db = session.query(Programa).filter_by(id=nombres_prog[prog_seleccionado]).first()
                    programa_db.ruta_programa = ruta
                    session.commit()
                    st.success(f"✅ ¡Archivo '{archivo.name}' vinculado con éxito a {prog_seleccionado}!")
                else:
                    st.error("Por favor, seleccioná un archivo.")
        else:
            st.warning("⚠️ No hay programas creados. Usá el botón de arriba (+) para crear el primer curso.")
    with tab_materiales:
        st.subheader("Subir material adicional (Videos/Guías)")
        # Aquí va tu código actual de carga de materiales (links de YouTube, etc.)...

    session.close()
