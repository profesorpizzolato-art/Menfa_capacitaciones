import streamlit as st
import os
from models import Material, Programa  # Importamos Programa también
from database_manager import Session

def modulo_biblioteca(session, rol, usuario_id):
    st.subheader("📚 Biblioteca Técnica - MENFA")

    # --- NUEVA SECCIÓN: PROGRAMAS OFICIALES ---
    st.write("### 📄 Programas de Capacitación")
    
    # Buscamos los programas que ya tienen un archivo vinculado
    programas_oficiales = session.query(Programa).filter(Programa.ruta_programa != None).all()

    if not programas_oficiales:
        st.info("Aún no se han publicado programas oficiales.")
    else:
        # Creamos columnas para que se vea más ordenado
        for prog in programas_oficiales:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{prog.nombre}**")
                    st.caption(prog.descripcion if prog.descripcion else "Sin descripción")
                with col2:
                    if os.path.exists(prog.ruta_programa):
                        with open(prog.ruta_programa, "rb") as f:
                            st.download_button(
                                label="📥 Descargar",
                                data=f,
                                file_name=os.path.basename(prog.ruta_programa),
                                key=f"btn_{prog.id}",
                                mime="application/octet-stream"
                            )
                st.write("---")

    # --- SECCIÓN: MATERIALES (VIDEOS/GUÍAS) ---
    st.write("### 📖 Material de Estudio Adicional")
    categorias = ["Todos", "Perforación", "Producción", "Seguridad", "General"]
    cat_sel = st.selectbox("Filtrar por categoría", categorias)

    if cat_sel == "Todos":
        query = session.query(Material).all()
    else:
        query = session.query(Material).filter_by(categoria=cat_sel).all()

    if not query:
        st.info("No hay materiales adicionales en esta categoría.")
    else:
        for item in query:
            with st.expander(f"📙 {item.titulo}"):
                st.write(f"Categoría: {item.categoria}")
                if "youtube.com" in item.link or "youtu.be" in item.link:
                    st.video(item.link)
                else:
                    st.link_button("Ver Recurso Externo", item.link)
