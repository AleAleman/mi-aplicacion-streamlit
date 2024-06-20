import streamlit as st
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Configuración inicial de la página
st.set_page_config(
   # layout="wide",  # Usa el layout "wide" que es más limpio
    initial_sidebar_state="collapsed",  # Colapsa la barra lateral por defecto
    menu_items={
        'Get Help': None,  # Desactiva el enlace de "Get Help"
        'Report a bug': None,  # Desactiva el enlace de "Report a bug"
        'About': None  # Desactiva la sección "About"
    }
)

# Carga la cadena JSON desde una variable de entorno
json_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if json_creds is None:
    st.error("La variable de entorno 'GOOGLE_APPLICATION_CREDENTIALS_JSON' no está configurada.")
    st.stop()

creds_dict = json.loads(json_creds)
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)
    sheet = client.open("App_streamlit").worksheet("Hoja 1")
except gspread.exceptions.SpreadsheetNotFound:
    st.error("La hoja de cálculo 'App_streamlit' no fue encontrada. Verifica el nombre y los permisos de acceso.")
    st.stop()
except gspread.exceptions.APIError as e:
    st.error(f"Error de API al intentar acceder a la hoja de cálculo: {e}")
    st.stop()
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")
    st.stop()

# Crear una instancia de DataFrame si no existe en el estado de la sesión
if 'df' not in st.session_state:
    try:
        data = sheet.get_all_records()
        st.session_state.df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al cargar los datos desde Google Sheets: {e}")

# Función para agregar datos
def agregar_datos():
    try:
        nuevo_dato = {'Nombre Completo': nombre, 'Identidad': identidad, 'Ciudad': ciudad}
        sheet.append_row(list(nuevo_dato.values()))
        # Usar pd.concat en lugar de append para actualizar el DataFrame
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nuevo_dato])], ignore_index=True)
        st.success("Datos agregados con éxito!")
    except Exception as e:
        st.error(f"Error al agregar datos a Google Sheets: {e}")

# Crear los campos del formulario
nombre = st.text_input("Nombre Completo")
identidad = st.text_input("Identidad")
ciudad = st.text_input("Ciudad")

# Botón para agregar datos
st.button("Agregar Datos", on_click=agregar_datos)

# Mostrar DataFrame
# st.write("Datos Actuales en el DataFrame:")
# st.dataframe(st.session_state.df)
