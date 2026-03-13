# =============================================================================
# ⚡ ANÁLISIS DE GENERACIÓN DE ENERGÍA GLOBAL
# Desarrollado por: María Alejandra Colorado
# Curso: Análisis de Datos · Talento Tech
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from PIL import Image
import warnings
import io

warnings.filterwarnings("ignore")
plt.rcParams['axes.formatter.use_locale'] = False

# ── Configuración global ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis de Energía Global",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

PALETA_DEFAULT = "mako"

sns.set_theme(style="whitegrid", font_scale=1.1)

# ── Mapeo de nombres al español ───────────────────────────────────────────────
PRODUCTOS_ES = {
    "Hydro": "Hidroeléctrica",
    "Wind": "Eólica",
    "Solar": "Solar",
    "Geothermal": "Geotérmica",
    "Nuclear": "Nuclear",
    "Coal": "Carbón",
    "Oil": "Petróleo",
    "Natural gas": "Gas Natural",
    "Combustible renewables": "Renovables Combustibles",
    "Net electricity production": "Producción Neta",
    "Electricity supplied": "Electricidad Suministrada",
    "Used for pumped storage": "Almacenamiento por Bombeo",
    "Distribution losses": "Pérdidas de Distribución",
    "Final consumption": "Consumo Final",
    "Renewables": "Renovables",
    "Non-renewables": "No Renovables",
    "Others": "Otros",
    "Other renewables aggregated": "Otras Renovables",
    "Low carbon": "Bajo Carbono",
    "Fossil fuels": "Combustibles Fósiles",
    "Total combustible fuels": "Total Combustibles",
    "Other combustible non-renewables": "Otros No Renovables",
    "Not specified": "No Especificado",
    "Total imports": "Importaciones Totales",
    "Total exports": "Exportaciones Totales",
    "Electricity trade": "Comercio Eléctrico",
    "Other renewables": "Otras Renovables",
    "Fossil fuels": "Combustibles Fósiles",
}

MESES_ES = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
}

RENOVABLES = ["Hydro", "Wind", "Solar", "Geothermal",
              "Combustible renewables", "Other renewables aggregated",
              "Other renewables", "Renewables"]

FUENTES_PRINCIPALES = ["Solar", "Wind", "Hydro", "Nuclear",
                       "Coal", "Natural gas", "Oil"]

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: linear-gradient(90deg, #0d1b2a, #1b4332);
        color: #a8d5b5; text-align: center;
        padding: 8px; font-size: 12px; z-index: 999;
        border-top: 1px solid #2d6a4f;
    }
    .kpi-card {
        background: linear-gradient(135deg, #0d1b2a, #1b4332);
        border-radius: 12px; padding: 16px; text-align: center;
        border: 1px solid #2d6a4f; margin: 4px;
    }
    .kpi-value { font-size: 28px; font-weight: bold; color: #52b788; }
    .kpi-label { font-size: 13px; color: #a8d5b5; margin-top: 4px; }
    .section-title {
        background: linear-gradient(90deg, #1b4332, #081c15);
        padding: 10px 20px; border-radius: 8px; margin: 20px 0 10px;
        border-left: 4px solid #52b788;
    }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ Desarrollado por <strong>María Alejandra Colorado</strong> &nbsp;·&nbsp;
    Talento Tech · Análisis de Datos &nbsp;·&nbsp; Dataset: IEA Electricity Statistics
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Cargando dataset...")
def cargar_datos():
    try:
        df = pd.read_csv("data.csv")
        df["PRODUCTO_ES"] = df["PRODUCT"].map(PRODUCTOS_ES).fillna(df["PRODUCT"])
        df["MES_ES"] = df["MONTH"].map(MESES_ES)
        df["ES_RENOVABLE"] = df["PRODUCT"].isin(RENOVABLES)
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return pd.DataFrame()


# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
def render_landing(df):
    try:
        img = Image.open("imagenA.jpeg")
        st.image(img, use_column_width=True)
    except Exception:
        st.image(
            "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1400",
            use_column_width=True
        )

    st.markdown("""
    <h1 style='text-align:center; color:#52b788; margin-top:20px;'>
        ⚡ Análisis de Generación de Energía Global
    </h1>
    <p style='text-align:center; font-size:17px; color:#a8d5b5; max-width:800px; margin:0 auto 30px;'>
        Explora las tendencias de producción eléctrica a nivel mundial basadas en datos históricos
        de la <strong>Agencia Internacional de Energía (IEA)</strong>. Analiza la transición hacia
        energías limpias, compara el rendimiento energético entre naciones y descubre patrones
        ocultos en más de 180.000 registros mensuales de 52 países (2010–2022).
    </p>
    """, unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    fuentes_principales = df[df["PRODUCT"].isin(FUENTES_PRINCIPALES)]["PRODUCT"].nunique()
    with c1:
        st.metric("📋 Total de Registros", f"{len(df):,}".replace(",", "."))
    with c2:
        st.metric("🌍 Países Incluidos",
                  df[~df["COUNTRY"].str.startswith("OECD") & (df["COUNTRY"] != "IEA Total")]["COUNTRY"].nunique())
    with c3:
        rango = f"{df['YEAR'].min()} – {df['YEAR'].max()}"
        st.metric("📅 Rango de Años", rango)
    with c4:
        st.metric("⚡ Fuentes de Energía", df["PRODUCT"].nunique())

    st.markdown("---")

    with st.expander("📖 Guía de uso rápido — 5 pasos para comenzar"):
        st.markdown("""
        **Paso 1 — Selecciona la página** desde el menú lateral izquierdo: *Landing* o *Dashboard*.

        **Paso 2 — Aplica filtros** en la barra lateral: elige países, fuentes de energía, rango de años y nivel de agregación.

        **Paso 3 — Explora los KPIs** en la fila superior del dashboard para obtener una visión rápida del estado energético global.

        **Paso 4 — Navega por las pestañas** del panel principal: *Explorador de Datos*, *Gráficos*, *Análisis por Energía* y *Funcionalidades Avanzadas*.

        **Paso 5 — Descarga los datos filtrados** usando el botón de exportación en la barra lateral para continuar el análisis externamente.
        """)

    with st.expander("📊 Sobre el Dataset — IEA Electricity Statistics"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Fuente:** Kaggle / Agencia Internacional de Energía (IEA)
            **Cobertura:** 52 países + agregados OCDE · 2010–2022 · Frecuencia mensual

            **Variables principales:**
            - `COUNTRY` — País o región
            - `PRODUCT` — Fuente energética (Solar, Eólica, Nuclear, etc.)
            - `VALUE` — Generación en GWh
            - `YEAR` / `MONTH` — Temporalidad
            - `share` — Participación porcentual en el total
            - `yearToDate` — Acumulado del año a la fecha
            """)
        with col2:
            fuentes_disp = [f"• {PRODUCTOS_ES.get(p, p)}" for p in df["PRODUCT"].unique()[:14]]
            st.markdown("**Fuentes de energía disponibles:**\n" + "\n".join(fuentes_disp))


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTROS
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar(df):
    st.sidebar.markdown("""
    <div style='text-align:center; padding:10px 0;'>
        <h3 style='color:#52b788; margin:0;'>⚡ Energía Global</h3>
        <p style='color:#a8d5b5; font-size:12px; margin:4px 0 0;'>
            M. A. Colorado · Talento Tech
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

    pagina = st.sidebar.radio(
        "🗺️ Navegación",
        ["🏠 Inicio", "📊 Dashboard"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("### 🔍 Filtros")

    # Países (excluir agregados OCDE para filtros)
    paises_reales = sorted(df[
        ~df["COUNTRY"].str.contains("OECD", na=False) &
        (df["COUNTRY"] != "IEA Total")
    ]["COUNTRY"].unique())

    paises_sel = st.sidebar.multiselect(
        "🌍 País / Región",
        options=paises_reales,
        default=["Colombia", "Brazil", "Spain", "Germany", "United States"]
    )

    productos_disp = sorted(df["PRODUCT"].unique())
    productos_labels = [PRODUCTOS_ES.get(p, p) for p in productos_disp]
    prod_map = dict(zip(productos_labels, productos_disp))

    fuentes_sel_labels = st.sidebar.multiselect(
        "⚡ Fuente de Energía",
        options=productos_labels,
        default=["Solar", "Eólica", "Hidroeléctrica",
                 "Nuclear", "Carbón", "Gas Natural"]
    )
    fuentes_sel = [prod_map[l] for l in fuentes_sel_labels if l in prod_map]

    anio_min, anio_max = int(df["YEAR"].min()), int(df["YEAR"].max())
    rango_anios = st.sidebar.slider(
        "📅 Rango de Años", anio_min, anio_max, (2015, 2022)
    )

    val_min = float(df["VALUE"].clip(lower=0).quantile(0.01))
    val_max = float(df["VALUE"].clip(lower=0).quantile(0.99))
    rango_val = st.sidebar.slider(
        "⚡ Rango de Valor (GWh)",
        val_min, val_max, (val_min, val_max),
        format="%.0f"
    )

    agregacion = st.sidebar.radio(
        "📆 Nivel de Agregación",
        ["Mensual", "Anual"]
    )

    paleta = st.sidebar.selectbox(
        "🎨 Paleta de Colores",
        ["mako", "viridis", "coolwarm", "Blues", "rocket", "magma", "crest"]
    )

    st.sidebar.markdown("### 👁️ Mostrar Secciones")
    mostrar_kpis       = st.sidebar.checkbox("KPIs resumen", True)
    mostrar_explorer   = st.sidebar.checkbox("Explorador de datos", True)
    mostrar_dist       = st.sidebar.checkbox("Análisis de distribución", True)
    mostrar_corr       = st.sidebar.checkbox("Correlación y estadística", True)
    mostrar_comp       = st.sidebar.checkbox("Comparación por fuente", True)
    mostrar_temporal   = st.sidebar.checkbox("Tendencias temporales", True)
    mostrar_geo        = st.sidebar.checkbox("Ranking geográfico", True)
    mostrar_profundo   = st.sidebar.checkbox("Análisis profundo por energía", True)
    mostrar_avanzado   = st.sidebar.checkbox("Funcionalidades avanzadas", True)

    st.sidebar.markdown("---")

    return {
        "pagina": pagina,
        "paises": paises_sel if paises_sel else paises_reales,
        "fuentes": fuentes_sel if fuentes_sel else productos_disp,
        "rango_anios": rango_anios,
        "rango_val": rango_val,
        "agregacion": agregacion,
        "paleta": paleta,
        "mostrar": {
            "kpis": mostrar_kpis,
            "explorer": mostrar_explorer,
            "dist": mostrar_dist,
            "corr": mostrar_corr,
            "comp": mostrar_comp,
            "temporal": mostrar_temporal,
            "geo": mostrar_geo,
            "profundo": mostrar_profundo,
            "avanzado": mostrar_avanzado,
        }
    }


# ── Helper para exportar CSV ──────────────────────────────────────────────────
def boton_descarga(df_fil):
    csv_bytes = df_fil.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="⬇️ Exportar datos filtrados (.csv)",
        data=csv_bytes,
        file_name="energia_filtrado.csv",
        mime="text/csv"
    )


# ══════════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════════
def render_kpis(df_fil):
    st.markdown("### 📊 Indicadores Clave (KPIs)")
    df_base = df_fil[df_fil["PRODUCT"].isin(FUENTES_PRINCIPALES)]

    total_gwh = df_base["VALUE"].sum()
    paises_uniq = df_base["COUNTRY"].nunique()
    prom_pais = total_gwh / paises_uniq if paises_uniq > 0 else 0

    top_pais = (df_base.groupby("COUNTRY")["VALUE"]
                .sum().idxmax() if not df_base.empty else "N/A")

    renovables_total = df_fil[df_fil["PRODUCT"].isin(RENOVABLES)]["VALUE"].sum()
    no_ren = df_fil[df_fil["PRODUCT"].isin(
        ["Coal", "Oil", "Natural gas", "Total combustible fuels"]
    )]["VALUE"].sum()
    pct_ren = (renovables_total / (renovables_total + no_ren) * 100
               if (renovables_total + no_ren) > 0 else 0)

    # Fuente mayor crecimiento
    try:
        crec = (df_base[df_base["YEAR"].isin([df_base["YEAR"].min(),
                                               df_base["YEAR"].max()])]
                .groupby(["PRODUCT", "YEAR"])["VALUE"].sum().unstack()
                .dropna(axis=1, how="any"))
        if crec.shape[1] >= 2:
            cols = sorted(crec.columns)
            crec["crecimiento"] = (crec[cols[-1]] - crec[cols[0]]) / (crec[cols[0]].abs() + 1e-9)
            fuente_crec = PRODUCTOS_ES.get(crec["crecimiento"].idxmax(), crec["crecimiento"].idxmax())
        else:
            fuente_crec = "N/A"
    except Exception:
        fuente_crec = "N/A"

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("⚡ Generación Total", f"{total_gwh/1e6:.2f} TWh")
    c2.metric("📈 Prom. por País (GWh)", f"{prom_pais:,.0f}".replace(",", "."))
    c3.metric("🏆 Mayor Productor", top_pais)
    c4.metric("🚀 Mayor Crecimiento", fuente_crec)
    c5.metric("🌿 % Renovable", f"{pct_ren:.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# EXPLORADOR DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
def render_explorador(df_fil, paleta):
    st.markdown("### 🔬 Explorador de Datos")

    col1, col2, col3 = st.columns(3)
    col1.info(f"**Filas:** {df_fil.shape[0]:,}".replace(",", "."))
    col2.info(f"**Columnas:** {df_fil.shape[1]}")
    dups = df_fil.duplicated().sum()
    if dups > 0:
        col3.warning(f"⚠️ Filas duplicadas: {dups}")
    else:
        col3.success("✅ Sin filas duplicadas")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Datos", "📐 Tipos y Estadísticas", "🔴 Valores Nulos", "📊 Describe"]
    )

    with tab1:
        df_show = df_fil.copy()
        df_show.columns = [c.replace("_", " ").title() for c in df_show.columns]
        st.dataframe(df_show.head(500), use_container_width=True)

    with tab2:
        tipos = pd.DataFrame({
            "Columna": df_fil.columns,
            "Tipo de Dato": df_fil.dtypes.astype(str).values,
            "Valores Únicos": [df_fil[c].nunique() for c in df_fil.columns],
            "Nulos": df_fil.isnull().sum().values
        })
        st.dataframe(tipos, use_container_width=True)

    with tab3:
        fig, ax = plt.subplots(figsize=(12, 4))
        nulos = df_fil.isnull().mean().to_frame().T
        sns.heatmap(nulos, annot=True, fmt=".1%", cmap="Reds",
                    linewidths=0.5, ax=ax, cbar_kws={"label": "% Nulos"})
        ax.set_title("Mapa de Calor — Proporción de Valores Nulos por Columna",
                     fontsize=13, pad=12)
        ax.set_xlabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with tab4:
        desc = df_fil.describe().round(2)
        desc.index = ["Conteo", "Media", "Desv. Estándar",
                      "Mínimo", "Percentil 25%", "Mediana",
                      "Percentil 75%", "Máximo"]
        st.dataframe(desc, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO A — DISTRIBUCIÓN
# ══════════════════════════════════════════════════════════════════════════════
def render_distribucion(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>📊 Grupo A · Análisis de Distribución</h3></div>",
        unsafe_allow_html=True
    )

    df_pos = df_fil[df_fil["VALUE"] > 0].copy()
    if df_pos.empty:
        st.warning("⚠️ Sin datos positivos para análisis de distribución con los filtros actuales.")
        return

    # 1. Histograma con KDE
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Distribución de Generación"):
        st.info("Muestra la frecuencia de los valores de generación eléctrica. "
                "La curva KDE suaviza la distribución. Picos altos indican rangos de "
                "generación más comunes entre los registros seleccionados.")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.histplot(data=df_pos, x="VALUE", kde=True,
                 color=sns.color_palette(paleta, 1)[0], ax=ax, bins=50)
    ax.set_title("Distribución de Generación Eléctrica (GWh) con Curva KDE", fontsize=14)
    ax.set_xlabel("Generación (GWh)")
    ax.set_ylabel("Frecuencia")
    plt.tight_layout()
    st.pyplot(fig); plt.close(fig)

    col1, col2 = st.columns(2)

    # 2. KDE por fuente
    with col1:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Densidad por Fuente"):
            st.info("Compara las densidades de distribución de generación entre "
                    "diferentes fuentes energéticas. Curvas más anchas = mayor variabilidad.")
        fuentes_top = (df_pos[df_pos["PRODUCT"].isin(FUENTES_PRINCIPALES)]
                       .groupby("PRODUCT")["VALUE"].sum()
                       .nlargest(6).index.tolist())
        df_kde = df_pos[df_pos["PRODUCT"].isin(fuentes_top)].copy()
        df_kde["Fuente"] = df_kde["PRODUCT"].map(PRODUCTOS_ES)
        fig, ax = plt.subplots(figsize=(10, 5))
        colores = sns.color_palette(paleta, len(fuentes_top))
        for i, f in enumerate(fuentes_top):
            d = df_kde[df_kde["PRODUCT"] == f]["VALUE"]
            if len(d) > 10:
                sns.kdeplot(d, ax=ax, label=PRODUCTOS_ES.get(f, f),
                            color=colores[i], linewidth=2)
        ax.set_title("Densidad de Generación por Fuente Energética", fontsize=13)
        ax.set_xlabel("Generación (GWh)")
        ax.set_ylabel("Densidad")
        ax.legend(title="Fuente", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 3. ECDF
    with col2:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Distribución Acumulada"):
            st.info("La función de distribución acumulada (ECDF) muestra qué porcentaje "
                    "de registros tiene un valor menor o igual a X. Útil para "
                    "identificar percentiles clave.")
        df_anual = df_pos.groupby(["YEAR", "PRODUCT"])["VALUE"].sum().reset_index()
        df_anual = df_anual[df_anual["PRODUCT"].isin(fuentes_top)]
        df_anual["Fuente"] = df_anual["PRODUCT"].map(PRODUCTOS_ES)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.ecdfplot(data=df_anual, x="VALUE", hue="Fuente",
                     palette=paleta, ax=ax, linewidth=2)
        ax.set_title("Distribución Acumulada de Generación Anual (ECDF)", fontsize=13)
        ax.set_xlabel("Generación Anual (GWh)")
        ax.set_ylabel("Proporción Acumulada")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 4. Rugplot top 5 países
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Dispersión Rugplot"):
        st.info("Cada línea vertical representa un registro individual. "
                "Zonas densas indican concentración de valores. "
                "Permite detectar valores extremos y su distribución real.")
    top5_paises = (df_pos[df_pos["PRODUCT"].isin(FUENTES_PRINCIPALES)]
                   .groupby("COUNTRY")["VALUE"].sum()
                   .nlargest(5).index.tolist())
    df_rug = df_pos[df_pos["COUNTRY"].isin(top5_paises) &
                    df_pos["PRODUCT"].isin(FUENTES_PRINCIPALES)]
    fig, ax = plt.subplots(figsize=(12, 4))
    colores_rug = sns.color_palette(paleta, len(top5_paises))
    for i, pais in enumerate(top5_paises):
        d = df_rug[df_rug["COUNTRY"] == pais]["VALUE"]
        sns.rugplot(d, ax=ax, color=colores_rug[i],
                    height=0.3 - i * 0.05, label=pais, alpha=0.6)
    ax.set_title("Dispersión de Valores de Generación — Top 5 Países (Rugplot)", fontsize=13)
    ax.set_xlabel("Generación (GWh)")
    ax.set_yticks([])
    ax.legend(title="País", loc="upper right")
    plt.tight_layout()
    st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO B — CORRELACIÓN
# ══════════════════════════════════════════════════════════════════════════════
def render_correlacion(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>🔗 Grupo B · Correlación y Estadística</h3></div>",
        unsafe_allow_html=True
    )

    df_num = df_fil[["VALUE", "YEAR", "MONTH", "share", "yearToDate"]].dropna()
    if df_num.empty:
        st.warning("⚠️ Sin datos numéricos suficientes con los filtros actuales.")
        return

    col1, col2 = st.columns(2)

    # 5. Heatmap correlación
    with col1:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Matriz de Correlación"):
            st.info("Los valores cercanos a 1 o -1 indican alta correlación "
                    "positiva o negativa. Valores cerca de 0 indican poca relación lineal. "
                    "Útil para detectar variables redundantes o complementarias.")
        df_num_renamed = df_num.rename(columns={
            "VALUE": "Generación (GWh)", "YEAR": "Año",
            "MONTH": "Mes", "share": "Participación (%)",
            "yearToDate": "Acum. Anual"
        })
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = df_num_renamed.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap=paleta,
                    linewidths=0.5, ax=ax, mask=False,
                    cbar_kws={"label": "Coeficiente de Pearson"})
        ax.set_title("Matriz de Correlación de Pearson\n(Variables Numéricas)", fontsize=13)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 6. Pairplot (muestra reducida)
    with col2:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Relaciones entre Variables"):
            st.info("Muestra simultáneamente las distribuciones individuales (diagonal) "
                    "y las relaciones entre pares de variables (off-diagonal). "
                    "Identifica patrones, clusters y relaciones no lineales.")
        df_pair = df_fil[df_fil["PRODUCT"].isin(["Solar", "Wind", "Hydro", "Nuclear"])].copy()
        df_pair = df_pair[["VALUE", "YEAR", "share", "PRODUCT"]].dropna()
        if df_pair.empty:
            st.warning("⚠️ Sin datos suficientes para el pairplot con los filtros actuales.")
        else:
            df_pair = df_pair.sample(min(1500, len(df_pair)), random_state=42)
            df_pair["Fuente"] = df_pair["PRODUCT"].map(PRODUCTOS_ES)
            df_pair = df_pair.rename(columns={
                "VALUE": "Generación", "YEAR": "Año", "share": "Participación"
            })
            colores_pair = sns.color_palette(paleta, 4)
            g = sns.pairplot(df_pair[["Generación", "Año", "Participación", "Fuente"]],
                             hue="Fuente", palette=colores_pair,
                             plot_kws={"alpha": 0.4, "s": 15}, height=2.2)
            g.figure.suptitle("Relaciones entre Variables por Fuente Energética",
                               y=1.02, fontsize=12)
            st.pyplot(g.figure); plt.close(g.figure)

    # 7. Clustermap
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Agrupamiento Jerárquico"):
        st.info("El clustermap reorganiza filas y columnas para agrupar países y fuentes "
                "con patrones similares. Los dendrogramas (árboles) muestran qué tan "
                "similares son los grupos. Colores más intensos = mayor generación.")
    pivot = (df_fil[df_fil["PRODUCT"].isin(FUENTES_PRINCIPALES)]
             .groupby(["COUNTRY", "PRODUCT"])["VALUE"].sum()
             .unstack(fill_value=0))
    pivot.columns = [PRODUCTOS_ES.get(c, c) for c in pivot.columns]
    pivot_norm = (pivot - pivot.min()) / (pivot.max() - pivot.min() + 1e-9)
    pivot_top = pivot_norm.loc[pivot.sum(axis=1).nlargest(20).index]
    fig = sns.clustermap(pivot_top, cmap=paleta, figsize=(12, 8),
                         linewidths=0.3, cbar_kws={"label": "Generación Normalizada"},
                         dendrogram_ratio=0.15)
    fig.fig.suptitle("Agrupamiento Jerárquico — País × Fuente de Energía (Top 20 países)",
                     y=1.01, fontsize=13)
    st.pyplot(fig.fig); plt.close(fig.fig)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO C — COMPARACIÓN POR FUENTE
# ══════════════════════════════════════════════════════════════════════════════
def render_comparacion(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>⚡ Grupo C · Comparación por Fuente Energética</h3></div>",
        unsafe_allow_html=True
    )

    df_f = df_fil[df_fil["PRODUCT"].isin(FUENTES_PRINCIPALES)].copy()
    if df_f.empty:
        st.warning("⚠️ Sin datos para comparar fuentes con los filtros actuales.")
        return
    df_f["Fuente"] = df_f["PRODUCT"].map(PRODUCTOS_ES)
    colores_c = sns.color_palette(paleta, len(FUENTES_PRINCIPALES))

    col1, col2 = st.columns(2)

    # 8. Boxplot
    with col1:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Boxplot por Fuente"):
            st.info("La caja muestra el rango intercuartílico (IQR: percentil 25%-75%). "
                    "La línea central es la mediana. Los puntos fuera son valores atípicos.")
        df_box = df_f[df_f["VALUE"] > 0]
        fig, ax = plt.subplots(figsize=(12, 5))
        orden = df_box.groupby("Fuente")["VALUE"].median().sort_values().index
        sns.boxplot(data=df_box, x="Fuente", y="VALUE",
                    order=orden, palette=paleta, ax=ax,
                    showfliers=False)
        ax.set_title("Distribución de Generación por Fuente Energética (Boxplot)", fontsize=13)
        ax.set_xlabel("Fuente de Energía")
        ax.set_ylabel("Generación (GWh)")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 9. Violinplot por década
    with col2:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Violín por Fuente"):
            st.info("El gráfico de violín combina boxplot y densidad. "
                    "Forma más ancha = mayor concentración de datos en ese rango de valores.")
        df_f["Década"] = (df_f["YEAR"] // 5 * 5).astype(str) + "s"
        df_viol = df_f[(df_f["VALUE"] > 0) &
                       (df_f["PRODUCT"].isin(["Solar", "Wind", "Hydro", "Nuclear", "Coal"]))].copy()
        df_viol["Fuente"] = df_viol["PRODUCT"].map(PRODUCTOS_ES)
        if df_viol.empty or df_viol["Fuente"].nunique() == 0:
            st.warning("⚠️ Sin datos suficientes para el gráfico de violín con los filtros actuales.")
        else:
            fig, ax = plt.subplots(figsize=(12, 5))
            try:
                sns.violinplot(data=df_viol, x="Fuente", y="VALUE",
                               hue="Década", palette=paleta, ax=ax,
                               inner="quartile")
            except TypeError:
                sns.violinplot(data=df_viol, x="Fuente", y="VALUE",
                               palette=paleta, ax=ax, inner="quartile")
            ax.set_title("Variabilidad de Generación por Fuente y Período (Violín)", fontsize=13)
            ax.set_xlabel("Fuente de Energía")
            ax.set_ylabel("Generación (GWh)")
            ax.tick_params(axis="x", rotation=20)
            ax.legend(title="Período", loc="upper right", fontsize=9)
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

    col3, col4 = st.columns(2)

    # 10. Stripplot
    with col3:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Puntos Individuales (Stripplot)"):
            st.info("Cada punto es un registro individual. Permite ver la densidad "
                    "y distribución real de los datos sin perder información.")
        df_strip_base = df_f[df_f["VALUE"] > 0].copy()
        if df_strip_base.empty:
            st.warning("⚠️ Sin datos para el stripplot con los filtros actuales.")
        else:
            n_strip = min(3000, len(df_strip_base))
            df_strip = df_strip_base.sample(n_strip, random_state=42)
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.stripplot(data=df_strip, x="Fuente", y="VALUE",
                          palette=paleta, ax=ax, alpha=0.3, size=3, jitter=True)
            ax.set_title("Puntos Individuales de Generación por Fuente (Stripplot)", fontsize=13)
            ax.set_xlabel("Fuente de Energía")
            ax.set_ylabel("Generación (GWh)")
            ax.tick_params(axis="x", rotation=30)
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

    # 11. Barplot media ± IC
    with col4:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Media con Intervalo de Confianza"):
            st.info("Las barras muestran la generación media. Las líneas de error "
                    "representan el intervalo de confianza al 95%. "
                    "Un intervalo más corto indica mayor consistencia en los datos.")
        fig, ax = plt.subplots(figsize=(10, 5))
        df_bar = df_f[df_f["VALUE"] > 0].copy()
        orden_bar = df_bar.groupby("Fuente")["VALUE"].mean().sort_values(ascending=False).index
        sns.barplot(data=df_bar, x="Fuente", y="VALUE",
                    order=orden_bar, palette=paleta, ax=ax,
                    capsize=0.1, errcolor="gray", errwidth=1.5)
        ax.set_title("Generación Media ± Intervalo de Confianza 95% por Fuente", fontsize=13)
        ax.set_xlabel("Fuente de Energía")
        ax.set_ylabel("Generación Media (GWh)")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 12. Pointplot tendencia
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Tendencia Media por Año"):
        st.info("Los puntos conectados muestran cómo evoluciona la media de generación "
                "de cada fuente a lo largo de los años. Pendientes positivas indican crecimiento.")
    fuentes_pt = ["Solar", "Wind", "Hydro", "Nuclear", "Coal"]
    df_pt = df_f[df_f["PRODUCT"].isin(fuentes_pt) & (df_f["VALUE"] > 0)].copy()
    df_pt["Fuente"] = df_pt["PRODUCT"].map(PRODUCTOS_ES)
    fig, ax = plt.subplots(figsize=(13, 5))
    sns.pointplot(data=df_pt, x="YEAR", y="VALUE", hue="Fuente",
                  palette=paleta, ax=ax, errorbar=None,
                  markers="o", linestyles="-", markersize=5)
    ax.set_title("Tendencia de Generación Media por Fuente Energética (2010–2022)", fontsize=13)
    ax.set_xlabel("Año")
    ax.set_ylabel("Generación Media (GWh)")
    ax.legend(title="Fuente", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO D — TENDENCIAS TEMPORALES
# ══════════════════════════════════════════════════════════════════════════════
def render_temporal(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>📅 Grupo D · Tendencias Temporales</h3></div>",
        unsafe_allow_html=True
    )

    df_f = df_fil[df_fil["PRODUCT"].isin(FUENTES_PRINCIPALES)].copy()
    if df_f.empty:
        st.warning("⚠️ Sin datos temporales con los filtros actuales.")
        return
    df_f["Fuente"] = df_f["PRODUCT"].map(PRODUCTOS_ES)

    # 13. Lineplot anual total multilínea
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Generación Anual Total"):
        st.info("Muestra la evolución total de generación por año para cada fuente. "
                "Las líneas ascendentes indican crecimiento sostenido. "
                "Útil para identificar qué fuentes están ganando o perdiendo participación.")
    anual = df_f.groupby(["YEAR", "Fuente"])["VALUE"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(13, 5))
    sns.lineplot(data=anual, x="YEAR", y="VALUE", hue="Fuente",
                 palette=paleta, ax=ax, marker="o", linewidth=2.5)
    ax.set_title("Generación Anual Total por Fuente Energética (2010–2022)", fontsize=13)
    ax.set_xlabel("Año")
    ax.set_ylabel("Generación Total (GWh)")
    ax.legend(title="Fuente", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.tight_layout()
    st.pyplot(fig); plt.close(fig)

    col1, col2 = st.columns(2)

    # 14. Estacionalidad mensual
    with col1:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Estacionalidad Mensual"):
            st.info("Muestra el promedio de generación para cada mes del año. "
                    "Permite detectar patrones estacionales: "
                    "picos en verano (solar) o invierno (demanda calefacción).")
        mensual = df_f.groupby(["MONTH", "Fuente"])["VALUE"].mean().reset_index()
        mensual["Mes"] = mensual["MONTH"].map(MESES_ES)
        orden_mes = [MESES_ES[i] for i in range(1, 13)]
        fig, ax = plt.subplots(figsize=(10, 5))
        fuentes_est = ["Solar", "Eólica", "Hidroeléctrica", "Nuclear"]
        df_est = mensual[mensual["Fuente"].isin(fuentes_est)]
        sns.lineplot(data=df_est, x="Mes", y="VALUE", hue="Fuente",
                     palette=paleta, ax=ax, marker="o", linewidth=2.5,
                     order=orden_mes)
        ax.set_title("Estacionalidad Mensual — Generación Promedio por Mes", fontsize=13)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Generación Promedio (GWh)")
        ax.legend(title="Fuente", fontsize=9)
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 15. Barplot año a año
    with col2:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Total Año a Año"):
            st.info("Compara la generación total acumulada año a año de las principales "
                    "fuentes. Permite visualizar el crecimiento global del sector energético.")
        total_anual = (df_f[df_f["VALUE"] > 0]
                       .groupby("YEAR")["VALUE"].sum().reset_index())
        total_anual.columns = ["Año", "Generación Total (GWh)"]
        fig, ax = plt.subplots(figsize=(10, 5))
        colores_bar = sns.color_palette(paleta, len(total_anual))
        sns.barplot(data=total_anual, x="Año", y="Generación Total (GWh)",
                    palette=colores_bar, ax=ax)
        ax.set_title("Generación Total Año a Año — Todas las Fuentes", fontsize=13)
        ax.set_xlabel("Año")
        ax.set_ylabel("Generación Total (GWh)")
        ax.tick_params(axis="x", rotation=30)
        for p in ax.patches:
            ax.annotate(f"{p.get_height()/1e6:.1f}M",
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha="center", va="bottom", fontsize=7.5, color="gray")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 16. Scatterplot generación vs año
    with st.expander("ℹ️ ¿Cómo leer este gráfico? — Generación vs Año (Scatter)"):
        st.info("Cada punto es un registro mensual. El color indica la fuente y "
                "el tamaño refleja la participación porcentual en el total. "
                "Permite detectar tendencias, dispersión y valores extremos por fuente y año.")
    df_sc_base = df_f[(df_f["VALUE"] > 0) & (df_f["share"] > 0)].copy()
    if df_sc_base.empty:
        st.warning("⚠️ Sin datos para el scatter con los filtros actuales.")
    else:
        df_sc = df_sc_base.sample(min(4000, len(df_sc_base)), random_state=42)
        fig, ax = plt.subplots(figsize=(13, 5))
        fuentes_sc = ["Solar", "Eólica", "Hidroeléctrica", "Nuclear", "Carbón", "Gas Natural"]
        df_sc2 = df_sc[df_sc["Fuente"].isin(fuentes_sc)]
        scatter_pal = dict(zip(fuentes_sc, sns.color_palette(paleta, len(fuentes_sc))))
        for fuente in fuentes_sc:
            d = df_sc2[df_sc2["Fuente"] == fuente]
            if d.empty:
                continue
            ax.scatter(d["YEAR"] + np.random.uniform(-0.3, 0.3, len(d)),
                       d["VALUE"], c=[scatter_pal[fuente]], alpha=0.4,
                       s=d["share"].clip(0, 1) * 80 + 5, label=fuente)
        ax.set_title("Generación vs Año — Color: Fuente · Tamaño: Participación (%)", fontsize=13)
        ax.set_xlabel("Año")
        ax.set_ylabel("Generación (GWh)")
        ax.legend(title="Fuente", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
        ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO E — RANKING GEOGRÁFICO
# ══════════════════════════════════════════════════════════════════════════════
def render_geografico(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>🌍 Grupo E · Ranking Geográfico</h3></div>",
        unsafe_allow_html=True
    )

    df_paises = df_fil[
        ~df_fil["COUNTRY"].str.contains("OECD", na=False) &
        (df_fil["COUNTRY"] != "IEA Total") &
        df_fil["PRODUCT"].isin(FUENTES_PRINCIPALES) &
        (df_fil["VALUE"] > 0)
    ].copy()

    col1, col2 = st.columns(2)

    # 17. Top 15 países (horizontal)
    with col1:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Top 15 Países"):
            st.info("Ranking de los 15 países con mayor generación total acumulada "
                    "en el período seleccionado. Las barras horizontales facilitan "
                    "la lectura de nombres largos.")
        top15 = (df_paises.groupby("COUNTRY")["VALUE"]
                 .sum().nlargest(15).reset_index())
        top15.columns = ["País", "Generación Total (GWh)"]
        fig, ax = plt.subplots(figsize=(10, 6))
        colores_g = sns.color_palette(paleta, len(top15))
        sns.barplot(data=top15, y="País", x="Generación Total (GWh)",
                    palette=colores_g, ax=ax, orient="h")
        ax.set_title("Top 15 Países por Generación Total (GWh)", fontsize=13)
        ax.set_xlabel("Generación Total (GWh)")
        ax.set_ylabel("País")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 18. Heatmap país × fuente
    with col2:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Mapa de Calor País × Fuente"):
            st.info("Cada celda muestra la generación total (GWh) de un país "
                    "para una fuente específica. Colores más intensos = mayor generación. "
                    "Útil para comparar el mix energético entre países.")
        pivot_hm = (df_paises.groupby(["COUNTRY", "PRODUCT"])["VALUE"]
                    .sum().unstack(fill_value=0))
        pivot_hm.columns = [PRODUCTOS_ES.get(c, c) for c in pivot_hm.columns]
        top20 = pivot_hm.sum(axis=1).nlargest(20).index
        pivot_hm = pivot_hm.loc[top20]
        pivot_hm_norm = pivot_hm / 1e3  # en TGh
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(pivot_hm_norm, cmap=paleta, ax=ax,
                    linewidths=0.3, annot=True, fmt=".0f",
                    cbar_kws={"label": "Generación (TWh)"}, annot_kws={"size": 7})
        ax.set_title("Generación Total por País y Fuente Energética (TWh)", fontsize=13)
        ax.set_xlabel("Fuente de Energía")
        ax.set_ylabel("País")
        ax.tick_params(axis="x", rotation=35)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    col3, col4 = st.columns(2)

    # 19. Countplot registros por país
    with col3:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Registros por País"):
            st.info("Muestra la cantidad de registros disponibles para cada país. "
                    "Más registros = mayor cobertura temporal o más fuentes reportadas.")
        conteo = (df_paises["COUNTRY"].value_counts().nlargest(20).reset_index())
        conteo.columns = ["País", "Cantidad de Registros"]
        fig, ax = plt.subplots(figsize=(10, 6))
        colores_cnt = sns.color_palette(paleta, len(conteo))
        sns.barplot(data=conteo, y="País", x="Cantidad de Registros",
                    palette=colores_cnt, ax=ax, orient="h")
        ax.set_title("Cantidad de Registros por País (Top 20)", fontsize=13)
        ax.set_xlabel("Número de Registros")
        ax.set_ylabel("País")
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

    # 20. Renovable vs No renovable por país
    with col4:
        with st.expander("ℹ️ ¿Cómo leer este gráfico? — Renovable vs No Renovable"):
            st.info("Compara la proporción de generación renovable vs no renovable "
                    "para los 10 principales países. Países con mayor barra verde "
                    "tienen una matriz energética más limpia.")
        ren_pais = df_paises.copy()
        ren_pais["Tipo"] = ren_pais["PRODUCT"].apply(
            lambda x: "Renovable" if x in RENOVABLES else "No Renovable"
        )
        top10_p = ren_pais.groupby("COUNTRY")["VALUE"].sum().nlargest(10).index
        ren_pais = ren_pais[ren_pais["COUNTRY"].isin(top10_p)]
        ren_sum = ren_pais.groupby(["COUNTRY", "Tipo"])["VALUE"].sum().unstack(fill_value=0)
        ren_pct = ren_sum.div(ren_sum.sum(axis=1), axis=0) * 100
        ren_pct = ren_pct.sort_values("Renovable", ascending=True)
        ren_pct_long = ren_pct.reset_index().melt(id_vars="COUNTRY",
                                                   var_name="Tipo",
                                                   value_name="Porcentaje (%)")
        fig, ax = plt.subplots(figsize=(10, 6))
        colores_rv = {"Renovable": sns.color_palette(paleta, 3)[1],
                      "No Renovable": sns.color_palette("rocket", 3)[2]}
        sns.barplot(data=ren_pct_long, y="COUNTRY", x="Porcentaje (%)",
                    hue="Tipo", palette=colores_rv, ax=ax, orient="h")
        ax.set_title("Participación Renovable vs No Renovable — Top 10 Países (%)", fontsize=13)
        ax.set_xlabel("Porcentaje (%)")
        ax.set_ylabel("País")
        ax.axvline(50, color="white", linestyle="--", linewidth=1.5, alpha=0.7, label="50%")
        ax.legend(title="Tipo de Energía", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# GRUPO F — ANÁLISIS PROFUNDO POR ENERGÍA
# ══════════════════════════════════════════════════════════════════════════════
def render_profundo(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>🔍 Grupo F · Análisis Profundo por Tipo de Energía</h3></div>",
        unsafe_allow_html=True
    )

    fuentes_deep = {
        "Solar": "☀️ Solar",
        "Wind": "💨 Eólica",
        "Hydro": "💧 Hidroeléctrica",
        "Nuclear": "⚛️ Nuclear",
        "Coal": "🪨 Carbón",
        "Natural gas": "🔥 Gas Natural",
    }

    df_paises = df_fil[
        ~df_fil["COUNTRY"].str.contains("OECD", na=False) &
        (df_fil["COUNTRY"] != "IEA Total")
    ]

    for prod_en, titulo in fuentes_deep.items():
        prod_es = PRODUCTOS_ES.get(prod_en, prod_en)
        df_src = df_paises[
            (df_paises["PRODUCT"] == prod_en) & (df_paises["VALUE"] > 0)
        ]
        if df_src.empty:
            continue

        with st.expander(f"🔍 Análisis Detallado — {titulo}"):

            # KPIs
            total = df_src["VALUE"].sum()
            anio_pico = df_src.groupby("YEAR")["VALUE"].sum().idxmax()
            pais_pico = df_src.groupby("COUNTRY")["VALUE"].sum().idxmax()
            anual_g = df_src.groupby("YEAR")["VALUE"].sum()
            if len(anual_g) >= 2:
                cagr = ((anual_g.iloc[-1] / anual_g.iloc[0]) **
                        (1 / (len(anual_g) - 1)) - 1) * 100
            else:
                cagr = 0.0

            k1, k2, k3, k4 = st.columns(4)
            k1.metric(f"⚡ Total GWh ({prod_es})", f"{total/1e6:.2f} TWh")
            k2.metric("📅 Año Pico", str(anio_pico))
            k3.metric("🏆 País Pico", pais_pico)
            k4.metric("📈 TCAC Anual", f"{cagr:.1f}%")

            c1, c2, c3 = st.columns(3)

            # Línea de crecimiento
            with c1:
                anual_plot = anual_g.reset_index()
                anual_plot.columns = ["Año", "Generación (GWh)"]
                fig, ax = plt.subplots(figsize=(7, 4))
                color_src = sns.color_palette(paleta, 3)[1]
                sns.lineplot(data=anual_plot, x="Año", y="Generación (GWh)",
                             color=color_src, ax=ax, marker="o", linewidth=2.5)
                ax.fill_between(anual_plot["Año"], anual_plot["Generación (GWh)"],
                                alpha=0.15, color=color_src)
                ax.set_title(f"Tendencia Anual — {prod_es}", fontsize=12)
                ax.set_xlabel("Año")
                ax.set_ylabel("Generación (GWh)")
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)

            # Top 10 países
            with c2:
                top10 = (df_src.groupby("COUNTRY")["VALUE"]
                         .sum().nlargest(10).reset_index())
                top10.columns = ["País", "Generación (GWh)"]
                fig, ax = plt.subplots(figsize=(7, 4))
                colores_t10 = sns.color_palette(paleta, len(top10))
                sns.barplot(data=top10, y="País", x="Generación (GWh)",
                            palette=colores_t10, ax=ax, orient="h")
                ax.set_title(f"Top 10 Países — {prod_es}", fontsize=12)
                ax.set_xlabel("Generación (GWh)")
                ax.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)

            # Boxplot estacional mensual
            with c3:
                df_men = df_src.copy()
                df_men["Mes"] = df_men["MONTH"].map(MESES_ES)
                orden_m = [MESES_ES[i] for i in range(1, 13)]
                df_men_f = df_men[df_men["Mes"].isin(orden_m)]
                fig, ax = plt.subplots(figsize=(7, 4))
                colores_m = sns.color_palette(paleta, 12)
                sns.boxplot(data=df_men_f, x="Mes", y="VALUE",
                            order=orden_m, palette=colores_m, ax=ax,
                            showfliers=False)
                ax.set_title(f"Variabilidad Mensual — {prod_es}", fontsize=12)
                ax.set_xlabel("Mes")
                ax.set_ylabel("Generación (GWh)")
                ax.tick_params(axis="x", rotation=45)
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — FUNCIONALIDADES AVANZADAS
# ══════════════════════════════════════════════════════════════════════════════
def render_avanzado(df_fil, paleta):
    st.markdown(
        "<div class='section-title'><h3 style='color:#52b788;margin:0'>💡 Funcionalidades Avanzadas de Análisis</h3></div>",
        unsafe_allow_html=True
    )

    df_paises = df_fil[
        ~df_fil["COUNTRY"].str.contains("OECD", na=False) &
        (df_fil["COUNTRY"] != "IEA Total")
    ].copy()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌿 Transición Energética",
        "🌍 Comparador de Países",
        "🚨 Detector de Anomalías",
        "📈 Tasa de Crecimiento",
        "🥧 Mix Energético"
    ])

    # ── RASTREADOR TRANSICIÓN ──────────────────────────────────────────────
    with tab1:
        st.subheader("🌿 Rastreador de Transición Energética")
        df_ren = df_paises.copy()
        df_ren["Tipo"] = df_ren["PRODUCT"].apply(
            lambda x: "Renovable" if x in RENOVABLES else "No Renovable"
        )
        df_ren = df_ren[df_ren["PRODUCT"].isin(FUENTES_PRINCIPALES + RENOVABLES)]
        ren_anual = (df_ren.groupby(["COUNTRY", "YEAR", "Tipo"])["VALUE"]
                     .sum().unstack(fill_value=0).reset_index())
        if "Renovable" in ren_anual.columns and "No Renovable" in ren_anual.columns:
            ren_anual["% Renovable"] = (
                ren_anual["Renovable"] /
                (ren_anual["Renovable"] + ren_anual["No Renovable"] + 1e-9) * 100
            )
            # Crecimiento % renovable por país
            crec_ren = (ren_anual.groupby("COUNTRY")
                        .apply(lambda g: g.sort_values("YEAR")["% Renovable"].iloc[-1] -
                               g.sort_values("YEAR")["% Renovable"].iloc[0])
                        .reset_index())
            crec_ren.columns = ["País", "Crecimiento % Renovable"]
            top10_ren = crec_ren.nlargest(10, "Crecimiento % Renovable")

            col1, col2 = st.columns([2, 1])
            with col1:
                fig, ax = plt.subplots(figsize=(10, 5))
                colores_ren = sns.color_palette(paleta, len(top10_ren))
                sns.barplot(data=top10_ren, y="País", x="Crecimiento % Renovable",
                            palette=colores_ren, ax=ax, orient="h")
                ax.set_title("Top 10 Países con Mayor Crecimiento en Energía Renovable (%)",
                             fontsize=13)
                ax.set_xlabel("Crecimiento Puntos Porcentuales (pp)")
                ax.set_ylabel("País")
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)

            with col2:
                st.markdown("**🏆 Países que superaron el 50% renovable:**")
                ult_anio = ren_anual.sort_values("YEAR").groupby("COUNTRY").last()
                sup50 = ult_anio[ult_anio["% Renovable"] >= 50].index.tolist()
                if sup50:
                    for p in sup50:
                        pct = ult_anio.loc[p, "% Renovable"]
                        st.success(f"✅ **{p}** → {pct:.1f}% renovable")
                else:
                    st.info("Ningún país en la selección supera el 50% renovable.")

    # ── COMPARADOR DE PAÍSES ───────────────────────────────────────────────
    with tab2:
        st.subheader("🌍 Comparador de Países")
        todos_paises = sorted(df_paises["COUNTRY"].unique())
        paises_comp = st.multiselect(
            "Selecciona entre 2 y 5 países para comparar:",
            todos_paises,
            default=["Colombia", "Brazil", "Spain", "Germany"]
        )
        if len(paises_comp) < 2:
            st.warning("⚠️ Selecciona al menos 2 países para comparar.")
        else:
            df_comp = df_paises[
                df_paises["COUNTRY"].isin(paises_comp) &
                df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
                (df_paises["VALUE"] > 0)
            ]
            anual_comp = df_comp.groupby(["COUNTRY", "YEAR"])["VALUE"].sum().reset_index()

            fig, ax = plt.subplots(figsize=(13, 5))
            colores_cp = sns.color_palette(paleta, len(paises_comp))
            for i, pais in enumerate(paises_comp):
                d = anual_comp[anual_comp["COUNTRY"] == pais]
                ax.plot(d["YEAR"], d["VALUE"] / 1e3, marker="o",
                        color=colores_cp[i], linewidth=2.5, label=pais)
            ax.set_title("Comparación de Generación Total Anual por País (TWh)", fontsize=13)
            ax.set_xlabel("Año")
            ax.set_ylabel("Generación Total (TWh)")
            ax.legend(title="País", fontsize=10)
            ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

            # Tabla resumen
            resumen = []
            for pais in paises_comp:
                d = anual_comp[anual_comp["COUNTRY"] == pais]["VALUE"]
                if len(d) >= 2:
                    cagr_p = ((d.iloc[-1] / d.iloc[0]) ** (1 / (len(d) - 1)) - 1) * 100
                else:
                    cagr_p = 0
                resumen.append({
                    "País": pais,
                    "Total (GWh)": f"{d.sum():,.0f}".replace(",", "."),
                    "Media (GWh)": f"{d.mean():,.0f}".replace(",", "."),
                    "Máximo (GWh)": f"{d.max():,.0f}".replace(",", "."),
                    "Mínimo (GWh)": f"{d.min():,.0f}".replace(",", "."),
                    "TCAC (%)": f"{cagr_p:.1f}%"
                })
            st.dataframe(pd.DataFrame(resumen), use_container_width=True)

    # ── DETECTOR DE ANOMALÍAS ──────────────────────────────────────────────
    with tab3:
        st.subheader("🚨 Detector de Anomalías (Método IQR)")
        df_anom = df_paises[df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
                            (df_paises["VALUE"] > 0)].copy()
        Q1 = df_anom["VALUE"].quantile(0.25)
        Q3 = df_anom["VALUE"].quantile(0.75)
        IQR = Q3 - Q1
        lim_inf = Q1 - 1.5 * IQR
        lim_sup = Q3 + 1.5 * IQR
        df_anom["Anomalía"] = ((df_anom["VALUE"] < lim_inf) |
                                (df_anom["VALUE"] > lim_sup))

        n_anom = df_anom["Anomalía"].sum()
        st.info(f"📊 Se detectaron **{n_anom:,}** registros anómalos "
                f"({n_anom/len(df_anom)*100:.1f}% del total) usando el método IQR.")

        fig, ax = plt.subplots(figsize=(13, 5))
        normales_base = df_anom[~df_anom["Anomalía"]]
        anomalos = df_anom[df_anom["Anomalía"]]
        normales = (normales_base.sample(min(2000, len(normales_base)), random_state=42)
                    if not normales_base.empty else normales_base)
        color_norm = sns.color_palette(paleta, 3)[1]
        if not normales.empty:
            ax.scatter(normales["YEAR"] + np.random.uniform(-0.3, 0.3, len(normales)),
                       normales["VALUE"], alpha=0.3, s=8, color=color_norm, label="Normal")
        if not anomalos.empty:
            ax.scatter(anomalos["YEAR"] + np.random.uniform(-0.3, 0.3, len(anomalos)),
                       anomalos["VALUE"], alpha=0.7, s=20, color="#e63946", label="Anomalía")
        ax.axhline(lim_sup, color="orange", linestyle="--", linewidth=1.5,
                   label=f"Límite superior IQR ({lim_sup:,.0f} GWh)")
        ax.set_title("Detección de Anomalías en Generación Eléctrica (Método IQR)", fontsize=13)
        ax.set_xlabel("Año")
        ax.set_ylabel("Generación (GWh)")
        ax.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

        with st.expander(f"📋 Ver registros anómalos ({n_anom} registros)"):
            cols_show = ["COUNTRY", "YEAR", "MONTH_NAME", "PRODUCT", "VALUE"]
            df_anom_show = anomalos[cols_show].copy()
            df_anom_show.columns = ["País", "Año", "Mes", "Fuente", "Generación (GWh)"]
            df_anom_show["Fuente"] = df_anom_show["Fuente"].map(PRODUCTOS_ES)
            st.warning(f"⚠️ Se encontraron {n_anom} registros con valores atípicos.")
            st.dataframe(df_anom_show.sort_values("Generación (GWh)", ascending=False),
                         use_container_width=True)

    # ── CALCULADORA DE CRECIMIENTO ─────────────────────────────────────────
    with tab4:
        st.subheader("📈 Calculadora de Tasa de Crecimiento Año a Año")
        df_crec = df_paises[
            df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
            (df_paises["VALUE"] > 0)
        ].groupby(["COUNTRY", "YEAR"])["VALUE"].sum().reset_index()

        df_crec["YoY (%)"] = (df_crec.groupby("COUNTRY")["VALUE"]
                               .pct_change() * 100).round(1)

        pivot_crec = (df_crec.dropna(subset=["YoY (%)"])
                      .pivot_table(index="COUNTRY", columns="YEAR",
                                   values="YoY (%)", aggfunc="mean"))
        top15 = df_crec.groupby("COUNTRY")["VALUE"].sum().nlargest(15).index
        pivot_crec = pivot_crec.loc[pivot_crec.index.isin(top15)].dropna(how="all")

        fig, ax = plt.subplots(figsize=(13, 7))
        sns.heatmap(pivot_crec, cmap="coolwarm", ax=ax, center=0,
                    annot=True, fmt=".0f", linewidths=0.3,
                    cbar_kws={"label": "Variación YoY (%)"},
                    annot_kws={"size": 8})
        ax.set_title("Tasa de Crecimiento Año a Año por País (%) — Top 15 Países",
                     fontsize=13)
        ax.set_xlabel("Año")
        ax.set_ylabel("País")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        st.pyplot(fig); plt.close(fig)

        # Top 5 mayor crecimiento / declive por fuente
        df_fuente_crec = df_paises[
            df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
            (df_paises["VALUE"] > 0)
        ].groupby(["PRODUCT", "YEAR"])["VALUE"].sum().reset_index()

        df_fuente_crec["CAGR"] = df_fuente_crec.groupby("PRODUCT")["VALUE"].pct_change() * 100
        crec_fuente = (df_fuente_crec.groupby("PRODUCT")["CAGR"]
                       .mean().reset_index())
        crec_fuente["Fuente"] = crec_fuente["PRODUCT"].map(PRODUCTOS_ES)
        crec_fuente = crec_fuente.sort_values("CAGR", ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            top5_crec = crec_fuente.nlargest(5, "CAGR")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.barplot(data=top5_crec, y="Fuente", x="CAGR",
                        palette=paleta, ax=ax, orient="h")
            ax.set_title("Top 5 Fuentes de Mayor Crecimiento Promedio YoY", fontsize=12)
            ax.set_xlabel("Crecimiento Promedio Anual (%)")
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

        with col2:
            top5_decl = crec_fuente.nsmallest(5, "CAGR")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.barplot(data=top5_decl, y="Fuente", x="CAGR",
                        palette="rocket", ax=ax, orient="h")
            ax.set_title("Top 5 Fuentes en Mayor Declive Promedio YoY", fontsize=12)
            ax.set_xlabel("Crecimiento Promedio Anual (%)")
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

    # ── MIX ENERGÉTICO ─────────────────────────────────────────────────────
    with tab5:
        st.subheader("🥧 Instantánea del Mix Energético")
        todos_paises_mix = sorted(df_paises["COUNTRY"].unique())
        col_a, col_b = st.columns(2)
        with col_a:
            pais_mix = st.selectbox("Selecciona un país:", todos_paises_mix,
                                    index=todos_paises_mix.index("Colombia")
                                    if "Colombia" in todos_paises_mix else 0)
        with col_b:
            anios_disp = sorted(df_paises["YEAR"].unique())
            anio_mix = st.selectbox("Selecciona un año:", anios_disp,
                                    index=len(anios_disp) - 1)

        df_mix = df_paises[
            (df_paises["COUNTRY"] == pais_mix) &
            (df_paises["YEAR"] == anio_mix) &
            df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
            (df_paises["VALUE"] > 0)
        ].groupby("PRODUCT")["VALUE"].sum()

        if df_mix.empty:
            st.warning("No hay datos disponibles para esta combinación de país y año.")
        else:
            df_mix.index = [PRODUCTOS_ES.get(i, i) for i in df_mix.index]
            fuente_dom = df_mix.idxmax()
            st.metric("⚡ Fuente Dominante", fuente_dom,
                      f"{df_mix.max()/df_mix.sum()*100:.1f}% del total")

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(7, 6))
                colores_mix = sns.color_palette(paleta, len(df_mix))
                wedges, texts, autotexts = ax.pie(
                    df_mix, labels=df_mix.index, autopct="%1.1f%%",
                    colors=colores_mix, startangle=90,
                    pctdistance=0.8, wedgeprops=dict(width=0.6)
                )
                for t in autotexts:
                    t.set_fontsize(9)
                ax.set_title(f"Mix Energético — {pais_mix} ({anio_mix})", fontsize=13)
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)

            with col2:
                # Comparar con promedio global
                df_global = df_paises[
                    (df_paises["YEAR"] == anio_mix) &
                    df_paises["PRODUCT"].isin(FUENTES_PRINCIPALES) &
                    (df_paises["VALUE"] > 0)
                ].groupby("PRODUCT")["VALUE"].sum()
                df_global.index = [PRODUCTOS_ES.get(i, i) for i in df_global.index]
                df_global_pct = df_global / df_global.sum() * 100
                df_mix_pct = df_mix / df_mix.sum() * 100

                df_comp_mix = pd.DataFrame({
                    pais_mix: df_mix_pct,
                    "Promedio Global": df_global_pct
                }).fillna(0)

                fig, ax = plt.subplots(figsize=(8, 5))
                df_comp_mix.plot(kind="bar", ax=ax,
                                 color=sns.color_palette(paleta, 2),
                                 width=0.7)
                ax.set_title(f"Mix de {pais_mix} vs Promedio Global — {anio_mix}",
                             fontsize=12)
                ax.set_xlabel("Fuente de Energía")
                ax.set_ylabel("Participación (%)")
                ax.legend(title="Referencia", fontsize=9)
                ax.tick_params(axis="x", rotation=30)
                plt.tight_layout()
                st.pyplot(fig); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    df = cargar_datos()
    if df.empty:
        st.error("No se pudo cargar el dataset. Verifica que data.csv esté disponible.")
        return

    cfg = render_sidebar(df)

    # Aplicar filtros
    df_fil = df[
        df["COUNTRY"].isin(cfg["paises"]) &
        df["PRODUCT"].isin(cfg["fuentes"]) &
        (df["YEAR"] >= cfg["rango_anios"][0]) &
        (df["YEAR"] <= cfg["rango_anios"][1]) &
        (df["VALUE"] >= cfg["rango_val"][0]) &
        (df["VALUE"] <= cfg["rango_val"][1])
    ]

    if cfg["agregacion"] == "Anual":
        df_fil = (df_fil.groupby(["COUNTRY", "YEAR", "PRODUCT", "PRODUCTO_ES",
                                   "ES_RENOVABLE"])
                  .agg({"VALUE": "sum", "share": "mean", "yearToDate": "max"})
                  .reset_index())
        df_fil["MONTH"] = 6
        df_fil["MES_ES"] = "Anual"

    paleta = cfg["paleta"]
    boton_descarga(df_fil)

    if cfg["pagina"] == "🏠 Inicio":
        render_landing(df)

    else:
        st.markdown(
            "<h2 style='color:#52b788;'>📊 Panel de Análisis — Generación de Energía Global</h2>",
            unsafe_allow_html=True
        )

        if df_fil.empty:
            st.warning("⚠️ No hay datos para los filtros seleccionados. Ajusta los filtros.")
            return

        st.info(f"📋 Datos filtrados: **{len(df_fil):,}** registros · "
                f"**{df_fil['COUNTRY'].nunique()}** países · "
                f"**{df_fil['PRODUCT'].nunique()}** fuentes")

        mostrar = cfg["mostrar"]

        if mostrar["kpis"]:
            render_kpis(df_fil)
            st.markdown("---")

        if mostrar["explorer"]:
            render_explorador(df_fil, paleta)
            st.markdown("---")

        if mostrar["dist"]:
            render_distribucion(df_fil, paleta)
            st.markdown("---")

        if mostrar["corr"]:
            render_correlacion(df_fil, paleta)
            st.markdown("---")

        if mostrar["comp"]:
            render_comparacion(df_fil, paleta)
            st.markdown("---")

        if mostrar["temporal"]:
            render_temporal(df_fil, paleta)
            st.markdown("---")

        if mostrar["geo"]:
            render_geografico(df_fil, paleta)
            st.markdown("---")

        if mostrar["profundo"]:
            render_profundo(df_fil, paleta)
            st.markdown("---")

        if mostrar["avanzado"]:
            render_avanzado(df_fil, paleta)


if __name__ == "__main__":
    main()
