import streamlit as st
import pandas as pd
import os

# === Archivos CSV ===
CAN = "Historial.csv"
EMP = "Empresarios.csv"

# === Función para guardar candidatos ===
def guardar_candidatos(df):
    df.to_csv(CAN, index=False)
    st.success(f"Datos guardados correctamente en {CAN}")

# === Función para cargar historial ===
def cargar_historial():
    if os.path.exists(CAN):
        return pd.read_csv(CAN)
    else:
        st.warning("No se encontró Historial.csv. Se creará uno nuevo al guardar.")
        return pd.DataFrame(columns=["genero", "discapacidad", "experiencia", "EstadoCivil", "edad"])

# === Buscar discapacidad desde historial ===
def obtener_discapacidad_desde_historial(genero):
    df = cargar_historial()
    candidato = df[df["genero"].str.lower() == genero.lower()]
    if not candidato.empty:
        return candidato.iloc[0]["discapacidad"]
    else:
        return None

# === Mostrar empresas compatibles ===
def mostrar_empresas_compatibles(discapacidad):
    if not os.path.exists(EMP):
        st.error("No se encontró Empresarios.csv.")
        return

    df_emp = pd.read_csv(EMP)
    if "discapacidad" not in df_emp.columns:
        st.error("El archivo Empresarios.csv no tiene una columna 'discapacidad'.")
        return

    compatibles = df_emp[df_emp["discapacidad"].str.lower() == discapacidad.lower()]
    if compatibles.empty:
        st.info("No se encontraron empresas que acepten esta discapacidad.")
    else:
        st.dataframe(compatibles)

# === Interfaz Streamlit ===
st.title("📜 Historial de Candidatos y Empresas")

menu = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["📁 Ver Historial", "📝 Agregar Candidato", "🔍 Buscar Empresas por Discapacidad"]
)

# === Ver historial ===
if menu == "📁 Ver Historial":
    st.subheader("Historial de candidatos")
    df = cargar_historial()
    st.dataframe(df)

# === Agregar candidato ===
elif menu == "📝 Agregar Candidato":
    st.subheader("Agregar nuevo candidato")

    genero = st.selectbox("Género:", ["Masculino", "Femenino", "Otro"])
    discapacidad = st.text_input("Tipo de discapacidad (si aplica):")
    experiencia = st.text_input("Experiencia laboral:")
    estado_civil = st.selectbox("Estado civil:", ["Soltero", "Casado", "Divorciado", "Viudo"])
    edad = st.number_input("Edad:", min_value=18, max_value=99)

    if st.button("Guardar candidato"):
        df = cargar_historial()
        nuevo = pd.DataFrame([[genero, discapacidad, experiencia, estado_civil, edad]],
                             columns=df.columns)
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar_candidatos(df)

# === Buscar empresas ===
elif menu == "🔍 Buscar Empresas por Discapacidad":
    st.subheader("Buscar empresas según discapacidad")

    genero = st.text_input("Ingrese el género del candidato:")
    discapacidad = st.text_input("Ingrese la discapacidad del candidato (dejar vacío para buscar en historial):")

    if st.button("Buscar"):
        if not discapacidad:
            discapacidad = obtener_discapacidad_desde_historial(genero)
        if discapacidad:
            st.write(f"🔎 Buscando empresas que aceptan discapacidad: **{discapacidad}**")
            mostrar_empresas_compatibles(discapacidad)
        else:
            st.warning("No se encontró el candidato o no tiene discapacidad registrada.")
