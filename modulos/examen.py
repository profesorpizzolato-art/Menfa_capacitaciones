import streamlit as st
from models import Pregunta, ExamenResultado

def modulo_examen(session, usuario_id, programa_id, nombre_programa):
    st.subheader(f"📝 Evaluación: {nombre_programa}")
    
    # Buscamos las preguntas cargadas para este curso
    preguntas = session.query(Pregunta).filter_by(programa_id=programa_id).all()
    
    if not preguntas:
        st.info("Aún no se han cargado preguntas para este examen. Consultá con el instructor.")
        return

    # Usamos un formulario para que no se refresque la página con cada click
    with st.form("examen_form"):
        respuestas_usuario = {}
        
        for i, p in enumerate(preguntas):
            st.write(f"**{i+1}. {p.enunciado}**")
            respuestas_usuario[p.id] = st.radio(
                "Seleccioná la respuesta correcta:",
                [p.opcion_a, p.opcion_b, p.opcion_c],
                key=f"preg_{p.id}"
            )
            st.write("---")
            
        btn_enviar = st.form_submit_button("Finalizar y Entregar Examen")

    if btn_enviar:
        aciertos = 0
        for p in preguntas:
            # Comparamos la opción seleccionada con la correcta (A, B o C)
            opciones_map = {p.opcion_a: 'A', p.opcion_b: 'B', p.opcion_c: 'C'}
            if opciones_map[respuestas_usuario[p.id]] == p.correcta:
                aciertos += 1
        
        nota = (aciertos / len(preguntas)) * 100
        
        # Guardamos el resultado en la base de datos
        nuevo_resultado = ExamenResultado(
            usuario_id=usuario_id,
            programa_id=programa_id,
            nota=nota
        )
        session.add(nuevo_resultado)
        session.commit()

        if nota >= 70:
            st.success(f"¡Felicitaciones! Aprobaste con {nota:.1f}%")
            st.balloons()
            st.info("Ya podés solicitar tu certificado oficial de MENFA.")
        else:
            st.error(f"Tu nota fue de {nota:.1f}%. Necesitás al menos 70% para aprobar.")
            st.warning("Repasá el material de estudio e intentálo nuevamente.")
