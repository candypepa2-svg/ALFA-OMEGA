import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Portal DANE - AgroDecide", page_icon="🌾", layout="wide")

# CSS personalizado para la estética DANE + AgroDecide
st.markdown('''
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .gov-bar { 
        background-color: #004884; 
        color: white; 
        padding: 6px 25px; 
        font-family: sans-serif; 
        font-weight: bold; 
        font-style: italic; 
        font-size: 18px; 
        width: 100%; 
    }
    .header-container { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 25px; 
        background-color: white; 
        border-bottom: 2px solid #e0e0e0; 
    }
    .logo-text { 
        color: #B3003B; 
        font-size: 36px; 
        font-weight: 800; 
        font-family: sans-serif; 
    }
    .purple-banner { 
        background: linear-gradient(120deg, #4A004A, #6a006a); 
        color: white; 
        padding: 40px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
    }
    .indicator-card { 
        background-color: white; 
        border-radius: 10px; 
        padding: 20px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.06); 
        text-align: center; 
        border-left: 5px solid #B3003B; 
        color: #333; 
    }
    .indicator-card h4 { color: #555; font-size: 14px; margin-bottom: 5px; }
    .indicator-card h2 { color: #4A004A; font-size: 26px; font-weight: bold; margin: 0; }
    
    .agro-header {
        background: linear-gradient(120deg, #1f5135, #39784d);
        color: white;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
    }
    .agro-card {
        background: #e8f2df;
        padding: 20px;
        border-radius: 14px;
        border-left: 5px solid #245b3b;
        margin-bottom: 15px;
        color: #26352b;
    }
    .agro-card h3 { color: #667568; font-size: 14px; margin: 0 0 5px 0; }
    .agro-card strong { color: #245b3b; font-size: 22px; }
    .agro-nota {
        background: #fff6dc;
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #f39c12;
        margin-top: 20px;
        font-size: 14px;
        color: #26352b;
    }
</style>

<div class="gov-bar">gov.co</div>
<div class="header-container">
    <div class="logo-text">📈 DATOS AGRO</div>
    <div style="color: #666; font-size: 14px;">
        🔍 <b>Portal Estadístico Institucional</b>
    </div>
</div>
''', unsafe_allow_html=True)

# Cargar Datos desde Excel (buscando tanto en la raíz como en data/)
@st.cache_data
def load_data():
    rutas_posibles = ['Datos_Productos_Precios_Demanda.xlsx', 'data/Datos_Productos_Precios_Demanda.xlsx']
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            try:
                df = pd.read_excel(ruta, sheet_name='Precios_y_Demanda_IPAP', header=3)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df.sort_values('Fecha')
            except Exception:
                pass
    return None

df_ipap = load_data()

# Navegación por pestañas institucionales
tab_inicio, tab_transparencia, tab_estadisticas, tab_nuestra_entidad, tab_cultura = st.tabs([
    "🏠 Inicio", 
    "📂 Transparencia y acceso", 
    "📊 Estadísticas por tema", 
    "🏢 Nuestra entidad (AgroDecide)", 
    "📚 Cultura Estadística"
])

# ==========================================
# PESTAÑA 1: INICIO
# ==========================================
with tab_inicio:
    st.markdown('<div class="purple-banner"><h2>Conozca la oferta de Datos Agropecuarios</h2><p>Aquí puede explorar y analizar los indicadores de precios interactivos basados en los registros oficiales. 🌾🚜</p></div>', unsafe_allow_html=True)
    
    if df_ipap is not None:
        ultimo_ipap = df_ipap['IP_agroipe'].iloc[-1]
        anterior_ipap = df_ipap['IP_agroipe'].iloc[-5]
        variacion = ((ultimo_ipap - anterior_ipap) / anterior_ipap) * 100
        fecha_actualizacion = df_ipap['Fecha'].iloc[-1].strftime("%d de %B de %Y")

        st.markdown("### 📌 Indicadores relevantes")
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown(f'<div class="indicator-card"><h4>📅 IPAP General Actual</h4><h2>{ultimo_ipap:.2f}</h2><p>Actualizado al {fecha_actualizacion}</p></div>', unsafe_allow_html=True)
        with col2: 
            st.markdown(f'<div class="indicator-card"><h4>📈 Variación Reciente</h4><h2>{variacion:+.2f}%</h2><p>Respecto a 4 semanas anteriores</p></div>', unsafe_allow_html=True)
        with col3: 
            st.markdown(f'<div class="indicator-card"><h4>🗃️ Volumen de Datos Históricos</h4><h2>{len(df_ipap)}</h2><p>Semanas registradas en el sistema</p></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("### 📊 Explorador General de Precios")
        
        nombres_amigables = {
            'papam': '🥔 Papa', 'arrozm': '🍚 Arroz', 'maizm': '🌽 Maíz', 
            'bovinom': '🥩 Carne Bovina', 'lechem': '🥛 Leche', 'pollom': '🍗 Pollo', 
            'huevosm': '🥚 Huevos', 'platanom': '🍌 Plátano', 'cacaom': '🍫 Cacao', 
            'bananom': '🍌 Banano', 'ofrutosm': '🍎 Otros Frutos', 'animalesm': '🐖 Otros Animales',
            'sojam': '🌿 Soya', 'floresm': '🌸 Flores'
        }
        
        columnas_raw = [col for col in df_ipap.columns if col not in ['Fecha', 'IP_agroipe']]
        columnas_display = [nombres_amigables.get(col.lower().strip(), col.capitalize()) for col in columnas_raw]
        diccionario_seleccion = dict(zip(columnas_display, columnas_raw))
        
        producto_display = st.selectbox("🛒 Seleccione un producto:", columnas_display, key="inicio_prod")
        producto_raw = diccionario_seleccion[producto_display]
        
        col_grafica, col_tabla = st.columns([2, 1])
        with col_grafica:
            fig = px.line(df_ipap, x='Fecha', y=[producto_raw, 'IP_agroipe'], 
                          title=f"Evolución Histórica de {producto_display} vs IPAP General",
                          labels={'value': 'Índice de Precio', 'variable': 'Serie'})
            st.plotly_chart(fig, use_container_width=True)
        with col_tabla:
            tabla_mostrar = df_ipap[['Fecha', producto_raw, 'IP_agroipe']].tail(15).copy()
            tabla_mostrar.rename(columns={producto_raw: producto_display}, inplace=True)
            st.dataframe(tabla_mostrar, height=350, use_container_width=True)
    else:
        st.error("⚠️ No se encontró el archivo de datos Excel. Asegúrate de tenerlo en la carpeta 'data/'.")

# ==========================================
# OTRAS PESTAÑAS INSTITUCIONALES
# ==========================================
with tab_transparencia:
    st.markdown("### 📂 Transparencia y Acceso a la Información Pública")
    st.info("Consulte la metodología oficial de recolección de precios agropecuarios de la Bolsa Mercantil de Colombia y el DANE.")

with tab_estadisticas:
    st.markdown("### 📊 Estadísticas Sectoriales Agropecuarias")
    st.write("Información desagregada por grupos de insumos, origen regional y volumen transado.")

with tab_cultura:
    st.markdown("### 📚 Cultura Estadística para el Campo")
    st.write("Recursos educativos, boletines interactivos y diccionarios de conceptos agropecuarios para productores.")

# ==========================================
# PESTAÑA 4: NUESTRA ENTIDAD -> AGRODECIDE
# ==========================================
with tab_nuestra_entidad:
    st.markdown('''
    <div class="agro-header">
        <h1 style="margin:0; font-size:32px;">🌱 AgroDecide</h1>
        <p style="font-size:18px; margin:5px 0 0 0;">Mi cosecha, mejor decisión.</p>
        <p style="font-size:14px; opacity:0.9; margin-top:5px;">Información sencilla para sembrar y comercializar mejor tus productos en Colombia[cite: 2].</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 🌾 Cuéntanos sobre tu cultivo")
        st.caption("No necesitas conocimientos técnicos. Solo responde estas preguntas.")
        
        productos_agro = {
            'Papa': 'papam', 'Plátano': 'platanom', 'Maíz': 'maizm', 
            'Arroz': 'arrozm', 'Cacao': 'cacaom', 'Banano': 'bananom', 
            'Soya': 'sojam', 'Huevos': 'huevosm', 'Leche': 'lechem', 'Ganado bovino': 'bovinom'
        }
        
        producto_sel = st.selectbox("¿Qué producto quieres sembrar?", list(productos_agro.keys()))
        
        nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        mes_sel_idx = st.selectbox("¿En qué mes vas a sembrar?", range(12), format_func=lambda x: nombres_meses[x])
        
        duracion_opciones = {
            60: "2 meses", 90: "3 meses", 120: "4 meses", 150: "5 meses", 
            180: "6 meses", 240: "8 meses", 300: "10 meses", 365: "1 año"
        }
        
        duracion_dias = st.selectbox("¿Cuánto tarda tu cultivo en estar listo?", list(duracion_opciones.keys()), 
                                   index=2, format_func=lambda x: duracion_opciones[x])
        
        departamento = st.text_input("¿En qué departamento produces?", value="Boyacá")
        st.button("🌿 Consultar mi cosecha", type="primary", use_container_width=True)

    with col_output:
        st.markdown("### 📊 Orientación Agrícola")
        
        meses_duracion = int(np.ceil(duracion_dias / 30.44))
        mes_cosecha_idx = (mes_sel_idx + meses_duracion) % 12
        mes_cosecha_nombre = nombres_meses[mes_cosecha_idx]
        
        col_excel = productos_agro[producto_sel]
        
        if df_ipap is not None and col_excel in df_ipap.columns:
            df_temp = df_ipap.copy()
            df_temp['Mes_Num'] = df_temp['Fecha'].dt.month - 1
            promedios_mes = df_temp.groupby('Mes_Num')[col_excel].mean()
            valores_mensuales = [promedios_mes.get(i, 100.0) for i in range(12)]
        else:
            valores_mensuales = [100, 105, 110, 108, 115, 120, 118, 112, 105, 110, 115, 120]
        
        mejor_mes_idx = int(np.argmax(valores_mensuales))
        mejor_mes_nombre = nombres_meses[mejor_mes_idx]
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'''
            <div class="agro-card">
                <h3>🌱 Mes estimado de cosecha</h3>
                <strong>{mes_cosecha_nombre}</strong>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="agro-card">
                <h3>🌾 Producto seleccionado</h3>
                <strong>{producto_sel}</strong>
            </div>
            ''', unsafe_allow_html=True)
        
        with c2:
            st.markdown(f'''
            <div class="agro-card">
                <h3>🧺 Mes recomendado para venta</h3>
                <strong>{mejor_mes_nombre}</strong>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="agro-card">
                <h3>📍 Departamento</h3>
                <strong>{departamento if departamento else "No especificado"}</strong>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Comportamiento histórico mensual de precios")
    
    fig_agro = go.Figure()
    fig_agro.add_trace(go.Scatter(
        x=nombres_meses, 
        y=valores_mensuales,
        mode='lines+markers',
        line=dict(color='#39784d', width=4),
        marker=dict(size=10, color='#245b3b')
    ))
    
    fig_agro.update_layout(
        title=f"Promedio de Precios Históricos para {producto_sel} por Mes",
        xaxis_title="Mes del Año",
        yaxis_title="Índice Promedio de Precio",
        template="plotly_white",
        height=320
    )
    
    st.plotly_chart(fig_agro, use_container_width=True)
    
    st.markdown('''
    <div class="agro-nota">
        💡 <b>Consejo para el campesino:</b><br>
        Antes de sembrar o vender, compara esta orientación con los precios de tu plaza de mercado local, 
        los costos de producción y las condiciones climáticas actuales de tu región.
    </div>
    ''', unsafe_allow_html=True)
