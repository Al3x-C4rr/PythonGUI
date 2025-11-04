
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Inclusión Laboral", layout="wide")

st.title("Simulador de Inclusión Laboral para Personas con Discapacidad — Panel de Empresas")

st.markdown(
    """
    Carga el archivo **DatosEmpresas.csv** con las columnas:
    - `nombreEmpresa` (str)
    - `tipoDiscapacidadAcepta` (str) — por ejemplo: *visual, auditiva, motriz, intelectual, psicosocial, múltiple*
    - `habilidadesRequeridas` (str) — separado por `;` si hay varias
    - `dias` (str) — por ejemplo: *L-V* o *L-S*
    - `ascensos` (str) — por ejemplo: *Sí/No*
    - `puesto` (str)
    - `salario` (float/int)
    - `lugar` (str) — municipio/departamento/ciudad
    - `prestacionDeLey` (bool/str) — admite `True/False`, `Sí/No`, `1/0`
    """
)

# ========== Carga de datos ==========
uploaded = st.file_uploader("Sube tu archivo DatosEmpresas.csv", type=["csv"])
if uploaded is None:
    st.info("Puedes usar la plantilla de ejemplo que acompaña a este proyecto.")
    st.stop()

df = pd.read_csv(uploaded)

# Normalizaciones mínimas
def to_bool(x):
    if isinstance(x, str):
        x = x.strip().lower()
        if x in ("true", "sí", "si", "1", "yes"):
            return True
        if x in ("false", "no", "0"):
            return False
    return bool(x)

if "prestacionDeLey" in df.columns:
    df["prestacionDeLey"] = df["prestacionDeLey"].apply(to_bool)

# Forzar salario numérico si existe
if "salario" in df.columns:
    df["salario"] = pd.to_numeric(df["salario"], errors="coerce")

st.sidebar.header("Filtros")
# ========== Filtros ==========
tipo_vals = sorted([t for t in df.get("tipoDiscapacidadAcepta", pd.Series(dtype=str)).dropna().unique()])
lugar_vals = sorted([t for t in df.get("lugar", pd.Series(dtype=str)).dropna().unique()])

sel_tipos = st.sidebar.multiselect("Tipo de discapacidad aceptada", tipo_vals, default=tipo_vals)
sel_lugares = st.sidebar.multiselect("Lugar", lugar_vals, default=lugar_vals)

prestacion_state = st.sidebar.selectbox("Prestación de Ley", ["Todos", "Sí", "No"], index=0)

df_filt = df.copy()

if sel_tipos and "tipoDiscapacidadAcepta" in df_filt.columns:
    df_filt = df_filt[df_filt["tipoDiscapacidadAcepta"].isin(sel_tipos)]

if sel_lugares and "lugar" in df_filt.columns:
    df_filt = df_filt[df_filt["lugar"].isin(sel_lugares)]

if prestacion_state != "Todos" and "prestacionDeLey" in df_filt.columns:
    df_filt = df_filt[df_filt["prestacionDeLey"] == (prestacion_state == "Sí")]

# ========== KPIs ==========
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Empresas (filtradas)", len(df_filt))
with col2:
    if "salario" in df_filt.columns and not df_filt["salario"].dropna().empty:
        st.metric("Salario promedio", f'Q {df_filt["salario"].mean():,.2f}')
    else:
        st.metric("Salario promedio", "N/D")
with col3:
    if "salario" in df_filt.columns and not df_filt["salario"].dropna().empty:
        st.metric("Salario mediano", f'Q {df_filt["salario"].median():,.2f}')
    else:
        st.metric("Salario mediano", "N/D")
with col4:
    if "prestacionDeLey" in df_filt.columns:
        st.metric("Con Prestación de Ley", int(df_filt["prestacionDeLey"].sum()))
    else:
        st.metric("Con Prestación de Ley", "N/D")

st.subheader("Listado de empresas (filtradas)")
st.dataframe(df_filt, use_container_width=True)

# ========== Gráficas sencillas (matplotlib) ==========
if "lugar" in df_filt.columns and not df_filt.empty:
    st.subheader("Conteo de empresas por lugar")
    conteo_lugar = df_filt["lugar"].value_counts().sort_values(ascending=False)
    fig = plt.figure()
    conteo_lugar.plot(kind="bar")
    plt.xlabel("Lugar")
    plt.ylabel("Número de empresas")
    plt.tight_layout()
    st.pyplot(fig)

if "tipoDiscapacidadAcepta" in df_filt.columns and not df_filt.empty:
    st.subheader("Conteo por tipo de discapacidad aceptada")
    conteo_tipo = df_filt["tipoDiscapacidadAcepta"].value_counts().sort_values(ascending=False)
    fig2 = plt.figure()
    conteo_tipo.plot(kind="bar")
    plt.xlabel("Tipo de discapacidad")
    plt.ylabel("Número de empresas")
    plt.tight_layout()
    st.pyplot(fig2)

if "salario" in df_filt.columns and not df_filt["salario"].dropna().empty:
    st.subheader("Distribución de salarios (filtrado)")
    fig3 = plt.figure()
    df_filt["salario"].dropna().plot(kind="hist", bins=20)
    plt.xlabel("Salario (Q)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    st.pyplot(fig3)

# ========== Descargas ==========
st.subheader("Descargar resultados")
st.download_button(
    "Descargar CSV filtrado",
    data=df_filt.to_csv(index=False).encode("utf-8"),
    file_name="Empresas_filtrado.csv",
    mime="text/csv",
)

# Vista rápida de detalle
st.subheader("Detalle por empresa")
if "nombreEmpresa" in df_filt.columns:
    nombres = ["(Selecciona)"] + sorted(df_filt["nombreEmpresa"].astype(str).unique().tolist())
    chosen = st.selectbox("Empresa", nombres, index=0)
    if chosen != "(Selecciona)":
        st.write(df_filt[df_filt["nombreEmpresa"].astype(str) == chosen])
else:
    st.info("No se encontró la columna 'nombreEmpresa' para mostrar el detalle.")
