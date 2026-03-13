import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Análisis de Energía Global - Talento Tech",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS Y PALETA GLOBAL ---
sns.set_theme(style="whitegrid")
PALETA_PRINCIPAL = "mako"
SNS_PALETTE = sns.color_palette(PALETA_PRINCIPAL)

# --- FUNCIONES DE CARGA Y PROCESAMIENTO ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Limpieza básica: Asegurar tipos de datos
        df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
        df['YEAR'] = df['YEAR'].astype(int)
        return df
    except Exception as e:
        st.error(f"Error al cargar el dataset: {e}")
        return None

def landing_page():
    st.title("⚡ Análisis de Generación Eléctrica Global")
    st.subheader("Proyecto Final: Análisis de Datos Talento Tech")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Sobre el Proyecto
        Este dashboard interactivo analiza la evolución y distribución de la generación de energía 
        a nivel mundial. Utiliza datos históricos de la IEA (Agencia Internacional de Energía) 
        para explorar cómo los países están transformando su matriz energética.
        
        **¿Qué problema resuelve?**
        Permite identificar tendencias en la transición hacia energías limpias, comparar la eficiencia 
        de producción entre naciones y visualizar el impacto de diferentes fuentes de energía (Solar, 
        Eólica, Fósil) en el suministro global.
        
        **Detalles del Dataset:**
        - **Filas:** +100,000 registros históricos.
        - **Columnas clave:** País, Año, Mes, Tipo de Producto (Energía), Valor Generado (GWh).
        - **Origen:** Dataset de Kaggle / Talento Tech.
        """)
    
    with col2:
        try:
            # Intento de cargar imagen local si existe, sino placeholder
            img = Image.open("imagenA.jpeg")
            st.image(img, use_container_width=True, caption="Transición Energética")
        except:
            st.image("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=800", 
                     caption="Energía Limpia y Sostenible")

    st.divider()
    
    st.markdown("### 🚀 Guía de Uso Rápido")
    cols_guia = st.columns(5)
    pasos = [
        "1. Selecciona **Dashboard** en el menú izquierdo.",
        "2. Filtra por **Países** de interés en la barra lateral.",
        "3. Ajusta el **Rango de Años** para ver la evolución.",
        "4. Explora los **6 gráficos interactivos**.",
        "5. Revisa los **Expansores** para entender la interpretación."
    ]
    for i, paso in enumerate(pasos):
        cols_guia[i].info(paso)

def dashboard(df):
    st.title("📊 Panel de Trabajo Interactivo")
    
    # --- SIDEBAR: FILTROS ---
    st.sidebar.header("🔍 Filtros de Datos")
    
    # Filtro de Países
    paises_disponibles = sorted(df['COUNTRY'].unique())
    selected_countries = st.sidebar.multiselect(
        "Selecciona Países", 
        paises_disponibles, 
        default=["Australia", "United States", "Mexico"] if "Mexico" in paises_disponibles else [paises_disponibles[0]]
    )
    
    # Filtro de Años
    year_range = st.sidebar.slider(
        "Rango de Años", 
        int(df['YEAR'].min()), 
        int(df['YEAR'].max()), 
        (2015, 2022)
    )
    
    # Visibilidad de gráficos
    st.sidebar.divider()
    show_raw_data = st.sidebar.checkbox("Mostrar Datos Crudos", value=False)
    show_charts = st.sidebar.checkbox("Mostrar Visualizaciones", value=True)

    # Filtrado de DataFrame
    df_filtered = df[
        (df['COUNTRY'].isin(selected_countries)) & 
        (df['YEAR'] >= year_range[0]) & 
        (df['YEAR'] <= year_range[1])
    ]

    # --- EXPLORACIÓN DE DATOS ---
    if show_raw_data:
        with st.expander("📂 Vista de Datos y Estadísticas", expanded=True):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write("**Primeras filas:**")
                st.dataframe(df_filtered.head(5), use_container_width=True)
            with col_d2:
                st.write("**Últimas filas:**")
                st.dataframe(df_filtered.tail(5), use_container_width=True)
            
            st.write("**Dimensiones y Tipos:**")
            st.write(f"Filas filtradas: {df_filtered.shape[0]} | Columnas: {df_filtered.shape[1]}")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write("**Estadísticas Descriptivas:**")
                st.dataframe(df_filtered.describe(), use_container_width=True)
            with col_s2:
                st.write("**Conteo de Nulos:**")
                nulls = df_filtered.isnull().sum()
                st.bar_chart(nulls[nulls > 0])
                if nulls.sum() == 0:
                    st.success("¡No se encontraron valores nulos!")

    # --- VISUALIZACIONES (SEABORN) ---
    if show_charts:
        st.divider()
        
        # Grid para gráficos
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)

        # 1. Distribución (Histplot)
        with row1_col1:
            st.markdown("#### 1. Distribución de Generación (VALUE) ℹ️", help="Muestra la frecuencia de los valores de generación eléctrica.")
            fig, ax = plt.subplots()
            sns.histplot(df_filtered['VALUE'], kde=True, color=SNS_PALETTE[0], ax=ax)
            ax.set_title("Distribución de Valores de Generación")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("Este histograma con KDE (Estimación de Densidad de Kernel) permite observar si la mayoría de los registros representan producciones pequeñas o grandes. Una cola larga a la derecha indica valores atípicos de alta producción.")

        # 2. Correlación (Heatmap)
        with row1_col2:
            st.markdown("#### 2. Matriz de Correlación ℹ️", help="Relación estadística entre variables numéricas.")
            fig, ax = plt.subplots()
            numeric_df = df_filtered.select_dtypes(include=[np.number])
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Correlación de Variables")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("Los valores cercanos a 1 indican una correlación positiva fuerte. Por ejemplo, el año y el acumulado anual (yearToDate) suelen estar altamente correlacionados.")

        # 3. Comparación por Categoría (Boxplot)
        with row2_col1:
            st.markdown("#### 3. Distribución por Fuente de Energía ℹ️", help="Comparación de la variabilidad entre productos.")
            fig, ax = plt.subplots(figsize=(10, 6))
            # Seleccionamos top 5 productos para evitar ruido
            top_products = df_filtered.groupby('PRODUCT')['VALUE'].sum().nlargest(5).index
            df_box = df_filtered[df_filtered['PRODUCT'].isin(top_products)]
            sns.boxplot(data=df_box, x='PRODUCT', y='VALUE', palette="viridis", ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Distribución de Valor por Tipo de Energía")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("La línea central de cada caja es la mediana. Los puntos fuera de los bigotes son valores atípicos (outliers), que representan picos excepcionales de producción.")

        # 4. Relación entre variables (Scatterplot)
        with row2_col2:
            st.markdown("#### 4. Tendencia Temporal vs Valor ℹ️", help="Relación entre el año y el valor generado segregado por país.")
            fig, ax = plt.subplots()
            sns.scatterplot(data=df_filtered, x='YEAR', y='VALUE', hue='COUNTRY', palette="tab10", alpha=0.6, ax=ax)
            ax.set_title("Evolución de Generación por Año")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("Permite observar si el volumen de datos o la producción está creciendo con el tiempo para países específicos. Cada color representa un país filtrado.")

        # 5. Conteo de Frecuencia (Countplot)
        with row3_col1:
            st.markdown("#### 5. Registros por País ℹ️", help="Muestra la cantidad de registros disponibles por país seleccionado.")
            fig, ax = plt.subplots()
            sns.countplot(data=df_filtered, y='COUNTRY', palette="Blues_d", ax=ax)
            ax.set_title("Frecuencia de Datos por País")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("Indica la densidad de información que tenemos para cada país. Si una barra es mucho más corta, significa que hay menos meses o productos reportados para ese país.")

        # 6. Análisis de Tendencia (Barplot)
        with row3_col2:
            st.markdown("#### 6. Generación Total por Año ℹ️", help="Suma total de generación por año para los países seleccionados.")
            fig, ax = plt.subplots()
            df_year = df_filtered.groupby('YEAR')['VALUE'].sum().reset_index()
            sns.barplot(data=df_year, x='YEAR', y='VALUE', palette="mako", ax=ax)
            ax.set_title("Generación Total Anual Sumada")
            st.pyplot(fig)
            with st.expander("📖 ¿Cómo interpretar este gráfico?"):
                st.write("Este gráfico de barras muestra la tendencia macro. Si las barras crecen, la demanda o capacidad de generación de los países seleccionados ha aumentado anualmente.")

# --- LÓGICA DE NAVEGACIÓN ---
def main():
    # Footer fijo
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: #31333F;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e6e9ef;
        z-index: 100;
    }
    </style>
    <div class="footer">
        Desarrollado por <b>María Alejandra Colorado</b> · Talento Tech · Análisis de Datos
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

    # Menú Lateral
    menu = st.sidebar.radio("Navegación", ["🏠 Landing Page", "📊 Dashboard"])
    
    # Carga de datos global
    df = load_data("data.csv")
    
    if df is not None:
        if menu == "🏠 Landing Page":
            landing_page()
        else:
            dashboard(df)
    else:
        st.warning("Por favor, asegúrate de que el archivo 'data.csv' esté en el mismo directorio.")

if __name__ == "__main__":
    main()
