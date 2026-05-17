# 📊 Dashboard Real-Time de Analítica de Metales Preciosos

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](https://appmetaleshoy.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-darkblue.svg)](https://pandas.pydata.org/)
[![Plotly Express](https://img.shields.io/badge/Plotly-Express-purple.svg)](https://plotly.com/)

Un dashboard analítico robusto, escalable y de alto rendimiento diseñado con **Streamlit** para la monitorización en tiempo real y el análisis histórico de la cotización de metales preciosos (**Oro, Plata, Platino y Paladio**) consumiendo la API global de **GoldAPI.io**.

---

## 🚀 Características Principales

* **KPIs Financieros Automatizados:** Despliegue dinámico de precios actuales con cálculo automático de deltas porcentuales (variación de las últimas 24h), codificados por color nativo (verde para alzas, rojo para bajas) mediante `st.metric`.
* **Gestión Eficiente de Memoria (TTL Caching):** Implementación de caché de datos mediante el decorador `@st.cache_data(ttl=3600)`, optimizando la cuota de peticiones HTTP de la API y acelerando la velocidad de carga global compartida.
* **Persistencia de Datos por Sesión (`st.session_state`):** Historial dinámico en tiempo de ejecución que acumula las consultas temporales de forma aislada y estanca por usuario (multi-usuario nativo).
* **Filtrado Inteligente de Datos (Pandas):** Prevención de anomalías y saltos de escala en gráficos a través de máscaras booleanas que separan estrictamente el histórico de divisas (EUR vs. USD).
* **Diseño Web Fluido (Wide UX):** Maquetación responsive basada en `layout="wide"` con cuadrículas de doble columna analítica (`st.columns`), maximizando el espacio de visualización de gráficos interactivos de **Plotly Express**.
* **Arquitectura Tolerante a Fallos:** Control exhaustivo de excepciones mediante bloques `try-except` y mitigación de caídas mediante el método seguro `.get()` en diccionarios para evitar errores de tipo `KeyError`.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.9+
* **Framework del Dashboard:** Streamlit
* **Procesamiento de Datos:** Pandas
* **Visualización Dinámica:** Plotly Express
* **Conectividad HTTP:** Requests (con control de `timeout=10` pasivo)
* **Fuente de Datos de Mercado:** API REST de GoldAPI.io

---

## 📂 Estructura del Proyecto

```bash
├── .streamlit/
│   └── secrets.toml          # Gestión segura de credenciales locales (API Key)
├── app.py                    # Script principal de la aplicación Streamlit
├── requirements.txt          # Dependencias de producción del proyecto
└── README.md                 # Documentación técnica del repositorio
```

### Parte 3: Guía de Instalación y Comando de Ejecución

## ⚙️ Instalación y Configuración Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/dashboard-metales-preciosos.git](https://github.com/tu-usuario/dashboard-metales-preciosos.git)
cd dashboard-metales-preciosos
```

### Entorno

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Parte 4: Arquitectura y Cierre del Documento

## 🧠 Aspectos de Diseño de Código Destacados

### Robustez en la Consulta de Diccionarios (Evitando KeyErrors)
```python
# Uso estratégico de .get con fallback por defecto
"cambio": raw.get("chp", 0)

