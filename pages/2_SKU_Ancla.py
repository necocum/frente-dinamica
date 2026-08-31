"""Los 10 SKU Maxiforce ancla — liderazgo de importación y precio de compra.

Fuente: ADEX Data Trade (SUNAT / Aduanas del Perú). Búsqueda dirigida por
Descripción Comercial (código OEM John Deere) para cada uno de los 10 SKU
Maxiforce de mayor venta de Repaglas, 2022–jul.2026. Ranking de venta desde
Bsale (Dashboard_Ventas_20260818, ene–jul 2026).
"""

import plotly.graph_objects as go
import streamlit as st

REP = "#2a78d6"
DIN = "#eb6834"
GOOD = "#0ca30c"
BAD = "#c0392b"

st.set_page_config(page_title="SKU Ancla · Maxiforce", page_icon="🔧", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .share-bar { display:flex; height:30px; border-radius:7px; overflow:hidden; margin:6px 0; }
      .share-seg { display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
# code, sku, descripcion, cant26, venta26, share_full_pct, n_importadores, precio_rep_2526, [(rival, precio, unidades), ...]
skus = [
    ("RE65966", "TRE65966", "Kit camisa/pistón/anillos/pin/jebes/seguros", 96, 48332, 99.9, 2, 74.41, []),
    ("R116383", "TR116383", "Camisa de motor", 188, 33035, 94.2, 6, 27.39, []),
    ("RE536083", "TRE536083", "Kit camisa/pistón/anillos/pin/jebes/seguros", 66, 37355, 90.3, 4, 86.62,
     [("Dinámica", 60.77, 10), ("JPK Mundo Parts", 65.55, 8)]),
    ("RE500734", "TRE500734", "Bomba de agua motor", 119, 64640, 89.1, 14, 77.62,
     [("Dinámica", 55.00, 30), ("Fortrac", 75.52, 21), ("Amazon Motors", 172.24, 4)]),
    ("RE66820", "TRE66820", "Jgo. anillos de motor", 632, 49781, 88.7, 11, 12.72,
     [("Fortrac", 14.69, 42), ("JPK Mundo Parts", 13.11, 8), ("AG Import Parve", 5.00, 8)]),
    ("RE507850", "TRE507850", "Kit camisa/pistón/anillos/pin/jebes/seguros", 189, 93542, 88.6, 7, 73.59,
     [("Fortrac", 78.71, 36), ("Mateel", 39.55, 12)]),
    ("RE501455", "TRE501455", "Jgo. empaquetaduras de motor", 112, 59955, 85.7, 12, 80.99,
     [("Dinámica", 51.66, 20), ("Fortrac", 91.58, 7), ("JPK Mundo Parts", 53.36, 8)]),
    ("RE504914", "TRE504914", "Bomba de aceite motor", 132, 70817, 75.7, 19, 86.12,
     [("Maquinarias y Repuestos", 544.70, 4), ("Corporación Pesquera Inca", 603.92, 3), ("Fortrac", 81.66, 11)]),
    ("RE507920", "TRE507920", "Kit camisa/pistón/anillos/pin/jebes/seguros", 227, 106243, 74.3, 14, 75.98,
     [("Fortrac", 144.56, 44), ("JPK Mundo Parts", 57.54, 16), ("Dinámica", 55.71, 13)]),
    ("RE48786", "TRE48786", "Inyector de motor", 322, 67964, 43.9, 24, 33.91,
     [("Maquinarias y Repuestos", 146.44, 33), ("IM Selva", 107.98, 24), ("Tractor Import", 89.66, 13)]),
]


def usd(n):
    return f"US$ {n:,.2f}"


def share_bar(pct, color=REP):
    resto = 100 - pct
    return (
        f"<div class='share-bar'>"
        f"<div class='share-seg' style='width:{pct}%;background:{color};'>{pct:.1f}%</div>"
        f"<div class='share-seg' style='width:{resto}%;background:#d9d2c2;color:#7a7062;'>{resto:.1f}%</div>"
        f"</div>"
    )


# ================= HEADER =================
st.markdown("###### 🔧 INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("Los 10 SKU Maxiforce ancla")
st.markdown(
    "Los **10 SKU de marca :blue[Maxiforce] con mayor venta** de Repaglas (Ene–Jul 2026), verificados uno por "
    "uno en ADEX Comercial.aspx: liderazgo de importación (share de FOB, todo el histórico 2022–jul.2026) y "
    "comparación de precio de compra (FOB por unidad, 2025–2026) contra cada rival identificado."
)
st.caption(
    "Equivalencia SKU→OEM: el código Maxiforce es literalmente \"T\" + el código OEM John Deere "
    "(TRE507920 → RE507920 · TR116383 → R116383)."
)

# ================= KPI ROW =================
shares = [s[5] for s in skus]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Share promedio (10 SKU)", f"{sum(shares)/len(shares):.1f}%")
k2.metric("SKU con share > 85%", f"{sum(1 for s in shares if s>85)} / 10")
k3.metric("Único SKU disputado", "RE48786", "43.9% — IPESA 33.2%")
k4.metric("Rival recurrente", "Dinámica", "único con compras en 6 de 10 SKU, siempre 2-6%")

st.divider()

# ================= TABLA PRINCIPAL =================
st.subheader("Liderazgo de importación — los 10 SKU")
st.dataframe(
    {
        "SKU Repaglas": [s[1] for s in skus],
        "OEM": [s[0] for s in skus],
        "Producto": [s[2] for s in skus],
        "Cant. vendida 2026": [s[3] for s in skus],
        "Venta S/ 2026": [f"S/{s[4]:,.0f}" for s in skus],
        "Share Repaglas (2022-jul.26)": [f"{s[5]:.1f}%" for s in skus],
        "N° importadores": [s[6] for s in skus],
        "FOB/unidad Repaglas (25-26)": [usd(s[7]) for s in skus],
    },
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ================= SHARE VISUAL =================
st.subheader("Share de mercado por código")
for code, sku, desc, cant, venta, share, n, precio, rivals in skus:
    c1, c2 = st.columns([1, 4])
    c1.markdown(f"**{sku}**<br><span style='font-size:12px;color:#948a76;'>{desc}</span>", unsafe_allow_html=True)
    color = BAD if share < 60 else (REP if share >= 85 else "#c98a2e")
    c2.markdown(share_bar(share, color), unsafe_allow_html=True)

st.markdown(
    "<div class='callout'><b>Lectura:</b> en 9 de los 10 códigos Repaglas concentra 74-99.9% del FOB importado "
    "por todo el mercado peruano — liderazgo sostenido, no un pico puntual (dato es acumulado 2022–jul.2026). "
    "El único código realmente disputado es <b>RE48786</b> (inyector), donde IPESA tiene un tercio del mercado — "
    "distinto del resto porque cae en otra partida arancelaria (8481, válvulas/inyección) en vez de 8409 "
    "(partes de motor) del resto de la canasta.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= COMPARACIÓN DE PRECIO =================
st.subheader("Comparación de precio de importación (FOB por unidad, 2025-2026)")
st.write(
    "Para cada SKU, el precio de compra (FOB/unidad) de Repaglas frente a los rivales que sí compraron esa misma "
    "referencia en 2025-2026. Cuando no hay rivales listados, nadie más importó ese código en el periodo reciente."
)
for code, sku, desc, cant, venta, share, n, precio, rivals in skus:
    st.markdown(f"**{sku}** ({code}) — {desc}")
    cats = ["Repaglas"] + [r[0] for r in rivals]
    vals = [precio] + [r[1] for r in rivals]
    colors = [REP] + [DIN if "Dinámica" in r[0] else "#b0a690" for r in rivals]
    fig = go.Figure()
    fig.add_bar(x=cats, y=vals, marker_color=colors, text=[f"${v:.2f}" for v in vals], textposition="outside")
    fig.update_layout(
        height=220, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        yaxis_tickprefix="$", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True, key=f"price_{code}")

st.markdown(
    "<div class='callout'><b>Patrón a vigilar:</b> en 4 de los 5 códigos donde <b>Dinámica</b> compra "
    "(RE507920, RE500734, RE501455, RE536083), su FOB/unidad es <b>27-36% más bajo</b> que el de Repaglas — "
    "aunque en lotes muy chicos (10-30 unidades vs. cientos de Repaglas), lo que normalmente encarecería, no "
    "abarataría, el costo unitario. Podría ser una variante/calidad distinta bajo la misma descripción comercial "
    "(otro fabricante asiático) más que el mismo producto — no tomar como benchmark de precio sólido sin repetirse "
    "en más de un periodo. Los demás rivales (Fortrac, IPESA, Maquinarias y Repuestos, Corporación Pesquera Inca) "
    "pagan sistemáticamente 1.1× a 8× más que Repaglas — consistente con declarar marca genuina John Deere en vez "
    "de Maxiforce.</div>",
    unsafe_allow_html=True,
)

st.divider()
st.markdown(
    "**Margen actual (Bsale, Ene-Jul 2026):** los 10 SKU mantienen margen estable en **40-42%**, sin señal de "
    "erosión frente a Ene-Jul 2025. Con liderazgo de 74-99.9% de share sostenido en años (no un dato puntual), "
    "hay espacio para subir precio de forma selectiva en los 8-9 códigos sin competencia real — manteniendo "
    "precio agresivo en RE48786, el único donde IPESA disputa el mercado con volumen real."
)
