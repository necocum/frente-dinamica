"""Poder de precio — subir, no tocar, o traer segunda línea, SKU por SKU.

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

Fuente de datos: utils/data.py —
  - SKU/venta/cantidad/margen: Bsale, Dashboard_Ventas_20260818, hoja "SKU Comparativo".
  - Share e importadores por OEM: ADEX Data Trade (Comercial.aspx), búsqueda dirigida por
    código OEM, 2022-jul.2026, investigada a mano SKU por SKU (no hay fuente ADEX "viva").
  - Alternativas de marca: cruce del código OEM contra el SKU de TODAS las marcas del
    catálogo Bsale (KMP, Sheng Bao, Yedpar, Ozgur, FDR, OPEX JD, Vapormatic, Bepco, TVH),
    excluyendo Maxiforce.
"""

import io
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data import (  # noqa: E402
    REP, DIN, GOOD, AMBER, BAD, NO_MATERIAL, MATERIALIDAD_UMBRAL,
    load_sku_ancla, load_importadores_por_oem, load_alternativas_marca,
)

st.set_page_config(page_title="Poder de Precio", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; margin-bottom: 10px; }
      .callout-warn { border-left: 3px solid #b03a2e; background: #f5dcd8; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; margin-bottom: 10px; }
      .formula { border-left: 3px solid #2a78d6; background: #dce8f7; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14px; line-height: 1.7; font-family: monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def build_rows():
    """precio/costo unitario + tier de negocio (share 60/85) para cada uno de los 10 SKU."""
    importadores = load_importadores_por_oem()
    alternativas = load_alternativas_marca()
    rows = []
    for r in load_sku_ancla():
        oem = r["oem"]
        precio_venta_u = r["venta26"] / r["cant26"]
        m = r["margen26_pct"] / 100.0
        costo_u = precio_venta_u * (1 - m)

        imp = importadores[oem]
        repaglas_u = next(i["unidades"] for i in imp if i["es_repaglas"])
        rivales = [i for i in imp if not i["es_repaglas"]]
        for i in rivales:
            i["fob_u"] = i["fob_total"] / i["unidades"] if i["unidades"] else 0
            i["material"] = i["unidades"] >= MATERIALIDAD_UMBRAL * repaglas_u
        materiales = [i for i in rivales if i["material"]]
        fob_rivales = sum(i["fob_total"] for i in rivales)
        u_rivales = sum(i["unidades"] for i in rivales)
        precio_ponderado_mercado = fob_rivales / u_rivales if u_rivales else None

        alts = alternativas[oem]
        alts_vendiendo = [a for a in alts if a["cant26"] > 0]
        if not alts:
            estado_alt = "Solo Maxiforce"
        elif alts_vendiendo:
            estado_alt = "Segunda línea disponible"
        else:
            estado_alt = "Segunda línea dormida"

        if r["share_full_pct"] >= 85:
            tier = "SUBIR"
        elif r["share_full_pct"] >= 60:
            tier = "INVESTIGAR"
        else:
            tier = "SEGUNDA_LINEA"

        rows.append(
            {
                **r,
                "precio_venta_u": precio_venta_u,
                "costo_u": costo_u,
                "margen_frac": m,
                "importadores": imp,
                "rivales": rivales,
                "materiales": materiales,
                "precio_ponderado_mercado": precio_ponderado_mercado,
                "alternativas": alts,
                "alt_vendiendo": alts_vendiendo,
                "estado_alt": estado_alt,
                "tier": tier,
            }
        )
    return rows


ROWS = build_rows()
TIER_COLOR = {"SUBIR": GOOD, "INVESTIGAR": AMBER, "SEGUNDA_LINEA": BAD}

# ================= HEADER =================
st.markdown("###### 💰 INTELIGENCIA COMERCIAL · DECISIÓN DE PRECIO")
st.title("Poder de precio")
st.markdown(
    "¿En qué SKU puede Repaglas **subir precio** sin riesgo, en cuáles **no debe tocarlo todavía**, y en cuáles "
    "conviene empujar una **segunda línea de marca más económica** en vez de pelear con Maxiforce? Cruce de "
    "share de importación ADEX, margen actual Bsale, y catálogo de marcas alternativas ya disponibles."
)
st.markdown(
    "<div class='formula'>"
    "margen% = (precio_venta − costo) / precio_venta &nbsp;·&nbsp; "
    "precio_venta_unitario = venta / cantidad &nbsp;·&nbsp; "
    "costo_unitario = precio_venta_unitario × (1 − margen%)<br>"
    "Si el precio sube <b>p</b>%: margen_nuevo = (margen + p) / (1 + p) &nbsp;·&nbsp; "
    "pérdida de volumen de equilibrio = p / (margen + p)"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='callout-warn'><b>⚠️ FOB no es costo puesto en almacén.</b> Repaglas trae 89% de su carga desde "
    "EE.UU.; Dinámica diversifica a Brasil, Turquía, India y China — con flete, arancel y lead time distintos "
    "para cada origen. Un FOB más bajo desde otro país no significa costo final más bajo puesto en Perú. "
    "Comparar FOB pelado exagera la brecha real. <b>Nada en esta hoja sugiere bajar precios.</b></div>"
    "<div class='callout-warn'><b>⚠️ El precio de un competidor sobre un lote pequeño no es benchmark.</b> "
    "Puede ser un saldo puntual, o una variante de calidad distinta bajo la misma descripción comercial de ADEX. "
    "Por eso la Sección B separa a los importadores \"material\" (≥10% de las unidades de Repaglas) del resto.</div>",
    unsafe_allow_html=True,
)
st.caption(
    "\"Share\" en toda esta hoja es share de **importación directa** según ADEX, no share de mercado final — "
    "ADEX no ve stock local ni compras a mayoristas importadores que revenden sin importar ellos mismos."
)

st.divider()

# ================= A) MATRIZ =================
st.subheader("A) Matriz de poder de precio")
st.write("Cada burbuja es un SKU. Tamaño = venta Ene-Jul 2026. Líneas de referencia en share 60% y 85%.")
st.caption(
    "Eje X: share de importación ADEX, **histórico completo 2022-jul.2026**. Eje Y y tamaño de burbuja: "
    "margen % y venta, **Bsale Ene-Jul 2026**. Son dos periodos distintos a propósito — el eje X mide "
    "liderazgo estructural (varios años), el eje Y el estado comercial actual (último corte disponible)."
)

fig = go.Figure()
for r in ROWS:
    fig.add_trace(
        go.Scatter(
            x=[r["share_full_pct"]], y=[r["margen26_pct"]],
            mode="markers+text", text=[r["sku"]], textposition="top center",
            marker=dict(size=max(22, r["venta26"] / 1300), color=TIER_COLOR[r["tier"]], opacity=0.95,
                        line=dict(width=2, color="white")),
            showlegend=False,
            hovertemplate=(
                f"<b>{r['sku']}</b> (OEM {r['oem']})<br>{r['producto']}<br>"
                f"Venta Ene-Jul 2026: S/{r['venta26']:,.0f}<br>Unidades vendidas Ene-Jul 2026: {r['cant26']}<br>"
                f"Margen Ene-Jul 2026: {r['margen26_pct']:.1f}%<br>"
                f"Share importación ADEX 2022-jul.2026: {r['share_full_pct']:.1f}%<br>"
                f"N° importadores (2022-jul.2026): {r['n_importadores']}"
                "<extra></extra>"
            ),
        )
    )
fig.add_vline(x=60, line_dash="dot", line_color="#948a76", annotation_text="60%")
fig.add_vline(x=85, line_dash="dash", line_color="#948a76", annotation_text="85%")
fig.update_layout(
    height=440, margin=dict(l=10, r=10, t=30, b=10),
    xaxis_title="Share de importación ADEX 2022-jul.2026 (%)", yaxis_title="Margen Bsale Ene-Jul 2026 (%)",
    xaxis=dict(range=[0, 105]), yaxis=dict(range=[30, 48]),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ================= B) PRECIO VS. CANTIDAD =================
st.subheader("B) Precio vs. cantidad — quién es competencia de verdad")
st.write(
    "Un importador que trajo 4 unidades a un precio raro **no mueve el mercado** — \"una golondrina no hace "
    "verano\". Por eso el eje X es unidades (escala log) y la línea punteada es el precio promedio "
    "**ponderado por unidades** de todo el mercado excluyendo a Repaglas: ese es el único benchmark que importa, "
    "no el precio de cualquier importador aislado."
)
st.caption(
    "Periodo de esta sección: **unidades y FOB/unidad de ADEX, histórico completo 2022-jul.2026** (para "
    "Repaglas y para todos los rivales, mismo rango) — distinto de la venta/cantidad/margen Bsale Ene-Jul 2026 "
    "que se usa en el resto de la hoja (Secciones A, D y E)."
)
st.markdown(
    f"<div class='callout'>🔵 <b>Repaglas</b> · 🟠 <b>Rival material</b> (trajo ≥{MATERIALIDAD_UMBRAL*100:.0f}% "
    "de las unidades de Repaglas para ese código — sí cuenta como competencia real) · "
    "⚪ <b>Rival no material</b> (lote chico, por debajo del umbral — se ve gris a propósito, para que no "
    "distraiga de la comparación de precio). Si un SKU no tiene ningún punto naranja, quiere decir que "
    "<b>nadie más trajo un volumen comparable al de Repaglas</b> en ese código.</div>",
    unsafe_allow_html=True,
)
seleccion_b = st.multiselect(
    "SKU a inspeccionar", options=[r["sku"] for r in ROWS], default=[r["sku"] for r in ROWS],
    format_func=lambda s: f"{s} ({[r['oem'] for r in ROWS if r['sku']==s][0]})", key="sel_b",
)

for r in [x for x in ROWS if x["sku"] in seleccion_b]:
    st.markdown(f"**{r['sku']}** ({r['oem']}) — {r['producto']}")
    fig2 = go.Figure()
    # Repaglas — mismo periodo que los rivales (ADEX 2022-jul.2026 completo), no Bsale Ene-Jul 2026
    rep_imp = next(i for i in r["importadores"] if i["es_repaglas"])
    rep_u, rep_fob_u = rep_imp["unidades"], rep_imp["fob_total"] / rep_imp["unidades"]
    fig2.add_trace(go.Scatter(
        x=[rep_u], y=[rep_fob_u], mode="markers",
        marker=dict(size=24, color=REP, opacity=0.95, line=dict(width=2, color="white")),
        name="Repaglas",
        hovertemplate=f"<b>Repaglas</b><br>Unidades (2022-jul.26): {rep_u}<br>FOB/u: ${rep_fob_u:.2f}<extra></extra>",
    ))
    for i in r["rivales"]:
        color = DIN if i["material"] else NO_MATERIAL
        label = i["nombre"] if i["material"] else f"{i['nombre']} (no material)"
        fig2.add_trace(go.Scatter(
            x=[i["unidades"]], y=[i["fob_u"]], mode="markers",
            marker=dict(size=max(9, min(28, i["fob_total"] / 350)) if i["material"] else 9,
                        color=color, opacity=1.0 if i["material"] else 0.9,
                        line=dict(width=1.5 if i["material"] else 1, color="white" if i["material"] else "#c9c0ae")),
            name=label, showlegend=False,
            hovertemplate=f"<b>{label}</b><br>Unidades: {i['unidades']}<br>FOB total: ${i['fob_total']:,.0f}<br>FOB/u: ${i['fob_u']:.2f}<extra></extra>",
        ))
    if r["precio_ponderado_mercado"] is not None:
        fig2.add_hline(
            y=r["precio_ponderado_mercado"], line_dash="dash", line_color="#948a76",
            annotation_text=f"promedio mercado (excl. Repaglas): ${r['precio_ponderado_mercado']:.2f}/u",
        )
    fig2.update_layout(
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Unidades importadas 2022-jul.2026, ADEX (escala log)", yaxis_title="FOB / unidad (US$)",
        xaxis_type="log", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, use_container_width=True, key=f"scatter_{r['oem']}")

    total_u = sum(i["unidades"] for i in r["importadores"])
    tabla_imp = sorted(r["importadores"], key=lambda i: -i["unidades"])
    st.dataframe(
        {
            "Importador": [("Repaglas" if i["es_repaglas"] else i["nombre"]) for i in tabla_imp],
            "Unidades (ADEX 2022-jul.26)": [i["unidades"] for i in tabla_imp],
            "FOB total (2022-jul.26)": [f"${i['fob_total']:,.0f}" for i in tabla_imp],
            "FOB/unidad": [f"${(i['fob_total']/i['unidades']) if i['unidades'] else 0:.2f}" for i in tabla_imp],
            "% de unidades del mercado": [f"{i['unidades']/total_u*100:.1f}%" for i in tabla_imp],
            "¿Material?": ["—" if i["es_repaglas"] else ("Sí" if i.get("material") else "No") for i in tabla_imp],
        },
        use_container_width=True, hide_index=True, key=f"tabla_{r['oem']}",
        column_config={
            "¿Material?": st.column_config.TextColumn(
                "¿Material?",
                help=f"Sí = trajo al menos {MATERIALIDAD_UMBRAL*100:.0f}% de las unidades de Repaglas para este "
                     "código, así que su precio sí cuenta como referencia de mercado. No = lote chico que no "
                     "debería influir en la comparación de precio.",
            ),
        },
    )
    st.divider()

# ================= C) SEGUNDA LÍNEA =================
st.subheader("C) ¿Ya tengo una alternativa de marca para este OEM?")
st.write(
    "Antes de salir a buscar un proveedor nuevo: ¿alguna otra marca del catálogo Bsale (KMP, Sheng Bao, Yedpar, "
    "Ozgur, FDR, OPEX John Deere, Vapormatic, Bepco, TVH) ya cubre este mismo código OEM?"
)
st.caption("Todos los precios y montos de venta de esta tabla son **Bsale, Ene-Jul 2026** (mismo corte que el resto del catálogo).")
alt_rows = []
for r in ROWS:
    if r["alternativas"]:
        resumen = "; ".join(
            f"{a['marca']} S/{a['precio_venta']:.2f} ({a['cant26']} und, S/{a['venta26']:,.0f}, Ene-Jul 26)"
            if a["cant26"] > 0 else f"{a['marca']} S/{a['precio_venta']:.2f} (sin venta Ene-Jul 26)"
            for a in r["alternativas"]
        )
    else:
        resumen = "—"
    alt_rows.append((r, resumen))

st.dataframe(
    {
        "OEM": [r["oem"] for r, _ in alt_rows],
        "SKU Maxiforce": [r["sku"] for r, _ in alt_rows],
        "Precio venta Maxiforce (Ene-Jul 26)": [f"S/{r['precio_venta_u']:,.2f}" for r, _ in alt_rows],
        "Marcas alternativas encontradas (Ene-Jul 26)": [s for _, s in alt_rows],
        "Estado": [r["estado_alt"] for r, _ in alt_rows],
    },
    use_container_width=True, hide_index=True,
)
st.markdown(
    "<div class='callout'>De los 10 SKU, <b>7 ya tienen al menos una marca alternativa en catálogo</b> (KMP, "
    "Fujian, Bepco, Ozgur, TVH), casi siempre a menor precio que Maxiforce — solo RE507920, RE65966 y RE536083 "
    "son \"Solo Maxiforce\". La mayoría de esas alternativas ya venden algo (no están del todo dormidas), pero a "
    "un volumen muy por debajo de Maxiforce: la oportunidad es de empuje comercial, no de sourcing.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= D) SIMULADOR =================
st.subheader("D) Simulador de subida de precio")
st.caption(
    "Base de cálculo: unidades, precio de venta y margen **Bsale Ene-Jul 2026** (misma base que la Sección A "
    "y la tabla E). El share ADEX usado para el default de selección es 2022-jul.2026."
)
default_skus = [r["sku"] for r in ROWS if r["share_full_pct"] >= 85]
seleccion_d = st.multiselect(
    "SKU a simular", options=[r["sku"] for r in ROWS], default=default_skus,
    format_func=lambda s: f"{s} ({[r['oem'] for r in ROWS if r['sku']==s][0]})", key="sel_d",
)
c1, c2 = st.columns(2)
with c1:
    p_pct = st.slider("Subida de precio", 0.0, 15.0, 5.0, 0.5, format="%.1f%%")
with c2:
    q_pct = st.slider("Pérdida de volumen esperada (escenario conservador)", 0.0, 25.0, 0.0, 1.0, format="%.0f%%")

sel_rows_d = [r for r in ROWS if r["sku"] in seleccion_d]
p = p_pct / 100.0
q = q_pct / 100.0

if sel_rows_d:
    incr_vol_constante = sum(r["cant26"] * (12 / 7) * r["precio_venta_u"] * p for r in sel_rows_d)
    incr_con_perdida = sum(
        r["cant26"] * (12 / 7) * (1 - q) * r["precio_venta_u"] * (r["margen_frac"] + p)
        - r["cant26"] * (12 / 7) * r["precio_venta_u"] * r["margen_frac"]
        for r in sel_rows_d
    )
    venta_total = sum(r["venta26"] for r in sel_rows_d)
    margen_nuevo_pond = (
        sum(((r["margen_frac"] + p) / (1 + p)) * r["venta26"] for r in sel_rows_d) / venta_total * 100
        if venta_total else 0
    )
    margen_pond_actual = sum(r["margen26_pct"] * r["venta26"] for r in sel_rows_d) / venta_total if venta_total else 0
    equilibrio_pct = (p / (margen_pond_actual / 100 + p) * 100) if (margen_pond_actual / 100 + p) > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Margen incremental anual (volumen constante)", f"S/{incr_vol_constante:,.0f}")
    m2.metric("Margen incremental anual (con pérdida de volumen)", f"S/{incr_con_perdida:,.0f}")
    m3.metric("Nuevo margen % (ponderado por venta)", f"{margen_nuevo_pond:.1f}%",
              f"+{margen_nuevo_pond - margen_pond_actual:.1f}pp")
    m4.metric("Pérdida de volumen de equilibrio", f"{equilibrio_pct:.1f}%",
              "por encima de esto, la subida resta margen total")
    st.caption(
        "\"Anual\" = cantidad Ene-Jul 2026 extrapolada ×(12/7) — proyección simple, no venta real de 12 meses."
    )
else:
    st.info("Selecciona al menos un SKU para simular.")

st.divider()

# ================= E) TABLA DE RECOMENDACIÓN =================
st.subheader("E) Tabla de recomendación")


def movimiento_recomendado(r):
    if r["tier"] == "SUBIR":
        return "SUBIR precio 3-6%. No introducir segunda línea de marca."
    if r["tier"] == "INVESTIGAR":
        if r["materiales"]:
            top = max(r["materiales"], key=lambda i: i["unidades"])
            return f"INVESTIGAR primero: {top['nombre']} toma {top['unidades']} unidades antes de mover precio."
        return "INVESTIGAR primero: sin rival material identificado, pero share aún no es dominante."
    alt = r["alt_vendiendo"][0] if r["alt_vendiendo"] else (r["alternativas"][0] if r["alternativas"] else None)
    if alt:
        diff = (r["precio_venta_u"] - alt["precio_venta"]) / r["precio_venta_u"] * 100 if r["precio_venta_u"] else 0
        return f"NO subir Maxiforce. Empujar {alt['marca']} (S/{alt['precio_venta']:.2f}, {diff:.0f}% más barato)."
    return "NO subir Maxiforce. Evaluar segunda línea económica — no hay alternativa en catálogo hoy."


rows_e = []
for r in ROWS:
    if r["tier"] == "SUBIR":
        margen_incr = r["cant26"] * (12 / 7) * r["precio_venta_u"] * 0.045  # punto medio 3-6%
    else:
        margen_incr = 0.0
    rows_e.append({**r, "movimiento": movimiento_recomendado(r), "margen_incr": margen_incr})

rows_e.sort(key=lambda r: -r["margen_incr"])
st.caption(
    "\"Venta\", \"Unidades\" y \"Margen %\" son Bsale Ene-Jul 2026. \"Share ADEX\", \"N° importadores\", "
    "\"Competidores materiales\" y \"Precio ponderado mercado\" son ADEX histórico completo 2022-jul.2026. "
    "\"Margen incremental\" es una proyección anualizada (×12/7) a partir de Ene-Jul 2026 — ver Sección D."
)
st.dataframe(
    {
        "SKU": [r["sku"] for r in rows_e],
        "OEM": [r["oem"] for r in rows_e],
        "Producto": [r["producto"] for r in rows_e],
        "Venta Ene-Jul 26 (S/)": [f"{r['venta26']:,.0f}" for r in rows_e],
        "Unidades vendidas (Ene-Jul 26)": [r["cant26"] for r in rows_e],
        "Margen % (Ene-Jul 26)": [f"{r['margen26_pct']:.1f}%" for r in rows_e],
        "Share ADEX (2022-jul.26)": [f"{r['share_full_pct']:.1f}%" for r in rows_e],
        "N° importadores (2022-jul.26)": [r["n_importadores"] for r in rows_e],
        "Competidores materiales (2022-jul.26)": [
            ", ".join(f"{i['nombre']} ({i['unidades']}u)" for i in r["materiales"]) or "Ninguno"
            for r in rows_e
        ],
        "Precio ponderado mercado (US$/u, 2022-jul.26)": [
            f"${r['precio_ponderado_mercado']:.2f}" if r["precio_ponderado_mercado"] else "—" for r in rows_e
        ],
        "Alternativa de marca (Ene-Jul 26)": [r["estado_alt"] for r in rows_e],
        "Movimiento recomendado": [r["movimiento"] for r in rows_e],
        "Margen incremental S/ (anualizado)": [f"{r['margen_incr']:,.0f}" for r in rows_e],
    },
    use_container_width=True, hide_index=True,
)

xlsx_buf = io.BytesIO()
try:
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Poder de Precio"
    ws.append([
        "SKU", "OEM", "Producto", "Venta Ene-Jul 26 (S/)", "Unidades vendidas (Ene-Jul 26)",
        "Margen % (Ene-Jul 26)", "Share ADEX % (2022-jul.26)", "N° importadores (2022-jul.26)",
        "Competidores materiales (2022-jul.26)", "Precio ponderado mercado US$/u (2022-jul.26)",
        "Alternativa de marca (Ene-Jul 26)", "Movimiento recomendado", "Margen incremental S/ (anualizado)",
    ])
    for r in rows_e:
        ws.append([
            r["sku"], r["oem"], r["producto"], round(r["venta26"], 0), r["cant26"],
            round(r["margen26_pct"], 1), round(r["share_full_pct"], 1), r["n_importadores"],
            ", ".join(f"{i['nombre']} ({i['unidades']}u)" for i in r["materiales"]) or "Ninguno",
            round(r["precio_ponderado_mercado"], 2) if r["precio_ponderado_mercado"] else None,
            r["estado_alt"], r["movimiento"], round(r["margen_incr"], 0),
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
