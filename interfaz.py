import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión",
    page_icon="📊",
    layout="wide"
)

# Inicializar estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'candidatos' not in st.session_state:
    st.session_state.candidatos = None
if 'empresas' not in st.session_state:
    st.session_state.empresas = None

# Título principal
st.title("🎯 Sistema de Gestión")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("📋 Menú Principal")
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    ["🔐 Iniciar sesión", "📂 Cargar datos", "👤 Ver candidatos", 
     "🏢 Ver empresas", "📊 Ver estadísticas"]
)

# Opción 1: Iniciar sesión
if opcion == "🔐 Iniciar sesión":
    st.header("🔐 Iniciar Sesión")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        usuario = st.text_input("Usuario:", placeholder="Ingresa tu usuario")
        contrasena = st.text_input("Contraseña:", type="password", placeholder="Ingresa tu contraseña")
        
        if st.button("Iniciar Sesión", type="primary"):
            if usuario and contrasena:
                st.session_state.logged_in = True
                st.success(f"✅ Bienvenido, {usuario}!")
            else:
                st.error("❌ Por favor completa todos los campos")
    
    with col2:
        if st.session_state.logged_in:
            st.info("✅ Sesión activa")
        else:
            st.warning("⚠ No has iniciado sesión")

# Opción 2: Cargar datos
elif opcion == "📂 Cargar datos":
    st.header("📂 Cargar Datos desde CSV")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cargar Candidatos")
        archivo_candidatos = st.file_uploader(
            "Selecciona archivo CSV de candidatos",
            type=['csv'],
            key="candidatos"
        )
        
        if archivo_candidatos is not None:
            try:
                st.session_state.candidatos = pd.read_csv(archivo_candidatos)
                st.success(f"✅ {len(st.session_state.candidatos)} candidatos cargados")
                st.dataframe(st.session_state.candidatos.head())
            except Exception as e:
                st.error(f"❌ Error al cargar archivo: {e}")
    
    with col2:
        st.subheader("Cargar Empresas")
        archivo_empresas = st.file_uploader(
            "Selecciona archivo CSV de empresas",
            type=['csv'],
            key="empresas"
        )
        
        if archivo_empresas is not None:
            try:
                st.session_state.empresas = pd.read_csv(archivo_empresas)
                st.success(f"✅ {len(st.session_state.empresas)} empresas cargadas")
                st.dataframe(st.session_state.empresas.head())
            except Exception as e:
                st.error(f"❌ Error al cargar archivo: {e}")

# Opción 3: Ver candidatos
elif opcion == "👤 Ver candidatos":
    st.header("👤 Lista de Candidatos")
    
    if st.session_state.candidatos is not None:
        # Búsqueda y filtros
        col1, col2 = st.columns([2, 1])
        
        with col1:
            busqueda = st.text_input("🔍 Buscar candidato:", placeholder="Nombre, email, etc.")
        
        with col2:
            st.metric("Total Candidatos", len(st.session_state.candidatos))
        
        # Mostrar datos
        if busqueda:
            # Filtrar por cualquier columna que contenga el texto de búsqueda
            mask = st.session_state.candidatos.astype(str).apply(
                lambda x: x.str.contains(busqueda, case=False)
            ).any(axis=1)
            df_filtrado = st.session_state.candidatos[mask]
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.dataframe(st.session_state.candidatos, use_container_width=True)
    else:
        st.warning("⚠ No hay datos de candidatos cargados. Ve a 'Cargar datos' primero.")

# Opción 4: Ver empresas
elif opcion == "🏢 Ver empresas":
    st.header("🏢 Lista de Empresas")
    
    if st.session_state.empresas is not None:
        # Búsqueda y filtros
        col1, col2 = st.columns([2, 1])
        
        with col1:
            busqueda = st.text_input("🔍 Buscar empresa:", placeholder="Nombre, sector, etc.")
        
        with col2:
            st.metric("Total Empresas", len(st.session_state.empresas))
        
        # Mostrar datos
        if busqueda:
            mask = st.session_state.empresas.astype(str).apply(
                lambda x: x.str.contains(busqueda, case=False)
            ).any(axis=1)
            df_filtrado = st.session_state.empresas[mask]
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.dataframe(st.session_state.empresas, use_container_width=True)
    else:
        st.warning("⚠ No hay datos de empresas cargados. Ve a 'Cargar datos' primero.")

# Opción 5: Ver estadísticas
elif opcion == "📊 Ver estadísticas":
    st.header("📊 Estadísticas del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        candidatos_count = len(st.session_state.candidatos) if st.session_state.candidatos is not None else 0
        st.metric("👤 Candidatos", candidatos_count)
    
    with col2:
        empresas_count = len(st.session_state.empresas) if st.session_state.empresas is not None else 0
        st.metric("🏢 Empresas", empresas_count)
    
    with col3:
        estado = "Activa ✅" if st.session_state.logged_in else "Inactiva ❌"
        st.metric("🔐 Sesión", estado)
    
    st.markdown("---")
    
    # Gráficos si hay datos
    if st.session_state.candidatos is not None:
        st.subheader("📈 Análisis de Candidatos")
        
        # Puedes agregar gráficos basados en las columnas de tu CSV
        # Por ejemplo, si tienes una columna de 'estado' o 'experiencia'
        if not st.session_state.candidatos.empty:
            st.bar_chart(st.session_state.candidatos.iloc[:, 0].value_counts())
    
    if st.session_state.empresas is not None:
        st.subheader("📈 Análisis de Empresas")
        
        if not st.session_state.empresas.empty:
            st.bar_chart(st.session_state.empresas.iloc[:, 0].value_counts())

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 *Tip:* Carga tus archivos CSV en la sección 'Cargar datos'")