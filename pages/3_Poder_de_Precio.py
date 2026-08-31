"""Poder de precio — en qué SKU Repaglas puede subir precio, y cuánto margen genera.

DEFINICIÓN DE MARGEN (confirmada — no reinterpretar):
El "margen %" de Bsale es margen SOBRE PRECIO DE VENTA, no markup sobre costo:
    margen% = (precio_venta - costo) / precio_venta
De ahí:
    precio_venta_unitario = venta / cantidad
    costo_unitario        = precio_venta_unitario * (1 - margen%)
Si el precio sube p% y el costo no cambia, el margen nuevo es:
    margen_nuevo = (margen + p) / (1 + p)
y la pérdida de volumen que deja el margen total sin cambio ("punto de equilibrio") es:
    perdida_equilibrio = p / (margen + p)
Control: margen=41%, p=5% -> 5/(41+5) = 10.9%.

Fuente de datos: utils/data.py (los 10 SKU Maxiforce ancla, investigados a mano en ADEX
Comercial.aspx — ver pages/2_SKU_Ancla.py) + Bsale (venta/cantidad/margen Ene-Jul 2026).
"""

import io
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data import REP, DIN, GOOD, AMBER, BAD, RIVAL_RELEVANTE_UMBRAL, load_sku_ancla  # noqa: E402

st.set_page_config(page_title="Poder de Precio", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-warn { border-left: 3px solid #b03a2e; background: #f5dcd8; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .formula { border-left: 3px solid #2a78d6; background: #dce8f7; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14px; line-height: 1.7; font-family: monospace; }
      .semaforo { display:inline-block; width:11px; height:11px; border-radius:50%; margin-right:6px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def build_rows():
    """Deriva precio/costo unitario y semáforo para cada uno de los 10 SKU ancla."""
    rows = []
    for r in load_sku_ancla():
        precio_venta_u = r["venta26"] / r["cant26"]
        m = r["margen26_pct"] / 100.0
        costo_u = precio_venta_u * (1 - m)

        if r["share_full_pct"] >= 85 and not r["rival_relevante"]:
            semaforo = "VERDE"
            subida_sugerida = 0.05
        elif r["share_full_pct"] < 60 or r["rival_relevante"]:
            semaforo = "ROJO"
            subida_sugerida = 0.0
        else:
            semaforo = "AMBAR"
            subida_sugerida = 0.02

        margen_incr_sugerida = r["cant26"] * (12 / 7) * precio_venta_u * subida_sugerida

        rows.append(
            {
                **r,
                "precio_venta_u": precio_venta_u,
                "costo_u": costo_u,
                "margen_frac": m,
                "semaforo": semaforo,
                "subida_sugerida": subida_sugerida,
                "margen_incr_sugerida_anual": margen_incr_sugerida,
            }
        )
    return rows


ROWS = build_rows()
SEM_COLOR = {"VERDE": GOOD, "AMBAR": AMBER, "ROJO": BAD}
SEM_LABEL = {"VERDE": "Subir", "AMBAR": "Evaluar", "ROJO": "No tocar"}

# ================= HEADER =================
st.markdown("###### 💰 INTELIGENCIA COMERCIAL · DECISIÓN DE PRECIO")
st.title("Poder de precio")
st.markdown(
    "¿En qué SKU puede Repaglas subir precio **sin riesgo real**, y cuánto margen adicional genera? Esta hoja "
    "cruza el **share de importación ADEX** (¿tan solo estás tú, o hay competencia real?) con el **margen actual "
    "Bsale** (¿ya hay margen sano, o está apretado?) para los 10 SKU Maxiforce ancla."
)

st.markdown(
    "<div class='formula'>"
    "margen% = (precio_venta − costo) / precio_venta &nbsp;·&nbsp; "
    "precio_venta_unitario = venta / cantidad &nbsp;·&nbsp; "
    "costo_unitario = precio_venta_unitario × (1 − margen%)<br>"
    "Si el precio sube <b>p</b>% y el costo no cambia: "
    "margen_nuevo = (margen + p) / (1 + p) &nbsp;·&nbsp; "
    "pérdida de volumen de equilibrio = p / (margen + p)"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='callout-warn'><b>⚠️ El precio FOB de Dinámica (27-36% por debajo de Repaglas en algunos "
    "códigos) NO es un benchmark válido para bajar precio.</b> Son lotes de 10-30 unidades contra los cientos "
    "que importa Repaglas, y la misma descripción comercial en ADEX no garantiza que sea la misma pieza (podría "
    "ser otro fabricante/calidad bajo el mismo código). Este análisis no sugiere bajar precio en ningún SKU por "
    "ese dato — solo identifica dónde subir.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= KPI ROW =================
verdes = [r for r in ROWS if r["semaforo"] == "VERDE"]
total_incr = sum(r["margen_incr_sugerida_anual"] for r in ROWS)
k1, k2, k3, k4 = st.columns(4)
k1.metric("SKU en verde (subir)", f"{len(verdes)} / 10")
k2.metric("SKU en rojo (no tocar)", f"{sum(1 for r in ROWS if r['semaforo']=='ROJO')} / 10", "RE48786")
k3.metric("Margen incremental potencial", f"S/{total_incr:,.0f}/año", "escenario sugerido por semáforo, volumen constante")
k4.metric("Margen actual promedio", f"{sum(r['margen26_pct'] for r in ROWS)/len(ROWS):.1f}%")

st.divider()

# ================= A) MATRIZ =================
st.subheader("A) Matriz de poder de precio")
st.write(
    "Cada burbuja es un SKU: a la derecha y arriba, más seguro subir precio (share alto, margen no excepcional "
    "todavía). El tamaño de la burbuja es la venta Ene-Jul 2026."
)

margen_mediano = sorted(r["margen26_pct"] for r in ROWS)[len(ROWS) // 2]
fig = go.Figure()
for r in ROWS:
    fig.add_trace(
        go.Scatter(
            x=[r["share_full_pct"]], y=[r["margen26_pct"]],
            mode="markers+text", text=[r["sku"]], textposition="top center",
            marker=dict(size=max(18, (r["venta26"] / 1500)), color=SEM_COLOR[r["semaforo"]], opacity=0.85,
                        line=dict(width=1, color="white")),
            name=r["sku"], showlegend=False,
            hovertemplate=(
                f"<b>{r['sku']}</b> (OEM {r['oem']})<br>{r['producto']}<br>"
                f"Venta Ene-Jul 26: S/{r['venta26']:,.0f}<br>Unidades: {r['cant26']}<br>"
                f"Margen: {r['margen26_pct']:.1f}%<br>Share ADEX: {r['share_full_pct']:.1f}%"
                "<extra></extra>"
            ),
        )
    )
fig.add_vline(x=85, line_dash="dash", line_color="#948a76", annotation_text="share 85%")
fig.add_hline(y=margen_mediano, line_dash="dash", line_color="#948a76", annotation_text="margen mediano")
fig.update_layout(
    height=460, margin=dict(l=10, r=10, t=30, b=10),
    xaxis_title="Share de importación ADEX (%)", yaxis_title="Margen actual (%)",
    xaxis=dict(range=[0, 105]), yaxis=dict(range=[30, 48]),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "⚠️ \"Share\" aquí es share de **importación directa** según ADEX, no share de mercado final — ADEX no ve "
    "stock local ni compras a mayoristas importadores que revenden sin importar ellos mismos."
)

st.divider()

# ================= B) SIMULADOR =================
st.subheader("B) Simulador de subida de precio")
default_skus = [r["sku"] for r in ROWS if r["share_full_pct"] >= 85]
seleccion = st.multiselect(
    "SKU a simular", options=[r["sku"] for r in ROWS], default=default_skus,
    format_func=lambda s: f"{s} ({[r['oem'] for r in ROWS if r['sku']==s][0]})",
)
c1, c2 = st.columns(2)
with c1:
    p_pct = st.slider("Subida de precio", 0.0, 15.0, 5.0, 0.5, format="%.1f%%")
with c2:
    q_pct = st.slider("Pérdida de volumen esperada (escenario conservador)", 0.0, 25.0, 0.0, 1.0, format="%.0f%%")

sel_rows = [r for r in ROWS if r["sku"] in seleccion]
p = p_pct / 100.0
q = q_pct / 100.0

if sel_rows:
    incr_vol_constante = sum(r["cant26"] * (12 / 7) * r["precio_venta_u"] * p for r in sel_rows)
    incr_con_perdida = sum(
        r["cant26"] * (12 / 7) * (1 - q) * r["precio_venta_u"] * (r["margen_frac"] + p)
        - r["cant26"] * (12 / 7) * r["precio_venta_u"] * r["margen_frac"]
        for r in sel_rows
    )
    venta_total = sum(r["venta26"] for r in sel_rows)
    margen_nuevo_pond = sum(
        ((r["margen_frac"] + p) / (1 + p)) * r["venta26"] for r in sel_rows
    ) / venta_total * 100 if venta_total else 0
    margen_pond_actual = sum(r["margen26_pct"] * r["venta26"] for r in sel_rows) / venta_total if venta_total else 0
    equilibrio_pct = (p / (margen_pond_actual / 100 + p) * 100) if (margen_pond_actual / 100 + p) > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Margen incremental anual (volumen constante)", f"S/{incr_vol_constante:,.0f}")
    m2.metric("Margen incremental anual (con pérdida de volumen)", f"S/{incr_con_perdida:,.0f}")
    m3.metric("Nuevo margen % (ponderado por venta)", f"{margen_nuevo_pond:.1f}%", f"+{margen_nuevo_pond - margen_pond_actual:.1f}pp")
    m4.metric("Pérdida de volumen de equilibrio", f"{equilibrio_pct:.1f}%",
              "por encima de esto, la subida resta margen total")
    st.caption(
        "\"Anual\" = cantidad Ene-Jul 2026 extrapolada ×(12/7) — no es venta real de 12 meses, es una "
        "proyección simple a partir del acumulado disponible."
    )
else:
    st.info("Selecciona al menos un SKU para simular.")

st.divider()

# ================= C) TABLA DE RECOMENDACIÓN =================
st.subheader("C) Tabla de recomendación")
rows_sorted = sorted(ROWS, key=lambda r: -r["margen_incr_sugerida_anual"])
st.dataframe(
    {
        "SKU": [r["sku"] for r in rows_sorted],
        "OEM": [r["oem"] for r in rows_sorted],
        "Producto": [r["producto"] for r in rows_sorted],
        "Venta Ene-Jul 26 (S/)": [f"{r['venta26']:,.0f}" for r in rows_sorted],
        "Unidades": [r["cant26"] for r in rows_sorted],
        "Margen actual": [f"{r['margen26_pct']:.1f}%" for r in rows_sorted],
        "Share ADEX": [f"{r['share_full_pct']:.1f}%" for r in rows_sorted],
        "Rival recurrente": [
            f"{'Sí' if r['rival_relevante'] else 'Marginal' if r['rival_share_pct']>0 else 'No'} — {r['rival_nombre']} ({r['rival_share_pct']:.1f}%)"
            for r in rows_sorted
        ],
        "Subida sugerida": [f"+{r['subida_sugerida']*100:.0f}%" for r in rows_sorted],
        "Margen incremental S/ (anual)": [f"{r['margen_incr_sugerida_anual']:,.0f}" for r in rows_sorted],
        "Semáforo": [f"{SEM_LABEL[r['semaforo']]}" for r in rows_sorted],
    },
    use_container_width=True,
    hide_index=True,
)
st.caption(
    f"Semáforo: 🟢 Verde = share ≥ 85% y sin rival ≥ {RIVAL_RELEVANTE_UMBRAL:.0f}% de share (subir +5% sugerido). "
    "🟡 Ámbar = share 60-85%, o rival presente pero por debajo del umbral (evaluar +2%). "
    "🔴 Rojo = share < 60% o rival con competencia activa (no tocar) — único caso: RE48786/TRE48786."
)

xlsx_buf = io.BytesIO()
try:
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Poder de Precio"
    headers = ["SKU", "OEM", "Producto", "Venta Ene-Jul 26 (S/)", "Unidades", "Margen actual %",
               "Share ADEX %", "Rival recurrente", "Share rival %", "Subida sugerida %",
               "Margen incremental S/ (anual)", "Semáforo"]
    ws.append(headers)
    for r in rows_sorted:
        ws.append([
            r["sku"], r["oem"], r["producto"], round(r["venta26"], 0), r["cant26"],
            round(r["margen26_pct"], 1), round(r["share_full_pct"], 1), r["rival_nombre"],
            round(r["rival_share_pct"], 1), round(r["subida_sugerida"] * 100, 1),
            round(r["margen_incr_sugerida_anual"], 0), SEM_LABEL[r["semaforo"]],
        ])
    wb.save(xlsx_buf)
    st.download_button(
        "⬇️ Descargar tabla (Excel)", data=xlsx_buf.getvalue(),
        file_name="poder_de_precio_repaglas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
except ImportError:
    st.caption("(Descarga a Excel no disponible: falta la librería `openpyxl` en el entorno.)")

st.divider()
st.markdown(
    "**Nota al pie.** Este análisis asume que Repaglas importa el 100% de su volumen bajo un solo RUC "
    "(20118992009). Si existe un segundo RUC no incluido en la búsqueda ADEX, los shares mostrados están "
    "subestimados — Repaglas sería aún más líder de lo que indica esta tabla, no menos."
)
