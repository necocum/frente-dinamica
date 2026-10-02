"""Frente Dinámica — comparativo de importaciones Repaglas vs. Dinámica.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú), ene.2022–ago.2026 (ago.2026 agregado el 2026-10-02).
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
yearly_rep = [635727, 707244, 950300, 826542, 483555]
yearly_din = [1469745, 1695184, 2016322, 2065093, 984608]

months = ["sep-24", "oct-24", "nov-24", "dic-24", "ene-25", "feb-25", "mar-25",
          "abr-25", "may-25", "jun-25", "jul-25", "ago-25", "sep-25", "oct-25", "nov-25",
          "dic-25", "ene-26", "feb-26", "mar-26", "abr-26", "may-26", "jun-26", "jul-26", "ago-26"]
monthly_rep = [82322, 6150, 51305, 96399, 5250, 72650, 122297, 90708, 68676, 63003,
               37970, 70041, 115723, 33523, 107491, 39211, 11830, 112411, 59115, 65049, 25029,
               74110, 81940, 54071]
monthly_din = [173023, 134422, 188103, 324560, 201811, 60848, 109070, 136392, 27131,
               129202, 225048, 254979, 213680, 318299, 158549, 230084, 134834, 141564, 93027,
               71746, 100839, 129090, 135932, 177576]

familias = ["Transmisión y ejes", "Motor (pistón, camisa, culata)", "Embrague",
            "Bombas e hidráulica", "Sellos, juntas y retenes", "Rodamientos y cojinetes",
            "Dirección", "Cosecha / labranza", "Sistema de combustible", "Frenos"]
fam_rep = [76022, 1398505, 90287, 488611, 521556, 318480, 81006, 311, 183878, 14842]
fam_din = [1970847, 572643, 1176696, 1038772, 552516, 502531, 286560, 208492, 18625, 182457]

countries = ["Brasil", "Estados Unidos", "Turquía", "India", "China", "Italia", "Reino Unido", "Colombia"]
cty_rep = [95986, 2463901, 270781, 278072, 243759, 3662, 168021, 0]
cty_din = [3967754, 41817, 1404322, 827797, 553722, 418970, 241213, 281151]

ue_rep = [19.19, 20.66, 21.59, 22.29, 22.90]
ue_din = [15.20, 12.44, 13.36, 11.01, 17.57]

duas_rep = [21, 19, 29, 22, 17]
duas_din = [64, 60, 72, 76, 40]

brand_rep = [("Maxiforce", 7896), ("John Deere", 2927), ("Vapormatic", 2227), ("Bepco", 1893),
             ("KMP", 692), ("TVH", 615), ("FDR", 267), ("ZF", 130)]
brand_din = [("Carraro", 2229), ("ZF", 1448), ("AGCO", 1229), ("Bepco", 1068), ("Morel", 941),
             ("Eaton", 913), ("CNH", 899), ("Assur Power", 388)]

sku1 = [
    ["Representaciones Agrícolas S.R.L.", "REP", 125602, 1676, 74.94, "Estados Unidos / Reino Unido / India", "Maxiforce"],
    ["Ipesa S.A.C.", "", 13830, 202, 68.47, "Estados Unidos", "John Deere"],
    ["Fortrac S.A.C.", "", 11974, 79, 151.58, "Estados Unidos", "John Deere"],
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
    ["R & T Rocckcat E.I.R.L.", "", 2008, 24, 83.66, "Estados Unidos", "Maxiforce"],
]
sku1.sort(key=lambda r: -r[2])
# Recalculado 2026-09-01 desde los 10 reportes ADEX reales (utils/data.py) — reemplaza la
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
    "Periodo: **enero 2022 – agosto 2026** (dato definitivo) · Fuente: **ADEX Data Trade** sobre registros de "
    "SUNAT / Aduanas · Descarga: **27 ago. 2026** (+ agosto 2026 el **2 oct. 2026**) · Universo: **32,515 partidas · 505 DUAs**"
)

# ================= KPI ROW =================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("FOB importado 2025", "$2.89M", "entre ambas empresas")
k2.metric("Participación Repaglas", "28.6%", "del FOB combinado 2025")
k3.metric("Brecha Dinámica / Repaglas", "2.3×", "promedio 2022–2025")
k4.metric("Envíos por año (DUAs)", "21 vs 68", "Repaglas vs. Dinámica")
k5.metric("Liderazgo en RE507920", "74.5%", "share de Repaglas en su SKU ancla")

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
    "2026 muestra el primer año con caída interanual para ambas: en base comparable enero–agosto, Repaglas "
    "retrocede 8.9% y Dinámica 14.0% (con corte a julio eran −6.7% y −9.3%: agosto profundizó la caída en ambas). Es "
    "una señal de mercado (tipo de cambio, demanda agrícola, o ambas), no de pérdida de terreno relativo — la brecha "
    "en ese mismo tramo (2.04×) sigue por debajo del promedio histórico anual (2.3×)."
)
# Variación 2026 vs 2025 en base comparable (ene–jul: 460,553→429,484 Rep, 889,501→807,032 Din;
# ene–ago: 530,594→483,555 Rep, 1,144,481→984,608 Din).
cortes = ["Corte a julio (ene–jul)", "Corte a agosto (ene–ago)"]
var_rep = [-6.7, -8.9]
var_din = [-9.3, -14.0]
v1, v2 = st.columns([3, 1])
with v1:
    st.markdown("**Variación interanual del FOB importado, 2026 vs. 2025 (mismos meses)**")
    legend()
    fig_var = go.Figure()
    for name, vals, color in (("Repaglas", var_rep, REP), ("Dinámica", var_din, DIN)):
        fig_var.add_bar(
            x=cortes, y=vals, name=name, marker_color=color, marker_cornerradius=4,
            text=[f"{v:.1f}%" for v in vals], textposition="outside", textfont=dict(color="#3d3a33", size=13),
            hovertemplate=f"<b>{name}</b><br>%{{x}}<br>%{{y:.1f}}% vs. 2025<extra></extra>",
        )
    fig_var.update_layout(
        barmode="group", bargap=0.35, bargroupgap=0.08, height=300, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, yaxis=dict(ticksuffix="%", range=[-17, 0], gridcolor="#e8e2d6", zeroline=True,
                                     zerolinecolor="#948a76"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_var, use_container_width=True)
with v2:
    st.metric("Brecha Dinámica / Repaglas", "2.04×", "ene–ago 2026", delta_color="off")
    st.metric("Promedio histórico anual", "2.3×", "2022–2025", delta_color="off")
    st.caption("Agosto profundizó la caída en ambas, más en Dinámica: la brecha 2026 sigue bajo el promedio.")
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
    "FOB en **motor** (pistones, camisas, culatas — US$ 1.40M) y **sistema de combustible**, mientras Dinámica "
    "domina de forma amplia **transmisión y ejes** (US$ 1.97M), **embrague**, **hidráulica**, **rodamientos**, "
    "**dirección**, **frenos** y **cosecha**. Son catálogos complementarios más que rivales frontales — salvo en "
    "dos zonas de fricción real."
)
legend()
st.plotly_chart(hbar_chart(familias, fam_rep, fam_din), use_container_width=True)
st.markdown(
    "<div class='callout'><b>Zonas de fricción:</b> en <b>sellos/juntas/retenes</b> (US$ 522K Repaglas vs US$ 553K "
    "Dinámica) y <b>bombas/hidráulica</b> (US$ 489K vs US$ 1.04M) ambos catálogos se superponen de forma directa "
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
    "Repaglas concentra 68% de su FOB en un único corredor: **Estados Unidos** (US$ 2.46M), con exposición "
    "secundaria a India, Turquía, China y Reino Unido. Dinámica reparte su abastecimiento entre **Brasil** "
    "(US$ 3.97M, su origen dominante — probablemente vinculado a manufactura local de ejes/Carraro), y un bloque "
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
    "El FOB por kilogramo de Repaglas (US$ 19–23/kg) es sistemáticamente 40–70% más alto que el de Dinámica "
    "(US$ 11–17/kg) en los cinco años de la serie. Confirma la lectura anterior: la canasta de Repaglas son "
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
    "14 importadores registrados, 2022–2026."
)
st.markdown(
    f"<div class='share-bar'>"
    f"<div class='share-seg' style='width:74.5%;background:{REP};'>Repaglas · 74.5% del FOB de mercado</div>"
    f"<div class='share-seg' style='width:25.5%;background:{DIN};'>Resto · 25.5%</div>"
    f"</div>",
    unsafe_allow_html=True,
)
st.caption(
    "Sobre US$ 168,562 FOB y 2,156 unidades importadas por todo el mercado peruano en esta referencia (ADEX, "
    "2022–jul.2026), Repaglas concentra 74.5% del valor y 77.7% de las unidades, mayoritariamente desde EE.UU. "
    "bajo su propia marca Maxiforce, a un precio consistentemente estable de US$ 75–77/unidad desde 2022."
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
    "decide escalarlo.</div>",
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
3. **La dependencia de un solo país (EE.UU., 68% del FOB) es el mayor riesgo estructural de Repaglas** frente a la
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
        "completo de Repaglas + Dinámica por RUC, 31,749 líneas (ene.2022–jul.2026), más el reporte de agosto 2026 "
        "(766 líneas, descargado 2-oct-2026); (2)–(3) búsquedas dirigidas por descripción "
        "comercial para los SKU RE507920 y 87317256; el detalle de Dinámica en solitario (15,097 líneas) se usó "
        "para validar cruces. Las familias de producto se derivaron agrupando la descripción arancelaria de cada "
        "partida por palabra clave; las marcas se cuentan por coincidencia de texto en los 5 campos de "
        "\"Descripción Comercial\" de cada DUA."
    )
with c2:
    st.markdown(
        "**Limitaciones.** ADEX reporta a nivel de DUA/partida, no a nivel de línea de factura — el \"US$/unidad\" "
        "es un promedio del embarque. Los datos de 2026 son parciales (hasta agosto, dato definitivo). Familias y marcas de agosto 2026 se sumaron "
        "con la misma clasificación por palabra clave sobre las cifras previas. \"Otros\" en "
        "familias de producto agrupa partidas de baja frecuencia no clasificadas por palabra clave."
    )
