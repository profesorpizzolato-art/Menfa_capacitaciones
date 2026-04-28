import streamlit as st
import sys
import os

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="MENFA Capacitaciones", layout="wide", page_icon="⚒️")

# 2. Forzar ruta raíz
path_raiz = os.path.dirname(os.path.abspath(__file__))
if path_raiz not in sys.path:
    sys.path.insert(0, path_raiz)

# 3. Importaciones (Limpias y ordenadas)
try:
    from modulos.styles import aplicar_estilos_web, mostrar_logo
    from database_manager import Session, inicializar_sistema
    from modulos.auth import login, logout
    from modulos.biblioteca import modulo_biblioteca
    from modulos.examen import modulo_examen
    from admin_panel import admin_module
    from crear_admin import crear_primer_admin
    import models
    exito_import = True
except ImportError as e:
    st.error(f"Error crítico de archivos: {e}")
    exito_import = False

def main():
    if not exito_import:
        return

    aplicar_estilos_web()
    inicializar_sistema()
    crear_primer_admin()
    
    session = Session()

    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False

    if not st.session_state['autenticado']:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mostrar_logo(ancho=300)
            login(session)
    else:
        with st.sidebar:
            mostrar_logo(ancho=150)
            st.write("---")
            st.sidebar.title(f"Hola, {st.session_state.get('nombre', 'Usuario')}")
            rol = st.session_state.get('rol', 'alumno')
            
            if rol == "admin":
                menu = ["Dashboard", "Administración CRM", "Biblioteca Técnica", "Vista Previa Examen"]
            else:
                menu = ["Mis Recursos", "Rendir Examen"]
            
            opcion = st.sidebar.selectbox("Navegación", menu)
            
            if st.sidebar.button("Cerrar Sesión"):
                logout()

        # --- ENRUTAMIENTO ---
        if opcion == "Administración CRM":
            admin_module()
        elif opcion in ["Biblioteca Técnica", "Mis Recursos"]:
            modulo_biblioteca(session, rol, st.session_state.get('usuario_id'))
        elif opcion in ["Rendir Examen", "Vista Previa Examen"]:
            st.title("📝 Centro de Evaluaciones")
            programas = session.query(models.Programa).all()
            if programas:
                nombres = {p.nombre: p.id for p in programas}
                sel = st.selectbox("Seleccioná el examen", list(nombres.keys()))
                modulo_examen(session, st.session_state.get('usuario_id'), nombres[sel], sel)
            else:
                st.info("No hay exámenes disponibles.")
        else:
            st.title("Panel de Control MENFA")
            st.write("---")
            st.info("Bienvenido. Seleccioná una opción para comenzar.")
            
    session.close()

if __name__ == "__main__":
    main()
