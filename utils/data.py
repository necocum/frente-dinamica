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

REP = "#1f6feb"
DIN = "#ff7a1a"
GOOD = "#14c766"
AMBER = "#f5a623"
BAD = "#ff4d4f"

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
MATERIALIDAD_UMBRAL = 0.10  # un importador es "material" si trae >= 10% de las unidades de Repaglas


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


# Lista COMPLETA de importadores por código OEM (2022-jul.2026, ADEX Comercial.aspx,
# búsqueda dirigida por descripción comercial) — no solo el top 3-4 como se resumía antes.
# Necesaria para el análisis unidades-vs-precio de la Sección B (Poder de Precio): un lote
# de pocas unidades a precio raro no debe pesar igual que un importador de volumen real.
_IMPORTADORES_RAW = {
    "RE507920": [
        ("Repaglas", 1659, 124383, True), ("IPESA", 202, 13830, False), ("Fortrac", 79, 11974, False),
        ("Dinámica", 61, 3406, False), ("Tractor Import", 14, 2605, False), ("R Y G Rockcat", 28, 2583, False),
        ("R & T Rockcat", 24, 2008, False), ("Mateel", 24, 1516, False), ("Monsante", 6, 1028, False),
        ("National Air & Motor", 4, 1001, False), ("Italtrac Selva", 6, 983, False),
        ("JPK Mundo Parts", 16, 921, False), ("MODASA", 12, 832, False), ("Solutra del Perú", 4, 272, False),
    ],
    "RE507850": [
        ("Repaglas", 1296, 92294, True), ("Cisar", 50, 4390, False), ("Dinámica", 60, 3358, False),
        ("Fortrac", 36, 2833, False), ("Mateel", 18, 793, False), ("R Y G Rockcat", 4, 334, False),
        ("R & T Rockcat", 2, 152, False),
    ],
    "RE504914": [
        ("Repaglas", 821, 71281, True), ("Maquinarias y Repuestos", 17, 9294, False),
        ("R Y G Rockcat", 20, 2213, False), ("Dinámica", 40, 2019, False),
        ("Corporación Pesquera Inca", 3, 1812, False), ("Suministros Automotrices e Imp.", 70, 1554, False),
        ("Fortrac", 18, 1458, False), ("Mateel", 14, 882, False), ("World Motors", 1, 742, False),
        ("R & T Rockcat", 6, 629, False), ("JPK Mundo Parts", 6, 524, False), ("MODASA", 5, 504, False),
        ("P&G Repuestos", 10, 455, False), ("T&E Import Perú Repuestos", 15, 341, False),
        ("Agritractor", 5, 173, False), ("(persona natural)", 1, 134, False),
        ("Repadiesel Repuestos", 1, 111, False), ("Guerrero Motor's", 1, 42, False),
        ("Solutra del Perú", 3, 33, False),
    ],
    "RE48786": [
        ("Repaglas", 2361, 80901, True), ("IPESA", 790, 61262, False), ("Maquinarias y Repuestos", 61, 8276, False),
        ("IM Selva", 66, 7304, False), ("Tractor Import", 75, 6373, False), ("Italtrac Selva", 54, 4680, False),
        ("Monsante", 45, 4092, False), ("Dinámica", 102, 2078, False), ("Fortrac", 50, 1772, False),
        ("Suministros Automotrices e Imp.", 98, 1637, False), ("Mateel", 18, 864, False),
        ("Corporación Pesquera Inca", 8, 861, False), ("Manserved Dealer", 6, 653, False),
        ("Inversiones Palmetto", 24, 590, False), ("Maquitracto Selva", 16, 485, False),
        ("Tractor House Perú", 16, 379, False), ("R Y G Rockcat", 8, 376, False),
        ("Gamotor Electronic", 20, 330, False), ("Daxparts", 8, 324, False), ("JPK Mundo Parts", 12, 253, False),
        ("Cisar", 6, 217, False), ("T&E Import Perú Repuestos", 12, 200, False),
        ("Fabr. y Repar. Mult. e Industriales", 4, 190, False), ("Construcción Mecánica J&K", 12, 184, False),
    ],
    "RE500734": [
        ("Repaglas", 826, 64584, True), ("R & T Rockcat", 18, 1701, False), ("Dinámica", 30, 1650, False),
        ("Fortrac", 21, 1586, False), ("R Y G Rockcat", 12, 1233, False), ("Amazon Motors", 4, 689, False),
        ("T&E Import Perú Repuestos", 15, 368, False), ("Suministros Automotrices e Imp.", 5, 163, False),
        ("Construcción Mecánica J&K", 5, 125, False), ("Guerrero Motor's", 5, 101, False),
        ("Tralex", 2, 98, False), ("Autorepuestos A&T", 3, 84, False),
        ("Tractus Implementos y Partes", 2, 65, False), ("Agritractor", 2, 61, False),
    ],
    "RE501455": [
        ("Repaglas", 733, 57012, True), ("Dinámica", 78, 4038, False),
        ("Suministros Automotrices e Imp.", 36, 1695, False), ("R Y G Rockcat", 12, 1163, False),
        ("Fortrac", 7, 641, False), ("Mateel", 7, 538, False), ("JPK Mundo Parts", 8, 427, False),
        ("Repuestos y Accesorios El Paraíso", 4, 390, False), ("Guerrero Motor's", 40, 390, False),
        ("Agritractor", 4, 88, False), ("R & T Rockcat", 1, 88, False), ("Pro & Ma Nuevo Horizonte", 2, 43, False),
    ],
    "RE66820": [
        ("Repaglas", 4910, 61909, True), ("Dinámica", 300, 3486, False),
        ("Suministros Automotrices e Imp.", 288, 1348, False), ("R Y G Rockcat", 80, 1328, False),
        ("Mateel", 46, 701, False), ("Fortrac", 42, 617, False), ("T&E Import Perú Repuestos", 50, 192, False),
        ("JPK Mundo Parts", 8, 105, False), ("Tractorandinas Parts", 10, 56, False),
        ("AG Import Parve", 8, 40, False), ("Rinai Repuestos", 1, 10, False),
    ],
    "RE65966": [
        ("Repaglas", 657, 45825, True), ("Nuevo Concepto de Maquinarias Agro Industrial", 1, 29, False),
    ],
    "RE536083": [
        ("Repaglas", 418, 34739, True), ("Dinámica", 32, 1942, False), ("R Y G Rockcat", 12, 1272, False),
        ("JPK Mundo Parts", 8, 524, False),
    ],
    "R116383": [
        ("Repaglas", 1110, 28916, True), ("R & T Rockcat", 30, 880, False), ("R Y G Rockcat", 12, 380, False),
        ("Suministros Automotrices e Imp.", 36, 360, False), ("Agritractor", 12, 101, False),
        ("Pro & Ma Nuevo Horizonte", 4, 45, False),
    ],
}


@st.cache_data
def load_importadores_por_oem():
    """Lista completa de importadores por OEM: {oem: [{nombre, unidades, fob_total, es_repaglas}, ...]}."""
    out = {}
    for oem, rows in _IMPORTADORES_RAW.items():
        out[oem] = [
            {"nombre": nombre, "unidades": unidades, "fob_total": fob, "es_repaglas": es_rep}
            for nombre, unidades, fob, es_rep in rows
        ]
    return out


# Alternativas de marca para el mismo código OEM, encontradas en el catálogo Bsale
# (búsqueda por coincidencia del código OEM en el SKU, excluyendo Maxiforce).
_ALTERNATIVAS_RAW = {
    "RE507920": [],
    "RE507850": [("KMP", "RE507850", "Kit cilinder (camisa/pistón)", 8, 2595)],
    "RE504914": [
        ("KMP", "RE504914", "Bomba de aceite Powertech", 5, 2079),
        ("Vapormatic", "VRE504914", "Bomba aceite motor", 0, 0),
        ("Bepco", "BRE504914", "Bomba aceite motor 3 huecos", 0, 0),
        ("Compras Locales", "RE504914KS", "Bomba de aceite (KS)", 0, 0),
    ],
    "RE48786": [
        ("Fujian", "RE48786-FIP", "Inyector C/T", 21, 2705),
        ("Fujian", "CHRE48786", "Inyector de motor", 0, 0),
    ],
    "RE500734": [
        ("Bepco", "RE500734BEP", "Bomba de agua motor", 11, 4661),
        ("Ozgur", "RE500734OT", "Bomba de agua 2C Powertech", 12, 3387),
    ],
    "RE501455": [
        ("KMP", "RE501455", "Jgo. empaque motor Powertech", 3, 1356),
        ("TVH", "RE501455TVH", "Jgo. empaque motor (Tractorcraft Imp.)", 1, 310),
        ("TVH", "RE501455-TC", "Jgo. empaque motor", 0, 0),
    ],
    "RE66820": [("Bepco", "RE66820BEP", "Jgo. anillos de motor Std.", 4, 210)],
    "RE65966": [],
    "RE536083": [],
    "R116383": [("KMP", "R116383", "Camisa motor Powertech", 4, 475)],
}


@st.cache_data
def load_alternativas_marca():
    """Alternativas de marca (Bsale) por OEM: {oem: [{marca, sku, producto, cant26, venta26, precio_venta}, ...]}."""
    out = {}
    for oem, rows in _ALTERNATIVAS_RAW.items():
        items = []
        for marca, sku, producto, cant26, venta26 in rows:
            items.append(
                {
                    "marca": marca,
                    "sku": sku,
                    "producto": producto,
                    "cant26": cant26,
                    "venta26": venta26,
                    "precio_venta": (venta26 / cant26) if cant26 else 0.0,
                }
            )
        out[oem] = items
    return out
