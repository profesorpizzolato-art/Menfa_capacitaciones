import streamlit as st
import os
from database_manager import Session
from models import Programa, Usuario, Material, Pregunta

def admin_module():
    st.title("⚙️ Panel de Administración - MENFA")
    session = Session()

    if not os.path.exists("archivos_programas"):
        os.makedirs("archivos_programas")

    # Esta es la línea 7 que fallaba. Ahora está bien alineada.
    tab_alumnos, tab_programas, tab_materiales, tab_examenes = st.tabs([
        "👥 Alumnos", "📄 Programas", "📚 Material", "📝 Exámenes"
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
                        st.error("Email ya existe.")
                    else:
                        nuevo_u = Usuario(nombre=nombre_alumno, email=email_alumno, password=pass_alumno, rol='alumno')
                        session.add(nuevo_u)
                        session.commit()
                        st.success(f"✅ {nombre_alumno} registrado.")
                        st.rerun()

    with tab_programas:
        st.subheader("📄 Gestión de Programas")
        with st.expander("➕ Crear Nuevo Programa"):
            with st.form("crear_prog"):
                n = st.text_input("Nombre del Curso")
                d = st.text_area("Descripción")
                if st.form_submit_button("Guardar"):
                    if n:
                        session.add(Programa(nombre=n, descripcion=d))
                        session.commit()
                        st.rerun()
        
        programas = session.query(Programa).all()
        if programas:
            prog_sel = st.selectbox("Seleccioná curso", {p.nombre: p.id for p in programas}.keys())
            archivo = st.file_uploader("Subir archivo", type=['pdf', 'docx'])
            if st.button("Vincular Archivo"):
                if archivo:
                    ruta = os.path.join("archivos_programas", archivo.name)
                    with open(ruta, "wb") as f: f.write(archivo.getbuffer())
                    p_db = session.query(Programa).filter_by(id={p.nombre: p.id for p in programas}[prog_sel]).first()
                    p_db.ruta_programa = ruta
                    session.commit()
                    st.success("Archivo vinculado.")

    with tab_examenes:
        st.subheader("📝 Configurar Preguntas")
        progs = session.query(Programa).all()
        if progs:
            p_sel_ex = st.selectbox("Curso para el examen", {p.nombre: p.id for p in progs}.keys())
            p_id_ex = {p.nombre: p.id for p in progs}[p_sel_ex]
            with st.form("f_preg"):
                enun = st.text_area("Pregunta")
                a = st.text_input("A")
                b = st.text_input("B")
                c = st.text_input("C")
                corr = st.selectbox("Correcta", ["A", "B", "C"])
                if st.form_submit_button("Cargar Pregunta"):
                    session.add(Pregunta(programa_id=p_id_ex, enunciado=enun, opcion_a=a, opcion_b=b, opcion_c=c, correcta=corr))
                    session.commit()
                    st.success("Pregunta cargada.")
        else:
            st.warning("Crea un programa primero.")

    session.close()
