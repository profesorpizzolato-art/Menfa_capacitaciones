import streamlit as st
from models import Pregunta, ExamenResultado

def mostrar_examen(session, usuario_id, programa_id):
    preguntas = session.query(Pregunta).filter_by(programa_id=programa_id).all()
    
    if not preguntas:
        st.info("Este curso aún no tiene examen disponible.")
        return

    st.write("### 📝 Evaluación Final")
    respuestas = {}
    
    for i, p in enumerate(preguntas):
        st.write(f"**{i+1}. {p.enunciado}**")
        respuestas[p.id] = st.radio(f"Seleccioná una respuesta", 
                                    [p.opcion_a, p.opcion_b, p.opcion_c], 
                                    key=f"q_{p.id}", label_visibility="collapsed")

    if st.button("Enviar Examen"):
        aciertos = 0
        for p in preguntas:
            # Mapeamos la respuesta elegida con la letra correcta
            opciones = {p.opcion_a: 'A', p.opcion_b: 'B', p.opcion_c: 'C'}
            if opciones[respuestas[p.id]] == p.correcta:
                aciertos += 1
        
        nota = (aciertos / len(preguntas)) * 100
        st.session_state.nota_final = nota
        
        # Guardar resultado
        resultado = ExamenResultado(usuario_id=usuario_id, programa_id=programa_id, nota=nota)
        session.add(resultado)
        session.commit()
        
        if nota >= 70:
            st.success(f"¡Aprobado! Tu nota es {nota}%.")
            st.balloons()
        else:
            st.error(f"Nota: {nota}%. Necesitás 70% para aprobar.")
