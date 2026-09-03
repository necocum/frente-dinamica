"""Fortrac y Mateel — perfil completo de dos competidores, más allá de los 10 SKU ancla.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú). Histórico completo por RUC de
FORTRAC S.A.C. (20394004643) y MATEEL E.I.R.L. (20601122015), ene.2022–jul.2026
(11,496 líneas, un solo export sin truncar). A diferencia de las hojas "SKU Ancla"
y "Competencia Maxiforce" (que solo miran los 10 códigos OEM ancla), esta hoja mira
el catálogo COMPLETO que cada empresa importa — para saber si son competidores
grandes o chicos en términos absolutos, no solo dentro de esa canasta puntual.
Comparado contra el histórico también completo de Repaglas (RUC 20118992009,
mismo archivo fuente que la hoja principal "Frente Dinámica").
"""

import plotly.graph_objects as go
import streamlit as st

REP = "#2a78d6"
FOR = "#c0392b"
MAT = "#c9a227"
GOOD = "#0ca30c"
BAD = "#c0392b"

st.set_page_config(page_title="Fortrac y Mateel", page_icon="🔩", layout="wide")

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
      .tag-for { color: #c0392b; font-weight: 700; }
      .tag-mat { color: #9a7d12; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
years = ["2022", "2023", "2024", "2025", "2026*"]
fob_rep = [635728, 707244, 950300, 826542, 429484]
fob_for = [507127, 368279, 378792, 482095, 490765]
fob_mat = [124685, 93098, 98815, 22452, 64366]

TOTAL_REP = sum(fob_rep)
TOTAL_FOR = sum(fob_for)
TOTAL_MAT = sum(fob_mat)

ytd_rep = (460553, 429484)   # ene-jul 2025, ene-jul 2026
ytd_for = (248007, 490765)
ytd_mat = (2427, 64366)
FOR_DUA_MOTORES = 127564  # un solo DUA (31376, ene.2026) de 10 motores JD completos

categorias_motor = [
    # (categoría, FOB Repaglas, FOB Fortrac, FOB Mateel)
    ("Émbolos (pistones) motor 84.08", 604659, 66633, 3369),
    ("Aros de obturación (retenes)", 139172, 258010, 29162),
    ("Cajas de cojinetes s/rodam.", 263724, 73816, 9369),
    ("Partes de motor 84.07/84.08", 242000, 103219, 15329),
    ("Juntas y surtidos de juntas", 229272, 12351, 1518),
    ("Empaquetaduras de caucho", 46969, 38598, 2628),
    ("Inyectores y partes de combustible", 182464, 37135, 15972),
    ("Válvulas de motor 84.07/84.08", 161146, 36814, 2671),
    ("Bombas de aceite de motor", 153654, 74486, 11342),
    ("Segmentos (anillos) de motor", 146216, 11706, 2611),
    ("Filtros: aparatos para filtrar lubricante/carburante", 18948, 78047, 5181),
    ("Filtros: elementos filtrantes de motor", 24362, 57211, 6077),
]

# FOB mensual 2026 (todo el catálogo, no solo Maxiforce) — para desagregar la barra "2026*" del
# gráfico anual en 7 barras mensuales.
mes_2026_rep = [11830, 112411, 59115, 65049, 25029, 74111, 81940]
mes_2026_for = [229477, 40442, 113449, 14996, 41029, 21742, 29630]
mes_2026_mat = [0, 8543, 0, 0, 25068, 28691, 2064]

# FOB mensual ene-jul, 2025 vs. 2026, para el comparativo de la Sección 2.
mes_2025_rep = [5250, 72650, 122297, 90708, 68676, 63003, 37970]
mes_2025_for = [10256, 80483, 20437, 32899, 20427, 44518, 38986]
mes_2025_mat = [0, 0, 2427, 0, 0, 0, 0]

# País de origen: top 6 por empresa, % del FOB total 2022-jul.2026.
paises_rep = [("Estados Unidos", 68.8), ("India", 7.5), ("Turquía", 7.5), ("China", 6.6), ("Reino Unido", 4.7), ("Brasil", 2.7)]
paises_for = [("Estados Unidos", 80.3), ("Francia", 6.6), ("México", 3.8), ("China", 1.5), ("España", 1.3), ("Alemania", 1.2)]
paises_mat = [("Estados Unidos", 49.0), ("Turquía", 29.9), ("Alemania", 9.3), ("China", 4.2), ("Italia", 2.6), ("Rep. Checa", 1.1)]

# Importaciones etiquetadas literalmente "MAXIFORCE" en el catálogo COMPLETO de Fortrac/Mateel
# (no solo dentro de los 10 SKU ancla, a diferencia de la hoja "Competencia Maxiforce") —
# calculado 2026-09-03 buscando el texto "MAXIFORCE" en los 5 campos de Descripción Comercial
# del mismo export usado en el resto de esta hoja.
mx_years = ["2022", "2023", "2024", "2025", "2026*"]
mx_fob_rep = [399806, 400188, 498663, 533448, 318488]
mx_fob_for = [2253, 0, 0, 14547, 7844]
mx_fob_mat = [0, 2962, 12404, 0, 0]
mx_unid_for = [389, 0, 0, 913, 381]
mx_unid_mat = [0, 206, 968, 0, 0]
MX_TOTAL_REP = sum(mx_fob_rep)
MX_TOTAL_FOR = sum(mx_fob_for)
MX_TOTAL_MAT = sum(mx_fob_mat)
MX_UNID_FOR = sum(mx_unid_for)
MX_UNID_MAT = sum(mx_unid_mat)

# Cada fila = 1 DUA con al menos una línea Maxiforce — "canasta" describe el tipo de compra.
mx_duas_for = [
    ("dic-2022", "179869", "Kit completo de reconstrucción: pistones/camisas, cojinetes, juntas, retenes, válvulas — 29 líneas"),
    ("jul-2025", "107339", "Kit completo: bombas agua/aceite/combustible, camisas, cojinetes, retenes, juntas — 40 líneas"),
    ("ago-2025", "132784", "Kit completo: bombas, kits pistón/camisa, cojinetes, retenes, juntas — 20 líneas"),
    ("nov-2025", "194126", "Kit completo: cojinetes, retenes, bombas de agua, kit pistón/camisa, pernos culata — 27 líneas"),
    ("mar-2026", "36088", "Kit completo: bombas, cojinetes, retenes, kit pistón/camisa, juntas — 22 líneas"),
    ("jul-2026", "111002", "Kit completo + 1 kit de reparación de motor turbo (US$590) — 35 líneas"),
]
MESES_2026 = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
# FOB Maxiforce mes a mes, ene-jul 2026, calculado con el mismo criterio (texto "MAXIFORCE" en
# los 5 campos de Descripción Comercial) sobre las TRES empresas — Repaglas incluido, para ver
# si el ritmo de restock de los rivales coincide con el propio.
mx_2026_rep = [11830, 78260, 53720, 59585, 25029, 30493, 59572]
mx_2026_for = [0, 0, 3194, 0, 0, 0, 4651]
mx_2026_mat = [0, 0, 0, 0, 0, 0, 0]

mx_duas_mat = [
    ("jun-2023", "78300", "Kit completo: culata, cojinetes, retenes, bombas, kits de retenes hidráulicos — 19 líneas"),
    ("ago-2024", "126614", "Kit completo: válvulas, cojinetes, bomba aceite, camisa, kit de juntas O/H — 17 líneas"),
    ("ago-2024", "130516", "Kit de reparación de motor completo (US$1,254) + cojinetes/válvulas/camisas — 25 líneas"),
]

# Precio FOB/unidad promedio pagado por Fortrac/Mateel vs. el de Repaglas, SOLO en los códigos
# ancla donde ambos compraron producto etiquetado Maxiforce (no equivalente/otra marca).
mx_precio = [
    # (oem, producto, precio_rep, precio_for, unid_for, precio_mat, unid_mat, nota)
    ("RE500734", "Bomba de agua motor", 75.63, 75.52, 21, None, 0, ""),
    ("RE66820", "Jgo. anillos de motor", 12.72, 14.69, 42, 15.24, 46, ""),
    ("RE507850", "Kit camisa/pistón", 73.59, 78.71, 36, 53.00, 6, "Mateel: kit de retenes hidráulicos, variante más chica — no 100% comparable"),
    ("RE507920", "Kit camisa/pistón", 75.88, 83.42, 24, 75.37, 16, ""),
    ("RE501455", "Jgo. empaquetaduras", 80.99, 91.58, 7, 88.75, 5, ""),
    ("RE504914", "Bomba de aceite motor", 86.12, 81.01, 18, 79.46, 9, ""),
]

# Top 10 categorías (partida arancelaria) de Fortrac por FOB total 2022-jul.2026, con el
# desglose año a año — para la tabla "qué trae más Fortrac cada año".
FOR_CAT_AÑOS = ["2022", "2023", "2024", "2025", "2026*"]
for_categorias_anio = [
    ("Aros de obturación (retenes)", [51787, 43979, 50164, 63482, 48597]),
    ("Motores completos (émbolo, >130 KW)", [0, 0, 18999, 11846, 127564]),
    ("Partes de motor 84.07/84.08", [20545, 26837, 18875, 20678, 16284]),
    ("Partes de máquinas 84.26/84.29/84.30", [31235, 16410, 14509, 19517, 15630]),
    ("Bombas (las demás)", [60511, 4305, 5688, 9504, 9308]),
    ("Filtros: aparatos para filtrar lubricante/carburante", [13349, 15029, 26334, 16328, 7007]),
    ("Bombas de aceite de motor", [25828, 8668, 12366, 22167, 5458]),
    ("Cajas de cojinetes s/rodamientos", [11719, 6511, 13671, 21417, 20498]),
    ("Émbolos (pistones) de motor 84.08", [21279, 13529, 8035, 15090, 8700]),
    ("Partes de árbol de transmisión (levas/cigüeñal)", [15439, 14118, 8312, 9548, 12558]),
]


def usd(n):
    return f"US$ {n:,.0f}"


def bar_years_3(cats, r, f, m, height=340):
    fig = go.Figure()
    fig.add_bar(x=cats, y=r, name="Repaglas", marker_color=REP)
    fig.add_bar(x=cats, y=f, name="Fortrac", marker_color=FOR)
    fig.add_bar(x=cats, y=m, name="Mateel", marker_color=MAT)
    fig.update_layout(
        barmode="group", height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def bar_years_2(cats, f, m, height=280):
    fig = go.Figure()
    fig.add_bar(x=cats, y=f, name="Fortrac", marker_color=FOR)
    fig.add_bar(x=cats, y=m, name="Mateel", marker_color=MAT)
    fig.update_layout(
        barmode="group", height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def bar_month_2y(months, v25, v26, color, height=260):
    fig = go.Figure()
    fig.add_bar(x=months, y=v25, name="2025", marker_color="#c7c2b8")
    fig.add_bar(x=months, y=v26, name="2026", marker_color=color)
    fig.update_layout(
        barmode="group", height=height, margin=dict(l=10, r=10, t=30, b=10), showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def hbar_pct(paises, color, height=200):
    fig = go.Figure()
    fig.add_bar(
        y=[p[0] for p in paises][::-1], x=[p[1] for p in paises][::-1],
        orientation="h", marker_color=color, text=[f"{p[1]:.1f}%" for p in paises][::-1], textposition="outside",
    )
    fig.update_layout(
        height=height, margin=dict(l=10, r=30, t=10, b=10), showlegend=False,
        xaxis=dict(ticksuffix="%", range=[0, 100]),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ================= HEADER =================
st.markdown("###### 🔩 INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("Fortrac y Mateel — perfil completo")
st.markdown(
    "**Fortrac S.A.C.** (RUC 20394004643) y **Mateel E.I.R.L.** (RUC 20601122015) ya habían aparecido en "
    "\"SKU Ancla\" y \"Competencia Maxiforce\" como rivales recurrentes, pero solo dentro de los 10 códigos "
    "OEM ancla. Esta hoja mira su **catálogo completo** de importación — para saber si son competidores "
    "chicos o grandes en términos absolutos, no solo en esa canasta puntual."
)
st.caption(
    "Periodo: **enero 2022 – julio 2026** · Fuente: **ADEX Data Trade** sobre registros de SUNAT / Aduanas · "
    "1 export por RUC, sin truncar (11,496 líneas) · Repaglas: mismo histórico completo de la hoja "
    "\"Frente Dinámica\""
)

st.divider()

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("FOB Fortrac 2022–jul.26", usd(TOTAL_FOR), f"{TOTAL_FOR/TOTAL_REP*100:.0f}% del FOB de Repaglas")
k2.metric("FOB con marca \"John Deere\" (Fortrac)", "91.1%", "vs. 28.8% en Mateel")
k3.metric("Crecimiento repuestos, ene-jul 2026", "+46%", "Fortrac, excl. 1 lote de motores · Repaglas: −6.7%")
k4.metric("¿Compran marca Maxiforce genuina?", "Sí, ambos", "Fortrac: 6 restocks 2022-jul.26 · Mateel: 3, ninguno desde ago-2024")

st.divider()

# ================= SECCIÓN 1: EVOLUCIÓN ANUAL =================
st.subheader("Evolución de FOB importado, año a año")
st.write(
    "Fortrac no es un jugador chico: importa el equivalente a **63% del FOB histórico de Repaglas** "
    "(US$2.23M vs. US$3.55M, 2022–jul.2026) — muy por encima de lo que sugería su presencia \"marginal\" "
    "dentro de los 10 SKU ancla. Mateel es bastante más chico (11% del FOB de Repaglas), pero su volumen "
    "se disparó en 2026. **2026 es parcial, solo hasta julio**, igual que en el resto del dashboard."
)
st.plotly_chart(bar_years_3(years, fob_rep, fob_for, fob_mat), use_container_width=True)
st.caption("2026 (\"2026*\") es un solo total parcial ene-jul — mismo criterio que el resto del dashboard. Su desglose mes a mes está justo abajo, en su propia escala.")

st.markdown("#### 2026 mes a mes (ene-jul) — el detalle detrás de la barra \"2026*\"")
st.write(
    "En el gráfico de arriba, la barra 2026 es chica al lado de un año completo — no porque falte data, sino "
    "porque son 7 meses contra 12. Este gráfico usa su propia escala para que se vea el detalle mes a mes de "
    "lo que ya pasó este año."
)
st.plotly_chart(bar_years_3(MESES_2026, mes_2026_rep, mes_2026_for, mes_2026_mat, height=300), use_container_width=True, key="mes_2026_general")
st.dataframe(
    {
        "Empresa": ["Repaglas", "Fortrac", "Mateel"],
        "2022": [usd(fob_rep[0]), usd(fob_for[0]), usd(fob_mat[0])],
        "2023": [usd(fob_rep[1]), usd(fob_for[1]), usd(fob_mat[1])],
        "2024": [usd(fob_rep[2]), usd(fob_for[2]), usd(fob_mat[2])],
        "2025": [usd(fob_rep[3]), usd(fob_for[3]), usd(fob_mat[3])],
        "2026*": [usd(fob_rep[4]), usd(fob_for[4]), usd(fob_mat[4])],
        "Total 2022-jul.26": [usd(TOTAL_REP), usd(TOTAL_FOR), usd(TOTAL_MAT)],
    },
    use_container_width=True, hide_index=True,
)

st.divider()

# ================= SECCIÓN 2: YTD 2025 vs 2026 =================
st.subheader("Ene-jul 2025 vs. ene-jul 2026 — la brecha se está abriendo")
c1, c2, c3 = st.columns(3)
c1.metric("Repaglas", f"{usd(ytd_rep[1])}", f"{(ytd_rep[1]/ytd_rep[0]-1)*100:+.1f}% vs. ene-jul 2025", delta_color="inverse")
c2.metric("Fortrac", f"{usd(ytd_for[1])}", f"{(ytd_for[1]/ytd_for[0]-1)*100:+.1f}% vs. ene-jul 2025")
c3.metric("Mateel", f"{usd(ytd_mat[1])}", f"{(ytd_mat[1]/ytd_mat[0]-1)*100:+.0f}% vs. ene-jul 2025")
st.markdown(
    f"<div class='callout'><b>Ojo con el dato bruto de Fortrac (+98%):</b> un solo DUA de enero 2026 "
    f"(10 motores completos John Deere \"bare engine\", {usd(FOR_DUA_MOTORES)}) infla el número — es "
    f"importación de motor completo, no repuesto, y no compite directamente con el catálogo de Repaglas. "
    f"<b>Descontando ese lote</b>, el crecimiento real de Fortrac en repuestos es <b>+46.4%</b> — bien por "
    f"encima igual, y en la dirección opuesta a Repaglas (−6.7% en la misma ventana). El salto de Mateel "
    f"(de US$2,427 a US$64,366) parte de una base casi nula — no viene de un solo lote grande, son varios "
    f"DUA de sellos, mangueras y kits repartidos entre febrero y julio, pero conviene ver un año completo "
    f"antes de leerlo como tendencia consolidada.</div>",
    unsafe_allow_html=True,
)

st.markdown("#### Mes a mes, ene-jul: 2025 vs. 2026")
st.write(
    "Mismo periodo (enero a julio), un año contra el otro, por empresa. La barra clara es 2025, la de color "
    "es 2026 — así se ve en qué meses específicos está la diferencia, no solo el total acumulado."
)
mcol1, mcol2, mcol3 = st.columns(3)
with mcol1:
    st.markdown("**Repaglas**")
    st.plotly_chart(bar_month_2y(MESES_2026, mes_2025_rep, mes_2026_rep, REP), use_container_width=True, key="m2y_rep")
with mcol2:
    st.markdown("**Fortrac**")
    st.plotly_chart(bar_month_2y(MESES_2026, mes_2025_for, mes_2026_for, FOR), use_container_width=True, key="m2y_for")
with mcol3:
    st.markdown("**Mateel**")
    st.plotly_chart(bar_month_2y(MESES_2026, mes_2025_mat, mes_2026_mat, MAT), use_container_width=True, key="m2y_mat")
st.caption(
    "Repaglas cae en la mayoría de los meses de 2026 salvo febrero. El pico de Fortrac en enero-2026 "
    "(US$229K) es el DUA de los 10 motores completos ya explicado arriba; sin ese mes, su patrón mensual es "
    "más parejo que el de Repaglas. Mateel prácticamente no compró nada en 2025 (solo marzo) — su actividad "
    "2026 es, en términos relativos, toda nueva."
)

st.divider()

# ================= SECCIÓN 3: CATEGORÍAS DE MOTOR =================
st.subheader("Qué importan — cabeza a cabeza contra el catálogo de Repaglas")
st.write(
    "Las categorías de mayor FOB de **Fortrac** (aros de obturación, partes de motor 84.07/84.08, bombas de "
    "aceite, cajas de cojinetes) son casi un calco de las categorías donde Repaglas más importa — a diferencia "
    "de Dinámica (transmisión/ejes) o Mateel (grifería/engranajes), Fortrac compite en el mismo terreno de "
    "**motor**, no en uno adyacente. **Mateel** es harina de otro costal: solo 28.8% de su FOB menciona "
    "\"John Deere\" y su categoría más grande es grifería/válvulas, no motor."
)
st.dataframe(
    {
        "Categoría (partida arancelaria)": [c[0] for c in categorias_motor],
        "Repaglas": [usd(c[1]) for c in categorias_motor],
        "Fortrac": [usd(c[2]) for c in categorias_motor],
        "Mateel": [usd(c[3]) for c in categorias_motor],
        "¿Quién lidera?": [
            "🔴 Fortrac" if c[2] > c[1] else "🔵 Repaglas" for c in categorias_motor
        ],
    },
    use_container_width=True, hide_index=True,
)
st.markdown(
    "<div class='callout-op'><b>Fortrac ya importa más que Repaglas en 3 de las 12 categorías de motor</b>: "
    "aros de obturación/retenes (US$258K vs. US$139K) y, sobre todo, <b>las dos líneas de filtro de motor</b> "
    "(US$78K + US$57K = US$135K vs. solo US$43K de Repaglas). Esto conecta directo con el hallazgo de filtros "
    "de la hoja \"IPESA\": no es solo IPESA quien le saca ventaja a Repaglas ahí — Fortrac, un competidor mucho "
    "más chico en tamaño total, también le gana en esa categoría específica. Confirma que filtros de motor es "
    "la brecha más consistente del proyecto, repetida en dos competidores distintos.</div>",
    unsafe_allow_html=True,
)

st.markdown("#### Detalle: qué trae más Fortrac cada año (top 10 categorías)")
st.write(
    "Las mismas categorías, pero solo Fortrac y año a año — para ver si el mix cambia con el tiempo, no solo "
    "el acumulado. Elige un año para reordenar la tabla por lo más relevante de **ese** año; \"Total\" la "
    "ordena por el acumulado 2022–jul.2026 (vista por defecto)."
)
filtro_anio_for = st.selectbox(
    "Ordenar por", options=["Total 2022-jul.26"] + FOR_CAT_AÑOS, index=0, key="filtro_cat_for",
)
if filtro_anio_for == "Total 2022-jul.26":
    orden_idx = None
else:
    orden_idx = FOR_CAT_AÑOS.index(filtro_anio_for)
filas_cat = [(cat, vals, sum(vals)) for cat, vals in for_categorias_anio]
if orden_idx is not None:
    filas_cat.sort(key=lambda x: -x[1][orden_idx])
else:
    filas_cat.sort(key=lambda x: -x[2])
st.dataframe(
    {
        "Categoría (partida arancelaria)": [f[0] for f in filas_cat],
        "2022": [usd(f[1][0]) for f in filas_cat],
        "2023": [usd(f[1][1]) for f in filas_cat],
        "2024": [usd(f[1][2]) for f in filas_cat],
        "2025": [usd(f[1][3]) for f in filas_cat],
        "2026*": [usd(f[1][4]) for f in filas_cat],
        "Total": [usd(f[2]) for f in filas_cat],
    },
    use_container_width=True, hide_index=True,
)
st.caption(
    "Retenes es la única categoría presente los 5 años sin huecos — la más estable del catálogo de Fortrac. "
    "Motores completos (>130 KW) pasa de US$0 en 2022-2023 a US$127.6K en 2026, el mayor salto de la tabla, "
    "pero es importación de motor entero, no repuesto (ver nota de la Sección 2). Filtros y bombas de aceite "
    "tuvieron su mejor año en 2025 y bajaron en 2026 — vigilar si se recuperan en lo que falta del año."
)

st.divider()

# ================= SECCIÓN 4: PAÍS DE ORIGEN =================
st.subheader("País de origen")
st.write(
    "Las tres empresas concentran su abastecimiento en Estados Unidos (repuesto genuino/OEM), pero no es lo "
    "único: Fortrac trae un 6.6% de Francia, Mateel diversifica fuerte hacia Turquía (30% del FOB) y "
    "Alemania (9.3%) — consistente con un catálogo menos atado a la marca John Deere que el de Fortrac."
)
pcol1, pcol2, pcol3 = st.columns(3)
with pcol1:
    st.markdown("**Repaglas**")
    st.plotly_chart(hbar_pct(paises_rep, REP), use_container_width=True, key="pais_rep")
with pcol2:
    st.markdown("**Fortrac**")
    st.plotly_chart(hbar_pct(paises_for, FOR), use_container_width=True, key="pais_for")
with pcol3:
    st.markdown("**Mateel**")
    st.plotly_chart(hbar_pct(paises_mat, MAT), use_container_width=True, key="pais_mat")
st.caption("% del FOB total 2022–jul.2026, top 6 países de origen por empresa.")

st.divider()

# ================= SECCIÓN 5: ¿IMPORTAN MARCA MAXIFORCE? =================
st.subheader("¿Fortrac y Mateel importan marca Maxiforce genuina? Sí, los 4.5 años")
st.write(
    "Buscando el texto **\"MAXIFORCE\"** en las 5 descripciones comerciales de todo el catálogo de ambas "
    "empresas (no solo dentro de los 10 SKU ancla, como en la hoja \"Competencia Maxiforce\"), aparecen "
    "**271 líneas**: Fortrac trajo Maxiforce en **6 embarques** entre dic.2022 y jul.2026 (1,683 unidades, "
    "US$24.6K), y Mateel en **3 embarques** entre jun.2023 y ago.2024 (1,174 unidades, US$15.4K) — y no ha "
    "vuelto a comprar la marca desde entonces."
)
st.markdown(
    "<div class='callout-op'><b>Esto es más grande de lo que mostraba \"Competencia Maxiforce\".</b> Esa hoja "
    "solo contaba unidades Maxiforce dentro de los 10 SKU ancla (Fortrac: 148 unidades). Mirando su catálogo "
    "completo, Fortrac trajo <b>1,683 unidades</b> con esa marca — 11× más — porque la mayoría de sus compras "
    "Maxiforce son piezas chicas (cojinetes, retenes, juntas, válvulas) que no están entre los 10 códigos "
    "seguidos, pero forman parte del mismo kit de reconstrucción de motor. El número real de competencia de "
    "marca es bastante mayor al reportado hasta ahora.</div>",
    unsafe_allow_html=True,
)
st.plotly_chart(bar_years_3(mx_years, mx_fob_rep, mx_fob_for, mx_fob_mat), use_container_width=True)
st.caption(
    "Nótese la escala: el eje mezcla el Maxiforce de Repaglas (US$318K-533K/año, prácticamente todo su "
    "negocio) con el de Fortrac y Mateel (unos pocos miles por año) — a propósito, para que el tamaño "
    "relativo real quede claro en un solo gráfico."
)

st.markdown("#### Cuadro año a año — con filtro por año")
filtro_anio_mx = st.selectbox(
    "Ver", options=["Todos los años (2022-jul.26)"] + mx_years, index=0, key="filtro_anio_mx",
)
if filtro_anio_mx == "Todos los años (2022-jul.26)":
    st.dataframe(
        {
            "Empresa": ["Repaglas", "Fortrac", "Mateel"],
            "2022": [usd(mx_fob_rep[0]), usd(mx_fob_for[0]), usd(mx_fob_mat[0])],
            "2023": [usd(mx_fob_rep[1]), usd(mx_fob_for[1]), usd(mx_fob_mat[1])],
            "2024": [usd(mx_fob_rep[2]), usd(mx_fob_for[2]), usd(mx_fob_mat[2])],
            "2025": [usd(mx_fob_rep[3]), usd(mx_fob_for[3]), usd(mx_fob_mat[3])],
            "2026*": [usd(mx_fob_rep[4]), usd(mx_fob_for[4]), usd(mx_fob_mat[4])],
            "Total": [usd(MX_TOTAL_REP), usd(MX_TOTAL_FOR), usd(MX_TOTAL_MAT)],
        },
        use_container_width=True, hide_index=True, key="mx_tabla_todos",
    )
else:
    i = mx_years.index(filtro_anio_mx)
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric(f"Repaglas — Maxiforce {filtro_anio_mx}", usd(mx_fob_rep[i]))
    mc2.metric(f"Fortrac — Maxiforce {filtro_anio_mx}", usd(mx_fob_for[i]), "sin compras" if mx_fob_for[i] == 0 else None)
    mc3.metric(f"Mateel — Maxiforce {filtro_anio_mx}", usd(mx_fob_mat[i]), "sin compras" if mx_fob_mat[i] == 0 else None)
st.caption("\"Solo Maxiforce\" = únicamente líneas cuya descripción comercial menciona el texto \"MAXIFORCE\" — no todo el catálogo John Deere/genérico de cada empresa.")

st.markdown("#### Mes a mes en 2026 — ¿el ritmo de los rivales se parece al de Repaglas?")
st.write(
    "Repaglas trae Maxiforce **los 7 meses del año** (chico en algunos, grande en otros, pero sin huecos) — "
    "un flujo de reposición continuo. Fortrac solo tuvo actividad en **2 de los 7 meses** (marzo y julio) y "
    "Mateel en **ninguno**. No hay coincidencia de calendario con Repaglas (no hay señal de que compren justo "
    "después o antes de un embarque tuyo) — el ritmo de Fortrac responde a su propio ciclo de reposición de "
    "kit de taller, no al tuyo."
)
st.dataframe(
    {
        "Mes (2026)": MESES_2026,
        "Repaglas": [usd(v) for v in mx_2026_rep],
        "Fortrac": [usd(v) if v else "—" for v in mx_2026_for],
        "Mateel": [usd(v) if v else "—" for v in mx_2026_mat],
    },
    use_container_width=True, hide_index=True,
)
st.caption(
    f"Total ene-jul 2026: Repaglas {usd(sum(mx_2026_rep))} en 7 embarques distintos (compra Maxiforce "
    f"prácticamente cada mes) · Fortrac {usd(sum(mx_2026_for))} en 2 embarques (mar y jul) · Mateel {usd(0)}, "
    f"sin compras. La cadencia mensual no aporta más que confirmar lo que ya dicen las 2 fechas de Fortrac: "
    f"con solo 2-3 restocks al año en cada rival, un cuadro mes a mes de ellos solos es mayormente ceros — "
    f"se vuelve útil recién al ponerlo al lado del propio ritmo de Repaglas, como aquí."
)

st.markdown("#### Cadencia de restock — cada embarque es una \"canasta\" de reconstrucción de motor")
st.write(
    "No son compras sueltas de una sola pieza: cada DUA junta 17-40 líneas distintas de Maxiforce en el "
    "mismo envío — pistones, camisas, cojinetes, retenes, juntas, bombas de agua/aceite/combustible, "
    "válvulas — el perfil de compra de alguien armando **kits completos de reparación de motor**, no de un "
    "distribuidor reponiendo estantería SKU por SKU."
)
st.dataframe(
    {
        "Fecha": [d[0] for d in mx_duas_for],
        "DUA": [d[1] for d in mx_duas_for],
        "Contenido de la canasta": [d[2] for d in mx_duas_for],
    },
    use_container_width=True, hide_index=True, key="mx_duas_for",
)
st.caption("Fortrac — 6 embarques. Gap de 2.5 años entre dic-2022 y jul-2025; desde entonces, restock cada 3-4 meses (jul, ago, nov-2025; mar, jul-2026) — ritmo estable, no oportunista.")
st.dataframe(
    {
        "Fecha": [d[0] for d in mx_duas_mat],
        "DUA": [d[1] for d in mx_duas_mat],
        "Contenido de la canasta": [d[2] for d in mx_duas_mat],
    },
    use_container_width=True, hide_index=True, key="mx_duas_mat",
)
st.caption("Mateel — 3 embarques, los 2 últimos el mismo mes (ago-2024). Sin compras de Maxiforce en los 23 meses siguientes (hasta jul-2026, corte de este reporte).")

st.markdown("#### El dato que cambia la estrategia: no ganan por precio")
st.write(
    "Comparando el FOB/unidad que pagó cada uno por el **mismo código OEM, misma marca Maxiforce** (no un "
    "equivalente), contra lo que paga Repaglas en el mismo periodo:"
)
st.dataframe(
    {
        "SKU (OEM)": [f"{p[0]} — {p[1]}" for p in mx_precio],
        "FOB/u Repaglas": [f"${p[2]:.2f}" for p in mx_precio],
        "FOB/u Fortrac": [f"${p[3]:.2f} ({p[4]}u)" for p in mx_precio],
        "vs. Repaglas": [f"{(p[3]/p[2]-1)*100:+.0f}%" for p in mx_precio],
        "FOB/u Mateel": [f"${p[5]:.2f} ({p[6]}u)" if p[5] else "— no compró" for p in mx_precio],
        "vs. Repaglas ": [f"{(p[5]/p[2]-1)*100:+.0f}%" if p[5] else "" for p in mx_precio],
    },
    use_container_width=True, hide_index=True,
)
st.caption("Mateel en RE507850 compró una variante más chica (kit de retenes hidráulicos, no el kit completo) — el −28% no es comparable 1 a 1, dejado en la tabla por transparencia.")
st.markdown(
    "<div class='callout'><b>Fortrac paga IGUAL o MÁS que Repaglas en 5 de 6 códigos comparables</b> "
    "(de −0.1% a +16%), a pesar de comprar lotes de 7-42 unidades contra los cientos que compra Repaglas. "
    "Solo en RE504914 paga algo menos (−6%). <b>No hay evidencia de que Fortrac tenga una fuente más barata "
    "del "
    "mismo producto</b> — están comprando el mismo catálogo Maxiforce, con el mismo número de parte "
    "(\"TRE...\"), del mismo país de origen (Estados Unidos), a un costo de fábrica similar o mayor al de "
    "Repaglas.</div>",
    unsafe_allow_html=True,
)

st.markdown("#### Lectura comercial y de cadena de suministro")
st.markdown(
    """
1. **Repaglas no tiene exclusividad de la marca Maxiforce en Perú.** Fortrac y Mateel acceden al mismo
   catálogo, con el mismo número de parte del fabricante, desde el mismo origen (EE.UU.). Si no existe hoy
   un acuerdo de distribución exclusiva o territorial con el fabricante/mayorista de Maxiforce, esta es la
   conversación a abrir — es la palanca de mayor impacto de todo este hallazgo, más allá del tamaño actual
   de Fortrac o Mateel.
2. **La ventaja de volumen de Repaglas no se está capturando en precio de compra.** Repaglas compra
   cientos de unidades por código y paga igual o más que Fortrac, que compra decenas. Eso es una señal para
   ir al proveedor a negociar un descuento por volumen o rebate anual escalonado — hoy esa escala no está
   generando ninguna ventaja de costo medible.
3. **Si Fortrac no gana por costo de compra, su amenaza (si existe) está en el mercado local**: precio de
   reventa, margen más chico, o servicio/cercanía al taller. Vale la pena un ejercicio de \"comprador
   fantasma\" sobre el precio de venta de Fortrac en Lima para saber si estos precios de importación
   similares se traducen en un precio final más barato al cliente (competencia real de precio) o si
   Fortrac simplemente tiene un margen menor (no es una amenaza de pricing para Repaglas).
4. **El patrón de compra de Fortrac (kit completo de reconstrucción en cada embarque) sugiere que atiende
   talleres que hacen overhaul integral de motor**, no una demanda de repuesto suelto. Vale la pena revisar
   si Repaglas ya vende un \"kit de reparación completa\" empaquetado con el mismo criterio (pistón + camisa
   + cojinetes + juntas + retenes + bombas en un solo pedido) o si hoy se vende todo por separado — podría
   ser una oportunidad comercial además de una respuesta competitiva.
5. **Cadencia a vigilar**: desde que Fortrac retomó la compra de Maxiforce en jul-2025, restockea cada 3-4
   meses de forma consistente (jul, ago, nov-2025; mar, jul-2026). Con ese ritmo, el siguiente pedido
   esperado cae entre **octubre y diciembre 2026** — si no llega, es señal de que Fortrac está bajando el
   pie; si llega antes o más grande, es señal de que está acelerando.
6. **Mateel no es una amenaza de marca activa hoy.** No compra Maxiforce desde agosto de 2024 (23 meses),
   pese a que su FOB total (todas las marcas) se disparó en 2026 — ese crecimiento viene de otra parte de su
   catálogo, no de competir con la línea Maxiforce de Repaglas. Monitorear, no priorizar.
"""
)

st.divider()

# ================= SECCIÓN 6: SÍNTESIS =================
st.subheader("Relectura: Fortrac no es un rival marginal")
st.markdown(
    """
1. **Cambio de marco.** Dentro de los 10 SKU ancla, Fortrac aparecía como un rival menor (2-9% de share
   por código). Visto en su catálogo completo, es un importador de **US$2.23M en 4.5 años, 91.1% marca
   John Deere, casi todo en categorías de motor** — el mismo terreno donde Repaglas construyó su liderazgo.
   Es chico comparado con IPESA (US$120.6M en repuestos), pero grande comparado con la escala real de
   Repaglas: **63% de su FOB histórico**, no un jugador anecdótico.
2. **La brecha de crecimiento 2026 es la señal más urgente.** Con el mismo criterio ene-jul usado en el
   resto del dashboard, Repaglas cae 6.7% mientras Fortrac crece 46.4% (ya descontado el lote de motores
   completos) y Mateel se dispara desde una base casi nula. Ninguno de los dos explica todavía un cambio de
   share grande por sí solo, pero es la primera vez que se ve a un rival de motor acelerando mientras
   Repaglas desacelera en la misma ventana.
3. **Filtros de motor, otra vez.** Fortrac ya supera a Repaglas en las dos categorías de filtro — la misma
   brecha identificada con IPESA (pendiente #1 y #2 de la bitácora del proyecto) aparece confirmada en un
   segundo competidor independiente.
4. **No hay exclusividad de marca ni ventaja de costo de compra** — el hallazgo más importante de esta
   sección: Fortrac y Mateel compran el mismo Maxiforce genuino, al mismo costo de fábrica o más, que
   Repaglas. El terreno de competencia real está en el mercado local (precio de reventa, servicio, kits
   empaquetados), no en quién accede más barato al proveedor.
5. **Mateel es un perfil distinto**, más cercano a Dinámica (transmisión, grifería, engranajes) que a
   Fortrac o IPESA — la señal a vigilar ahí es el salto de volumen 2026, no el solapamiento de catálogo, y
   su compra de Maxiforce está inactiva desde ago-2024.
"""
)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "**Metodología.** Export único de ADEX Data Trade por los 2 RUC (Fortrac 20394004643, Mateel "
        "20601122015), ene.2022–jul.2026, 11,496 líneas sin truncar. Comparado contra el histórico completo "
        "de Repaglas (RUC 20118992009) del mismo periodo, usado también en la hoja \"Frente Dinámica\". "
        "\"% marca John Deere\" = FOB de líneas cuya descripción comercial (5 campos) menciona el texto "
        "\"JOHN DEERE\", como en la metodología de la hoja IPESA."
    )
with c2:
    st.markdown(
        "**Limitaciones.** El campo de marca es texto libre declarado por el importador — puede subestimar "
        "el verdadero % John Deere si algún despacho lo omite. El DUA de 10 motores completos de Fortrac "
        "(ene.2026) se identificó y descontó manualmente por ser importación de motor completo, no repuesto "
        "— podría haber otros lotes atípicos menores sin detectar. 2026 es parcial (solo hasta julio) en "
        "las tres empresas."
    )
