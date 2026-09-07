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

import plotly.graph_objects as go
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
    ("TDZ100217", "Kit de boquillas (inyección)", "Inyección", 85896, 213, 12),
    ("TRE507959", "Bomba", "Bomba de agua", 32470, 16, 9),
    ("TRE568070", "Bomba de inyección", "Inyección", 29305, 23, 5),
    ("TRE71550",  "Turbocompresor", "Turbo", 29030, 32, 11),
    ("TDZ100216", "Kit de boquillas (inyección)", "Inyección", 27647, 87, 9),
    ("TDZ100211", "Kit de boquillas (inyección)", "Inyección", 13552, 28, 3),
    ("TDZ111137", "Distribuidor", "Inyección", 12007, 31, 10),
    ("TDZ111135", "Distribuidor", "Inyección", 7786, 26, 6),
    ("TRE507852", "Juego segmentos de pistón", "Anillos", 7170, 331, 8),
    ("TRE502079", "Bujía de precalentamiento", "Otros", 5187, 104, 12),
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
    motores = [m[0] for m in resumen_motores]
    actuales = [m[1] for m in resumen_motores]
    faltan = [m[4] for m in resumen_motores]
    fig = go.Figure()
    fig.add_bar(name="SKU que ya traes", x=motores, y=actuales, marker_color=REP)
    fig.add_bar(name="SKU que faltan (catálogo Maxiforce)", x=motores, y=faltan, marker_color=BAD)
    fig.update_layout(
        height=340, margin=dict(l=10, r=10, t=10, b=10), barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
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
k3.metric("De esos, con demanda ya confirmada (IPESA)", "75", "US$ 362K acumulado")
k4.metric("Venta 2026 de estos 5 motores (Ene-Ago)", sr(1490448 + 82965 + 97302))

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

st.markdown("#### Top 10 códigos que faltan, con demanda ya confirmada por IPESA (no es especulación)")
st.dataframe(
    {
        "SKU sugerido": [t[0] for t in top_faltantes_4045],
        "Producto": [t[1] for t in top_faltantes_4045],
        "Categoría": [t[2] for t in top_faltantes_4045],
        "FOB IPESA (2022-jul.26)": [usd(t[3]) for t in top_faltantes_4045],
        "Unidades IPESA": [t[4] for t in top_faltantes_4045],
        "N° embarques": [t[5] for t in top_faltantes_4045],
    },
    use_container_width=True, hide_index=True,
)
st.markdown(
    "<div class='callout-n1'><b>Por qué es la apuesta de menor riesgo:</b> mismo motor, mismo cliente, mismo "
    "proveedor (Maxiforce/EE.UU., el mismo canal de compra que ya usas). De los 126 códigos que faltan en el "
    "4045, <b>44 ya tienen demanda real confirmada</b> — alguien en Perú (IPESA) los está importando, no es una "
    "apuesta a ciegas. Los 3 más grandes son <b>kits de boquillas de inyección</b> (US$85,896 + US$27,647 + "
    "US$13,552 = US$127K solo en esa sub-categoría) y un <b>turbocompresor</b> (US$29,030) — categoría que hoy "
    "tienes en <b>cero</b> SKU en este motor. Inyección y kits camisa/pistón/anillos son, juntos, el 40% de todo "
    "el hueco (50 de 126 códigos) — y son exactamente las 2 categorías donde ya vendes más fuerte.</div>",
    unsafe_allow_html=True,
)

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
    "<div class='callout-n2'><b>Lectura:</b> el 6090 tiene la mejor proporción demanda-confirmada del análisis "
    "(23 de 58 códigos faltantes ya tienen import de IPESA detrás, 40%) — más alto que el 4045 (35%) o el 6068 "
    "(12%). Con solo 36 SKU abiertos ya vende casi tanto como el 6068 con 30 — sugiere que cada SKU nuevo en "
    "este motor rinde más que el promedio.</div>",
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
1. **🟢 4045 — completa lo que ya vendes.** 126 códigos faltantes, 44 con demanda real ya confirmada
   (US$290K), concentrados en inyección y kits — tus 2 categorías más fuertes. Riesgo más bajo de los 3 niveles.
2. **🟡 6068 y 6090 — sigue el crecimiento.** Ya crecen solos (+34% y +28%) con poco catálogo. 6090 en particular
   muestra la mejor señal de demanda confirmada (40% de sus códigos faltantes ya tienen import real detrás).
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
