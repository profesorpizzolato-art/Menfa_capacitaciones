import streamlit as st
from models import Material  # <--- Antes decía Recurso, ahora Material
from database_manager import Session

def modulo_biblioteca(session, rol, usuario_id):
    st.subheader("📚 Biblioteca Técnica")

    # 1. Filtro por categoría
    categorias = ["Todos", "Perforación", "Producción", "Seguridad", "General"]
    cat_sel = st.selectbox("Filtrar por categoría", categorias)

    # 2. Consulta a la base de datos (Cambiamos Recurso por Material)
    if cat_sel == "Todos":
        query = session.query(Material).all()
    else:
        query = session.query(Material).filter_by(categoria=cat_sel).all()

    # 3. Mostrar los materiales
    if not query:
        st.info("No hay materiales cargados en esta categoría.")
    else:
        for item in query:
            with st.expander(f"📖 {item.titulo}"):
                st.write(f"Categoría: {item.categoria}")
                st.video(item.link) if "youtube" in item.link or "vimeo" in item.link else st.write(f"Link: {item.link}")
                
                # Botón de acceso (estilo MENFA se hereda de styles.py)
                st.link_button("Ver Material", item.link)
