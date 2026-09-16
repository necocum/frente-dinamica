"""Catálogo chino (Guangzhou HD Parts) — qué se podría cotizar.

Fuente: catálogo de fabricante `2026 资料书 PDF.pdf` (650 págs., 100% imágenes,
Guangzhou HD Parts Construction Machinery Parts Co., Ltd. — marcas "Star Mustang",
"HD Engine Spare Parts", "Genuine Izumi JP"). Se identificaron en la tabla de
contenidos del catálogo las secciones de John Deere, Perkins, Caterpillar y
Yanmar dentro de 15 categorías de repuesto de motor (cigüeñal, culata, pistón,
camisa, bomba de agua/aceite, kit de junta, inyector, etc.) y se leyeron
visualmente esas páginas — no las ~500 páginas de hidráulica/electrónica de
cabina de excavadora del mismo catálogo, fuera del negocio actual de Repaglas.
Cada código se cruzó contra el catálogo Bsale de Repaglas (7,230 SKU únicos,
export 14-09-2026) probando el código tal cual y con las convenciones de
prefijo ya usadas en el proyecto (John Deere: "T"+OEM; Caterpillar: "B"+código
sin guión; Perkins: prefijos P/PU/PZZ/PUPRK/PMXF).
"""

import io
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Catálogo Chino (HD Parts)", page_icon="🇨🇳", layout="wide")

st.markdown(
    """
    <style>
      .callout { border-left: 3px solid #9a5a1f; background: #f0e0c9; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-warn { border-left: 4px solid #c0392b; background: #fbe4e1; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
      .callout-ok { border-left: 4px solid #0ca30c; background: #e2f6e2; padding: 14px 18px;
          border-radius: 0 8px 8px 0; font-size: 14.5px; line-height: 1.55; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🇨🇳 Catálogo Chino — Guangzhou HD Parts")
st.caption(
    "Reconocimiento del catálogo 2026 de un fabricante chino de repuestos de motor, cruzado contra el "
    "catálogo Bsale de Repaglas — qué se podría pedir cotizar y qué tan maduro es cada línea de marca."
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "catalogo_chino_hd.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Stock Bsale"] = pd.to_numeric(df["Stock Bsale"], errors="coerce")
    df["Precio Bsale"] = pd.to_numeric(df["Precio Bsale"], errors="coerce")
    return df


df = load_data()

st.markdown("### ¿Quién es este proveedor?")
st.markdown(
    "<div class='callout'><b>Guangzhou HD Parts Construction Machinery Parts Co., Ltd.</b> (广州厚多机械), "
    "marcas \"Star Mustang\" / \"HD Engine Spare Parts\" / \"Genuine Izumi JP\". Fabricante con ~30 años en "
    "el rubro y ~500,000 piezas de inventario declarado. Cubre repuestos de motor para <b>Kubota, Yanmar, "
    "Isuzu, Mitsubishi, Komatsu, Perkins, Caterpillar, Cummins, Volvo, Doosan, Hyundai, Nissan y Hino</b> "
    "(su propia lista de marketing) — <b>John Deere no aparece en esa lista</b> pero sí tiene páginas "
    "dedicadas dentro del catálogo: señal de que es una línea nueva/menor para el fabricante, no su fuerte. "
    "Caterpillar y Perkins, en cambio, son líneas mucho más maduras y completas — y buena parte de las "
    "marcas donde el fabricante es fuerte (Komatsu, Doosan, Hyundai, Isuzu, Kubota) calzan más con el "
    "negocio de <b>IPESA</b> (dealer de equipo pesado, ~20× la escala de Repaglas) que con el de Repaglas.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= KPIs =================
total = len(df)
nuevos = int((df["Ya existe en Bsale"] == "No").sum())
existentes = total - nuevos
por_marca = df["Marca Motor"].value_counts()
por_marca_nuevos = df[df["Ya existe en Bsale"] == "No"]["Marca Motor"].value_counts()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Códigos/ítems extraídos", f"{total:,}")
c2.metric("Ya existen en Bsale", f"{existentes:,}", help="Comparar costo, no es SKU nuevo")
c3.metric("No existen en Bsale", f"{nuevos:,}", help="Oportunidad limpia de SKU nuevo")
c4.metric("Marcas cubiertas", "4", help="John Deere, Perkins, Caterpillar, Yanmar")

st.markdown("#### Desglose por marca de motor")
cols = st.columns(4)
orden_marcas = ["John Deere", "Caterpillar", "Perkins", "Yanmar"]
for col, marca in zip(cols, orden_marcas):
    tot_m = int(por_marca.get(marca, 0))
    new_m = int(por_marca_nuevos.get(marca, 0))
    with col:
        st.markdown(f"**{marca}**")
        st.markdown(f"{tot_m} extraídos · <span style='color:#0ca30c'><b>{new_m} nuevos</b></span>", unsafe_allow_html=True)

fig = go.Figure()
fig.add_bar(name="Ya existe en Bsale", x=orden_marcas,
            y=[por_marca.get(m, 0) - por_marca_nuevos.get(m, 0) for m in orden_marcas],
            marker_color="#8a8a8a")
fig.add_bar(name="Nuevo (no en Bsale)", x=orden_marcas,
            y=[por_marca_nuevos.get(m, 0) for m in orden_marcas],
            marker_color="#0ca30c")
fig.update_layout(barmode="stack", height=340, margin=dict(t=20, b=20, l=20, r=20),
                   legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<div class='callout-warn'><b>Lectura de madurez:</b> John Deere es la línea más delgada del catálogo "
    "de este fabricante (muchas celdas de la tabla vienen vacías), pero los motores que sí cubre son "
    "exactamente los que ya trabaja Repaglas/Maxiforce (4045, 6068, 6090) — y algunas páginas (pistón, bomba "
    "de agua) sí vienen completas con código OEM real. Caterpillar es la línea más madura y completa del "
    "fabricante: es donde Repaglas tiene más exposición (334 SKU Caterpillar en su catálogo Maxiforce) y "
    "donde cualquier competidor podría cotizar con mayor certeza de encontrar el código que busca.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ================= TABLA FILTRABLE =================
st.markdown("### 📋 Tabla completa — filtrable")

fc1, fc2, fc3 = st.columns(3)
marca_sel = fc1.multiselect("Marca Motor", orden_marcas, default=orden_marcas)
cat_sel = fc2.multiselect("Categoría", sorted(df["Categoria"].unique()), default=[])
existe_sel = fc3.radio("¿Ya existe en Bsale?", ["Todos", "Solo nuevos (No)", "Solo existentes (Sí)"], horizontal=False)

filtrado = df[df["Marca Motor"].isin(marca_sel)]
if cat_sel:
    filtrado = filtrado[filtrado["Categoria"].isin(cat_sel)]
if existe_sel == "Solo nuevos (No)":
    filtrado = filtrado[filtrado["Ya existe en Bsale"] == "No"]
elif existe_sel == "Solo existentes (Sí)":
    filtrado = filtrado[filtrado["Ya existe en Bsale"] != "No"]

st.caption(f"{len(filtrado):,} de {total:,} filas")
st.dataframe(
    filtrado.rename(columns={
        "Pagina": "Página", "Categoria": "Categoría", "Codigo Fabricante HD": "Código Fabricante (HD)",
        "Codigo OEM": "Código OEM",
    }),
    use_container_width=True, hide_index=True, height=440,
)

# ================= DESCARGA =================
xlsx_buf = io.BytesIO()
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen"
    ws.sheet_view.showGridLines = False
    ws["B2"] = "Catálogo Chino — Guangzhou HD Parts (Star Mustang / Genuine Izumi JP)"
    ws["B2"].font = Font(size=16, bold=True, color="1F4E78")
    ws["B3"] = "Repuestos de motor cotizables — cruce contra catálogo Bsale de Repaglas"
    ws["B3"].font = Font(size=11, italic=True, color="595959")
    ws["B5"] = "Total de códigos/ítems extraídos"
    ws["D5"] = total
    ws["B6"] = "Ya existen en Bsale (comparar costo, no SKU nuevo)"
    ws["D6"] = existentes
    ws["B7"] = "No existen en Bsale (oportunidad limpia de SKU nuevo)"
    ws["D7"] = nuevos
    for r in (5, 6, 7):
        ws[f"B{r}"].font = Font(size=10)
        ws[f"D{r}"].font = Font(size=10, bold=True)
    ws["B9"] = "Marca Motor"
    ws["C9"] = "Total extraído"
    ws["D9"] = "Nuevos (no en Bsale)"
    for c in ("B9", "C9", "D9"):
        ws[c].font = Font(size=10, bold=True, color="FFFFFF")
        ws[c].fill = PatternFill("solid", fgColor="1F4E78")
    for i, marca in enumerate(orden_marcas, start=10):
        ws[f"B{i}"] = marca
        ws[f"C{i}"] = int(por_marca.get(marca, 0))
        ws[f"D{i}"] = int(por_marca_nuevos.get(marca, 0))
    ws.column_dimensions["B"].width = 40
    for col in "CDEFGHIJ":
        ws.column_dimensions[col].width = 16

    ws2 = wb.create_sheet("Para Cotizar")
    headers = ["Página", "Categoría", "Marca Motor", "Código Fabricante (HD)", "Modelo Motor", "Código OEM",
               "¿Ya existe en Bsale?", "SKU Bsale", "Marca Bsale", "Stock Bsale", "Precio Bsale (S/)"]
    for i, h in enumerate(headers, start=1):
        c = ws2.cell(row=1, column=i, value=h)
        c.font = Font(size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")
        c.alignment = Alignment(horizontal="center")
    export_df = filtrado if len(filtrado) < total else df
    for ridx, (_, row) in enumerate(export_df.iterrows(), start=2):
        vals = [row["Pagina"], row["Categoria"], row["Marca Motor"], row["Codigo Fabricante HD"],
                row["Modelo Motor"], row["Codigo OEM"], row["Ya existe en Bsale"], row["SKU Bsale"],
                row["Marca Bsale"], row["Stock Bsale"], row["Precio Bsale"]]
        for cidx, v in enumerate(vals, start=1):
            ws2.cell(row=ridx, column=cidx, value=(None if pd.isna(v) else v))
    widths = [8, 18, 14, 20, 20, 32, 16, 14, 14, 12, 14]
    for i, w in enumerate(widths, start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"

    wb.save(xlsx_buf)
    st.download_button(
        "⬇️ Descargar Excel — Catálogo Chino para Cotización",
        data=xlsx_buf.getvalue(),
        file_name="Catalogo_Chino_HD_Parts_Cotizacion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.caption("El Excel exporta las filas visibles según los filtros de arriba (o todo, si no filtraste).")
except ImportError:
    st.caption("(Descarga a Excel no disponible: falta la librería `openpyxl` en el entorno.)")

st.divider()

st.markdown("### ⚠️ Alcance de este reconocimiento")
st.markdown(
    "<div class='callout-warn'>Se cubrieron las secciones John Deere / Perkins / Caterpillar / Yanmar de "
    "15 categorías de repuesto de motor (cigüeñal, culata, pistón, camisa, bomba de agua/aceite, kit de "
    "junta, alternador, motor de arranque, enfriador de aceite, árbol de levas, termostato, bujía "
    "incandescente e inyector — estos dos últimos solo revisados parcialmente — y silenciador). "
    "<b>No se cubrieron</b> las ~500 páginas de hidráulica/electrónica de cabina de excavadora del mismo "
    "catálogo (joystick, válvulas hidráulicas, sensores, aire acondicionado) por estar fuera del negocio "
    "actual de Repaglas. Muchas celdas del catálogo original vienen vacías — el fabricante no ha completado "
    "su línea John Deere/Perkins para todos los modelos — por lo que solo se registraron celdas con "
    "contenido real (foto + código o modelo de motor).</div>",
    unsafe_allow_html=True,
)
