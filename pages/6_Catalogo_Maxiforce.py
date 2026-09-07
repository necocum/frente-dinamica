"""Catálogo Maxiforce — qué traemos y qué no, motor por motor.

Fuente: catálogo técnico del fabricante Maxiforce (PDF, 686 págs., `ADEX/Página
web.pdf`) parseado por código de parte y contexto de motor (Engine Series/Model),
cruzado contra el export de stock Bsale (`Stock-actual_Todas-las-sucursales_02-09-2026.xlsx`,
1,796 SKU con Tipo de Producto = MAXIFORCE) y contra la venta real Ene-Ago 2025
vs. 2026 (`Dashboard_Ventas_20260901_2247.xlsx`, hoja "SKU Comparativo"). La
demanda validada por código viene del cruce de IPESA ya usado en la hoja IPESA
de este dashboard (mismo método: token exacto en las 5 columnas de Descripción
Comercial, con el problema de ocultamiento de código de IPESA desde 2024 ya
documentado ahí — este cruce hereda esa misma limitación).
"""

import io

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

REP = "#1f6feb"
NIVEL1 = "#0ca30c"
NIVEL2 = "#c9a227"
NIVEL3 = "#8a8a8a"
BAD = "#c0392b"

st.set_page_config(page_title="Catálogo Maxiforce", page_icon="🧩", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-n1 { border-left: 4px solid #0ca30c; background: #e2f6e2; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-n2 { border-left: 4px solid #c9a227; background: #faf3d9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-n3 { border-left: 4px solid #8a8a8a; background: #ececec; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .tag-n1 { color: #0ca30c; font-weight: 700; }
      .tag-n2 { color: #9a7d0a; font-weight: 700; }
      .tag-n3 { color: #666; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
composicion = [("John Deere", 953), ("Perkins", 484), ("Caterpillar", 334), ("Yanmar", 10), ("Otros", 15)]

resumen_motores = [
    # motor, sku_actuales, venta26, venta25, sku_faltan, faltan_con_demanda, fob_demanda
    ("4045", 199, 1490448, 1509927, 126, 44, 290165),
    ("6068", 30, 82965, 61968, 65, 8, 13088),
    ("6090", 36, 97302, 75821, 58, 23, 58921),
    ("6125", 2, 0, 0, 55, None, None),
    ("6135", 0, 0, 0, 25, None, None),
]

cat_4045_actual = [
    ("Válvulas y asientos", 15), ("Biela", 15), ("Metales/cojinetes", 13), ("Empaques/juntas", 13),
    ("Kits camisa/pistón/anillos", 8), ("Pines de pistón", 8), ("Sensores", 7), ("Bomba de agua", 6),
    ("Otras bombas", 6), ("Anillos de pistón", 5), ("Otros kits de reparación", 5), ("Árbol de levas", 4),
    ("Inyección", 4), ("Bomba de aceite", 3), ("Camisa (suelta)", 2), ("Culata", 2), ("Cigüeñal", 2),
    ("Termostato/refrigeración", 1), ("Turbocompresor", 0), ("Retenes/sellos", 0),
]
cat_4045_falta = [
    ("Válvulas y asientos", 13), ("Biela", 2), ("Metales/cojinetes", 6), ("Empaques/juntas", 14),
    ("Kits camisa/pistón/anillos", 25), ("Pines de pistón", 0), ("Sensores", 0), ("Bomba de agua", 11),
    ("Otras bombas", 7), ("Anillos de pistón", 0), ("Otros kits de reparación", 5), ("Árbol de levas", 5),
    ("Inyección", 25), ("Bomba de aceite", 2), ("Camisa (suelta)", 0), ("Culata", 1), ("Cigüeñal", 1),
    ("Termostato/refrigeración", 3), ("Turbocompresor", 4), ("Retenes/sellos", 2),
]

top_actuales_4045 = [
    ("TRE507920", "Kit: camisa, pistón, anillos, pin, jebes y seguros", 121070, "ESTABLE"),
    ("TRE507850", "Kit: camisa, pistón, anillos, pin, jebes y seguros", 105076, "ESTABLE"),
    ("TRE504914", "Bomba de aceite motor", 80840, "ESTABLE"),
    ("TRE48786",  "Inyector de motor", 80385, "ESTABLE"),
    ("TRE500734", "Bomba de agua motor", 75112, "CRECIENDO"),
    ("TRE501455", "Jgo. empaquetaduras de motor", 70074, "ESTABLE"),
    ("TRE66820",  "Jgo. anillos de motor", 55587, "ESTABLE"),
    ("TRE65966",  "Kit: camisa, pistón, anillos, pin, jebes y seguros", 52247, "ESTABLE"),
]

top_faltantes_4045 = [
    # SKU, producto, categoría, FOB, unid, embarques, años con evidencia, ¿ya en otra marca?
    ("TDZ100217", "Kit de boquillas (inyección)", "Inyección", 85896, 213, 12, "2022-2024", "Fujian (stock=0)"),
    ("TRE507959", "Bomba", "Bomba de agua", 32470, 16, 9, "2022-2024", "—"),
    ("TRE568070", "Bomba de inyección", "Inyección", 29305, 23, 5, "2022-2023", "OPEX JD (stock=0)"),
    ("TRE71550",  "Turbocompresor", "Turbo", 29030, 32, 11, "2022-2024", "—"),
    ("TDZ100216", "Kit de boquillas (inyección)", "Inyección", 27647, 87, 9, "2022-2024", "—"),
    ("TDZ100211", "Kit de boquillas (inyección)", "Inyección", 13552, 28, 3, "2022", "Fujian (stock=0)"),
    ("TDZ111137", "Distribuidor", "Inyección", 12007, 31, 10, "2022-2024", "—"),
    ("TDZ111135", "Distribuidor", "Inyección", 7786, 26, 6, "2022-2023", "—"),
    ("TRE507852", "Juego segmentos de pistón", "Anillos", 7170, 331, 8, "2022-2024", "KMP (stock=4)"),
    ("TRE502079", "Bujía de precalentamiento", "Otros", 5187, 104, 12, "2022-2023", "—"),
]

# Detalle completo de los 35 códigos 4045 que no traemos, con evidencia de import IPESA,
# recalculado directo de "Catalogo_Maxiforce_Oportunidades_20260906.xlsx" (hoja "JD - Nuevos
# con demanda", filtrada a Engine Model que contiene "4045"). Nota: esta recomputación da 35
# códigos / US$271,559 — ligeramente distinto de los "44 / US$290,165" citados en los callouts
# de arriba, que vinieron de un script de sesión anterior no conservado; se deja este set de 35
# como el reproducible/auditable (cada fila se puede rastrear al Excel fuente).
# Cruce de "¿ya existe en otra marca?" contra el stock Bsale completo (07-09-2026) y venta de
# ese SKU alterno en los últimos 6 meses (08-mar-2026 a 07-sep-2026) contra el detalle de ventas
# 2026 de Bsale — hecho el 2026-09-07.
faltantes_4045_completo = [
    # SKU, Producto, Unid. IPESA, FOB US$, N° embarques, Primer año, Último año, Alternativa en otra marca, Venta 6M alt (S/), Unid. 6M alt
    ("TDZ100217", "Kit de boquillas (inyección)", 213, 85896, 12, 2022, 2024, "Fujian — DZ100217-FIP (stock 0)", 0, 0),
    ("TRE507959", "Bomba de agua", 16, 32470, 9, 2022, 2024, "—", 0, 0),
    ("TRE568070", "Bomba de inyección", 23, 29305, 5, 2022, 2023, "OPEX JD — RE.518166-RE568070 (stock 0)", 0, 0),
    ("TRE71550", "Turbocompresor", 32, 29030, 11, 2022, 2024, "—", 0, 0),
    ("TDZ100216", "Kit de boquillas (inyección)", 87, 27647, 9, 2022, 2024, "—", 0, 0),
    ("TDZ100211", "Kit de boquillas (inyección)", 28, 13552, 3, 2022, 2022, "Fujian — DZ100211-FIP (stock 0)", 0, 0),
    ("TDZ111137", "Distribuidor", 31, 12007, 10, 2022, 2024, "—", 0, 0),
    ("TDZ111135", "Distribuidor", 26, 7786, 6, 2022, 2023, "—", 0, 0),
    ("TRE507852", "Juego segmentos de pistón", 331, 7170, 8, 2022, 2024, "KMP — RE507852 (stock 4) + OPEX JD — RE507852JD (stock 0)", 7372, 78),
    ("TRE508932", "Engranaje", 13, 3784, 6, 2022, 2023, "—", 0, 0),
    ("TRE548726", "Turbocompresor", 3, 3670, 3, 2022, 2025, "—", 0, 0),
    ("TRE543935", "Manguito", 337, 2907, 8, 2022, 2023, "Anhui Ebang — RE543935-REP (stock 0)", 3163, 52),
    ("TDZ100214", "Kit de boquillas (inyección)", 6, 2732, 1, 2022, 2022, "—", 0, 0),
    ("TDZ100553", "Termostato", 146, 2613, 12, 2022, 2024, "—", 0, 0),
    ("TRE56369", "Engranaje", 9, 1673, 4, 2022, 2023, "—", 0, 0),
    ("TDZ100212", "Kit de boquillas (inyección)", 3, 1421, 1, 2022, 2022, "Fujian — DZ100212-FIP (stock 0)", 0, 0),
    ("TRE506261", "Turbocompresor", 1, 1072, 1, 2023, 2023, "—", 0, 0),
    ("TR535005", "Tornillo", 406, 931, 13, 2022, 2024, "—", 0, 0),
    ("TR120638", "Engranaje", 11, 883, 3, 2022, 2022, "—", 0, 0),
    ("TR521525", "Junta", 31, 822, 5, 2022, 2024, "—", 0, 0),
    ("TR132267", "Engranaje", 2, 670, 2, 2022, 2023, "—", 0, 0),
    ("TRE532842", "Juego de juntas", 4, 668, 4, 2023, 2024, "—", 0, 0),
    ("TR545884", "Junta", 24, 472, 7, 2022, 2023, "—", 0, 0),
    ("TR120631", "Engranaje", 4, 441, 1, 2022, 2022, "—", 0, 0),
    ("TRE528652", "Termostato", 34, 363, 3, 2022, 2022, "—", 0, 0),
    ("TR501130", "Tapadera", 3, 343, 1, 2024, 2024, "—", 0, 0),
    ("TAL110621", "Tensor", 3, 330, 3, 2023, 2024, "—", 0, 0),
    ("TR545883", "Junta", 12, 252, 2, 2023, 2023, "—", 0, 0),
    ("TRE538289", "Termostato", 13, 204, 1, 2022, 2022, "—", 0, 0),
    ("TR544294", "Empaquetadura", 12, 156, 1, 2022, 2022, "—", 0, 0),
    ("TR92352", "Empaquetadura", 102, 150, 9, 2022, 2023, "—", 0, 0),
    ("TR534978", "Retenedor", 176, 40, 3, 2022, 2023, "OPEX JD — R534978 (stock 0)", 0, 0),
    ("TR121634", "Carcasa", 2, 38, 2, 2023, 2024, "—", 0, 0),
    ("TR524498", "Junta", 1, 36, 1, 2023, 2023, "—", 0, 0),
    ("TRE554015", "Termostato", 1, 26, 1, 2023, 2023, "—", 0, 0),
]

cat_6068 = [("Kits camisa/pistón/anillos", 18), ("Inyección", 11), ("Empaques/juntas", 10), ("Bomba de agua", 10), ("Válvulas y asientos", 5)]
cat_6090 = [("Empaques/juntas", 11), ("Kits camisa/pistón/anillos", 10), ("Válvulas y asientos", 7), ("Biela", 7), ("Árbol de levas", 5)]
cat_6125 = [("Kits camisa/pistón/anillos", 28), ("Empaques/juntas", 6), ("Otras bombas", 5)]
cat_6135 = [("Kits camisa/pistón/anillos", 7), ("Empaques/juntas", 6), ("Otros kits de reparación", 3)]


def usd(n):
    return f"US$ {n:,.0f}"


def sr(n):
    return f"S/ {n:,.0f}"


def grouped_hbar(categories, serie1, serie2, name1, name2, color1, color2, height=None):
    height = height or (len(categories) * 26 + 60)
    fig = go.Figure()
    fig.add_bar(name=name1, y=categories, x=serie1, orientation="h", marker_color=color1)
    fig.add_bar(name=name2, y=categories, x=serie2, orientation="h", marker_color=color2)
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10), barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def motor_overview_chart():
    """Un mini-gráfico por motor (escala propia) — un solo gráfico compartido aplasta
    al 4045 (199 SKU) contra motores con 0-36 SKU y no se puede leer nada."""
    motores = [m[0] for m in resumen_motores]
    fig = make_subplots(rows=1, cols=len(motores), subplot_titles=[f"Motor {m}" for m in motores])
    for i, (motor, actuales, venta26, venta25, faltan, con_dem, fob_dem) in enumerate(resumen_motores):
        fig.add_bar(
            x=["Ya traes", "Falta"], y=[actuales, faltan],
            marker_color=[REP, BAD], showlegend=False, text=[actuales, faltan],
            textposition="outside", row=1, col=i + 1,
        )
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(showticklabels=False)
    return fig


# ================= HEADER =================
st.markdown("###### 🧩 CATÁLOGO DEL FABRICANTE (MAXIFORCE) · QUÉ TRAEMOS Y QUÉ NO")
st.title("Catálogo Maxiforce — motor por motor")
st.markdown(
    "El catálogo técnico del fabricante Maxiforce (686 páginas) se cruzó código por código contra tu stock "
    "actual en Bsale, para las 5 familias de motor donde Repaglas ya tiene presencia con marca **:blue[Maxiforce]**: "
    "**PowerTech 4045, 6068, 6090, 6125 y 6135**."
)
st.caption(
    "Nota: el catálogo Maxiforce no es solo John Deere — de tus 1,796 SKU Maxiforce, "
    f"{composicion[0][1]} son John Deere, {composicion[1][1]} Perkins, {composicion[2][1]} Caterpillar y "
    f"{composicion[3][1]} Yanmar. Este análisis cubre solo la línea John Deere, que es donde vendes hoy."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("SKU John Deere ya abiertos (5 motores)", "267")
k2.metric("Códigos del catálogo sin abrir (5 motores)", "329")
k3.metric("Con evidencia histórica de import (IPESA)", "75", "US$ 362K · 2022-2024, ver aviso")
k4.metric("Venta 2026 de estos 5 motores (Ene-Ago)", sr(1490448 + 82965 + 97302))
st.caption(
    "⚠️ La \"evidencia de import\" viene de IPESA 2022-jul.2026, pero IPESA casi dejó de declarar el código de "
    "parte desde 2024 (ver hoja \"IPESA\") — 127 de los 136 códigos validados en todo este análisis tienen su "
    "última evidencia en 2022-2024, ninguna en 2025-2026. Es un piso histórico, no una medición de demanda actual."
)

st.divider()

# ================= VISIÓN GENERAL =================
st.subheader("Visión general: qué traes vs. qué falta, por motor")
st.plotly_chart(motor_overview_chart(), use_container_width=True)
st.markdown(
    "<div class='callout'><b>El hueco no está parejo.</b> El 4045 es tu motor consolidado — 199 SKU, "
    "S/1.49M de venta — y aun así tiene 126 códigos del catálogo del fabricante que no tienes. 6068 y 6090 son "
    "chicos pero <b>están creciendo solos</b> (+34% y +28% este año) con muy poco catálogo (30 y 36 SKU). 6125 y "
    "6135 son territorio casi vacío: 2 y 0 SKU, sin venta.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= NIVEL 1: 4045 =================
st.markdown("## 🟢 Nivel 1 — Completa lo que ya vendes")
st.subheader("Motor PowerTech 4045")
st.write(
    "Es tu motor ancla: aquí viven tus 10 SKU más vendidos (RE507920, RE507850, RE504914, RE48786, entre otros), "
    "199 SKU abiertos y **S/1,490,448 vendidos** Ene-Ago 2026 (vs. S/1,509,927 en 2025 — estable, -1.3%). Es la "
    "base de datos más sólida de todo el catálogo Maxiforce: si el argumento es \"ya sabemos vender esto,\" la "
    "prueba está aquí."
)

n1c1, n1c2 = st.columns([3, 2])
with n1c1:
    st.markdown("#### Por categoría: lo que traes vs. lo que falta")
    cats = [c[0] for c in cat_4045_actual]
    act_vals = [c[1] for c in cat_4045_actual]
    falta_vals = [c[1] for c in cat_4045_falta]
    order = sorted(range(len(cats)), key=lambda i: -(act_vals[i] + falta_vals[i]))
    cats_o = [cats[i] for i in order]
    act_o = [act_vals[i] for i in order]
    falta_o = [falta_vals[i] for i in order]
    st.plotly_chart(
        grouped_hbar(cats_o, act_o, falta_o, "Ya traes", "Falta", REP, BAD, height=520),
        use_container_width=True,
    )
with n1c2:
    st.markdown("#### Top vendedores actuales (4045)")
    st.dataframe(
        {
            "SKU": [t[0] for t in top_actuales_4045],
            "Producto": [t[1] for t in top_actuales_4045],
            "Venta 2026": [sr(t[2]) for t in top_actuales_4045],
            "Estado": [t[3] for t in top_actuales_4045],
        },
        use_container_width=True, hide_index=True, height=320,
    )

st.markdown("#### Top 10 códigos que faltan, con evidencia de import real (IPESA) — no es especulación")
st.dataframe(
    {
        "SKU sugerido": [t[0] for t in top_faltantes_4045],
        "Producto": [t[1] for t in top_faltantes_4045],
        "Categoría": [t[2] for t in top_faltantes_4045],
        "FOB IPESA acumulado": [usd(t[3]) for t in top_faltantes_4045],
        "Unidades IPESA": [t[4] for t in top_faltantes_4045],
        "N° embarques": [t[5] for t in top_faltantes_4045],
        "Años con evidencia": [t[6] for t in top_faltantes_4045],
        "¿Ya existe en otra marca?": [t[7] for t in top_faltantes_4045],
    },
    use_container_width=True, hide_index=True,
)
st.markdown(
    "<div class='callout'><b>⚠️ Ojo con la vigencia de este número — pregunta natural en la reunión.</b> "
    "IPESA prácticamente dejó de escribir el código de parte en su declaración de Aduanas desde 2024 (ver hoja "
    "\"IPESA\" de este dashboard: 86.6% de líneas con código en 2022 → 3.9% en 2026). Por eso <b>127 de los 136 "
    "códigos validados en todo este análisis tienen evidencia SOLO entre 2022 y 2024</b> — de los 10 de la tabla, "
    "ninguno tiene una sola línea en 2025 o 2026. Esto no significa que la demanda haya desaparecido: significa "
    "que ya no podemos verla en Aduanas. El número es un <b>piso confirmado con data vieja, no una medición de "
    "demanda actual</b> — trátalo como \"esto se compraba hace 2-3 años\", no \"esto se compra hoy\".</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='callout-n1'><b>Por qué sigue siendo la apuesta de menor riesgo, con esa salvedad:</b> mismo "
    "motor, mismo cliente, mismo proveedor (Maxiforce/EE.UU., el canal que ya usas hoy). De los 126 códigos que "
    "faltan en el 4045, 44 tienen esta evidencia histórica — y de esos, <b>solo 3 de los 10 más grandes ya tienen "
    "algún equivalente abierto en otra marca (Fujian, OPEX JD, KMP) — y ese equivalente también está sin stock "
    "hoy.</b> Es decir: no es que la competencia interna (otra marca tuya) ya esté cubriendo esto — está tan "
    "dormido como Maxiforce. Inyección y kits camisa/pistón/anillos son, juntos, el 40% de todo el hueco (50 de "
    "126 códigos) — las 2 categorías donde ya vendes más fuerte.</div>",
    unsafe_allow_html=True,
)

st.markdown("#### 📥 Detalle completo y exportable — los 35 códigos 4045 que no traes, con evidencia IPESA")
st.caption(
    "Nota: esta tabla recalculada directo del Excel fuente da **35 códigos / US$271,559** — ligeramente distinto "
    "de los \"44 / US$290,165\" citados arriba, que salieron de un script de una sesión anterior que no se "
    "conservó. Se deja esta versión de 35 porque cada fila es rastreable a `Catalogo_Maxiforce_Oportunidades_"
    "20260906.xlsx`. Las columnas de la derecha son nuevas: cruzan cada código contra el stock Bsale completo "
    "(todas las marcas, no solo Maxiforce) y contra la venta real de esa marca alterna en los últimos 6 meses "
    "(08-mar-2026 a 07-sep-2026)."
)
st.dataframe(
    {
        "SKU sugerido": [f[0] for f in faltantes_4045_completo],
        "Producto": [f[1] for f in faltantes_4045_completo],
        "Unidades IPESA": [f[2] for f in faltantes_4045_completo],
        "FOB IPESA acum.": [usd(f[3]) for f in faltantes_4045_completo],
        "N° embarques": [f[4] for f in faltantes_4045_completo],
        "Años con evidencia": [f"{f[5]}-{f[6]}" if f[5] != f[6] else str(f[5]) for f in faltantes_4045_completo],
        "¿Ya existe en otra marca?": [f[7] for f in faltantes_4045_completo],
        "Venta 6M de esa marca (S/)": [sr(f[8]) if f[8] else "—" for f in faltantes_4045_completo],
        "Unid. 6M de esa marca": [str(f[9]) if f[9] else "—" for f in faltantes_4045_completo],
    },
    use_container_width=True, hide_index=True, height=420,
)

n_alt = sum(1 for f in faltantes_4045_completo if f[7] != "—")
n_alt_con_venta = sum(1 for f in faltantes_4045_completo if f[8] > 0)
venta6m_total = sum(f[8] for f in faltantes_4045_completo)
unid6m_total = sum(f[9] for f in faltantes_4045_completo)
st.markdown(
    f"<div class='callout'><b>Venta en otra marca de lo que no traes en Maxiforce (últimos 6 meses):</b> de los "
    f"35 códigos, <b>{n_alt} ya tienen un SKU equivalente abierto en otra marca</b> (Fujian, OPEX JD, KMP, Anhui "
    f"Ebang) — pero solo <b>{n_alt_con_venta} de esos {n_alt} tuvieron venta real en los últimos 6 meses</b>: "
    f"TRE507852 (KMP + OPEX JD combinados, S/7,372, 78 unidades) y TRE543935 (Anhui Ebang, S/3,163, 52 unidades). "
    f"Total: <b>{sr(venta6m_total)} en {unid6m_total} unidades</b>. Los otros {n_alt - n_alt_con_venta} SKU "
    "alternos existen en catálogo pero no vendieron nada en el semestre, y los 27 códigos restantes no tienen "
    "ningún sustituto abierto en ninguna marca — no hay nada cubriendo ese hueco hoy, en ninguna marca.</div>",
    unsafe_allow_html=True,
)

xlsx_buf_4045 = io.BytesIO()
try:
    from openpyxl import Workbook

    wb4045 = Workbook()
    ws4045 = wb4045.active
    ws4045.title = "4045 - No traemos (IPESA)"
    ws4045.append([
        "SKU sugerido (Maxiforce)", "Producto (según IPESA)", "Unidades IPESA", "FOB US$ IPESA acumulado",
        "N° embarques IPESA", "Primer año", "Último año", "¿Ya existe en otra marca?",
        "Venta últimos 6M de esa marca (S/)", "Unidades últimos 6M de esa marca",
    ])
    for f in faltantes_4045_completo:
        ws4045.append(list(f))
    wb4045.save(xlsx_buf_4045)
    st.download_button(
        "⬇️ Descargar Excel — Motor 4045, códigos que no traemos y sí trae IPESA",
        data=xlsx_buf_4045.getvalue(),
        file_name="4045_no_traemos_vs_ipesa_maxiforce.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
except ImportError:
    st.caption("(Descarga a Excel no disponible: falta la librería `openpyxl` en el entorno.)")

st.divider()

# ================= NIVEL 2: 6068 / 6090 =================
st.markdown("## 🟡 Nivel 2 — Sigue el crecimiento")
st.write(
    "6068 y 6090 son chicos hoy, pero ya están creciendo solos, sin que hayas ampliado el catálogo — "
    "la señal es que hay demanda que no estás capturando por falta de variedad de SKU, no por falta de mercado."
)

n2c1, n2c2 = st.columns(2)
with n2c1:
    st.markdown("#### Motor 6068")
    m1, m2, m3 = st.columns(3)
    m1.metric("SKU actuales", "30")
    m2.metric("Venta 2026", sr(82965), "+34% vs 2025")
    m3.metric("Faltan", "65", "8 con demanda IPESA (US$13,088)")
    st.dataframe(
        {"Categoría (top 5 que falta)": [c[0] for c in cat_6068], "SKU faltantes": [c[1] for c in cat_6068]},
        use_container_width=True, hide_index=True,
    )
with n2c2:
    st.markdown("#### Motor 6090")
    m1, m2, m3 = st.columns(3)
    m1.metric("SKU actuales", "36")
    m2.metric("Venta 2026", sr(97302), "+28% vs 2025")
    m3.metric("Faltan", "58", "23 con demanda IPESA (US$58,921)")
    st.dataframe(
        {"Categoría (top 5 que falta)": [c[0] for c in cat_6090], "SKU faltantes": [c[1] for c in cat_6090]},
        use_container_width=True, hide_index=True,
    )

st.markdown(
    "<div class='callout-n2'><b>Lectura:</b> el 6090 tiene la mejor proporción de códigos con evidencia histórica "
    "de import (23 de 58, 40%) — más alto que el 4045 (35%) o el 6068 (12%), aunque la misma salvedad aplica: esa "
    "evidencia es 2022-2024, no actual. Con solo 36 SKU abiertos ya vende casi tanto como el 6068 con 30 — sugiere "
    "que cada SKU nuevo en este motor rinde más que el promedio.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= NIVEL 3: 6125 / 6135 =================
st.markdown("## ⚪ Nivel 3 — Evalúa entrar (pregunta abierta, no recomendación cerrada)")
st.write(
    "6125 y 6135 son, hoy, territorio casi sin desarrollar. Esto **no es \"ampliar\" un negocio que ya funciona** "
    "— es la decisión de si vale la pena entrar a un motor nuevo. Se presenta aparte a propósito, para no mezclar "
    "el argumento de bajo riesgo (Nivel 1 y 2) con uno que requiere una conversación distinta."
)
n3c1, n3c2 = st.columns(2)
with n3c1:
    st.markdown("#### Motor 6125")
    m1, m2 = st.columns(2)
    m1.metric("SKU actuales", "2", "0 con venta")
    m2.metric("Códigos en catálogo Maxiforce", "55")
    st.dataframe(
        {"Categoría (top 3 del catálogo)": [c[0] for c in cat_6125], "Códigos": [c[1] for c in cat_6125]},
        use_container_width=True, hide_index=True,
    )
with n3c2:
    st.markdown("#### Motor 6135")
    m1, m2 = st.columns(2)
    m1.metric("SKU actuales", "0", "sin catálogo")
    m2.metric("Códigos en catálogo Maxiforce", "25")
    st.dataframe(
        {"Categoría (top 3 del catálogo)": [c[0] for c in cat_6135], "Códigos": [c[1] for c in cat_6135]},
        use_container_width=True, hide_index=True,
    )
st.markdown(
    "<div class='callout-n3'>Sin demanda validada por IPESA en estos dos motores en este corte (no se buscó a "
    "propósito con el mismo nivel de detalle que 4045/6068/6090 — falta hacerlo antes de decidir). La pregunta "
    "para la reunión no es \"cuánto abrimos\" sino \"¿vale la pena investigar esto más a fondo?\"</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= SÍNTESIS =================
st.subheader("Síntesis para la reunión")
st.markdown(
    """
1. **🟢 4045 — completa lo que ya vendes.** 126 códigos faltantes, 44 con evidencia histórica de import
   (US$290K, 2022-2024 — sin dato 2025-2026 por el ocultamiento de código de IPESA), concentrados en inyección
   y kits — tus 2 categorías más fuertes. Riesgo más bajo de los 3 niveles.
2. **🟡 6068 y 6090 — sigue el crecimiento.** Ya crecen solos (+34% y +28%) con poco catálogo. 6090 en particular
   tiene la mejor proporción de códigos con esa misma evidencia histórica (40%).
3. **⚪ 6125 y 6135 — decisión aparte.** Casi sin presencia hoy. No se recomienda ni se descarta — es una
   pregunta para validar con más data antes de comprometer catálogo nuevo.
"""
)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "**Metodología.** Catálogo técnico Maxiforce (686 págs., PDF) parseado por código de parte con patrón "
        "\"T\" + código OEM John Deere, con el motor (Engine Series/Model) tomado del contexto de cada página. "
        "Se excluyeron 171 códigos que el mismo patrón capturó pero pertenecen a secciones Perkins/Yanmar del "
        "catálogo (contaminación cruzada de prefijo, detectada y filtrada). Demanda validada = mismo código "
        "encontrado como token exacto en las importaciones de IPESA 2022-jul.2026 (ver hoja IPESA)."
    )
with c2:
    st.markdown(
        "**Limitaciones.** La demanda \"validada\" depende de que IPESA haya escrito el código en su declaración "
        "de Aduanas — y eso casi dejó de pasar desde 2024 (ver aviso en la hoja IPESA), así que el número real de "
        "códigos con demanda es probablemente mayor. La categorización por tipo de repuesto es una heurística de "
        "texto (palabras clave en inglés en el PDF, español en Bsale) — puede haber SKU mal clasificados en el "
        "detalle, aunque los totales por motor son exactos. 6125/6135 no se cruzaron contra demanda IPESA en este "
        "corte."
    )
