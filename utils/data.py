"""Datos compartidos entre páginas del dashboard Frente Dinámica.

Los 10 SKU Maxiforce ancla se investigaron a mano en ADEX Data Trade
(Comercial.aspx, búsqueda dirigida por código OEM) — no existe una fuente ADEX
"viva" que cubra todo el catálogo, así que esta lista es literal (no se carga
de un archivo) y es la única fuente de verdad para share/precio de importación.
Los campos de venta/cantidad/margen vienen de Bsale
(`01 DASHBOARD/reportes finales/Dashboard_Ventas_20260818_1959.xlsx`, hoja
"SKU Comparativo", Ene-Jul 2026).
"""

import streamlit as st

REP = "#2a78d6"
DIN = "#eb6834"
GOOD = "#0ca30c"
AMBER = "#c98a2e"
BAD = "#c0392b"

# code, sku, producto, cant26, venta26 (S/, Ene-Jul), margen26_pct, share_full_pct,
# n_importadores, precio_fob_rep_usd (2025-26), rival_nombre, rival_share_pct (full periodo)
_RAW = [
    ("RE65966",  "TRE65966",  "Kit camisa/pistón/anillos/pin/jebes/seguros", 96,  48332,  41.5, 99.9,  2, 74.41,
     "Nuevo Concepto de Maquinarias Agro Industrial", 0.1),
    ("R116383",  "TR116383",  "Camisa de motor",                            188, 33035,  41.1, 94.2,  6, 27.39,
     "R & T Rockcat", 2.9),
    ("RE536083", "TRE536083", "Kit camisa/pistón/anillos/pin/jebes/seguros", 66,  37355,  39.9, 90.3,  4, 86.62,
     "Dinámica", 5.0),
    ("RE500734", "TRE500734", "Bomba de agua motor",                        119, 64640,  42.0, 89.1, 14, 77.62,
     "R & T Rockcat", 2.3),
    ("RE66820",  "TRE66820",  "Jgo. anillos de motor",                      632, 49781,  41.5, 88.7, 11, 12.72,
     "Dinámica", 5.0),
    ("RE507850", "TRE507850", "Kit camisa/pistón/anillos/pin/jebes/seguros", 189, 93542,  39.4, 88.6,  7, 73.59,
     "Cisar", 4.2),
    ("RE501455", "TRE501455", "Jgo. empaquetaduras de motor",               112, 59955,  40.2, 85.7, 12, 80.99,
     "Dinámica", 6.1),
    ("RE504914", "TRE504914", "Bomba de aceite motor",                      132, 70817,  39.7, 75.7, 19, 86.12,
     "Maquinarias y Repuestos", 9.9),
    ("RE507920", "TRE507920", "Kit camisa/pistón/anillos/pin/jebes/seguros", 227, 106243, 40.2, 74.3, 14, 75.98,
     "IPESA", 8.3),
    ("RE48786",  "TRE48786",  "Inyector de motor",                          322, 67964,  42.2, 43.9, 24, 33.91,
     "IPESA", 33.2),
]

RIVAL_RELEVANTE_UMBRAL = 10.0  # % de share del rival a partir del cual se considera "competencia activa"


@st.cache_data
def load_sku_ancla():
    """Devuelve la lista de los 10 SKU Maxiforce ancla como diccionarios."""
    out = []
    for (oem, sku, producto, cant26, venta26, margen26, share_full, n_imp, precio_fob,
         rival_nombre, rival_share) in _RAW:
        out.append(
            {
                "oem": oem,
                "sku": sku,
                "producto": producto,
                "cant26": cant26,
                "venta26": venta26,
                "margen26_pct": margen26,
                "share_full_pct": share_full,
                "n_importadores": n_imp,
                "precio_fob_rep_usd": precio_fob,
                "rival_nombre": rival_nombre,
                "rival_share_pct": rival_share,
                "rival_relevante": rival_share >= RIVAL_RELEVANTE_UMBRAL,
            }
        )
    return out
