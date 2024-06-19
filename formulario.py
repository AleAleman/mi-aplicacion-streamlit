import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de la autenticación de Google
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\aleja\OneDrive\Documentos\client_secret_317714585896-9oob5m22gpqg4k4sfn8pdve16htlebpua.apps.googleusercontent.com.json', scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo de Google por nombre
sheet = client.open("App_streamlit").sheet1

# Crear una instancia de DataFrame si no existe en el estado de la sesión
if 'df' not in st.session_state:
    # Cargar datos existentes desde Google Sheets
    data = sheet.get_all_records()
    st.session_state.df = pd.DataFrame(data)

# Función para agregar datos
def agregar_datos():
    nuevo_dato = {'Nombre Completo': nombre, 'Identidad': identidad, 'Ciudad': ciudad}
    sheet.append_row(list(nuevo_dato.values()))
    st.session_state.df = st.session_state.df.append(nuevo_dato, ignore_index=True)
    st.success("Datos agregados con éxito!")

# Crear los campos del formulario
nombre = st.text_input("Nombre Completo")
identidad = st.text_input("Identidad")
ciudad = st.text_input("Ciudad")

# Botón para agregar datos
st.button("Agregar Datos", on_click=agregar_datos)

# Mostrar DataFrame
st.write("Datos Actuales en el DataFrame:")
st.dataframe(st.session_json.df)

