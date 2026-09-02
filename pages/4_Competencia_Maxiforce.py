"""Competencia en marca Maxiforce — quién más importa la misma marca que Repaglas.

Fuente: ADEX Data Trade. Se buscó el texto "MAXIFORCE" en los 5 campos de
Descripción Comercial de los 10 reportes ADEX reales de "TOP SKU MAX +
EQUIVALENTES/" (mismos datos que las hojas SKU Ancla y Poder de Precio),
deduplicado por DUA+RUC+cantidad+FOB. A diferencia del resto del dashboard
(que compara Repaglas contra otras marcas/equivalentes), esta hoja aísla
únicamente las importaciones etiquetadas explícitamente como marca Maxiforce
por otras empresas — es decir, quién trae el mismo producto, no un sustituto.
"""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data import REP, load_competencia_maxiforce, load_maxiforce_detalle_anual  # noqa: E402

st.set_page_config(page_title="Competencia Maxiforce", page_icon="🏷️", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
data = load_competencia_maxiforce()
detalle_anual = load_maxiforce_detalle_anual()

RIVAL_COLORS = ["#c0392b", "#e67e22", "#8a7f6a", "#2e8b57", "#6a4c93", "#c9a227", "#4a90a4"]
ANIOS_NUM = [2022, 2023, 2024, 2025, 2026]
ANIOS_LABEL = ["2022", "2023", "2024", "2025", "2026*"]

rep_total = sum(data["repaglas"].values())
riv_total = sum(r["total"] for r in data["rivales"])
share_repaglas = rep_total / (rep_total + riv_total) * 100
n_rivales = len(data["rivales"])
n_rivales_repetidos = sum(1 for r in data["rivales"] if len(r["detalle_sku"]) >= 2)
mayor_rival = data["rivales"][0]

# ================= HEADER =================
st.markdown("###### 🏷️ INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("Competencia en marca Maxiforce")
st.markdown(
    "Repaglas no es la única empresa que importa productos etiquetados literalmente como "
    "**marca Maxiforce** en el Perú. Esta hoja aísla, dentro de los 10 SKU ancla, a quién más "
    "trae la misma marca — no un equivalente ni otro fabricante — y con qué frecuencia."
)
st.caption(
    "Metodología: búsqueda del texto \"MAXIFORCE\" en los 5 campos de Descripción Comercial de "
    "los 10 reportes ADEX (2022–jul.2026), deduplicado por DUA+RUC+cantidad+FOB. Un importador "
    "puede traer Maxiforce para un SKU y otra marca (John Deere, genérico) para otro — esta hoja "
    "solo cuenta las unidades explícitamente etiquetadas Maxiforce."
)

st.divider()

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("Share Repaglas (marca Maxiforce)", f"{share_repaglas:.1f}%", f"{rep_total:,} de {rep_total+riv_total:,} unidades")
k2.metric("Importadores de Maxiforce detectados", f"{n_rivales + 1}", f"{n_rivales} además de Repaglas")
k3.metric("Compiten en 2+ SKU (no es lote suelto)", f"{n_rivales_repetidos}", "R Y G Rockcat, Fortrac, Mateel, R & T Rockcat")
k4.metric("Mayor competidor de marca", mayor_rival["nombre"], f"{mayor_rival['total']} unidades, {len(mayor_rival['detalle_sku'])} SKU")

st.divider()

# ================= CUADRO + GRÁFICO DE EVOLUCIÓN (JUNTOS) =================
st.subheader("Evolución de importación de marca Maxiforce, por año")
st.write(
    "Repaglas frente a los 7 importadores que trajeron marca Maxiforce genuina en al menos uno de "
    "los 10 SKU ancla, con unidades por año (agregado de todos los SKU en los que aparece cada "
    "uno). **2026 es parcial** (solo hasta julio)."
)

fig = go.Figure()
fig.add_bar(x=ANIOS_LABEL, y=[data["repaglas"].get(a, 0) for a in ANIOS_NUM], name="Repaglas", marker_color=REP)
for i, riv in enumerate(data["rivales"]):
    fig.add_bar(
        x=ANIOS_LABEL, y=[riv["por_anio"].get(a, 0) for a in ANIOS_NUM],
        name=f"{riv['nombre']} ({riv['total']}u total)",
        marker_color=RIVAL_COLORS[i % len(RIVAL_COLORS)],
    )
fig.update_layout(
    barmode="group", height=380, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    yaxis_title="Unidades (marca Maxiforce, todos los SKU combinados)",
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

filas_tabla = [{"nombre": "Repaglas", "por_anio": data["repaglas"], "total": rep_total}] + data["rivales"]
total_general = rep_total + riv_total
st.dataframe(
    {
        "Importador": [f["nombre"] for f in filas_tabla],
        "2022": [f["por_anio"].get(2022, 0) for f in filas_tabla],
        "2023": [f["por_anio"].get(2023, 0) for f in filas_tabla],
        "2024": [f["por_anio"].get(2024, 0) for f in filas_tabla],
        "2025": [f["por_anio"].get(2025, 0) for f in filas_tabla],
        "2026*": [f["por_anio"].get(2026, 0) for f in filas_tabla],
        "Total 2022-jul.26": [f["total"] for f in filas_tabla],
        "Share %": [f"{f['total']/total_general*100:.1f}%" for f in filas_tabla],
    },
    use_container_width=True, hide_index=True,
)
st.caption("0 = sin importaciones de marca Maxiforce registradas ese año. 2026 es parcial, solo hasta julio.")

st.markdown(
    "<div class='callout'><b>Lectura:</b> <b>R Y G Rockcat</b> se retiró de forma limpia "
    "(116→44→16→0→0), la misma señal de \"vía libre\" que ya vimos en otros rivales caros. "
    "<b>Fortrac</b> es la señal a vigilar: pasó de 7 unidades (2022) a <b>0 en 2023 y 2024</b> y "
    "luego saltó a <b>99 en 2025</b> — ese salto coincide con el mismo salto que ya habíamos "
    "marcado 🔴 en RE507850 (Sección \"Tendencia por importador\" de SKU Ancla): ahora sabemos que "
    "parte de ese volumen es marca Maxiforce genuina, no un equivalente. <b>Mateel</b> y "
    "<b>R & T Rockcat</b> aparecieron solo en 2023-2024 y no repitieron en 2025-2026 — dormidos, no "
    "confirmados como retirados.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= DETALLE POR SKU =================
st.subheader("Detalle por SKU y año — en qué códigos compite cada rival, y a qué precio")
st.write(
    "Mismos 4 rivales recurrentes, comparados **año contra año** — el precio del rival en 2024 se "
    "compara con el precio de Repaglas en 2024, no con un promedio 2022-jul.2026 mezclado. "
    "Ordenado del **año más reciente al más viejo**, así lo primero que se ve es lo más vigente."
)
st.caption(
    "\"Sin comparación\" = Repaglas no importó ese código ese mismo año en el reporte ADEX "
    "(no hay contra qué comparar el precio, aunque el rival sí compró)."
)
rivales_recurrentes = [r for r in data["rivales"] if len(r["detalle_sku"]) >= 2]
seleccion_riv = st.multiselect(
    "Rival a inspeccionar", options=[r["nombre"] for r in rivales_recurrentes],
    default=[r["nombre"] for r in rivales_recurrentes],
)


def comparacion_str(pct):
    if pct is None:
        return "— Sin comparación"
    if pct < 90:
        return f"🟢 {100 - pct:.0f}% más barato"
    if pct > 110:
        return f"🔴 {pct - 100:.0f}% más caro"
    return "⚪ Precio similar"


for riv in rivales_recurrentes:
    if riv["nombre"] not in seleccion_riv:
        continue
    filas = sorted(
        [d for d in detalle_anual if d["rival"] == riv["nombre"]],
        key=lambda d: (-d["anio"], d["oem"]),
    )
    st.markdown(f"**{riv['nombre']}** — {riv['total']} unidades Maxiforce en {len(riv['detalle_sku'])} SKU")
    st.dataframe(
        {
            "SKU · Año": [f"{f['oem']} · {f['anio']}" for f in filas],
            "Unidades (rival / Repaglas)": [f"{f['riv_u']} / {f['rep_u'] or '—'}" for f in filas],
            "FOB/u rival": [f"${f['riv_fob_u']:.2f}" for f in filas],
            "FOB/u Repaglas": [f"${f['rep_fob_u']:.2f}" if f["rep_fob_u"] else "—" for f in filas],
            "Comparación": [comparacion_str(f["pct"]) for f in filas],
        },
        use_container_width=True, hide_index=True, key=f"detalle_{riv['nombre']}",
    )

st.markdown(
    "<div class='callout'><b>Lectura año contra año:</b> comparado en el mismo año, la mayoría de "
    "estos precios sigue en 90%-140% del precio de Repaglas (a la par o más caro) — el promedio "
    "multi-año no estaba maquillando nada grave en general. La excepción real es "
    "<b>Fortrac en RE504914</b>: pagó 94% en 2022, subió a 104% en 2025, y bajó a <b>80% en 2026</b> "
    "— el dato más reciente de todos y el único caso donde un rival recurrente quedó claramente por "
    "debajo de Repaglas en su año más actual. El resto de comparaciones \"baratas\" (Mateel 77% en "
    "RE507850, 78% en RE507920) son de <b>2023-2024</b>, no del año más reciente — no asumir que "
    "siguen vigentes sin una compra más nueva que lo confirme.</div>",
    unsafe_allow_html=True,
)

st.divider()
st.markdown(
    "**Nota al pie.** Esta hoja solo cuenta unidades con la palabra \"MAXIFORCE\" explícita en la "
    "descripción comercial del DUA. Es posible que algún importador traiga Maxiforce genuino sin "
    "declararlo con ese texto (o lo declare mal escrito) y no quede capturado aquí — el número real "
    "de competencia de marca podría ser algo mayor al mostrado, nunca menor."
)
