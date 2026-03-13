# Análisis de Generación de Energía Global ⚡

> Este proyecto es una aplicación web interactiva desarrollada como parte del curso de **Análisis de Datos de Talento Tech**. Su objetivo es visualizar y analizar las tendencias de producción eléctrica a nivel mundial, permitiendo a los usuarios explorar la transición hacia energías limpias y comparar el rendimiento energético entre naciones.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0?logo=python&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?logo=kaggle&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)
![Author](https://img.shields.io/badge/Made%20by-María%20Alejandra%20Colorado-9B59B6?logo=github&logoColor=white)

---

## 📌 Descripción del Proyecto

La aplicación utiliza datos históricos de la **Agencia Internacional de Energía (IEA)** para realizar un **Análisis Exploratorio de Datos (EDA)** dinámico. A través de una interfaz intuitiva en Streamlit, los usuarios pueden filtrar miles de registros por país y periodo de tiempo, obteniendo visualizaciones estadísticas de alta calidad técnica con Seaborn.

---

## 📸 Vista Previa

> _Nota: Sustituir con captura de pantalla real una vez ejecutado localmente._

---

## 📑 Tabla de Contenidos

1. [Instalación](#️-instalación)
2. [Cómo Ejecutar](#-cómo-ejecutar)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Dataset](#-dataset)
5. [Visualizaciones Incluidas](#-visualizaciones-incluidas)
6. [Créditos](#-créditos)

---

## 🛠️ Instalación

**1.** Descarga el proyecto: asegúrate de tener los archivos `app.py`, `requirements.txt` y `data.csv` en una misma carpeta.

**2.** Requisito: instalación de **Python 3.10 o superior**.

**3.** Crea un entorno virtual (recomendado):
```bash
python -m venv env

# Activa el entorno:

# En Windows:
env\Scripts\activate

# En macOS/Linux:
source env/bin/activate
```

**4.** Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

---

## 🚀 Cómo Ejecutar

Desde la terminal, dentro de la carpeta del proyecto, ejecuta:
```bash
streamlit run app.py
```

---

## 📁 Estructura del Proyecto
```
.
├── app.py              # Código fuente (lógica de Streamlit, filtros y gráficos)
├── requirements.txt    # Dependencias del sistema
├── README.md           # Documentación técnica
├── data.csv            # Dataset (estadísticas de energía global)
└── imagenA.jpeg        # Elemento visual para la landing page
```

---

## 📊 Dataset

| Campo | Detalle |
|---|---|
| **Fuente** | Kaggle / Dataset de Talento Tech (IEA Electricity Statistics) |
| **Descripción** | Registros de generación eléctrica por país, mes y fuente de energía |

### Variables principales

| Variable | Descripción |
|---|---|
| `COUNTRY` | Nombre del país |
| `PRODUCT` | Fuente energética (Solar, Wind, Hydro, Nuclear, etc.) |
| `VALUE` | Generación en GWh |
| `YEAR` / `MONTH` | Temporalidad de los datos |
| `share` | Participación porcentual del producto en el total |

---

## 📈 Visualizaciones Incluidas

La aplicación implementa **6 visualizaciones avanzadas** con Seaborn:

| # | Gráfico | Descripción |
|---|---|---|
| 1 | **Distribución de Generación** | Histograma con KDE para analizar la densidad de los valores producidos |
| 2 | **Matriz de Correlación** | Mapa de calor con coeficientes de Pearson entre variables numéricas |
| 3 | **Análisis por Fuente** | Boxplots para comparar la variabilidad y detectar valores atípicos entre tipos de energía |
| 4 | **Relación Temporal** | Scatterplot que muestra la evolución de la producción a través de los años |
| 5 | **Frecuencia por Región** | Countplot de los registros disponibles por país seleccionado |
| 6 | **Tendencia Anual** | Gráfico de barras que resume la suma total de generación por año |

---

## 🎓 Créditos

**Desarrollado por:** María Alejandra Colorado  
**Curso:** Análisis de Datos · Talento Tech  
**Certificación:** Científico de Datos

---

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT).
