import streamlit as st
from models import Material

def modulo_biblioteca(session, rol, usuario_id):
    st.title("📚 Biblioteca Técnica")
    
    # Filtros por categoría (útil para Perforación/Producción)
    categorias = ["Todos", "Perforación", "Producción", "Well Control", "Seguridad"]
    cat_sel = st.selectbox("Filtrar por categoría", categorias)
    
    query = session.query(Recurso)
    if cat_sel != "Todos":
        query = query.filter_by(categoria=cat_sel)
    
    recursos = query.all()
    
    if not recursos:
        st.info("No hay material cargado en esta sección todavía.")
        return

    for res in recursos:
        with st.expander(f"{res.titulo} ({res.tipo})"):
            st.write(f"Categoría: {res.categoria}")
            st.video(res.url) if res.tipo == "Video" else st.markdown(f"[🔗 Abrir Recurso]({res.url})")
            
            # Botón de marcar como completado
            if st.button(f"Marcar como visto: {res.titulo}", key=f"btn_{res.id}"):
                nuevo_progreso = Progreso(usuario_id=usuario_id, recurso_id=res.id, completado=1)
                session.add(nuevo_progreso)
                session.commit()
                st.success("¡Progreso guardado!")
