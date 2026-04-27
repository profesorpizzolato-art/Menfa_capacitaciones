import streamlit as st
import sys
import os

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="MENFA Capacitaciones", layout="wide", page_icon="⚒️")

# 2. Forzar que Python reconozca la raíz del proyecto
path_raiz = os.path.dirname(os.path.abspath(__file__))
if path_raiz not in sys.path:
    sys.path.insert(0, path_raiz)

# 3. Importaciones seguras
try:
    from modulos.styles import aplicar_estilos_web, mostrar_logo
    from database_manager import Session, inicializar_sistema
    from modulos.auth import login, logout
    from modulos.biblioteca import modulo_biblioteca
    from admin_panel import admin_module
    from crear_admin import crear_primer_admin
    import models
    exito_import = True
except ImportError as e:
    st.error(f"Error crítico de archivos: {e}")
    st.info("Asegurate de que todos los archivos .py estén en la raíz o sus carpetas correspondientes.")
    exito_import = False

def main():
    if not exito_import:
        return

    # Aplicar estética MENFA (Fondo oscuro y dorado)
    aplicar_estilos_web()

    # Inicializar base de datos y asegurar usuario admin
    inicializar_sistema()
    crear_primer_admin()
    
    session = Session()

    # Manejo de la sesión en Streamlit
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False

    if not st.session_state['autenticado']:
        # --- PANTALLA DE LOGIN ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mostrar_logo(ancho=300) # Logo grande centrado
            login(session)
    else:
        # --- INTERFAZ DE USUARIO LOGUEADO ---
        with st.sidebar:
            mostrar_logo(ancho=150) # Logo pequeño en barra lateral
            st.write("---")
            st.sidebar.title(f"Hola, {st.session_state.get('nombre', 'Usuario')}")
            rol = st.session_state.get('rol', 'alumno')
            
            # Definir menú según el rol
            if rol == "admin":
                menu = ["Dashboard", "Administración CRM", "Biblioteca Técnica"]
            else:
                menu = ["Mis Recursos"]
            
            opcion = st.sidebar.selectbox("Navegación", menu)
            
            if st.sidebar.button("Cerrar Sesión"):
                logout()

        # Enrutamiento de la aplicación
        if opcion == "Administración CRM":
            admin_module()
        elif opcion in ["Biblioteca Técnica", "Mis Recursos"]:
            modulo_biblioteca(session, rol, st.session_state.get('usuario_id'))
        else:
            # Pantalla de inicio
            st.title("Panel de Control MENFA")
            st.write("---")
            st.info("Bienvenido a la plataforma. Seleccioná una opción en el menú lateral para comenzar.")
            
    session.close()

if __name__ == "__main__":
    main()
