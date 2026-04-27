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
        st.subheader("Cargar Programa Oficial (Archivo)")
        st.write("Subí el PDF o Word con el programa completo del curso.")

        # Buscamos qué programas existen en la DB para asociar el archivo
        programas = session.query(Programa).all()
        nombres_prog = {p.nombre: p.id for p in programas}

        if nombres_prog:
            prog_seleccionado = st.selectbox("Seleccioná el curso", list(nombres_prog.keys()))
            
            archivo = st.file_uploader("Seleccioná el programa", type=['pdf', 'docx', 'doc'])
            
            if st.button("Vincular Archivo al Programa"):
                if archivo:
                    # Guardamos el archivo físico
                    ruta = os.path.join("archivos_programas", archivo.name)
                    with open(ruta, "wb") as f:
                        f.write(archivo.getbuffer())
                    
                    # Guardamos la ruta en la base de datos
                    programa_db = session.query(Programa).filter_by(id=nombres_prog[prog_seleccionado]).first()
                    programa_db.ruta_programa = ruta
                    session.commit()
                    
                    st.success(f"✅ Programa de '{prog_seleccionado}' actualizado con el archivo: {archivo.name}")
                else:
                    st.error("Por favor, seleccioná un archivo.")
        else:
            st.warning("⚠️ No hay programas creados. Primero creá un programa (nombre y descripción) para poder subirle un archivo.")

    with tab_materiales:
        st.subheader("Subir material adicional (Videos/Guías)")
        # Aquí va tu código actual de carga de materiales (links de YouTube, etc.)...

    session.close()
