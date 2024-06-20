import streamlit as st
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Carga la cadena JSON desde una variable de entorno
json_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if json_creds is None:
    st.error("La variable de entorno 'GOOGLE_APPLICATION_CREDENTIALS_JSON' no está configurada.")
    st.stop()

creds_dict = json.loads(json_creds)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ['https://www.googleapis.com/auth/spreadsheets'])

try:
    client = gspread.authorize(creds)
    # Asegúrate de que el nombre de la hoja de cálculo sea correcto
    spreadsheet = client.open("App_streamlit")
    # Si tu hoja se llama "Hoja 1", accede a ella de esta manera
    sheet = spreadsheet.worksheet("Hoja 1")
except gspread.exceptions.SpreadsheetNotFound:
    st.error("La hoja de cálculo 'App_streamlit' no fue encontrada. Verifica el nombre y los permisos de acceso.")
    st.stop()
except gspread.exceptions.WorksheetNotFound:
    st.error("La hoja 'Hoja 1' no fue encontrada en la hoja de cálculo 'App_streamlit'. Verifica el nombre de la hoja.")
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
        st.session_state.df = st.session_state.df.append(nuevo_dato, ignore_index=True)
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
st.write("Datos Actuales en el DataFrame:")
st.dataframe(st.session_state.df)

