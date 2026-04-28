import streamlit as st
import os
from database_manager import Session
from models import Programa, Usuario, Material

# Dentro de admin_module(), agregar tab_examenes a los st.tabs
    tab_alumnos, tab_programas, tab_materiales, tab_examenes = st.tabs([
        "👥 Alumnos", "📄 Programas", "📚 Material", "📝 Configurar Examen"
    ])

    with tab_alumnos:
        st.subheader("👤 Registro de Nuevos Alumnos")
        with st.form("registro_alumno"):
            nombre_alumno = st.text_input("Nombre Completo")
            email_alumno = st.text_input("Email (Usuario)")
            pass_alumno = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Registrar Alumno"):
                if nombre_alumno and email_alumno and pass_alumno:
                    existe = session.query(Usuario).filter_by(email=email_alumno).first()
                    if existe:
                        st.error("Este email ya existe.")
                    else:
                        nuevo_u = Usuario(nombre=nombre_alumno, email=email_alumno, password=pass_alumno, rol='alumno')
                        session.add(nuevo_u)
                        session.commit()
                        st.success(f"✅ {nombre_alumno} registrado.")
                        st.rerun()
                else:
                    st.warning("Completá todos los campos.")

    with tab_programas:
        st.subheader("Gestión de Programas Oficiales")
        with st.expander("➕ Crear Nuevo Nombre de Programa"):
            with st.form("crear_prog_form"):
                nuevo_nombre = st.text_input("Nombre del Curso")
                nueva_desc = st.text_area("Descripción")
                if st.form_submit_button("Guardar Programa"):
                    if nuevo_nombre:
                        nuevo_p = Programa(nombre=nuevo_nombre, descripcion=nueva_desc)
                        session.add(nuevo_p)
                        session.commit()
                        st.rerun()

        st.write("---")
        programas = session.query(Programa).all()
        nombres_prog = {p.nombre: p.id for p in programas}
        if nombres_prog:
            prog_sel = st.selectbox("Seleccioná el curso", list(nombres_prog.keys()))
            archivo = st.file_uploader("Subir archivo", type=['pdf', 'docx', 'doc', 'pptx'])
            if st.button("Vincular Archivo"):
                if archivo:
                    ruta = os.path.join("archivos_programas", archivo.name)
                    with open(ruta, "wb") as f:
                        f.write(archivo.getbuffer())
                    p_db = session.query(Programa).filter_by(id=nombres_prog[prog_sel]).first()
                    p_db.ruta_programa = ruta
                    session.commit()
                    st.success("✅ Archivo vinculado.")
        else:
            st.warning("Crea un programa primero.")

    with tab_materiales:
        st.subheader("Subir material adicional")
        st.info("Sección para videos y guías.")
    # Dentro de admin_module(), agregar tab_examenes a los st.tabs
    tab_alumnos, tab_programas, tab_materiales, tab_examenes = st.tabs([
        "👥 Alumnos", "📄 Programas", "📚 Material", "📝 Configurar Examen"
    ])

    with tab_examenes:
        st.subheader("📝 Cargar Preguntas de Examen")
        programas = session.query(Programa).all()
        if programas:
            prog_sel = st.selectbox("Curso del Examen", {p.nombre: p.id for p in programas}.keys(), key="prog_exam")
            prog_id = {p.nombre: p.id for p in programas}[prog_sel]
            
            with st.form("nueva_pregunta"):
                enunciado = st.text_area("Pregunta")
                col1, col2, col3 = st.columns(3)
                a = col1.text_input("Opción A")
                b = col2.text_input("Opción B")
                c = col3.text_input("Opción C")
                correcta = st.selectbox("Correcta", ["A", "B", "C"])
                
                if st.form_submit_button("Guardar Pregunta"):
                    nueva_q = Pregunta(programa_id=prog_id, enunciado=enunciado, 
                                       opcion_a=a, opcion_b=b, opcion_c=c, correcta=correcta)
                    session.add(nueva_q)
                    session.commit()
                    st.success("Pregunta agregada.")
        else:
            st.warning("Primero creá un programa.")
    session.close()
