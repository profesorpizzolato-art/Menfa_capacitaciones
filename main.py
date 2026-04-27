import streamlit as st
import sys
import os

st.set_page_config(page_title="MENFA Capacitaciones", layout="wide", page_icon="⚒️")

# Forzar rutas para que Streamlit vea todo
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from database_manager import Session, inicializar_sistema
    from modulos.auth import login, logout
    from modulos.biblioteca import modulo_biblioteca
    from admin_panel import admin_module
    exito = True
except ImportError as e:
    st.error(f"Error de archivos: {e}")
    st.stop()

def main():
  def main():
     if exito:
        inicializar_sistema()
        
        # --- AGREGÁ ESTO PARA CREAR AL ADMIN ---
        from crear_admin import crear_primer_admin
        crear_primer_admin()
        # ----------------------------------------
        
        session = Session()
        # ... resto del código
  
        if 'autenticado' not in st.session_state:
            st.session_state['autenticado'] = False

        if not st.session_state['autenticado']:
            login(session)
        else:
            st.sidebar.title(f"Hola, {st.session_state.get('nombre', 'Usuario')}")
            rol = st.session_state.get('rol', 'alumno')
            
            menu = ["Dashboard", "Administración CRM", "Biblioteca Técnica"] if rol == "admin" else ["Mis Recursos"]
            opcion = st.sidebar.selectbox("Menú", menu)
            
            if st.sidebar.button("Cerrar Sesión"):
                logout()

            if opcion == "Administración CRM":
                admin_module()
            elif opcion in ["Biblioteca Técnica", "Mis Recursos"]:
                modulo_biblioteca(session, rol, st.session_state.get('usuario_id'))
            else:
                st.title("Panel Control MENFA")
                st.info("Seleccioná una opción para empezar.")

if __name__ == "__main__":
    main()
