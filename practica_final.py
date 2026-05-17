import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Dashboard Metales - Examen Final",
    page_icon="🪙",
    layout="wide", # Aprovecha todo el ancho de la pantalla
)

# Constantes y Configuración
# ESTA API SE QUE DEBO OCULTARLA PERO SINO TE LA MUESTRO NO FUNCIONARÁ
# Solo me permite 100 llamadas al mes y ya llevo en las pruebas varias
API_KEY = st.secrets["GOLD_API_KEY"]
INTERVALO_SEGUNDOS = 3600

# Diccionario para mapear símbolos de la API con nombres legibles
METALES = {"XAU": "Oro", "XAG": "Plata", "XPT": "Platino"}


# 2. FUNCIÓN DE CARGA (ENCAPSULADA Y CON CACHÉ)
# REQUISITO: La carga de datos debe estar encapsulada en una función.
# @st.cache_data(ttl=INTERVALO_SEGUNDOS): Guardamos los datos 1 hora para no agotar las 
# 100 peticiones mensuales de la API gratuita cada vez que se mueva un botón.
@st.cache_data(ttl=INTERVALO_SEGUNDOS) 
def obtener_datos_metales(divisa):
    # Realiza peticiones HTTP a GoldAPI.
    # Usa el parámetro 'divisa' para que el dashboard sea dinámico.
    
    '''
    Resultado: Contenedor temporal. Su función es almacenar los datos ya "limpios" 
    (precios y variaciones) que iremos extrayendo de la API para cada uno de los metales (Oro, Plata y Platino)
    '''
    resultado = {}
    Headers = {"x-access-token": API_KEY, "Content-Type": "application/json"} 
    # Diccionario que define las cabeceras HTTP de la petición.
    
    try:
        # Iteramos sobre el diccionario de metales para hacer una petición por cada uno
        for simbolo, nombre in METALES.items():
            url = f"https://www.goldapi.io/api/{simbolo}/{divisa}"
            # Petición GET con timeout de 10s para evitar que la app se cuelgue
            r = requests.get(url, headers=Headers, timeout=10)
            r.raise_for_status() # Lanza excepción si hay error (404, 500, etc.)
            raw = r.json() # Se deserializa el JSON y es convierte en diccionario estructurado
            # Este objeto contiene toda la información que el servidor nos envió, incluyendo el código de estado
            
            # Limpiamos los datos extrayendo solo lo que necesitamos
            resultado[nombre] = {
                "precio": raw["price"],
                "cambio": raw.get("chp", 0), # Usar .get("chp", 0) asegura que si el dato no 
                # viene, la aplicación le asigne un 0 de forma segura y siga ejecutándose sin romperse
            }
        
        # Registramos el momento exacto de la descarga
        resultado["timestamp"] = datetime.now().strftime("%H:%M:%S")
        return resultado
    except Exception as e:
        # Manejo de errores para que la app no "explote" si falla internet o la API
        st.error(f"Fallo en la comunicación con la API: {e}")
        return None

# 3. GESTIÓN DEL ESTADO (SESSION STATE)
# REQUISITO: Histórico y persistencia de datos.
# st.session_state permite que los datos sobrevivan a la recarga del script (Rerun).
# sino se pusiera el IF cada recarga se borraría y no se acumularian los puntos
if 'historial' not in st.session_state:
    st.session_state['historial'] = [] # Si es la primera se crea, no podemos poner una lista
    # común de python por que quedaría vacía cada vez que que ejecutara el archivo
    # st.session_state es el mecanismo para persistir variables

# 4. BARRA LATERAL (INTERACTIVIDAD)
# REQUISITO: Al menos un control que no sea un dropdown básico.
# He usado Radio Buttons y un Botón de acción para la carga manual.
st.sidebar.header("Panel de Control")
st.sidebar.info("La API gratuita tiene límite de 100 peticiones al mes. Usamos caché para ahorrar créditos.")

moneda = st.sidebar.radio("Divisa de comparación:", ["EUR", "USD", "GBP"])

# REQUISITO: Automatización / Forzar actualización.
# Como el caché es de 1 hora, este botón permite al usuario saltarse el caché.
if st.sidebar.button("Actualizar Datos Ahora"):
    st.cache_data.clear() # Borra el almacenamiento temporal
    st.rerun() # Fuerza a Streamlit a volver a ejecutar todo el código
    '''
    ¿Qué pasa si pasan dos horas y le doy al botón?"
    Ocurren dos cosas: Primero, el Caché ya habrá expirado por el TTL de una hora, 
    por lo que la función disparará una nueva petición a la API para traer datos frescos. 
    Segundo, el Session State es independiente del tiempo; por lo tanto, el historial de la 
    sesión seguirá ahí y simplemente añadirá el nuevo dato al gráfico de líneas, 
    permitiendo ver la evolución entre lo que pasó hace dos horas y el momento actual.
    '''
st.sidebar.info("Pako García")
# 5. PROCESAMIENTO Y LÓGICA DE NEGOCIO
datos = obtener_datos_metales(moneda)

if datos:
    # Añadimos el nuevo punto al historial de la sesión para el gráfico de líneas
    # Esto ocurre cada vez que hay datos frescos o cambiamos la divisa
    nuevo_punto = {
        'tiempo': datos["timestamp"],
        'Oro': datos['Oro']['precio'],
        'Plata': datos['Plata']['precio'],
        'Platino': datos['Platino']['precio'],
        'Divisa': moneda
    }
    st.session_state['historial'].append(nuevo_punto)

    # --- CABECERA DEL DASHBOARD ---
    st.title("Monitor Financiero de Metales Preciosos")
    # Título del dashboard
    st.caption(f'Datos obtenidos a las: {datos["timestamp"]} | Moneda: {moneda}')
    # escribe un texto con letra pequeña, sutil y de color gris
    st.divider()

    # 6. INDICADORES (KPIs)
    # REQUISITO: Al menos dos indicadores numéricos destacados.
    # Calculamos valores dinámicos y usamos el parámetro 'delta' para mostrar tendencia.
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Oro", f"{datos['Oro']['precio']:,.2f} {moneda}", f"{datos['Oro']['cambio']:+.2f} %")
    kpi2.metric("Plata", f"{datos['Plata']['precio']:,.2f} {moneda}", f"{datos['Plata']['cambio']:+.2f} %")
    kpi3.metric("Platino", f"{datos['Platino']['precio']:,.2f} {moneda}", f"{datos['Platino']['cambio']:+.2f} %")
    st.divider()


    # 7. VISUALIZACIONES (GRÁFICOS)
    # REQUISITO: Al menos dos gráficos de tipos distintos.
    col_izq, col_der = st.columns(2)

    with col_izq:
        # GRÁFICO 1: LÍNEAS (Evolución histórica de la sesión)
        # Convierto el historial de la sesión en un DataFrame de Pandas
        df_hist = pd.DataFrame(st.session_state['historial'])
        # Filtro condicional para que si cambiamos de moneda, la gráfica no de saltos raros
        # intentando unir puntos de € con $
        df_filtrado = df_hist[df_hist['Divisa'] == moneda] 
        
        # Creamos un objeto de figura (gráfico de líneas) usando Plotly Express (px)
        fig_lineas = px.line(
            df_filtrado, # Indicamos el DataFrame que contiene los datos (ya filtrado por la divisa actual)
            x='tiempo', # Definimos qué columna irá en el eje horizontal (el tiempo capturado de la API)
            y=['Oro', 'Plata', 'Platino'], # Definimos qué columnas se graficarán en el eje vertical (las tres series de precios)
            title=f'Histórico de Sesión ({moneda})', # Establecemos un título dinámico que cambia según la moneda seleccionada (usando f-string)
            template='plotly_dark', # Aplicamos un estilo visual oscuro para que combine con la estética del dashboard
            markers=True # Activamos los marcadores (puntos) para resaltar cada toma de datos individual
        )

        # Modificamos la configuración visual de la figura para ocultar la leyenda lateral
        # Hacemos esto para ganar espacio y evitar redundancia, ya que los nombres están en los KPIs
        fig_lineas.update_layout(showlegend=False)

        # Función de Streamlit para renderizar el gráfico de Plotly en la interfaz web
        # width="stretch" asegura que el gráfico se expanda para ocupar todo el ancho de su columna
        st.plotly_chart(fig_lineas, width="stretch")

    with col_der:
        # GRÁFICO 2: BARRAS (Comparativa de precios actuales)
        nombres = ['Oro', 'Plata', 'Platino']
        precios = [datos['Oro']['precio'], datos['Plata']['precio'], datos['Platino']['precio']]
        
        fig_barras = px.bar(
            x=nombres,
            y=precios,
            color=nombres, # Colores diferenciados por metal
            color_discrete_sequence=['#FFD700', '#C0C0C0', '#E5E4E2'], # Uso códigos Hex para asegurar colores metálicos (Oro, Plata, Platino)
            title=f'Precio por Onza ({moneda})',
            template='plotly_dark',
            labels={'x': 'Metal Precioso', 'y': 'Precio'}
        )
        # Quitamos la leyenda porque el nombre ya sale en el eje X (Evitamos redundancia)
        fig_barras.update_layout(showlegend=False)
        st.plotly_chart(fig_barras, width="stretch")

else:
    # Mensaje informativo si la API no responde
    st.warning("No se han podido cargar los datos. Comprueba tu conexión o la API Key.")