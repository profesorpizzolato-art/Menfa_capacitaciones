import streamlit as st
import os

# CONFIGURACIÓN DE IDENTIDAD VISUAL MENFA
COLOR_PRIMARIO = "#fca311"   # Dorado Industrial
COLOR_SECUNDARIO = "#14213d"  # Azul Petróleo (Barra lateral)
COLOR_FONDO = "#0e1117"      # Fondo Oscuro
COLOR_TEXTO = "#ffffff"      # Texto Blanco

def aplicar_estilos_web():
    """Inyecta el CSS de la marca en la interfaz de Streamlit"""
    st.markdown(f"""
        <style>
        /* Fondo de la aplicación */
        .stApp {{
            background-color: {COLOR_FONDO};
        }}
        /* Botones principales */
        div.stButton > button:first-child {{
            background-color: {COLOR_PRIMARIO};
            color: #000000;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            width: 100%;
        }}
        /* Títulos */
        h1, h2, h3 {{
            color: {COLOR_PRIMARIO} !important;
        }}
        /* Barra lateral personalizada */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_SECUNDARIO};
        }}
        /* Estilo de los inputs y textos */
        .stMarkdown, p, label {{
            color: {COLOR_TEXTO} !important;
        }}
        </style>
        """, unsafe_allow_html=True)

def mostrar_logo(ancho=200):
    """
    Busca y muestra el logo oficial. 
    Se usa tanto en el login como en la barra lateral.
    """
    # Verificamos extensiones comunes por las dudas
    nombres_posibles = ["logo_menfa.png", "logo_menfa.jpg", "logo_menfa.jpeg"]
    
    logo_encontrado = False
    for nombre in nombres_posibles:
        if os.path.exists(nombre):
            st.image(nombre, width=ancho)
            logo_encontrado = True
            break
            
    if not logo_encontrado:
        st.sidebar.title("⚒️ MENFA")
