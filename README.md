# 🌾 Portal DANE - AgroDecide: Modelo Predictivo y Orientación Agrícola

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-DataAnalysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scipy](https://img.shields.io/badge/SciPy-Statistics-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![Status](<https://img.shields.io/badge/Status-Desplegado-success?style=for-the-badge>)](https://republican-developers-latitude-yard.trycloudflare.com/)

Repositorio oficial del equipo **G9 DataLab Challenge (BMC)** para el desarrollo de un modelo analítico y plataforma de toma de decisiones agrícolas en Colombia.

</div>

---

## 🎯 1. Contexto y Problemática del Reto
* **Contexto:** Los pequeños y medianos productores agrícolas enfrentan graves desafíos estructurales en la comercialización y estabilidad de sus ingresos.
* **El Dolor Detectado:**
  1. 📉 **Intermediación injusta:** Márgenes de ganancia reducidos para el campesino debido a cadenas de distribución opacas.
  2. ⚠️ **Bajos ingresos e incertidumbre:** Fluctuaciones drásticas de precios desprovistas de herramientas predictivas accesibles.
  3. 🗑️ **Desperdicio de producción:** Pérdidas masivas de cosechas por falta de previsión en la demanda y estacionalidad de los mercados.

---

## 💡 2. Solución: Plataforma "AgroDecide"
Una solución analítica basada en arquitectura institucional (DANE / gov.co) orientada a transformar los datos en decisiones inteligentes:

* **AgroDecide ("Mi cosecha, mejor decisión"):** Módulo interactivo amigable donde el productor selecciona su cultivo, mes de siembra y duración del ciclo para obtener de forma automática el **mes estimado de cosecha** y el **mes históricamente más rentable para la venta**.
* **Explorador General del IPAP:** Visualización en tiempo real de índices de precios, variaciones semanales y comparativas históricas mediante gráficos interactivos de Plotly.

---

## 👥 3. Beneficiarios Directos e Indirectos
* 👨‍🌾 **Campesinos y Productores:** Mayor rentabilidad, autonomía y acceso a planificación sin barreras técnicas.
* 🤝 **Cooperativas Agropecuarias:** Eficiencia operativa y optimización de acopio.
* 🏛️ **Gobiernos y Entidades:** Herramientas estratégicas para garantizar la seguridad alimentaria basada en datos reales.

---

## 📈 4. Análisis Estadístico y Comportamiento del Mercado

Se procesaron **667 semanas de registros históricos** (Dataset IPAP y Transacciones).

### Resumen de Estadísticos Descriptivos
| Variable / Producto | Media | Mediana | Desv. Estándar | IQR (Rango Intercuartílico) | Mínimo | Máximo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **IP_agroipe (Índice Gral.)** | 132.77 | 121.00 | 44.84 | 41.40 | 83.75 | 258.69 |
| **Papa (`papam`)** | 141.46 | 116.08 | 69.73 | 80.14 | 57.30 | 356.66 |
| **Plátano (`platanom`)** | 154.76 | 132.99 | 66.26 | 56.41 | 86.53 | 426.57 |
| **Flores (`floresm`)** | 190.71 | 169.40 | 132.44 | 145.81 | 28.71 | 684.13 |
| **Maíz (`maizm`)** | 139.03 | 118.73 | 47.23 | 34.70 | 79.86 | 278.01 |
| **Arroz (`arrozm`)** | 126.90 | 118.22 | 30.18 | 27.82 | 91.38 | 219.04 |
| **Pollo (`pollom`)** | 101.83 | 94.88 | 25.37 | 21.56 | 46.29 | 194.28 |

### Hallazgos Clave de la Investigación:
* **Sesgo Positivo:** La Media supera consistentemente a la Mediana (ej. Papa: 141.46 vs 116.08), evidenciando picos inflacionarios y choques de oferta estacionales.
* **Pruebas de Normalidad (Shapiro-Wilk):** Los valores de $p < 0.05$ descartan una distribución gaussiana, justificando el uso de modelos robustos orientados a la mediana y percentiles.

---

## 🛠️ 5. Estructura del Repositorio
```text
/
├── data/
│   └── Datos_Productos_Precios_Demanda.xlsx  # Registros históricos oficiales
├── src/
│   ├── app.py                     # Aplicación Web Streamlit (AgroDecide + DANE)
│   └── analisis_estadistico.py    # Script de procesamiento y pruebas estadísticas
└── README.md                      # Documentación principal del proyecto

## 📓 Enlace al Cuaderno de Google Colab
Puedes explorar el código fuente, la validación de datos y las pruebas estadísticas ejecutadas en la nube:
* [🔗 Abrir Cuaderno de Análisis Estadístico en Google Colab](## 📓 Enlace al Cuaderno de Google Colab
Puedes explorar el código fuente, la validación de datos y las pruebas estadísticas ejecutadas en la nube:
* [🔗 Abrir Cuaderno de Análisis Estadístico en Google Colab](https://colab.research.google.com/drive/1CIwtrEcY8-I4MMXpImFEDGbIo_dqgv6c)
