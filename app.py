"""Frente Dinámica — comparativo de importaciones Repaglas vs. Dinámica.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú), ene.2022–set.2026 (ago.2026 agregado el 2026-10-02; ago–set 2026 recargado el 2026-11-06).
"""

import plotly.graph_objects as go
import streamlit as st

REP = "#2a78d6"
DIN = "#eb6834"
GOOD = "#0ca30c"

st.set_page_config(page_title="Frente Dinámica", page_icon="🚜", layout="wide")

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
      .tag-rep { color: #2a78d6; font-weight: 700; }
      .tag-din { color: #eb6834; font-weight: 700; }
      .share-bar { display:flex; height:34px; border-radius:8px; overflow:hidden; margin:14px 0 8px; }
      .share-seg { display:flex; align-items:center; justify-content:center; font-size:12.5px; font-weight:700; color:#fff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
years = ["2022", "2023", "2024", "2025", "2026*"]
yearly_rep = [635727, 707244, 950300, 826542, 585415]
yearly_din = [1469745, 1695184, 2016322, 2065093, 1131046]

months = ["oct-24", "nov-24", "dic-24", "ene-25", "feb-25", "mar-25", "abr-25",
          "may-25", "jun-25", "jul-25", "ago-25", "sep-25", "oct-25", "nov-25", "dic-25",
          "ene-26", "feb-26", "mar-26", "abr-26", "may-26", "jun-26", "jul-26", "ago-26", "sep-26"]
monthly_rep = [6150, 51305, 96399, 5250, 72650, 122297, 90708, 68676, 63003,
               37970, 70041, 115723, 33523, 107491, 39211, 11830, 112411, 59115, 65049, 25029,
               74110, 81940, 54071, 101860]
monthly_din = [134422, 188103, 324560, 201811, 60848, 109070, 136392, 27131,
               129202, 225048, 254979, 213680, 318299, 158549, 230084, 134834, 141564, 93027,
               71746, 100839, 129090, 135932, 177576, 146437]

familias = ["Transmisión y ejes", "Motor (pistón, camisa, culata)", "Embrague",
            "Bombas e hidráulica", "Sellos, juntas y retenes", "Rodamientos y cojinetes",
            "Dirección", "Cosecha / labranza", "Sistema de combustible", "Frenos"]
# set-2026 sumado sobre las cifras previas clasificando cada partida a 6 dígitos en la misma familia (2026-11-06).
fam_rep = [83848, 1440863, 92958, 505563, 534824, 326815, 81061, 311, 184008, 15221]
fam_din = [1976596, 576414, 1190478, 1052170, 555080, 543045, 313350, 222856, 19049, 183317]

countries = ["Brasil", "Estados Unidos", "Turquía", "India", "China", "Italia", "Reino Unido", "Colombia"]
cty_rep = [113940, 2493522, 271769, 292269, 257588, 3663, 191462, 0]
cty_din = [4102434, 41817, 1404321, 828159, 553935, 418970, 252273, 281151]

ue_rep = [19.19, 20.66, 21.59, 22.29, 22.53]
ue_din = [15.20, 12.44, 13.36, 11.01, 15.77]

duas_rep = [21, 19, 29, 22, 21]
duas_din = [64, 60, 72, 76, 46]

brand_rep = [("Maxiforce", 8072), ("John Deere", 2934), ("Vapormatic", 2227), ("Bepco", 1893),
             ("KMP", 839), ("TVH", 615), ("FDR", 267), ("ZF", 137)]
brand_din = [("Carraro", 2229), ("ZF", 1450), ("AGCO", 1239), ("Bepco", 1068), ("Morel", 941),
             ("Eaton", 913), ("CNH", 899), ("Assur Power", 388)]

sku1 = [
    ["Representaciones Agrícolas S.R.L.", "REP", 130484, 1746, 74.73, "Estados Unidos / India / Reino Unido", "Maxiforce"],
    ["Ipesa S.A.C.", "", 13830, 202, 68.47, "Estados Unidos", "John Deere"],
    ["Fortrac S.A.C.", "", 13518, 99, 136.55, "Estados Unidos", "John Deere / Maxiforce"],
    ["R Y G Rockcat E.I.R.L.", "", 2583, 28, 92.25, "Estados Unidos", "Maxiforce"],
    ["Tractor Import SAC", "", 2605, 14, 186.05, "Estados Unidos / Brasil", "John Deere"],
    ["Dinámica Implementos & Piezas S.A.C.", "DIN", 3406, 61, 55.84, "China", "Assur Power"],
    ["Mateel E.I.R.L.", "", 1516, 24, 63.15, "Estados Unidos", "—"],
    ["Monsante EIRL", "", 1028, 6, 171.40, "Estados Unidos", "—"],
    ["National Air & Motor Co. S.R.L.", "", 1001, 4, 250.34, "Estados Unidos", "—"],
    ["Motores Diesel Andinos MODASA", "", 832, 12, 69.33, "China", "—"],
    ["JPK Mundo Parts E.I.R.L.", "", 921, 16, 57.55, "China", "—"],
    ["Italtrac Selva SAC", "", 983, 6, 163.86, "Estados Unidos", "John Deere"],
    ["Solutra del Perú SRL", "", 272, 4, 67.99, "China", "—"],
    ["R & T Rocckcat E.I.R.L.", "", 3341, 48, 69.60, "Estados Unidos / China", "Maxiforce / Assur Power"],
    ["NGB Packing E.I.R.L.", "", 320, 4, 80.11, "Estados Unidos", "KMP"],
]
sku1.sort(key=lambda r: -r[2])
# Recalculado 2026-09-01 desde los 10 reportes ADEX reales (utils/data.py); ago–set 2026 sumado el 2026-11-06 — reemplaza la
# investigación a mano previa para este SKU (los valores casi no cambiaron: valida el método).


def usd(n):
    return f"US$ {n:,.0f}"


def legend():
    st.markdown(
        f"<span class='tag-rep'>● Repaglas</span> &nbsp;&nbsp; <span class='tag-din'>● Dinámica</span>",
        unsafe_allow_html=True,
    )


def grouped_bar(categories, series_rep, series_din, height=340, yfmt="$,.0f"):
    fig = go.Figure()
    fig.add_bar(x=categories, y=series_rep, name="Repaglas", marker_color=REP)
    fig.add_bar(x=categories, y=series_din, name="Dinámica", marker_color=DIN)
    fig.update_layout(
        barmode="group", height=height, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def line_chart(labels, series_rep, series_din, height=300, prefix="$"):
    fig = go.Figure()
    fig.add_scatter(x=labels, y=series_rep, name="Repaglas", mode="lines", line=dict(color=REP, width=2.5))
    fig.add_scatter(x=labels, y=series_din, name="Dinámica", mode="lines", line=dict(color=DIN, width=2.5))
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        yaxis_tickprefix=prefix, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def hbar_chart(categories, series_rep, series_din, height=None):
    height = height or (len(categories) * 46 + 40)
    fig = go.Figure()
    fig.add_bar(y=categories, x=series_rep, name="Repaglas", orientation="h", marker_color=REP)
    fig.add_bar(y=categories, x=series_din, name="Dinámica", orientation="h", marker_color=DIN)
    fig.update_layout(
        barmode="group", height=height, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, xaxis_tickprefix="$", xaxis_tickformat=",.0f",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def brand_bars(items, color):
    max_v = max(v for _, v in items)
    for name, v in items:
        c1, c2, c3 = st.columns([2, 5, 1])
        c1.markdown(f"<div style='text-align:right;font-size:13px;font-weight:600;'>{name}</div>", unsafe_allow_html=True)
        pct = max(3, v / max_v * 100)
        c2.markdown(
            f"<div style='background:#efe8d8;border-radius:5px;height:9px;overflow:hidden;'>"
            f"<div style='background:{color};width:{pct}%;height:100%;border-radius:5px;'></div></div>",
            unsafe_allow_html=True,
        )
        c3.markdown(f"<div style='font-size:12px;color:#948a76;'>{v:,}</div>", unsafe_allow_html=True)


# ================= HEADER =================
st.markdown("###### 🚜 INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("Frente Dinámica")
st.markdown(
    "Comparativo de importaciones de repuestos agrícolas: **:blue[Repaglas]** (Representaciones Agrícolas S.R.L.) "
    "frente a **:orange[Dinámica Implementos & Piezas S.A.C.]**, su competidor de mayor volumen en el mercado peruano."
)
st.caption(
    "Periodo: **enero 2022 – setiembre 2026** (dato definitivo; octubre aún no publicado) · Fuente: **ADEX Data Trade** "
    "sobre registros de SUNAT / Aduanas · Descarga: **27 ago. 2026** (+ agosto–setiembre 2026 el **6 nov. 2026**) · "
    "Universo: **33,230 partidas · 430 DUAs**"
)

# ================= KPI ROW =================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("FOB importado 2025", "$2.89M", "entre ambas empresas")
k2.metric("Participación Repaglas", "28.6%", "del FOB combinado 2025")
k3.metric("Brecha Dinámica / Repaglas", "2.3×", "promedio 2022–2025")
k4.metric("Envíos por año (DUAs)", "21 vs 68", "Repaglas vs. Dinámica")
k5.metric("Liderazgo en RE507920", "73.9%", "share de Repaglas en su SKU ancla")

st.divider()

# ================= SECCIÓN 1: PANORAMA =================
st.subheader("Panorama comparativo")
st.markdown("#### Dinámica importa 2 a 2.5 veces más que Repaglas, todos los años")
st.write(
    "Desde 2022, Dinámica ha sostenido un valor FOB importado muy superior al de Repaglas en cada ejercicio, "
    "con una brecha que se ha mantenido estructural — no es un año atípico. En el acumulado 2022–2025, Repaglas "
    "creció 30% en valor FOB; Dinámica creció 41%, es decir, la distancia se amplía más de lo que se cierra."
)
st.write(
    "Mirado al mismo corte (enero–setiembre), ambas importan menos en 2026: Repaglas −9.4% y Dinámica −16.7%. Para "
    "Repaglas la baja no empezó este año — su pico fue 2024 y ya en 2025 cayó 18.8% en el mismo tramo. Repaglas "
    "está importando **con más frecuencia y en lotes más chicos** (27 DUAs en los últimos 12 meses vs. 21 un año "
    "antes, con 26% menos FOB por DUA), así que el acumulado a una fecha depende mucho de en qué mes cae cada "
    "embarque. En **12 meses móviles** (oct–sep), Repaglas baja −4.3% (US$ 766K, 1.8% por debajo de su promedio "
    "anual 2022–2025 de US$ 780K) y Dinámica baja el doble (−8.3%). Ojo: con la ventana anterior (sep–ago) Repaglas "
    "daba +1.7% — la diferencia es que setiembre 2025 (US$ 116K) fue un mes fuerte que ahora sale de la ventana."
)
# FOB acumulado YTD ene–set de cada año (US$), mismos meses en todos los años para que sea comparable.
ytd_years = ["2022", "2023", "2024", "2025", "2026"]
ytd_rep = [491667, 616228, 796446, 646317, 585415]
ytd_din = [1064293, 1374637, 1369236, 1358161, 1131046]


def ytd_chart(values, color, name):
    var = [None] + [(b / a - 1) * 100 for a, b in zip(values, values[1:])]
    money = [f"US$ {v / 1e6:.2f}M" if v >= 1e6 else f"US$ {v / 1000:,.0f}K" for v in values]
    labels = [f"<b>{m}</b>" + ("" if p is None else f"<br>{p:+.1f}%") for m, p in zip(money, var)]
    fig = go.Figure()
    fig.add_bar(
        x=ytd_years, y=values, marker_color=color, marker_cornerradius=4, text=labels, textposition="outside",
        textfont=dict(color="#3d3a33", size=12.5), cliponaxis=False,
        customdata=[("—" if p is None else f"{p:+.1f}% vs. año anterior") for p in var],
        hovertemplate=f"<b>{name}</b> · ene–set %{{x}}<br>US$ %{{y:,.0f}}<br>%{{customdata}}<extra></extra>",
    )
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, bargap=0.35,
        yaxis=dict(tickprefix="$", tickformat=",.0f", range=[0, max(values) * 1.25], gridcolor="#e8e2d6"),
        uniformtext=dict(minsize=12, mode="show"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


st.markdown("**FOB importado acumulado enero–setiembre, año a año** (mismo tramo de meses en cada año)")
y1, y2 = st.columns(2)
with y1:
    st.markdown("<span class='tag-rep'>● Repaglas</span>", unsafe_allow_html=True)
    st.plotly_chart(ytd_chart(ytd_rep, REP, "Repaglas"), use_container_width=True)
with y2:
    st.markdown("<span class='tag-din'>● Dinámica</span>", unsafe_allow_html=True)
    st.plotly_chart(ytd_chart(ytd_din, DIN, "Dinámica"), use_container_width=True)
st.caption(
    "Cada gráfico tiene su propia escala (Dinámica importa ~2× más). El % bajo cada monto es la variación contra "
    "el mismo tramo enero–setiembre del año anterior. Brecha Dinámica / Repaglas ene–set 2026: 1.93×."
)

# 12 meses móviles cerrando en setiembre (oct–sep): neutraliza el efecto de en qué mes cae cada DUA.
ltm_labels = ["oct22–sep23", "oct23–sep24", "oct24–sep25", "oct25–sep26"]
ltm_rep = [760288, 887462, 800172, 765640]
ltm_din = [1780089, 1689784, 2005246, 1837977]
ltm_duas_rep = [21, 26, 21, 27]
ltm_duas_din = [68, 59, 73, 73]


def ltm_chart(values, duas, color, name):
    var = [None] + [(b / a - 1) * 100 for a, b in zip(values, values[1:])]
    money = [f"US$ {v / 1e6:.2f}M" if v >= 1e6 else f"US$ {v / 1000:,.0f}K" for v in values]
    labels = [f"<b>{m}</b>" + ("" if p is None else f"<br>{p:+.1f}%") for m, p in zip(money, var)]
    fig = go.Figure()
    fig.add_bar(
        x=[f"{l}<br>{d} DUAs · {v / d / 1000:,.0f}K/DUA"
           for l, d, v in zip(ltm_labels, duas, values)],
        y=values, marker_color=color, marker_cornerradius=4, text=labels, textposition="outside",
        textfont=dict(color="#3d3a33", size=12.5), cliponaxis=False,
        customdata=[[d, v / d] for d, v in zip(duas, values)],
        hovertemplate=(f"<b>{name}</b> · %{{x}}<br>US$ %{{y:,.0f}}<br>%{{customdata[0]}} DUAs · "
                       "US$ %{customdata[1]:,.0f} por DUA<extra></extra>"),
    )
    fig.update_layout(
        height=340, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, bargap=0.35,
        xaxis=dict(tickangle=0, tickfont=dict(size=11)),
        yaxis=dict(tickprefix="$", tickformat=",.0f", range=[0, max(values) * 1.25], gridcolor="#e8e2d6"),
        uniformtext=dict(minsize=12, mode="show"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


st.markdown("**Visión anual: FOB importado en 12 meses móviles cerrando en setiembre** (octubre a setiembre)")
l1, l2 = st.columns(2)
with l1:
    st.markdown("<span class='tag-rep'>● Repaglas</span>", unsafe_allow_html=True)
    st.plotly_chart(ltm_chart(ltm_rep, ltm_duas_rep, REP, "Repaglas"), use_container_width=True)
with l2:
    st.markdown("<span class='tag-din'>● Dinámica</span>", unsafe_allow_html=True)
    st.plotly_chart(ltm_chart(ltm_din, ltm_duas_din, DIN, "Dinámica"), use_container_width=True)
m1, m2, m3 = st.columns(3)
m1.metric("Repaglas · 12 meses a set-26", "−4.3%", "1.8% bajo su promedio anual 2022–25", delta_color="off")
m2.metric("Dinámica · 12 meses a set-26", "−8.3%", "tras su máximo en oct24–sep25", delta_color="off")
m3.metric("Repaglas · frecuencia de pedido", "21 → 27 DUAs", "−26% FOB por DUA (lotes más chicos)", delta_color="off")
st.markdown(
    "<div class='callout'><b>Lectura:</b> con la estrategia de pedidos más frecuentes y más chicos, Repaglas debe "
    "leerse en base anual (12 meses móviles), no en acumulado a una fecha. Aun así, cerrando en setiembre el año "
    "móvil muestra una baja moderada (−4.3%) que con la ventana sep–ago no se veía (+1.7%): conviene confirmarlo "
    "con octubre antes de leerlo como tendencia. Dinámica cae el doble (−8.3%). En 12 meses la brecha con "
    "Dinámica es 2.40× (vs. 1.93× en el corte ene–set y 2.3× de promedio anual 2022–2025).</div>",
    unsafe_allow_html=True,
)
st.markdown("**FOB importado por año**")
legend()
st.plotly_chart(grouped_bar(years, yearly_rep, yearly_din), use_container_width=True)

st.divider()

# ================= SECCIÓN 2: MENSUAL =================
st.subheader("Cadencia mensual · últimos 24 meses")
st.markdown("#### Dinámica compra en lotes más grandes y más volátiles")
st.write(
    "El perfil mensual de Dinámica muestra picos pronunciados (hasta US$ 325 mil en diciembre 2024, US$ 318 mil "
    "en octubre 2025) seguidos de valles profundos — compras por contenedor completo, probablemente ligadas a "
    "consolidación de carga desde Brasil. Repaglas exhibe un patrón más plano y frecuente, compatible con una "
    "política de reposición más continua desde EE.UU."
)
legend()
st.plotly_chart(line_chart(months, monthly_rep, monthly_din, height=320), use_container_width=True)

st.divider()

# ================= SECCIÓN 3: FAMILIAS =================
st.subheader("Qué importa cada uno")
st.markdown("#### El mercado está repartido por especialidad, no por precio")
st.write(
    "Clasificando cada partida arancelaria por familia de producto, el patrón es nítido: Repaglas concentra su "
    "FOB en **motor** (pistones, camisas, culatas — US$ 1.44M) y **sistema de combustible**, mientras Dinámica "
    "domina de forma amplia **transmisión y ejes** (US$ 1.98M), **embrague**, **hidráulica**, **rodamientos**, "
    "**dirección**, **frenos** y **cosecha**. Son catálogos complementarios más que rivales frontales — salvo en "
    "dos zonas de fricción real."
)
legend()
st.plotly_chart(hbar_chart(familias, fam_rep, fam_din), use_container_width=True)
st.markdown(
    "<div class='callout'><b>Zonas de fricción:</b> en <b>sellos/juntas/retenes</b> (US$ 535K Repaglas vs US$ 555K "
    "Dinámica) y <b>bombas/hidráulica</b> (US$ 506K vs US$ 1.05M) ambos catálogos se superponen de forma directa "
    "— son las familias donde vale la pena comparar precio unitario SKU a SKU, no solo volumen agregado.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 4: MARCAS =================
st.subheader("Huella de marca en descripción comercial")
st.markdown("#### Catálogos con identidad propia — y un cruce a vigilar")
st.write(
    "Contando menciones de marca en el campo \"Descripción Comercial\" de cada DUA (proxy de qué líneas realmente "
    "mueve cada empresa), Repaglas se apoya en **Maxiforce**, referencias cruzadas a **John Deere**, **Vapormatic** "
    "y **Bepco**. Dinámica construye su catálogo alrededor de **Carraro**, **ZF**, **AGCO**, **Bepco**, **Morel**, "
    "**CNH** y **Eaton** — el vocabulario de un especialista en trenes de potencia."
)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Repaglas · menciones de marca**")
    brand_bars(brand_rep, REP)
with c2:
    st.markdown("**Dinámica · menciones de marca**")
    brand_bars(brand_din, DIN)
st.markdown(
    "<div class='callout'><b>Bepco aparece en ambos catálogos</b> con volumen comparable (1,893 menciones en "
    "Repaglas vs. 1,068 en Dinámica) — junto con presencia menor cruzada de ZF, KMP, Dana, FDR, TVH y Rota. Es la "
    "marca más expuesta a comparación directa de precio entre ambos importadores.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 5: PAÍS DE ORIGEN =================
st.subheader("Estrategia de abastecimiento")
st.markdown("#### Un corredor concentrado frente a una red diversificada")
st.write(
    "Repaglas concentra 67% de su FOB en un único corredor: **Estados Unidos** (US$ 2.49M), con exposición "
    "secundaria a India, Turquía, China y Reino Unido. Dinámica reparte su abastecimiento entre **Brasil** "
    "(US$ 4.10M, su origen dominante — probablemente vinculado a manufactura local de ejes/Carraro), y un bloque "
    "asiático de bajo costo (Turquía, India, China) más Europa y Colombia."
)
st.write(
    "La lectura estratégica: Repaglas opera un modelo de alta dependencia de un solo origen (eficiente, pero "
    "expuesto a shocks de flete, tipo de cambio o arancel de EE.UU.); Dinámica corre una red multi-origen que le "
    "da resiliencia y, en paralelo, acceso a manufactura de bajo costo para escalar volumen."
)
legend()
st.plotly_chart(hbar_chart(countries, cty_rep, cty_din), use_container_width=True)

st.divider()

# ================= SECCIÓN 6: ECONOMÍA UNITARIA =================
st.subheader("Economía unitaria")
st.markdown("#### Repaglas importa menos kilos, pero de mayor valor por kilo")
st.write(
    "El FOB por kilogramo de Repaglas (US$ 19–23/kg) es sistemáticamente entre 25% y 100% más alto que el de "
    "Dinámica (US$ 11–16/kg) en los cinco años de la serie. Confirma la lectura anterior: la canasta de Repaglas son "
    "componentes de precisión (pistones, inyectores) livianos y de alto valor; la de Dinámica son piezas de "
    "transmisión y ejes, más pesadas y de menor valor por kilo — de ahí que mueva casi el doble de toneladas con "
    "\"solo\" 2.3× más FOB."
)
legend()
st.plotly_chart(line_chart(years, ue_rep, ue_din, height=260), use_container_width=True)

st.divider()

# ================= SECCIÓN 7: SKU RE507920 =================
st.subheader("Caso SKU · búsqueda dirigida en ADEX")
st.markdown("#### RE507920 es el SKU ancla de Repaglas — y lo defiende bien")
st.markdown(
    "**`RE507920`** — Kit de pistón / camisa / anillos — motor John Deere (partida 8409.99). "
    "15 importadores registrados, 2022–set.2026."
)
st.markdown(
    f"<div class='share-bar'>"
    f"<div class='share-seg' style='width:73.9%;background:{REP};'>Repaglas · 73.9% del FOB de mercado</div>"
    f"<div class='share-seg' style='width:26.1%;background:{DIN};'>Resto · 26.1%</div>"
    f"</div>",
    unsafe_allow_html=True,
)
st.caption(
    "Sobre US$ 176,641 FOB y 2,274 unidades importadas por todo el mercado peruano en esta referencia (ADEX, "
    "2022–set.2026), Repaglas concentra 73.9% del valor y 76.8% de las unidades, mayoritariamente desde EE.UU. "
    "bajo su propia marca Maxiforce, a un precio consistentemente estable de US$ 72–76/unidad desde 2022."
)
st.dataframe(
    {
        "Importador": [r[0] + (" 🔵 Repaglas" if r[1] == "REP" else " 🟠 Dinámica" if r[1] == "DIN" else "") for r in sku1],
        "FOB US$": [usd(r[2]) for r in sku1],
        "Unidades": [f"{r[3]:,}" for r in sku1],
        "US$/unidad": [f"{r[4]:.2f}" for r in sku1],
        "Origen": [r[5] for r in sku1],
        "Marca declarada": [r[6] for r in sku1],
    },
    use_container_width=True,
    hide_index=True,
)
st.markdown(
    "<div class='callout'><b>Lectura competitiva:</b> los importadores que declaran \"John Deere\" genuino "
    "(IPESA, Fortrac) pagan entre <b>US$ 121–165/unidad</b> — 2 a 3 veces más que el kit Maxiforce de Repaglas. "
    "Ese diferencial de precio es la base de la posición de Repaglas en el canal. Dinámica apenas probó esta "
    "referencia una vez (mayo 2022, China, marca Assur Power, US$ 56/unidad) y no ha vuelto a repetir — no es hoy "
    "una amenaza activa sobre este SKU, pero confirma que sabe sortear a un proveedor asiático más barato si "
    "decide escalarlo. <b>Nuevo (set-2026):</b> R & T Rockcat trajo 24 kits de esta referencia desde China con "
    "marca Assur Power a US$ 56/unidad (25% menos que Repaglas) — la misma marca y precio que Dinámica en 2022; "
    "vigilar si repite.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 8: SKU 87317256 =================
st.subheader("Caso SKU · búsqueda dirigida en ADEX")
st.markdown("#### 87317256: una referencia donde Repaglas todavía no aparece")
st.markdown(
    "**`87317256`** — Set de pistón — motor CNH / Case-New Holland. Solo 2 importaciones registradas en todo el "
    "histórico ADEX."
)
c1, c2, c3 = st.columns(3)
c1.metric("Repaglas", "Sin registro")
c2.metric("Dinámica · nov. 2025", "$425", "12 piezas · China · Assur Power")
c3.metric("Inversiones Rodatract · jun. 2023", "$165", "1 unidad · Turquía · CNH")
st.markdown(
    "<div class='callout'><b>Señal débil, no un patrón todavía:</b> con solo dos compras de prueba en tres años "
    "(la última recién en noviembre 2025), no hay evidencia de que Dinámica esté escalando esta referencia. Vale "
    "la pena volver a consultarla en ADEX dentro de 2–3 trimestres: si aparece un tercer embarque de Dinámica con "
    "mayor cantidad, sería indicio de que está validando un proveedor chino para motores CNH y podría estar "
    "preparando entrada de catálogo.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SECCIÓN 9: OPERATIVO =================
st.subheader("Huella operativa y logística")
st.markdown("#### Mismo puerto, mismo régimen — pero Dinámica mueve el doble de contenedores")
st.write(
    "Ambas empresas nacionalizan prácticamente el 100% de su carga por vía marítima en la Aduana Marítima del "
    "Callao, y ambas concentran su despacho en un solo agente de aduana (Repaglas: Konekta Aduanas, 98% de sus "
    "DUAs · Dinámica: Mundo Aduanero, 99.7%) — una dependencia operativa compartida por todo el sector, no una "
    "ventaja diferencial."
)
st.write(
    "La diferencia real está en la cadencia: Dinámica promedia **68 DUAs al año** (~5–6 embarques mensuales) "
    "frente a los **21 DUAs** de Repaglas (~2 mensuales). No solo importa más valor — importa con 3 veces más "
    "frecuencia, lo que sostiene un catálogo más ancho y una reposición de stock más rápida."
)
legend()
st.plotly_chart(grouped_bar(years, duas_rep, duas_din, height=280), use_container_width=True)

st.divider()

# ================= SECCIÓN 10: CONCLUSIONES =================
st.subheader("Síntesis")
st.markdown("#### Cinco lecturas para la decisión comercial")
st.markdown(
    """
1. **Dinámica no es un competidor genérico, es un especialista en trenes de potencia con volumen.** Domina
   transmisión, ejes, embrague, hidráulica y dirección con una brecha de FOB de 4× a 27× sobre Repaglas según la
   familia — mientras Repaglas domina motor y combustible con márgenes similares a su favor.
2. **El SKU RE507920 demuestra que Repaglas puede ganar y sostener liderazgo (74% de share) cuando compite en su
   terreno** — con precio, marca propia y consistencia de abastecimiento. Ese mismo libro de jugadas es replicable
   en otras referencias de motor donde hoy no se ha medido el mercado.
3. **La dependencia de un solo país (EE.UU., 67% del FOB) es el mayor riesgo estructural de Repaglas** frente a la
   red multi-origen de Dinámica (Brasil + Asia + Europa). Diversificar 1–2 líneas de motor hacia un segundo origen
   reduciría exposición cambiaria/arancelaria sin resignar el diferencial de calidad.
4. **Bepco es la marca de mayor solapamiento directo** entre ambos catálogos — el mejor candidato para un
   ejercicio de benchmarking de precio unitario SKU a SKU antes que cualquier otra familia.
5. **La cadencia de Dinámica (68 DUAs/año vs. 21) es tanto un riesgo como un mapa.** Su ritmo de importación
   revela qué tan rápido está reponiendo catálogo; monitorear DUAs trimestrales por familia de producto es una
   alerta temprana más barata que monitorear precios.
"""
)

st.info(
    "**Para profundizar este análisis**, sería útil compartir la lista completa de SKUs ya extraídos (más allá de "
    "RE507920 y 87317256) para correr la misma búsqueda dirigida en ADEX sobre cada uno — especialmente en las "
    "familias de fricción directa (sellos/juntas y bombas/hidráulica). También se puede cruzar estos hallazgos "
    "contra el catálogo actual en Bsale para señalar qué SKUs de Dinámica no están cubiertos todavía, o sumar "
    "otros RUC de competidores (IPESA, Fortrac, Italtrac Selva) para ampliar el mapa competitivo."
)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "**Metodología.** Se procesaron 5 reportes ADEX Data Trade (aduanas del Perú, 2022–2026): (1) histórico "
        "completo de Repaglas + Dinámica por RUC, 31,749 líneas (ene.2022–jul.2026), más el reporte de agosto–"
        "setiembre 2026 (1,481 líneas, descargado 6-nov-2026; reemplaza al de agosto del 2-oct, que no cambió para "
        "estas dos empresas); (2)–(3) búsquedas dirigidas por descripción "
        "comercial para los SKU RE507920 y 87317256; el detalle de Dinámica en solitario (15,097 líneas) se usó "
        "para validar cruces. Las familias de producto se derivaron agrupando la descripción arancelaria de cada "
        "partida por palabra clave; las marcas se cuentan por coincidencia de texto en los 5 campos de "
        "\"Descripción Comercial\" de cada DUA."
    )
with c2:
    st.markdown(
        "**Limitaciones.** ADEX reporta a nivel de DUA/partida, no a nivel de línea de factura — el \"US$/unidad\" "
        "es un promedio del embarque. Los datos de 2026 son parciales (hasta setiembre, dato definitivo). Familias y marcas de agosto y setiembre 2026 se sumaron "
        "con la misma clasificación por palabra clave sobre las cifras previas. \"Otros\" en "
        "familias de producto agrupa partidas de baja frecuencia no clasificadas por palabra clave."
    )
