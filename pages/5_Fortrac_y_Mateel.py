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

paises = [
    ("Repaglas", 68.8, "Estados Unidos"),
    ("Fortrac", 80.3, "Estados Unidos"),
    ("Mateel", 49.0, "Estados Unidos"),
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
k4.metric("Categorías donde Fortrac ya supera a Repaglas", "3 de 12", "retenes y las 2 líneas de filtro")

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

st.divider()

# ================= SECCIÓN 4: PAÍS DE ORIGEN =================
st.subheader("País de origen")
st.write(
    "Las tres empresas concentran su abastecimiento en Estados Unidos (repuesto genuino/OEM), con Mateel "
    "algo más diversificado (Turquía es su segundo origen, 30% del FOB) — consistente con un catálogo menos "
    "atado a la marca John Deere."
)
st.dataframe(
    {
        "Empresa": [p[0] for p in paises],
        "% FOB desde Estados Unidos": [f"{p[1]:.1f}%" for p in paises],
    },
    use_container_width=True, hide_index=True,
)

st.divider()

# ================= SECCIÓN 5: SÍNTESIS =================
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
4. **Mateel es un perfil distinto**, más cercano a Dinámica (transmisión, grifería, engranajes) que a
   Fortrac o IPESA — la señal a vigilar ahí es el salto de volumen 2026, no el solapamiento de catálogo.
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
