"""IPESA — repuestos de motor: dónde está la oportunidad para Repaglas.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú). Histórico completo por RUC
de IPESA S.A.C. (20101639275), ene.2022–jul.2026, 5 tramos anuales sin truncar
(183,499 líneas). Se excluye maquinaria completa (excavadoras, cargadoras,
tractores, niveladoras, etc.) para quedarnos solo con repuestos.
"""

import plotly.graph_objects as go
import streamlit as st

REP = "#2a78d6"
IPE = "#6b3fa0"
GOOD = "#0ca30c"
BAD = "#c0392b"

st.set_page_config(page_title="IPESA · Repuestos", page_icon="🏭", layout="wide")

st.markdown(
    """
    <style>
      .callout {
          border-left: 3px solid #9a5a1f;
          background: #f0e0c9;
          padding: 14px 18px;
          border-radius: 0 8px 8px 0;
          font-size: 14.5px;
          line-height: 1.55;
      }
      .callout-op {
          border-left: 3px solid #5a1f9a;
          background: #e7dcf5;
          padding: 14px 18px;
          border-radius: 0 8px 8px 0;
          font-size: 14.5px;
          line-height: 1.55;
      }
      .tag-rep { color: #2a78d6; font-weight: 700; }
      .tag-ipe { color: #6b3fa0; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
categorias = [
    "Filtro lubricante/carburante (8421.23)",
    "Elementos filtrantes de motor (8421.99)",
    "Filtro entrada de aire (8421.31)",
    "Partes de maquinaria 84.26/29/30",
    "Partes árbol de transmisión (levas/cigüeñal)",
    "Partes de máquinas n.e.p. (8479.90)",
    "Partes máq. cosechar/trillar (8433.90)",
    "Cuchillas agrícolas (8208.40)",
    "Filtrar/depurar líquidos (8421.29)",
    "Bombas volumétricas rotativas (8413.60)",
]
fob_categorias = [9913565, 6606861, 5889986, 5248431, 4247412, 2610505, 2541348, 2419806, 1980021, 1954009]

years = ["2022", "2023", "2024", "2025", "2026*"]
filtros_fob = [4419694, 3910145, 5660933, 6390467, 4009194]
filtros_fob_anualizado_2026 = 6900000

marcas = [("John Deere", 126339, 69331245), ("Cummins", 1901, 3270549), ("CAT", 78, 91784),
          ("Scania", 22, 69610), ("Volvo", 11, 11095), ("Case", 6, 9672), ("Deutz", 1, 8138)]

codigos = [
    ["RE504836", "Filtro aceite/combustible motor", 75, 420762, True, "OPEX JD"],
    ["RE541922", "Elemento filtrante motor", 34, 225510, True, "OPEX JD / Vapormatic"],
    ["RE522868", "Elemento filtrante motor", 43, 152497, True, "OPEX JD / Sheng Bao"],
    ["KV16429", "Filtro de aire", 57, 101454, True, "Vapormatic"],
    ["AT332908", "Elemento filtrante motor", 78, 95542, False, "—"],
    ["AT365869", "Elemento filtrante motor", 52, 81088, False, "—"],
    ["AT300487", "Elemento filtrante motor", 47, 73565, False, "—"],
    ["AT330978", "Elemento filtrante motor", 55, 73286, False, "—"],
    ["DZ118283", "Filtro aceite/combustible motor", 57, 67510, False, "—"],
    ["AT332909", "Elemento filtrante motor", 49, 54685, False, "—"],
    ["HXE11090", "Elemento filtrante motor", 40, 48454, False, "—"],
    ["AT178516", "Elemento filtrante motor", 38, 34530, False, "—"],
    ["AT472928", "Elemento filtrante motor", 33, 20457, False, "—"],
    ["AT191102", "Filtro de aire", 34, 19366, False, "—"],
    ["RE253519", "Elemento filtrante motor", 37, 15388, False, "—"],
]


def usd(n):
    return f"US$ {n:,.0f}"


def hbar_single(categories, values, color, height=None):
    height = height or (len(categories) * 42 + 30)
    fig = go.Figure()
    fig.add_bar(y=categories, x=values, orientation="h", marker_color=color)
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        xaxis_tickprefix="$", xaxis_tickformat=",.0f",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def bar_years(categories, values, color, height=280):
    fig = go.Figure()
    fig.add_bar(x=categories, y=values, marker_color=color)
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ================= HEADER =================
st.markdown("###### 🏭 INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("IPESA — repuestos de motor")
st.markdown(
    "Perfil de **IPESA S.A.C.** (RUC 20101639275) como importador de **repuestos** (excluyendo maquinaria "
    "completa: excavadoras, cargadoras, tractores, niveladoras) — con foco en la familia de **motor**, buscando "
    "dónde está la oportunidad comercial para **:blue[Repaglas]**."
)
st.caption(
    "Periodo: **enero 2022 – julio 2026**, 5 tramos anuales descargados sin truncar · Fuente: **ADEX Data Trade** "
    "sobre registros de SUNAT / Aduanas · Universo tras excluir maquinaria: **177,140 líneas · US$120.6M FOB**"
)

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("Repuestos IPESA 2022–jul.26", "US$120.6M", "excl. maquinaria completa")
k2.metric("Filtros de motor", "US$24.4M", "8421.23 + 8421.31 + 8421.99 + 8421.29")
k3.metric("FOB repuestos con marca John Deere", "57.5%", "US$69.3M de US$120.6M")
k4.metric("Crecimiento filtros 2022→2026e", "+56%", "US$4.42M → US$6.9M anualizado")

st.divider()

# ================= SECCIÓN 1: JOHN DEERE =================
st.subheader("El hallazgo de fondo: IPESA es, ante todo, un importador de repuestos John Deere")
st.write(
    "**71.3%** de las líneas de repuesto de IPESA (126,339 de 177,140) mencionan \"John Deere\" en la descripción "
    "comercial, concentrando **57.5% del FOB** (US$69.3M de US$120.6M). El resto del mercado que atiende es "
    "residual: Cummins (motores/generadores, US$3.3M), y menciones marginales de CAT, Scania, Volvo, Case y Deutz."
)
st.markdown(
    "<div class='callout-op'><b>Esto cambia el marco de la comparación.</b> IPESA no es un competidor "
    "\"adyacente\" que de vez en cuando toca tu terreno — es, en volumen, el mayor importador de repuestos John "
    "Deere del Perú, en el mismo segmento de marca donde Repaglas construyó su liderazgo con Maxiforce (74–100% "
    "de share en los 10 SKU ancla ya verificados). La escala de IPESA en repuestos JD (US$69.3M) es ~20× el FOB "
    "total histórico de Repaglas (US$3.5M) en el mismo periodo.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 2: CATEGORÍAS =================
st.subheader("Qué tipo de repuesto trae más")
st.markdown("#### Filtración de motor es, por lejos, la categoría más grande")
st.write(
    "Ordenando las partidas arancelarias de repuesto (excluyendo aceites/lubricantes, que son un consumible, no "
    "una pieza) por valor FOB acumulado 2022–jul.2026, las tres primeras posiciones son las tres familias de "
    "filtro de motor — juntas suman **US$22.4M**, más del doble que la siguiente categoría."
)
st.plotly_chart(hbar_single(categorias, fob_categorias, IPE), use_container_width=True)
st.caption(
    "Partes de árbol de transmisión (levas/cigüeñal) y partes de máquinas cosechadoras/trilladoras también son "
    "relevantes, pero a una fracción del tamaño de filtración."
)

st.divider()

# ================= SECCIÓN 3: FILTROS EN EL TIEMPO =================
st.subheader("Filtros de motor: una categoría en crecimiento sostenido")
st.write(
    "El FOB de filtros de motor que importa IPESA no es plano — creció de US$3.9M (2023, su año más bajo) a "
    "US$6.4M (2025), y 2026 va camino a superarlo (US$4.0M en solo ene–jul, ≈US$6.9M anualizado). No es una "
    "categoría de nicho ni en declive: es la línea de repuesto de mayor y más consistente crecimiento en todo el "
    "catálogo de IPESA."
)
st.plotly_chart(bar_years(years, filtros_fob, IPE, height=280), use_container_width=True)

st.divider()

# ================= SECCIÓN 4: CÓDIGOS ESPECÍFICOS =================
st.subheader("Qué códigos específicos trae más — y cuáles ya tienes en catálogo")
st.write(
    "Extrayendo los números de parte que aparecen repetidamente en la descripción comercial de los envíos de "
    "filtro, estos son los 15 más frecuentes. La columna **¿En catálogo Repaglas?** cruza cada código contra el "
    "export actual de Bsale."
)
st.dataframe(
    {
        "Código": [c[0] for c in codigos],
        "Tipo": [c[1] for c in codigos],
        "Envíos IPESA": [c[2] for c in codigos],
        "FOB acumulado": [usd(c[3]) for c in codigos],
        "¿En catálogo Repaglas?": ["✅ Sí" if c[4] else "❌ No" for c in codigos],
        "Marca en Bsale": [c[5] for c in codigos],
    },
    use_container_width=True,
    hide_index=True,
)
st.markdown(
    "<div class='callout-op'><b>4 de los 15 códigos más repetidos por IPESA ya existen en el catálogo Bsale de "
    "Repaglas</b> (RE504836, RE541922, RE522868 vía OPEX John Deere / Sheng Bao / Vapormatic, y KV16429 como "
    "VKV16429 de Vapormatic) — pero con venta prácticamente en cero (S/0–1,695 en 7 meses cada uno). No es un "
    "problema de que falte el SKU: está creado y sin vender, mientras IPESA lo trae de forma recurrente año tras "
    "año. Los otros 11 códigos (prefijo AT, DZ, HXE) no existen en el catálogo — ahí sí falta abrir el SKU, "
    "probablemente a través de los mismos proveedores (OPEX JD, Vapormatic) que ya cubren los otros cuatro.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 5: LÍMITE DEL DATO =================
st.subheader("Para qué tractores — el límite real del dato ADEX")
st.write(
    "Se intentó extraer el modelo de tractor específico (ej. 5075E, 6100M) asociado a cada filtro, pero casi "
    "ningún registro lo declara: la convención del sector es marcar la descripción comercial como **\"S/M\"** "
    "(sin modelo), porque un mismo filtro suele calzar en varias series de motor. El dato de aduanas identifica "
    "**qué código y qué marca**, pero no **qué tractor** — para eso hace falta cruzar el código OEM (ej. RE504836) "
    "contra un catálogo de aplicaciones John Deere, no contra ADEX."
)

st.divider()

# ================= SECCIÓN 6: SÍNTESIS =================
st.subheader("Dónde está la oportunidad para Repaglas")
st.markdown(
    """
1. **Filtración de motor es la brecha más grande y más clara de todo el catálogo de IPESA** — US$24.4M en 4.5
   años, creciendo, y 100% fuera del alcance actual de Repaglas (Maxiforce no fabrica filtros; OPEX JD/Vapormatic
   los tienen pero casi no se venden).
2. **El primer movimiento no requiere buscar proveedor nuevo.** RE504836, RE541922, RE522868 y KV16429 ya están
   en Bsale — el problema es de stock/precio/visibilidad, no de sourcing. Activar esos 4 SKU es la victoria más
   rápida y de menor riesgo.
3. **El segundo movimiento es ampliar catálogo dentro de los proveedores que ya tienes** (OPEX John Deere,
   Vapormatic) para cubrir los códigos AT/DZ/HXE que hoy no existen en Bsale — mismo canal de compra, sin abrir
   relación con un proveedor nuevo.
4. **IPESA es, en el fondo, un competidor de la misma familia de marca que tú** (John Deere / aftermarket), no un
   jugador de otro segmento — el hallazgo cambia la lectura: no compite contigo en maquinaria pesada donde no
   tienes nada que hacer, compite en tu terreno específico de motor, solo que en una categoría (filtros) que
   Repaglas nunca desarrolló.
"""
)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "**Metodología.** 5 exports ADEX Data Trade por RUC de IPESA (2022, 2023, 2024, 2025, 2026 por separado "
        "para evitar el límite de 80,000 filas), 183,499 líneas totales. Se excluyó maquinaria completa "
        "filtrando por partida arancelaria (tractores 87.01, palas/cargadoras/niveladoras 84.29/84.30, "
        "cosechadoras completas 84.33.5x, trituradoras 84.74, gensets 85.02, camiones 87.04/87.05). Los códigos "
        "de parte se extrajeron por patrón alfanumérico de los 5 campos de \"Descripción Comercial\" de cada DUA."
    )
with c2:
    st.markdown(
        "**Limitaciones.** El campo de marca/modelo es texto libre declarado por cada importador — no hay "
        "estandarización, así que el conteo de \"John Deere\" subestima el verdadero share si algún despachador "
        "omite la marca. El nivel de aplicación (tractor/modelo específico) no está disponible en ADEX para la "
        "mayoría de líneas de filtro. El cruce contra catálogo Bsale es por coincidencia de texto de código, no "
        "por match garantizado de especificación técnica."
    )
