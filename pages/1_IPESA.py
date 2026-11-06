"""IPESA — repuestos de motor: dónde está la oportunidad para Repaglas.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú). Histórico completo por RUC
de IPESA S.A.C. (20101639275), ene.2022–set.2026, tramos anuales sin truncar (ene.2022–jul.2026)
+ agosto–setiembre 2026 (11,655 líneas, descarga 2026-11-06; reemplaza al agosto del 2026-10-02, que
ADEX corrigió). Se excluyen máquinas y equipos completos con el perímetro común a las 3 empresas
(ver sección "Crecimiento comparado"). Recalculado completo 2026-11-06.
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
    "Partes de maquinaria 84.26/29/30 (8431.49)",
    "Partes árbol de transmisión (8483.90)",
    "Partes de motor diésel (8409.99)",
    "Partes de máquinas n.e.p. (8479.90)",
    "Partes máq. cosechar/trillar (8433.90)",
    "Cuchillas agrícolas (8208.40)",
    "Partes de transmisiones cardánicas (8708.99)",
]
fob_categorias = [10727164, 7315781, 6491271, 5634409, 5115199, 2803602, 2732646, 2680683, 2543276, 2477715]

years = ["2022", "2023", "2024", "2025", "2026*"]
filtros_fob = [4476250, 3956153, 5699546, 6470242, 6149843]
filtros_fob_anualizado_2026 = 8199791

marcas = [("John Deere", 133866, 70275268), ("Cummins", 2070, 3609081), ("Wirtgen", 2565, 3205007),
          ("CAT", 29, 66965), ("Scania", 22, 69610), ("Volvo", 13, 17381), ("Case", 7, 12252)]

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


def pct_codigo_chart(years_, ipesa_pct, repaglas_pct, height=320):
    fig = go.Figure()
    fig.add_bar(name="IPESA", x=years_, y=ipesa_pct, marker_color=IPE)
    fig.add_bar(name="Repaglas", x=years_, y=repaglas_pct, marker_color=REP)
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10), barmode="group",
        yaxis_ticksuffix="%", yaxis_range=[0, 100],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
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
    "Periodo: **enero 2022 – setiembre 2026**, tramos anuales descargados sin truncar + agosto–setiembre 2026 · Fuente: "
    "**ADEX Data Trade** sobre registros de SUNAT / Aduanas · Universo tras excluir máquinas y equipos completos: "
    "**188,537 líneas · US$123.4M FOB**"
)

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("Repuestos IPESA 2022–set.26", "US$123.4M", "excl. máquinas y equipos completos")
k2.metric("Filtros de motor", "US$26.8M", "8421.23 + 8421.31 + 8421.99 + 8421.29")
k3.metric("FOB repuestos con marca John Deere", "57.0%", "US$70.3M de US$123.4M")
k4.metric("Crecimiento filtros 2022→2026e", "+83%", "US$4.48M → US$8.2M anualizado")

st.divider()

# ================= CRECIMIENTO COMPARADO (12 MESES MÓVILES) =================
# Mismo perímetro para las 3 empresas: repuestos = todo menos máquinas/equipos completos (8701, 8429,
# 8430, 8474, 8502, 8704, 8705, 8716, 8427, 8426, 8408 motores completos, 8479.10 pavimentadoras/
# fresadoras, 8428.33, 8432/8433/8436 salvo sus partidas de "partes", 9015/9023/9024/8526 instrumentos).
# "Canasta Repaglas" = las 10 partidas de 4 dígitos que suman el 95.5% del FOB de Repaglas 2022–ago.2026:
# 8409, 8413, 8483, 8484, 8708, 8487, 8481, 8421, 4016, 8482. Fuente: reportes ADEX por RUC + ago–set 2026
# (descarga 2026-11-06). Recalculado 2026-11-06 con ventanas oct–sep (antes sep–ago).
ventanas = ["oct22–sep23", "oct23–sep24", "oct24–sep25", "oct25–sep26"]
crec = {
    "Total repuestos (sin máquinas completas)": {
        "Repaglas": [760288, 887462, 800172, 765640],
        "Dinámica": [1780089, 1689784, 2005246, 1837725],
        "IPESA": [19350624, 22491727, 28399739, 33758516],
    },
    "Canasta Repaglas (mismas 10 partidas)": {
        "Repaglas": [726604, 846493, 761360, 740640],
        "Dinámica": [1516246, 1376871, 1613224, 1669140],
        "IPESA": [9794290, 11729941, 14340298, 18679310],
    },
    "Canasta Repaglas sin filtros": {
        "Repaglas": [702592, 830168, 747423, 733983],
        "Dinámica": [1423289, 1286833, 1533871, 1588539],
        "IPESA": [6527050, 6267178, 7904272, 10611002],
    },
    "Filtros de motor": {
        "Repaglas": [24012, 16325, 13937, 6657],
        "Dinámica": [92957, 90038, 79353, 80601],
        "IPESA": [3267240, 5462763, 6436026, 8068308],
    },
}
duas_12m = {"Repaglas": [21, 26, 21, 27], "Dinámica": [68, 59, 73, 73], "IPESA": [1079, 960, 1148, 1263]}
colores = {"Repaglas": REP, "Dinámica": "#eb6834", "IPESA": IPE}


def fmt_money(v):
    return f"US$ {v / 1e6:.2f}M" if v >= 1e6 else f"US$ {v / 1000:,.0f}K"


def crec_chart(datos):
    fig = go.Figure()
    for emp, vals in datos.items():
        idx = [v / vals[0] * 100 for v in vals]
        fig.add_scatter(
            x=ventanas, y=idx, mode="lines+markers+text", name=emp,
            line=dict(color=colores[emp], width=2.5), marker=dict(size=9, color=colores[emp]),
            text=[""] * 3 + [f"{emp} {idx[-1]:.0f}"], textposition="middle right",
            textfont=dict(color="#3d3a33", size=12.5), cliponaxis=False,
            customdata=[fmt_money(v) for v in vals],
            hovertemplate=f"<b>{emp}</b>: índice %{{y:.0f}} · %{{customdata}}<extra></extra>",
        )
    fig.add_hline(y=100, line=dict(color="#948a76", width=1, dash="dot"))
    fig.update_layout(
        height=360, margin=dict(l=10, r=120, t=10, b=10), hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis=dict(title="Índice (oct22–sep23 = 100)", gridcolor="#e8e2d6"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


st.subheader("Crecimiento comparado: IPESA vs. Repaglas vs. Dinámica, últimos 12 meses")
st.write(
    "Comparación **papas con papas**: las tres empresas medidas con el mismo perímetro (solo repuestos, sin "
    "máquinas ni equipos completos), en los mismos periodos de **12 meses móviles cerrando en setiembre** — que "
    "neutralizan la distinta frecuencia de pedido de cada una — y en **índice (oct22–sep23 = 100)**, porque "
    "IPESA es ~40× más grande que Repaglas y en US$ no se vería a las tres en un mismo gráfico."
)
alcance = st.radio("Qué comparar", list(crec.keys()), index=1, horizontal=True, label_visibility="collapsed")
datos = crec[alcance]

g1, g2 = st.columns([3, 2])
with g1:
    st.plotly_chart(crec_chart(datos), use_container_width=True)
with g2:
    st.markdown("**Últimos 12 meses (oct25–sep26) vs. 12 meses anteriores**")
    for emp, vals in datos.items():
        st.metric(emp, fmt_money(vals[3]), f"{(vals[3] / vals[2] - 1) * 100:+.1f}% vs. oct24–sep25")

st.dataframe(
    {
        "Empresa": list(datos.keys()),
        **{v: [fmt_money(vals[i]) for vals in datos.values()] for i, v in enumerate(ventanas)},
        "Var. último año": [f"{(vals[3] / vals[2] - 1) * 100:+.1f}%" for vals in datos.values()],
        "DUAs (últ. 12m vs. ant.)": [f"{duas_12m[e][3]:,} vs {duas_12m[e][2]:,}" for e in datos],
    },
    use_container_width=True,
    hide_index=True,
)
st.markdown(
    "<div class='callout-op'><b>Lectura — IPESA crece ~30% en las partidas de Repaglas mientras Repaglas baja y "
    "Dinámica está casi plana.</b> En los últimos 12 meses (oct25–sep26) IPESA creció <b>+19%</b> en repuestos y "
    "<b>+30% en la misma canasta de partidas que trae Repaglas</b> (Repaglas −2.7%, Dinámica +3.5%). No es solo "
    "filtros (+25%): sacando filtros, IPESA crece <b>+34%</b> en el núcleo motor/transmisión, con 8409 partes de "
    "motor duplicándose (US$0.50M → US$1.08M). Ese crecimiento <b>no viene de repuestos declarados John Deere</b> "
    "(planos: US$5.06M → US$5.10M en la canasta sin filtros), sino de <b>Cummins</b> (US$0.29M → US$1.79M), "
    "repuestos del grupo Wirtgen (US$0.32M → US$0.74M) y otras marcas. IPESA está ensanchando catálogo dentro de "
    "las mismas partidas arancelarias de Repaglas, pero hacia marcas donde Repaglas no está. (Con la ventana "
    "sep–ago el total daba +29%; el +19% actual es menor porque el año anterior incluye octubre 2024, un mes "
    "muy alto de IPESA.)</div>",
    unsafe_allow_html=True,
)
st.caption(
    "Perímetro común: se excluyen máquinas y equipos completos (tractores, maquinaria vial, pavimentadoras/fresadoras "
    "8479.10, cisternas 8716, motores completos 8408, implementos agrícolas completos, instrumentos) — el mismo que "
    "usa toda esta hoja. "
    "Ojo con Dinámica: −8.4% en total repuestos pero +3.5% en la canasta Repaglas — toda su caída está fuera de "
    "las partidas de Repaglas (US$392K → US$169K, −57%); en lo que compite con Repaglas está estable o sube "
    "levemente."
)

st.divider()

# ================= AVISO: IPESA DEJÓ DE DECLARAR CÓDIGOS =================
st.subheader("⚠️ Aviso: desde 2024, IPESA casi dejó de declarar el código de parte en Aduanas")
st.write(
    "Cualquier análisis de este dashboard que busca **códigos de parte específicos** (OEM/John Deere) dentro de "
    "las importaciones de IPESA — incluyendo el cruce contra el catálogo Maxiforce — depende de que IPESA escriba "
    "ese código en la Descripción Comercial de su declaración de Aduanas. **Eso dejó de pasar de forma masiva a "
    "partir de 2024.**"
)

anios_codigo = ["2022", "2023", "2024", "2025", "2026"]
# 2026 ajustado el 2026-11-06 sumando setiembre (IPESA: ~32 de 4,223 líneas JD con código; Repaglas: 5 de 7)
# sobre la base ene–ago; el patrón exacto de 2022–2025 no se volvió a correr.
ipesa_pct_codigo = [86.6, 87.3, 19.7, 9.1, 3.0]
repaglas_pct_codigo = [84.0, 83.9, 78.3, 84.5, 83.3]

cc1, cc2 = st.columns([3, 2])
with cc1:
    st.plotly_chart(
        pct_codigo_chart(anios_codigo, ipesa_pct_codigo, repaglas_pct_codigo),
        use_container_width=True,
    )
    st.caption(
        "% de líneas de importación que mencionan \"John Deere\" y además traen un código de parte identificable "
        "(patrón alfanumérico tipo RE12345, R123456, DZ111138, etc.) en alguno de los 5 campos de Descripción "
        "Comercial, por año, 2022–set.2026 (2026 parcial, solo hasta setiembre; en agosto 2026 IPESA no declaró "
        "código en ninguna de sus líneas John Deere, y en setiembre en menos de 1%)."
    )
with cc2:
    st.metric("IPESA con código, 2022", "86.6%")
    st.metric("IPESA con código, 2026", "3.0%", "-83.6 pp", delta_color="inverse")
    st.metric("Repaglas con código, 2022→2026", "84.0% → 83.3%", "sin caída")

st.markdown(
    "<div class='callout'><b>No es un cambio de formato de ADEX — es un comportamiento específico de IPESA.</b> "
    "Se comparó contra el historial propio de Repaglas en el mismo periodo: Repaglas mantiene entre 78% y 85% de "
    "sus líneas con código de parte identificable <b>todos los años, sin caída</b>. Si el cambio fuera de ADEX o "
    "de SUNAT, afectaría a ambas empresas por igual. Como solo le pasa a IPESA, y justo a partir de 2024, la "
    "lectura más razonable es que es deliberado: una forma común de que un importador dificulte que la "
    "competencia (como Repaglas, mirando estos mismos reportes) reconstruya su lista de partes desde Aduanas. "
    "Antes del cambio, una línea típica decía <code>ARANDELA DE EMPUJE, JOHN DEERE, S/M | RE527834</code>; ahora "
    "dice <code>ARANDELA DE EMPUJE, JOHN DEERE, S/M | DIFERIDO A 49 DIAS FACTURA</code> — mismo repuesto, mismo "
    "formato, pero donde antes iba el código ahora va la condición de pago.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='callout-op'><b>Consecuencia práctica.</b> Todo hallazgo de este dashboard basado en \"qué código "
    "específico importa IPESA\" (los 15 códigos de filtro de más abajo, y el cruce completo contra el catálogo "
    "Maxiforce) está sesgado hacia evidencia de <b>2022-2023</b> — no porque IPESA haya dejado de traer esas "
    "piezas, sino porque desde 2024 ya no es visible en ADEX qué código trae. La oportunidad real hoy es, con "
    "toda probabilidad, <b>mayor</b> a lo que estos números muestran: son un piso confirmado, no el techo. Para "
    "ver qué trae IPESA hoy código por código haría falta otra fuente — ADEX ya no alcanza para eso.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 1: JOHN DEERE =================
st.subheader("El hallazgo de fondo: IPESA es, ante todo, un importador de repuestos John Deere")
st.write(
    "**71.0%** de las líneas de repuesto de IPESA (133,866 de 188,537) mencionan \"John Deere\" en la descripción "
    "comercial, concentrando **57.0% del FOB** (US$70.3M de US$123.4M). El resto del mercado que atiende es "
    "residual: Cummins (motores/generadores, US$3.6M), repuestos de maquinaria vial Wirtgen (US$3.2M), y menciones marginales de CAT, Scania, Volvo y Case."
)
st.markdown(
    "<div class='callout-op'><b>Esto cambia el marco de la comparación.</b> IPESA no es un competidor "
    "\"adyacente\" que de vez en cuando toca tu terreno — es, en volumen, el mayor importador de repuestos John "
    "Deere del Perú, en el mismo segmento de marca donde Repaglas construyó su liderazgo con Maxiforce (74–100% "
    "de share en los 10 SKU ancla ya verificados). La escala de IPESA en repuestos JD (US$70.3M) es ~19× el FOB "
    "total histórico de Repaglas (US$3.7M) en el mismo periodo.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 2: CATEGORÍAS =================
st.subheader("Qué tipo de repuesto trae más")
st.markdown("#### Filtración de motor es, por lejos, la categoría más grande")
st.write(
    "Ordenando las partidas arancelarias de repuesto (excluyendo aceites/lubricantes, que son un consumible, no "
    "una pieza) por valor FOB acumulado 2022–set.2026, las tres primeras posiciones son las tres familias de "
    "filtro de motor — juntas suman **US$24.5M**, más del doble que la siguiente categoría."
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
    "El FOB de filtros de motor que importa IPESA no es plano — creció de US$4.0M (2023, su año más bajo) a "
    "US$6.5M (2025), y 2026 va camino a superarlo con holgura (US$6.1M en ene–set, ≈US$8.2M anualizado; agosto "
    "2026 sumó US$1.17M, su mes más alto del año, y setiembre US$0.94M). No es una "
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
1. **Filtración de motor es la brecha más grande y más clara de todo el catálogo de IPESA** — US$26.8M en 4.75
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
        "para evitar el límite de 80,000 filas) hasta julio 2026, + agosto–setiembre 2026 (11,655 líneas, descarga "
        "6-nov-2026). Se excluyen máquinas "
        "y equipos completos por partida arancelaria (tractores 87.01, maquinaria vial 84.29/84.30/84.26/84.27, "
        "pavimentadoras/fresadoras 84.79.10, fajas sobre oruga 84.28.33, implementos agrícolas completos "
        "84.32/84.33/84.36 salvo sus partidas de partes, trituradoras 84.74, motores completos 84.08, gensets 85.02, "
        "camiones 87.04/87.05, remolques/cisternas 87.16, instrumentos 90.15/90.23/90.24/85.26) — el mismo perímetro "
        "aplicado a Repaglas y Dinámica en la sección de crecimiento comparado. Los códigos "
        "de parte se extrajeron por patrón alfanumérico de los 5 campos de \"Descripción Comercial\" de cada DUA."
    )
with c2:
    st.markdown(
        "**Limitaciones.** El campo de marca/modelo es texto libre declarado por cada importador — no hay "
        "estandarización, así que el conteo de \"John Deere\" subestima el verdadero share si algún despachador "
        "omite la marca. El nivel de aplicación (tractor/modelo específico) no está disponible en ADEX para la "
        "mayoría de líneas de filtro. El cruce contra catálogo Bsale es por coincidencia de texto de código, no "
        "por match garantizado de especificación técnica. **Desde 2024, IPESA casi dejó de declarar el código de "
        "parte** (ver aviso arriba) — cualquier hallazgo por código específico está sesgado hacia 2022-2023 y es "
        "un piso, no el techo, de la oportunidad real."
    )
