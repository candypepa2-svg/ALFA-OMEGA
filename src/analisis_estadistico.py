import os
import time
import pandas as pd
import numpy as np
from scipy import stats
from google.colab import files

# 1. Verificar y cargar el archivo Excel
nombre_archivo = 'Datos_Productos_Precios_Demanda.xlsx'
if not os.path.exists(nombre_archivo):
    print(f"⚠️ Falta el archivo '{nombre_archivo}'. Súbelo usando el botón de carga:")
    subidos = files.upload()
    for fn in subidos.keys():
        if fn != nombre_archivo:
            os.rename(fn, nombre_archivo)

print("✅ Archivo de datos verificado correctamente.")

# 2. Análisis Estadístico y Pruebas de Normalidad
df_prices = pd.read_excel(nombre_archivo, sheet_name='Precios_y_Demanda_IPAP', skiprows=3)
df_prices.columns = [
    'Fecha', 'IP_agroipe', 'bovinom', 'lechem', 'pollom', 'huevosm',
    'maizm', 'platanom', 'arrozm', 'papam', 'ofrutosm', 'animalesm',
    'sojam', 'cacaom', 'floresm', 'bananom'
]

df_prices['Fecha'] = pd.to_datetime(df_prices['Fecha'])
prices_numeric = df_prices.drop(columns=['Fecha'])

resultados = []
for col in prices_numeric.columns:
    data = prices_numeric[col].dropna()
    resultados.append({
        'Variable / Producto': col,
        'Media': round(data.mean(), 2),
        'Mediana': round(data.median(), 2),
        'Desv. Estándar': round(data.std(), 2),
        'IQR': round(stats.iqr(data), 2),
        'Mínimo': round(data.min(), 2),
        'Máximo': round(data.max(), 2),
        'P-value (Shapiro)': f"{stats.shapiro(data.sample(min(len(data), 5000), random_state=42)).pvalue:.5e}"
    })

df_resultados = pd.DataFrame(resultados)
print("\n=========================================================================")
print("             RESUMEN ESTADÍSTICO Y PRUEBAS DE NORMALIDAD                ")
print("=========================================================================")
print(df_resultados.to_string(index=False))
print("\n" + "="*73 + "\n")

# 3. Crear el código de la aplicación web (app.py)
app_code = """
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Portal DANE - AgroDecide", page_icon="🌾", layout="wide")

st.markdown('''
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .gov-bar { background-color: #004884; color: white; padding: 6px 25px; font-family: sans-serif; font-weight: bold; font-style: italic; font-size: 18px; width: 100%; }
    .header-container { display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; background-color: white; border-bottom: 2px solid #e0e0e0; }
    .logo-text { color: #B3003B; font-size: 36px; font-weight: 800; font-family: sans-serif; }
    .purple-banner { background: linear-gradient(120deg, #4A004A, #6a006a); color: white; padding: 40px; border-radius: 12px; margin-bottom: 25px; }
    .indicator-card { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); text-align: center; border-left: 5px solid #B3003B; color: #333; }
    .indicator-card h4 { color: #555; font-size: 14px; margin-bottom: 5px; }
    .indicator-card h2 { color: #4A004A; font-size: 26px; font-weight: bold; margin: 0; }
    .agro-header { background: linear-gradient(120deg, #1f5135, #39784d); color: white; padding: 30px; border-radius: 16px; margin-bottom: 25px; }
    .agro-card { background: #e8f2df; padding: 20px; border-radius: 14px; border-left: 5px solid #245b3b; margin-bottom: 15px; color: #26352b; }
    .agro-card h3 { color: #667568; font-size: 14px; margin: 0 0 5px 0; }
    .agro-card strong { color: #245b3b; font-size: 22px; }
    .agro-nota { background: #fff6dc; padding: 18px; border-radius: 10px; border-left: 4px solid #f39c12; margin-top: 20px; font-size: 14px; color: #26352b; }
</style>
<div class="gov-bar">gov.co</div>
<div class="header-container"><div class="logo-text">📈 DATOS AGRO</div><div style="color: #666; font-size: 14px;">🔍 <b>Portal Estadístico Institucional</b></div></div>
''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not os.path.exists('Datos_Productos_Precios_Demanda.xlsx'): return None
    try:
        df = pd.read_excel('Datos_Productos_Precios_Demanda.xlsx', sheet_name='Precios_y_Demanda_IPAP', header=3)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df.sort_values('Fecha')
    except:
        return None

df_ipap = load_data()

tab_inicio, tab_transparencia, tab_estadisticas, tab_nuestra_entidad, tab_cultura = st.tabs([
    "🏠 Inicio", "📂 Transparencia y acceso", "📊 Estadísticas por tema", "🏢 Nuestra entidad (AgroDecide)", "📚 Cultura Estadística"
])

with tab_inicio:
    st.markdown('<div class="purple-banner"><h2>Conozca la oferta de Datos Agropecuarios</h2><p>Aquí puede explorar y analizar los indicadores de precios interactivos basados en los registros oficiales. 🌾🚜</p></div>', unsafe_allow_html=True)
    if df_ipap is not None:
        ultimo_ipap = df_ipap['IP_agroipe'].iloc[-1]
        anterior_ipap = df_ipap['IP_agroipe'].iloc[-5]
        variacion = ((ultimo_ipap - anterior_ipap) / anterior_ipap) * 100
        fecha_act = df_ipap['Fecha'].iloc[-1].strftime("%d de %B de %Y")

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="indicator-card"><h4>📅 IPAP Actual</h4><h2>{ultimo_ipap:.2f}</h2><p>Al {fecha_act}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="indicator-card"><h4>📈 Variación Reciente</h4><h2>{variacion:+.2f}%</h2><p>Respecto a 4 semanas</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="indicator-card"><h4>🗃️ Registros Totales</h4><h2>{len(df_ipap)}</h2><p>Semanas analizadas</p></div>', unsafe_allow_html=True)
        st.write("---")

        nombres_amigables = {
            'papam': '🥔 Papa', 'arrozm': '🍚 Arroz', 'maizm': '🌽 Maíz', 'bovinom': '🥩 Carne Bovina',
            'lechem': '🥛 Leche', 'pollom': '🍗 Pollo', 'huevosm': '🥚 Huevos', 'platanom': '🍌 Plátano',
            'cacaom': '🍫 Cacao', 'bananom': '🍌 Banano', 'ofrutosm': '🍎 Otros Frutos', 'animalesm': '🐖 Otros Animales',
            'sojam': '🌿 Soya', 'floresm': '🌸 Flores'
        }
        cols_raw = [c for c in df_ipap.columns if c not in ['Fecha', 'IP_agroipe']]
        cols_disp = [nombres_amigables.get(c.lower().strip(), c.capitalize()) for c in cols_raw]
        mapa_cols = dict(zip(cols_disp, cols_raw))

        prod_disp = st.selectbox("🛒 Seleccione un producto:", cols_disp)
        prod_raw = mapa_cols[prod_disp]

        cg, ct = st.columns([2, 1])
        with cg:
            fig = px.line(df_ipap, x='Fecha', y=[prod_raw, 'IP_agroipe'], title=f"Evolución: {prod_disp} vs IPAP General")
            st.plotly_chart(fig, use_container_width=True)
        with ct:
            st.dataframe(df_ipap[['Fecha', prod_raw, 'IP_agroipe']].tail(15).rename(columns={prod_raw: prod_disp}), height=350, use_container_width=True)

with tab_transparencia: st.info("Consulte la metodología oficial de recolección de precios agropecuarios.")
with tab_estadisticas: st.info("Información desagregada por grupos de insumos y regiones.")
with tab_cultura: st.info("Recursos educativos y diccionarios agropecuarios.")

with tab_nuestra_entidad:
    st.markdown('<div class="agro-header"><h1 style="margin:0; font-size:32px;">🌱 AgroDecide</h1><p style="font-size:18px; margin:5px 0 0 0;">Mi cosecha, mejor decisión.</p></div>', unsafe_allow_html=True)
    ci, co = st.columns([1, 1.2])
    with ci:
        productos_agro = {'Papa': 'papam', 'Plátano': 'platanom', 'Maíz': 'maizm', 'Arroz': 'arrozm', 'Cacao': 'cacaom', 'Banano': 'bananom', 'Soya': 'sojam', 'Huevos': 'huevosm', 'Leche': 'lechem', 'Ganado bovino': 'bovinom'}
        prod_sel = st.selectbox("¿Qué producto quieres sembrar?", list(productos_agro.keys()))
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_idx = st.selectbox("¿En qué mes vas a sembrar?", range(12), format_func=lambda x: meses[x])
        dura_dict = {60: "2 meses", 90: "3 meses", 120: "4 meses", 150: "5 meses", 180: "6 meses", 240: "8 meses", 300: "10 meses", 365: "1 año"}
        dias = st.selectbox("¿Cuánto tarda tu cultivo?", list(dura_dict.keys()), index=2, format_func=lambda x: dura_dict[x])
        depto = st.text_input("¿En qué departamento produces?", value="Boyacá")
        st.button("🌿 Consultar mi cosecha", type="primary", use_container_width=True)

    with co:
        st.markdown("### 📊 Orientación Agrícola")
        meses_dur = int(np.ceil(dias / 30.44))
        mes_cosecha = meses[(mes_idx + meses_dur) % 12]
        col_exc = productos_agro[prod_sel]

        if df_ipap is not None and col_exc in df_ipap.columns:
            df_t = df_ipap.copy()
            df_t['Mes'] = df_t['Fecha'].dt.month - 1
            p_mes = df_t.groupby('Mes')[col_exc].mean()
            val_m = [p_mes.get(i, 100.0) for i in range(12)]
        else:
            val_m = [100]*12

        mejor_mes = meses[int(np.argmax(val_m))]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agro-card"><h3>🌱 Mes estimado de cosecha</h3><strong>{mes_cosecha}</strong></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="agro-card"><h3>🌾 Producto seleccionado</h3><strong>{prod_sel}</strong></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agro-card"><h3>🧺 Mes recomendado para venta</h3><strong>{mejor_mes}</strong></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="agro-card"><h3>📍 Departamento</h3><strong>{depto}</strong></div>', unsafe_allow_html=True)

        fig_ag = go.Figure(go.Scatter(x=meses, y=val_m, mode='lines+markers', line=dict(color='#39784d', width=4)))
        fig_ag.update_layout(title=f"Comportamiento Histórico para {prod_sel}", xaxis_title="Mes", yaxis_title="Precio Promedio", template="plotly_white", height=280)
        st.plotly_chart(fig_ag, use_container_width=True)
        st.markdown('<div class="agro-nota">💡 <b>Consejo:</b> Compara esta orientación con los precios locales de tu plaza de mercado y las condiciones climáticas.</div>', unsafe_allow_html=True)
"""

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# 4. Configurar servidor, dependencias y túnel de Cloudflare
print("\n⚙️ Instalando librerías y configurando servidor web...")
get_ipython().system_raw("pip install streamlit openpyxl plotly scipy pandas numpy -q")
get_ipython().system_raw("pkill -9 -f streamlit")
get_ipython().system_raw("pkill -9 -f cloudflared")

if not os.path.exists('cloudflared-linux-amd64'):
    get_ipython().system_raw("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64")
    get_ipython().system_raw("chmod +x cloudflared-linux-amd64")

print("⚡ Iniciando Streamlit...")
get_ipython().system_raw("streamlit run app.py --server.port=8501 &")
time.sleep(5)

if os.path.exists("tunnel.log"): os.remove("tunnel.log")
get_ipython().system_raw("./cloudflared-linux-amd64 tunnel --url http://127.0.0.1:8501 &> tunnel.log &")
time.sleep(6)

print("\n" + "="*65)
print("✨ ¡TODO LISTO! HAZ CLIC EN EL ENLACE AZUL PARA VER TU PÁGINA: ✨")
print("="*65)
!grep -o 'https://.*\.trycloudflare.com' tunnel.log
