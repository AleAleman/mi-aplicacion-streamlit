import streamlit as st
import pandas as pd
from openpyxl import Workbook

# Crear una instancia de DataFrame si no existe en el estado de la sesión
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Nombre Completo', 'Identidad', 'Ciudad'])

# Función para agregar datos
def agregar_datos():
    nuevo_dato = pd.DataFrame([{'Nombre Completo': nombre, 'Identidad': identidad, 'Ciudad': ciudad}])
    st.session_state.df = pd.concat([st.session_state.df, nuevo_dato], ignore_index=True)
    st.success("Datos agregados con éxito!")

# Función para guardar a Excel
def guardar_excel():
    with pd.ExcelWriter('DatosFormulario.xlsx') as writer:
        st.session_state.df.to_excel(writer, index=False)
    st.success("Datos guardados en Excel.")

# Crear los campos del formulario
nombre = st.text_input("Nombre Completo")
identidad = st.text_input("Identidad")
ciudad = st.text_input("Ciudad")

# Botones para interacción
st.button("Agregar Datos", on_click=agregar_datos)
st.button("Guardar en Excel", on_click=guardar_excel)

# Mostrar DataFrame
st.write("Datos Actuales en el DataFrame:")
st.dataframe(st.session_state.df)
