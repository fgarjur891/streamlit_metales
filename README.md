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

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.9+
* **Framework del Dashboard:** Streamlit
* **Procesamiento de Datos:** Pandas
* **Visualización Dinámica:** Plotly Express
* **Conectividad HTTP:** Requests (con control de `timeout=10` pasivo)
* **Fuente de Datos de Mercado:** API REST de GoldAPI.io

---

## 📂 Estructura del Proyecto
