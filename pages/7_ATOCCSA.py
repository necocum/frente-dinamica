"""ATOCCSA — SKU en común con Repaglas.

Fuente: reporte ADEX Data Trade más reciente filtrado por RUC 20614437368
(`Reporte_-_Importaciones_20260910171716_21_38759.xlsx`, generado 2026-09-10), 199
líneas / 2 DUAs de REPUESTOS E IMPORTACIONES ATOCCSA S.A.C. (repuestos de motor,
100% China, vía Marítima del Callao). Solo el DUA 96288 (feb-2026, 130 líneas)
declara el código de parte en el campo "Descripción Comercial 2" con el patrón
"NUMBER PART<código>" — el DUA 167059 (abr-2026, 69 líneas) declara por modelo de
motor (ej. "V2203", "D722") sin código de pieza, por lo que esas 69 líneas no son
comparables por código y quedan fuera de este cruce.

El cruce es por código exacto (normalizado: sin guiones/espacios, mayúsculas)
contra el SKU y el SKU-sin-sufijo-de-marca del export de stock Bsale
`Stock-actual_Todas-las-sucursales_07-09-2026 (1).xlsx` (14,462 filas, todas las
marcas y sucursales). Hecho 2026-09-10.
"""

import io

import plotly.graph_objects as go
import streamlit as st

REP = "#2a78d6"
BAD = "#c0392b"
GOOD = "#0ca30c"

st.set_page_config(page_title="ATOCCSA — SKU en común", page_icon="🔧", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-ok { border-left: 4px solid #0ca30c; background: #e2f6e2; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= DATA =================
# (PartNum, Descripción ATOCCSA, FOB US$, Cantidad, ¿match?, SKU Repaglas, Marca Repaglas, Stock actual)
codigos = [
    ("320/09216", "JUEGO EMPAQUES, S/M, 320/09216", 2202.0, 100, False, "", "", 0),
    ("320/09211", "KIT DE PISTÓN, S/M, 320/09211", 1559.0, 100, False, "", "", 0),
    ("320/09383", "JUEGO EMPAQUES, S/M, 320/09383", 1440.0, 100, False, "", "", 0),
    ("320/03616", "VÁLVULA ESCAPE, S/M, 320/03616", 1152.0, 400, False, "", "", 0),
    ("3135M111", "PISTÓN, S/M, 3135M111", 1066.2, 60, False, "", "", 0),
    ("4132F071", "BOMBA DE ACEITE, S/M, 4132F071", 1050.0, 20, False, "", "", 0),
    ("1206", "EMPAQUE MOTOR, S/M, 1206", 1048.0, 8, False, "", "", 0),
    ("3135M141", "KIT DE PISTÓN, S/M, 3135M141", 826.4, 40, False, "", "", 0),
    ("T417956", "KIT DE PISTÓN, S/M, T417956", 779.2, 40, False, "", "", 0),
    ("575-3355", "PISTÓN C/ ANILLOS, S/M, 575-3355", 774.9, 30, False, "", "", 0),
    ("320/03612", "VÁLVULA ADMISIÓN, S/M, 320/03612", 772.0, 400, False, "", "", 0),
    ("3612486", "PISTÓN C/ ANILLOS, S/M, 3612486", 720.0, 30, False, "", "", 0),
    ("T409184", "PISTÓN, S/M, T409184", 690.0, 30, False, "", "", 0),
    ("U5LL0015", "PISTÓN, S/M, 5LL0015", 655.5, 30, True, "U5LL0015-CL", "COMPRAS LOCALES", 0),
    ("T407944", "BOMBA DE ACEITE, S/M, T407944", 643.5, 10, False, "", "", 0),
    ("320/08657", "TEMPLADOR DE FAJA, S/M, 320/08657", 609.6, 40, False, "", "", 0),
    ("B3154678", "BOMBA DE ACEITE, S/M, B3154678", 609.6, 20, True, "B3154678", "MAXIFORCE", 8),
    ("U5MW0204", "BOMBA DE AGUA, S/M, U5MW0204", 609.6, 20, False, "", "", 0),
    ("U5MW0205", "BOMBA DE AGUA, S/M, U5MW0205", 609.6, 20, False, "", "", 0),
    ("415-4315", "JUEGO PISTÓN, S/M, 415-4315", 594.9, 30, False, "", "", 0),
    ("320/03698", "VÁLVULA ESCAPE, S/M, 320/03698", 560.0, 400, False, "", "", 0),
    ("U5LL0014", "PISTÓN, S/M, U5LL0014", 524.4, 24, True, "U5LL0014", "KMP", 4),
    ("320/09213", "JUEGO ANILLOS DE PISTON, S/M, 320/09213", 520.96, 176, False, "", "", 0),
    ("320/04186", "BOMBA ACEITE, S/M, 320/04186", 508.0, 20, False, "", "", 0),
    ("320/03697", "VÁLVULA ADMISIÓN, S/M, 320/03697", 508.0, 400, False, "", "", 0),
    ("T413424", "BOMBA DE AGUA, S/M, T413424", 492.0, 10, False, "", "", 0),
    ("4133L508", "TERMOSTATO, S/M, 4133L508", 491.0, 50, False, "", "", 0),
    ("41733082", "CONJUNTO BALANCEADOR, S/M, 41733082", 460.64, 4, True, "41733082", "KMP", 4),
    ("320/09335", "METAL DE BANCADA, S/M, 320/09335", 440.0, 50, False, "", "", 0),
    ("115017581", "PISTÓN, S/M, 115017581", 433.2, 40, False, "", "", 0),
    ("320/07207", "BOMBA Y FILTRO, S/M, 320/07207", 406.0, 10, False, "", "", 0),
    ("UPRK0005", "JUEGO DE ANILLOS, S/M, UPRK0005", 398.0, 100, False, "", "", 0),
    ("320/04138", "ENFRIADOR ACEITE, S/M, 320/04138", 389.6, 20, False, "", "", 0),
    ("276-7476", "JUEGO ANILLOS DE PISTON, S/M, 276-7476", 367.0, 100, False, "", "", 0),
    ("115104021", "JUEGO DE ANILLOS, S/M, 115104021", 350.0, 100, False, "", "", 0),
    ("115107970", "JUEGO DE ANILLOS, S/M, 115107970", 350.0, 100, False, "", "", 0),
    ("UPRK0002", "JUEGO DE ANILLOS, S/M, UPRK0002", 350.0, 100, False, "", "", 0),
    ("U5LP0009", "PISTÓN, S/M, U5LP0009", 338.8, 20, True, "U5LP0009", "KMP", 0),
    ("360-2028", "JUEGO ANILLOS DE PISTON, S/M, 360-2028", 330.3, 90, False, "", "", 0),
    ("320/02691", "ASIENTO ADMISIÓN, S/M, 320/02691", 320.0, 400, False, "", "", 0),
    ("320/02596", "ASIENTO ESCAPE, S/M, 320/02596", 320.0, 400, False, "", "", 0),
    ("4181A033", "JUEGO DE ANILLOS, S/M, 4181A033", 318.0, 100, True, "4181A033-CL", "COMPRAS LOCALES", 0),
    ("U5MK8266", "BOMBA DE ACEITE, S/M, U5MK8266", 304.8, 10, False, "", "", 0),
    ("U5MK8267", "BOMBA DE ACEITE, S/M, U5MK8267", 304.8, 10, False, "", "", 0),
    ("41158017", "JUEGO DE ANILLOS, S/M, 41158017", 286.0, 100, False, "", "", 0),
    ("2486A222", "ENFRIADOR DE ACEITE, S/M, 2486A222", 274.4, 10, False, "", "", 0),
    ("U5LT0342", "JUEGO DE EMPAQUETADURAS, S/M, U5LT0342", 271.0, 10, False, "", "", 0),
    ("2486A241", "ENFRIADOR DE ACEITE, S/M, 2486A241", 267.6, 10, False, "", "", 0),
    ("2418F704", "RETÉN POSTERIOR, S/M, 2418F704", 262.5, 50, True, "2418F704", "KMP", 0),
    ("320/03017", "BUJE DE BIELA, S/M, 320/03017", 260.0, 200, False, "", "", 0),
    ("320/07040", "BOMBA DE PETRÓLEO, S/M, 320/07040", 254.1, 30, False, "", "", 0),
    ("81558", "CONCHA DE BANCADA, S/M, 81558", 254.0, 50, True, "81558", "KMP", 18),
    ("360-1978", "JUEGO METALES, S/M, 360-1978", 249.9, 30, False, "", "", 0),
    ("T416115", "EMPAQUE CULATA, S/M, T416115", 245.6, 10, False, "", "", 0),
    ("320/03119", "RETÉN FRONTAL, S/M, 320/03119", 237.0, 100, False, "", "", 0),
    ("T417342", "BOMBA TRANSF.COMBUSTIBLE, S/M, T417342", 226.95, 5, False, "", "", 0),
    ("T417445", "BOMBA TRANSF.COMBUSTIBLE, S/M, T417445", 226.95, 5, False, "", "", 0),
    ("3113A003", "SURTIDOR DE ACEITE, S/M, 3113A003", 221.0, 100, False, "", "", 0),
    ("4132F056", "BOMBA DE ACEITE, S/M, 4132F056", 203.2, 10, False, "", "", 0),
    ("3681E074", "JUNTA DE CULATA, S/M, 3681E074", 203.1, 30, False, "", "", 0),
    ("320/09210", "KIT DE PISTÓN, S/M, 320/09210", 199.56, 12, False, "", "", 0),
    ("320/03184", "KIT DE PISTÓN, S/M, 320/03184", 199.56, 12, False, "", "", 0),
    ("320/09208", "ARANDELA EMPUJE, S/M, 320/09208", 198.0, 150, False, "", "", 0),
    ("145017951", "BOMBA DE AGUA, S/M, 145017951", 196.4, 20, False, "", "", 0),
    ("T410666", "RETÉN FRONTAL, S/M, T410666", 193.0, 20, False, "", "", 0),
    ("518-5437", "JUEGO METALES, S/M, 518-5437", 189.9, 30, False, "", "", 0),
    ("360-1564", "JUEGO METALES, S/M, 360-1564", 189.9, 30, False, "", "", 0),
    ("320/09336", "METAL DE BANCADA, S/M, 320/09336", 179.6, 20, False, "", "", 0),
    ("31431315", "VÁLVULA DE ESCAPE, S/M, 31431315", 178.2, 120, False, "", "", 0),
    ("320/04618", "TERMOSTATO, S/M, 320/04618", 178.0, 50, False, "", "", 0),
    ("320/04542", "BOMBA DE AGUA, S/M, 320/04542", 177.8, 10, False, "", "", 0),
    ("4132F012", "BOMBA DE ACEITE, S/M, 4132F012", 177.8, 10, False, "", "", 0),
    ("4111A021", "ENGRANAJE, S/M, 4111A021", 176.2, 20, False, "", "", 0),
    ("320/07201", "BOMBA DE PETRÓLEO, S/M, 320/07201", 169.4, 20, False, "", "", 0),
    ("41314182", "BOMBA DE ACEITE, S/M, 41314182", 169.4, 10, False, "", "", 0),
    ("T410927", "METAL DE BIELA, S/M, T410927", 152.4, 30, False, "", "", 0),
    ("U5LC0018", "JUEGO DE EMPAQUETADURAS, S/M, U5LC0018", 152.4, 15, False, "", "", 0),
    ("81558A", "CONCHA DE BANCADA, S/M, 81558A", 152.4, 30, True, "81558A", "KMP", 2),
    ("U5LB0384", "EMPAQUE INFERIOR, S/M, U5LB0384", 152.4, 10, True, "U5LB0384", "KMP", 8),
    ("3343J002", "GUÍA DE VÁLVULA, S/M, 3343J002", 147.6, 360, False, "", "", 0),
    ("3343F002", "GUÍA DE VÁLVULA, S/M, 3343F002", 147.6, 360, False, "", "", 0),
    ("320/03029", "RETÉN POSTERIOR, S/M, 320/03029", 142.4, 40, False, "", "", 0),
    ("31162121", "CORONA DENTADA, S/M, 31162121", 142.2, 20, False, "", "", 0),
    ("276-7478", "BUJE, S/M, 276-7478", 142.0, 100, False, "", "", 0),
    ("3399637", "VÁLVULA DE ESCAPE, S/M, 3399637", 131.0, 100, False, "", "", 0),
    ("320/01519", "BUJE DE LEVAS, S/M, 320/01519", 128.0, 80, False, "", "", 0),
    ("233-5470", "VÁLVULA DE ESCAPE, S/M, 233-5470", 127.8, 60, False, "", "", 0),
    ("U5LB0363", "JUEGO DE EMPAQUETADURAS, S/M, U5LB0363", 127.0, 10, False, "", "", 0),
    ("4133L032", "TERMOSTATO, S/M, 4133L032", 125.4, 20, False, "", "", 0),
    ("4132F067", "BOMBA DE ACEITE, S/M, 4132F067", 121.92, 6, False, "", "", 0),
    ("360-3986", "JUEGO METALES, S/M, 360-3986", 120.0, 30, True, "3603986", "KMP", 0),
    ("4133L507", "TERMOSTATO, S/M, 4133L507", 118.6, 20, True, "4133L507", "BEPCO", 0),
    ("320/A4904", "BOMBA DE AGUA, S/M, 320/A4904", 118.5, 5, False, "", "", 0),
    ("320/03270", "METAL DE BIELA, S/M, 320/03270", 115.0, 25, False, "", "", 0),
    ("3096678", "VÁLVULA DE ADMISIÓN, S/M, 3096678", 115.0, 100, False, "", "", 0),
    ("T405211", "VÁLVULA ESCAPE, S/M, T405211", 111.6, 60, False, "", "", 0),
    ("T406777", "VÁLVULA ADMISIÓN, S/M, T406777", 111.6, 60, False, "", "", 0),
    ("2418F705", "RETÉN POSTERIOR, S/M, 2418F705", 108.4, 20, False, "", "", 0),
    ("85042A", "METAL DE BIELA, S/M, 85042A", 101.7, 30, True, "85042A", "KMP", 2),
    ("4197640", "SOLENOIDE, S/M, 4197640", 93.1, 10, False, "", "", 0),
    ("U5LB1310", "EMPAQUE INFERIOR, S/M, U5LB1310", 93.1, 10, False, "", "", 0),
    ("2335469", "VÁLVULA DE ADMISIÓN, S/M, 2335469", 88.8, 60, False, "", "", 0),
    ("3142A181", "VÁLVULA DE ESCAPE, S/M, 3142A181", 86.4, 64, False, "", "", 0),
    ("U5MB0020A", "METAL DE BANCADA, S/M, U5MB0020A", 85.0, 10, False, "", "", 0),
    ("4138A033", "VÁLVULA DE ALIVIO, S/M, 4138A033", 84.7, 10, False, "", "", 0),
    ("T409188", "METAL DE BANCADA, S/M, T409189", 84.7, 10, False, "", "", 0),
    ("3142A101", "VÁLVULA DE ADMISIÓN, S/M, 3142A101", 78.6, 60, False, "", "", 0),
    ("50209083", "RETÉN POSTERIOR, S/M, 50209083", 76.2, 30, False, "", "", 0),
    ("U5MW0108", "BOMBA DE AGUA, S/M, U5MW0108", 76.2, 5, True, "U5MW0108", "KMP", 10),
    ("81558B", "METAL DE BANCADA, S/M, 81558B", 76.2, 15, True, "81558B", "KMP", 0),
    ("198517265", "BUJE DE BIELA, S/M, 198517265", 74.0, 100, False, "", "", 0),
    ("120176380", "VÁLVULA DE ESCAPE, S/M, 120176380", 71.4, 60, False, "", "", 0),
    ("3142H011", "VÁLVULA DE ADMISIÓN, S/M, 3142H011", 69.0, 60, False, "", "", 0),
    ("U5ME0022A", "METAL DE BIELA, S/M, U5ME0022A", 68.0, 10, False, "", "", 0),
    ("T415862", "METAL DE BIELA, S/M, T415862", 67.7, 10, False, "", "", 0),
    ("3142H071", "VÁLVULA DE ADMISIÓN, S/M, 3142H071", 66.0, 60, False, "", "", 0),
    ("3142H091", "VÁLVULA DE ADMISIÓN, S/M, 3142H091", 65.28, 64, False, "", "", 0),
    ("3271H004", "PIN DE BANCADA, S/M, 3271H004", 63.4, 20, False, "", "", 0),
    ("120166380", "VÁLVULA ADM/ESC, S/M, 120166380", 51.0, 60, False, "", "", 0),
    ("85042B", "METAL DE BIELA, S/M, 85042B", 50.85, 15, True, "85042B", "KMP", 0),
    ("81558C", "CONCHA DE BANCADA, S/M, 81558C", 50.8, 10, True, "81558C", "KMP", 4),
    ("341-8536", "CONO INYECTOR, S/M, 341-8536", 50.7, 30, False, "", "", 0),
    ("T405824", "EMPAQUE ESCAPE, S/M, T405824", 45.7, 10, False, "", "", 0),
    ("3501028", "EMPAQUE ENFRIADOR, S/M, 3501028", 45.7, 10, False, "", "", 0),
    ("T406926", "EMPAQUE, S/M, T406926", 45.7, 10, False, "", "", 0),
    ("T407192", "JUNTA TAPA VÁLVULA, S/M, T407192", 30.5, 10, False, "", "", 0),
    ("T410538", "EMPAQUE ESCAPE, S/M, T410538", 30.5, 10, False, "", "", 0),
    ("198636160", "RETÉN FRONTAL, S/M, 198636160", 22.0, 20, False, "", "", 0),
]

fob_total_reporte = 94422.31
fob_dua_feb = 39917.67
fob_dua_abr = 54504.64
n_lineas_total = 199
n_lineas_con_codigo = 130
n_codigos_distintos = len(codigos)
matches = [c for c in codigos if c[4]]
sin_match = [c for c in codigos if not c[4]]
fob_match = sum(c[2] for c in matches)
fob_sin_match = sum(c[2] for c in sin_match)
n_match_stock0 = sum(1 for c in matches if c[7] == 0)

# ================= HEADER =================
st.markdown("###### 🔧 INTELIGENCIA COMERCIAL · ADUANAS DEL PERÚ (ADEX DATA TRADE)")
st.title("ATOCCSA — ¿qué SKU traemos también nosotros?")
st.markdown(
    "**REPUESTOS E IMPORTACIONES ATOCCSA S.A.C.** (RUC 20614437368) — repuestos de motor "
    "(pistones, válvulas, metales, bombas) importados **100% de China**, vía Marítima del "
    "Callao. Se cruzó cada código de parte de su reporte ADEX más reciente contra el catálogo "
    "de SKU de Repaglas en Bsale, para ver cuántos productos coinciden exactamente."
)
st.caption(
    "Fuente: reporte ADEX generado 2026-09-10 (2 DUAs: 96288 del 28-feb-2026 y 167059 del "
    "10-abr-2026, US$94,422 FOB combinado). Solo el DUA de febrero declara código de parte "
    "reconocible (\"NUMBER PART...\"); el de abril declara por modelo de motor (V2203, D722, "
    "4D94-2) sin código de pieza, por lo que sus 69 líneas no son comparables por SKU y quedan "
    "fuera de este cruce. Catálogo Repaglas: stock Bsale de todas las sucursales, 07-09-2026."
)

st.divider()

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("FOB total del reporte (2 DUAs)", f"US$ {fob_total_reporte:,.0f}")
k2.metric("Líneas comparables (con código de parte)", f"{n_lineas_con_codigo} de {n_lineas_total}", "solo DUA 96288, feb-2026")
k3.metric("Códigos que también tenemos", f"{len(matches)} de {n_codigos_distintos}", f"{len(matches)/n_codigos_distintos*100:.1f}% de match")
k4.metric("FOB en códigos que sí tenemos", f"US$ {fob_match:,.0f}", f"{fob_match/fob_dua_feb*100:.1f}% del FOB comparable")

st.divider()

# ================= GRÁFICO =================
st.subheader("FOB comparable: lo que ya tenemos vs. lo que no")
fig = go.Figure()
fig.add_bar(
    x=["Ya lo tenemos (mismo código)", "No está en catálogo Repaglas"],
    y=[fob_match, fob_sin_match],
    marker_color=[GOOD, BAD],
    text=[f"US$ {fob_match:,.0f}", f"US$ {fob_sin_match:,.0f}"],
    textposition="outside",
)
fig.update_layout(
    height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
    yaxis_title="US$ FOB (solo líneas con código de parte, DUA 96288)",
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    f"<div class='callout'><b>Lectura:</b> de los {n_codigos_distintos} códigos distintos que "
    f"ATOCCSA declaró con número de parte, solo <b>{len(matches)} ({len(matches)/n_codigos_distintos*100:.1f}%)</b> "
    f"coinciden exactamente con un SKU que Repaglas ya tiene abierto en Bsale — mayormente marca "
    f"<b>KMP</b>. El <b>{n_match_stock0} de {len(matches)}</b> de esos coincidentes está hoy con "
    f"<b>stock en 0</b>: son productos que compiten directo con ATOCCSA y que hoy no podemos "
    f"vender por falta de inventario, no por falta de catálogo.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= TABLA: COINCIDENCIAS =================
st.subheader(f"Los {len(matches)} SKU en común")
matches_sorted = sorted(matches, key=lambda c: -c[2])
st.dataframe(
    {
        "Código": [c[0] for c in matches_sorted],
        "Producto (declarado por ATOCCSA)": [c[1] for c in matches_sorted],
        "SKU Repaglas": [c[5] for c in matches_sorted],
        "Marca Repaglas": [c[6] for c in matches_sorted],
        "Stock actual": [c[7] for c in matches_sorted],
        "⚠️": ["Sin stock" if c[7] == 0 else "" for c in matches_sorted],
        "FOB ATOCCSA": [f"US$ {c[2]:,.2f}" for c in matches_sorted],
        "Cantidad ATOCCSA": [c[3] for c in matches_sorted],
    },
    use_container_width=True, hide_index=True, height=420,
)

st.divider()

# ================= TABLA: OPORTUNIDADES (SIN MATCH, TOP FOB) =================
st.subheader("Top 15 códigos que ATOCCSA importa y Repaglas NO tiene")
st.write(
    "Ordenado por FOB — son las piezas de mayor valor que ATOCCSA trae y que no aparecen con "
    "ese código exacto en el catálogo Repaglas. Puede haber equivalencias reales (mismo repuesto, "
    "código distinto de otro fabricante) que este cruce por código exacto no detecta."
)
sin_match_sorted = sorted(sin_match, key=lambda c: -c[2])[:15]
st.dataframe(
    {
        "Código": [c[0] for c in sin_match_sorted],
        "Producto (declarado por ATOCCSA)": [c[1] for c in sin_match_sorted],
        "FOB ATOCCSA": [f"US$ {c[2]:,.2f}" for c in sin_match_sorted],
        "Cantidad": [c[3] for c in sin_match_sorted],
    },
    use_container_width=True, hide_index=True,
)

st.divider()

# ================= DESCARGA =================
st.subheader("Descargar cruce completo")
xlsx_buf = io.BytesIO()
try:
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "ATOCCSA vs Repaglas"
    ws.append([
        "Código de parte", "Producto (declarado por ATOCCSA)", "FOB US$", "Cantidad",
        "¿Coincide con SKU Repaglas?", "SKU Repaglas", "Marca Repaglas", "Stock actual",
    ])
    for c in sorted(codigos, key=lambda x: -x[2]):
        ws.append([c[0], c[1], c[2], c[3], "SÍ" if c[4] else "NO", c[5], c[6], c[7]])
    wb.save(xlsx_buf)
    st.download_button(
        "⬇️ Descargar Excel — ATOCCSA, 128 códigos vs. catálogo Repaglas",
        data=xlsx_buf.getvalue(),
        file_name="ATOCCSA_vs_Repaglas_SKU_20260910.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
except ImportError:
    st.caption("(Descarga a Excel no disponible: falta la librería `openpyxl` en el entorno.)")

st.divider()
st.markdown(
    "**Metodología.** Reporte ADEX filtrado por RUC 20614437368, código de parte extraído del "
    "campo \"Descripción Comercial 2\" con el patrón \"NUMBER PART&lt;código&gt;\" (130 de 199 "
    "líneas; las 69 restantes, del DUA 167059, declaran por modelo de motor y no tienen código "
    "de pieza comparable). Cruce contra el SKU y el SKU sin sufijo de marca "
    "(ej. \"831907M1-VAP\" → \"831907M1\") del export de stock Bsale de todas las sucursales "
    "(07-09-2026), coincidencia por texto exacto tras normalizar (sin guiones/espacios, "
    "mayúsculas)."
)
st.markdown(
    "**Limitaciones.** El match es solo por código idéntico — no detecta equivalencias reales "
    "entre fabricantes con numeración distinta para la misma pieza (el mismo método usado en la "
    "hoja \"Catálogo Maxiforce\" de este dashboard subestima el traslape real por esta razón). "
    "El 34.7% de las líneas del reporte (DUA de abril) no tiene código de pieza declarado y no "
    "pudo evaluarse."
)
