"""Datos compartidos entre páginas del dashboard Frente Dinámica.

Los 10 SKU Maxiforce ancla se investigaron en ADEX Data Trade (Comercial.aspx,
búsqueda dirigida por código OEM + equivalente). Desde el 2026-09-01 el share,
el conteo de importadores y el país de origen por importador ya NO son
estimaciones a mano: se recalculan proceso­sando los 10 reportes Excel
descargados de ADEX ("TOP SKU MAX + EQUIVALENTES/Reporte_-_Importaciones_*.xlsx"),
deduplicados por DUA+RUC+cantidad+FOB (un mismo DUA puede salir en más de un
reporte cuando dos SKU ancla comparten archivo de búsqueda) y con las filas de
"29279" (equivalente de RE48786) filtradas a las que sí mencionan "48786" en la
descripción comercial — ese código por sí solo era demasiado genérico y traía
ruido de importadores no relacionados (Merck, Volvo, Ford, etc.).
"Share" = % del FOB total 2022–jul.2026 que concentra Repaglas (RUC 20118992009).
Los campos de venta/cantidad/margen vienen de Bsale
(`01 DASHBOARD/reportes finales/Dashboard_Ventas_20260818_1959.xlsx`, hoja
"SKU Comparativo", Ene-Jul 2026).
"""

import streamlit as st

REP = "#1f6feb"
DIN = "#ff7a1a"
GOOD = "#00c853"
AMBER = "#ffab00"
BAD = "#ff1744"
NO_MATERIAL = "#e4ddd0"  # gris casi invisible a propósito: lotes chicos que no deben distraer

# code, sku, producto, cant26, venta26 (S/, Ene-Jul), margen26_pct, share_full_pct,
# n_importadores, precio_fob_rep_usd (2025-26), rival_nombre, rival_share_pct (full periodo)
# share_full_pct / n_importadores / precio_fob_rep_usd / rival_* recalculados 2026-09-01
# desde los reportes ADEX reales (antes eran estimados a mano y subestimaban a IPESA en
# 6 de los 10 códigos — ver docstring del módulo).
_RAW = [
    ("RE65966",  "TRE65966",  "Kit camisa/pistón/anillos/pin/jebes/seguros", 96,  48332,  41.5, 83.6,  4, 74.41,
     "IPESA", 14.4),
    ("R116383",  "TR116383",  "Camisa de motor",                            188, 33035,  41.1, 94.2,  6, 27.39,
     "R & T Rockcat", 2.9),
    ("RE536083", "TRE536083", "Kit camisa/pistón/anillos/pin/jebes/seguros", 66,  37355,  39.9, 68.5,  6, 85.91,
     "IPESA", 15.3),
    ("RE500734", "TRE500734", "Bomba de agua motor",                        119, 64640,  42.0, 81.9, 21, 75.63,
     "Dinámica", 3.4),
    ("RE66820",  "TRE66820",  "Jgo. anillos de motor",                      632, 49781,  41.5, 88.7, 11, 12.72,
     "Dinámica", 5.0),
    ("RE507850", "TRE507850", "Kit camisa/pistón/anillos/pin/jebes/seguros", 189, 93542,  39.4, 59.3, 15, 73.59,
     "IPESA", 13.7),
    ("RE501455", "TRE501455", "Jgo. empaquetaduras de motor",               112, 59955,  40.2, 74.0, 21, 80.99,
     "IPESA", 9.7),
    ("RE504914", "TRE504914", "Bomba de aceite motor",                      132, 70817,  39.7, 42.3, 30, 86.12,
     "IPESA", 17.5),
    ("RE507920", "TRE507920", "Kit camisa/pistón/anillos/pin/jebes/seguros", 227, 106243, 40.2, 74.5, 14, 75.88,
     "IPESA", 8.2),
    ("RE48786",  "TRE48786",  "Inyector de motor",                          322, 67964,  42.2, 44.7, 24, 33.91,
     "IPESA", 33.0),
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


# Lista COMPLETA de importadores por código OEM (2022-jul.2026), recalculada 2026-09-01
# desde los 10 reportes ADEX reales en "TOP SKU MAX + EQUIVALENTES/" (ver docstring del
# módulo) — reemplaza la investigación a mano anterior, que subestimaba unidades/FOB de
# IPESA (y omitía por completo a varios importadores chicos) en 6 de los 10 códigos.
# Tupla: (nombre, unidades, fob_total, es_repaglas, origenes) — origenes es una tupla
# (país, unidades) por país de embarque, para saber de dónde trae cada importador ese SKU.
_IMPORTADORES_RAW = {
    "RE65966": [
        ("Repaglas", 657, 45825, True, (("Estados Unidos", 609), ("India", 40), ("Reino Unido", 8),)),
        ("IPESA", 51, 7907, False, (("Estados Unidos", 51),)),
        ("Corporación Pesquera Inca", 4, 1078, False, (("Estados Unidos", 4),)),
        ("Nuevo Concepto de Maquinarias Agro Industrial", 1, 29, False, (("China", 1),)),
    ],
    "R116383": [
        ("Repaglas", 1110, 28916, True, (("Estados Unidos", 1098), ("Reino Unido", 12),)),
        ("Suministros Automotrices e Imp.", 36, 360, False, (("China", 36),)),
        ("R & T Rockcat", 30, 880, False, (("Estados Unidos", 30),)),
        ("Agritractor", 12, 101, False, (("China", 12),)),
        ("R Y G Rockcat", 12, 380, False, (("Estados Unidos", 12),)),
        ("Pro & Ma Nuevo Horizonte", 4, 45, False, (("China", 4),)),
    ],
    "RE536083": [
        ("Repaglas", 422, 34971, True, (("Estados Unidos", 418), ("Reino Unido", 4),)),
        ("IPESA", 60, 7830, False, (("Estados Unidos", 60),)),
        ("Dinámica", 32, 1942, False, (("China", 32),)),
        ("Fortrac", 24, 4536, False, (("Estados Unidos", 24),)),
        ("R Y G Rockcat", 12, 1272, False, (("Estados Unidos", 12),)),
        ("JPK Mundo Parts", 8, 524, False, (("China", 8),)),
    ],
    "RE500734": [
        ("Repaglas", 846, 65395, True, (("Estados Unidos", 746), ("India", 40), ("Turquía", 20), ("China", 20), ("Reino Unido", 20),)),
        ("Suministros Automotrices e Imp.", 65, 1611, False, (("China", 65),)),
        ("Dinámica", 55, 2686, False, (("Turquía", 50), ("Italia", 5),)),
        ("P&G Repuestos", 40, 1023, False, (("China", 40),)),
        ("Fortrac", 31, 1938, False, (("Estados Unidos", 21), ("Turquía", 10),)),
        ("R & T Rockcat", 24, 2170, False, (("Estados Unidos", 24),)),
        ("Repuestos y Accesorios El Paraíso", 17, 979, False, (("Brasil", 17),)),
        ("T&E Import Perú Repuestos", 15, 368, False, (("China", 15),)),
        ("R Y G Rockcat", 12, 1233, False, (("Estados Unidos", 12),)),
        ("Tralex", 7, 300, False, (("Estados Unidos", 4), ("Turquía", 3),)),
        ("Guerrero Motor's", 7, 137, False, (("China", 7),)),
        ("Maquitracto Selva", 6, 231, False, (("China", 6),)),
        ("Construcción Mecánica J&K", 5, 125, False, (("China", 5),)),
        ("Amazon Motors", 4, 689, False, (("Estados Unidos", 4),)),
        ("Autorepuestos A&T", 3, 84, False, (("China", 3),)),
        ("Agroindustrias San Jacinto", 3, 490, False, (("Brasil", 3),)),
        ("Agritractor", 2, 61, False, (("China", 2),)),
        ("Serviagri de Ica", 2, 184, False, (("Estados Unidos", 2),)),
        ("Pitahaya Servicios Integrales", 2, 61, False, (("China", 2),)),
        ("Tractus Implementos y Partes", 2, 65, False, (("Turquía", 2),)),
        ("Cisar", 1, 54, False, (("China", 1),)),
    ],
    "RE66820": [
        ("Repaglas", 4910, 61909, True, (("Estados Unidos", 4680), ("China", 230),)),
        ("Dinámica", 300, 3486, False, (("China", 300),)),
        ("Suministros Automotrices e Imp.", 288, 1348, False, (("China", 288),)),
        ("R Y G Rockcat", 80, 1328, False, (("Estados Unidos", 80),)),
        ("T&E Import Perú Repuestos", 50, 192, False, (("China", 50),)),
        ("Mateel", 46, 701, False, (("Estados Unidos", 46),)),
        ("Fortrac", 42, 617, False, (("Estados Unidos", 42),)),
        ("Tractorandinas Parts", 10, 56, False, (("Brasil", 10),)),
        ("JPK Mundo Parts", 8, 105, False, (("China", 8),)),
        ("AG Import Parve", 8, 40, False, (("China", 8),)),
        ("Rinai Repuestos", 1, 10, False, (("Italia", 1),)),
    ],
    "RE507850": [
        ("Repaglas", 1296, 92294, True, (("Estados Unidos", 1196), ("Reino Unido", 60), ("India", 40),)),
        ("IPESA", 207, 21406, False, (("Estados Unidos", 203), ("Argentina", 4),)),
        ("Fortrac", 194, 13868, False, (("Estados Unidos", 194),)),
        ("Dinámica", 60, 3358, False, (("China", 60),)),
        ("Cisar", 50, 4390, False, (("Brasil", 50),)),
        ("Maquinarias y Repuestos", 36, 9998, False, (("Estados Unidos", 36),)),
        ("Mateel", 18, 793, False, (("Estados Unidos", 18),)),
        ("Tractor Import", 8, 1721, False, (("Estados Unidos", 8),)),
        ("MODASA", 8, 555, False, (("China", 8),)),
        ("IM Selva", 7, 3585, False, (("Estados Unidos", 7),)),
        ("Italtrac Selva", 6, 1105, False, (("Estados Unidos", 6),)),
        ("ITM Tractor", 6, 743, False, (("Estados Unidos", 6),)),
        ("Monsante", 6, 1399, False, (("Estados Unidos", 6),)),
        ("R Y G Rockcat", 4, 334, False, (("Estados Unidos", 4),)),
        ("R & T Rockcat", 2, 152, False, (("Estados Unidos", 2),)),
    ],
    "RE501455": [
        ("Repaglas", 738, 57211, True, (("Estados Unidos", 692), ("India", 20), ("Reino Unido", 15), ("Brasil", 11),)),
        ("Dinámica", 82, 4182, False, (("China", 78), ("Reino Unido", 4),)),
        ("Guerrero Motor's", 40, 390, False, (("Turquía", 40),)),
        ("Suministros Automotrices e Imp.", 36, 1695, False, (("China", 36),)),
        ("IPESA", 35, 7510, False, (("Estados Unidos", 35),)),
        ("Fortrac", 13, 840, False, (("Estados Unidos", 7), ("Turquía", 6),)),
        ("R Y G Rockcat", 12, 1163, False, (("Estados Unidos", 12),)),
        ("Mateel", 8, 668, False, (("Estados Unidos", 8),)),
        ("JPK Mundo Parts", 8, 427, False, (("China", 8),)),
        ("Construcción Mecánica J&K", 6, 123, False, (("China", 6),)),
        ("MODASA", 5, 321, False, (("China", 5),)),
        ("Monsante", 4, 845, False, (("Estados Unidos", 4),)),
        ("Agritractor", 4, 88, False, (("China", 4),)),
        ("Repuestos y Accesorios El Paraíso", 4, 390, False, (("Italia", 4),)),
        ("P&G Repuestos", 3, 122, False, (("Turquía", 3),)),
        ("Solutra del Perú", 2, 81, False, (("Reino Unido", 1), ("China", 1),)),
        ("Pro & Ma Nuevo Horizonte", 2, 43, False, (("China", 2),)),
        ("National Air & Motor", 1, 356, False, (("Estados Unidos", 1),)),
        ("R & T Rockcat", 1, 88, False, (("Estados Unidos", 1),)),
        ("Geprocem", 1, 345, False, (("Estados Unidos", 1),)),
        ("Corporación Pesquera Inca", 1, 370, False, (("Estados Unidos", 1),)),
    ],
    "RE504914": [
        ("Repaglas", 819, 71042, True, (("Estados Unidos", 776), ("China", 25), ("Reino Unido", 13), ("Brasil", 5),)),
        ("IPESA", 130, 29426, False, (("Argentina", 66), ("Estados Unidos", 48), ("Argelia", 16),)),
        ("Fortrac", 73, 15039, False, (("Estados Unidos", 63), ("Argentina", 6), ("Reino Unido", 4),)),
        ("Suministros Automotrices e Imp.", 70, 1554, False, (("China", 70),)),
        ("Dinámica", 40, 2019, False, (("Reino Unido", 40),)),
        ("Maquinarias y Repuestos", 29, 17146, False, (("Estados Unidos", 29),)),
        ("R Y G Rockcat", 20, 2213, False, (("Estados Unidos", 20),)),
        ("T&E Import Perú Repuestos", 15, 341, False, (("China", 15),)),
        ("Mateel", 15, 1422, False, (("Estados Unidos", 15),)),
        ("Monsante", 13, 6481, False, (("Estados Unidos", 5), ("Argelia", 3), ("India", 3), ("Argentina", 2),)),
        ("P&G Repuestos", 10, 455, False, (("Turquía", 10),)),
        ("IM Selva", 9, 5991, False, (("Estados Unidos", 6), ("Argentina", 3),)),
        ("Italtrac Selva", 6, 2488, False, (("Argentina", 6),)),
        ("R & T Rockcat", 6, 629, False, (("Estados Unidos", 6),)),
        ("JPK Mundo Parts", 6, 524, False, (("China", 6),)),
        ("Agritractor", 5, 173, False, (("China", 5),)),
        ("MODASA", 5, 504, False, (("China", 5),)),
        ("Tractor Import", 4, 2509, False, (("Estados Unidos", 4),)),
        ("Geprocem", 3, 1525, False, (("Estados Unidos", 3),)),
        ("Solutra del Perú", 3, 33, False, (("China", 3),)),
        ("(Persona natural — dato protegido)", 2, 782, False, (("Estados Unidos", 1), ("Reino Unido", 1),)),
        ("Cisar", 2, 155, False, (("Italia", 2),)),
        ("Corporación Pesquera Inca", 2, 1206, False, (("Estados Unidos", 2),)),
        ("Baustelle", 1, 1369, False, (("Estados Unidos", 1),)),
        ("World Motors", 1, 742, False, (("Estados Unidos", 1),)),
        ("National Air & Motor", 1, 726, False, (("Estados Unidos", 1),)),
        ("Parts and Services BVC", 1, 820, False, (("Argentina", 1),)),
        ("Guerrero Motor's", 1, 42, False, (("China", 1),)),
        ("Repadiesel Repuestos", 1, 111, False, (("Estados Unidos", 1),)),
        ("Emimaq", 1, 595, False, (("Reino Unido", 1),)),
    ],
    "RE507920": [
        ("Repaglas", 1676, 125602, True, (("Estados Unidos", 1595), ("Reino Unido", 41), ("India", 40),)),
        ("IPESA", 202, 13830, False, (("Estados Unidos", 202),)),
        ("Fortrac", 79, 11974, False, (("Estados Unidos", 79),)),
        ("Dinámica", 61, 3406, False, (("China", 61),)),
        ("R Y G Rockcat", 28, 2583, False, (("Estados Unidos", 28),)),
        ("Mateel", 24, 1516, False, (("Estados Unidos", 24),)),
        ("R & T Rockcat", 24, 2008, False, (("Estados Unidos", 24),)),
        ("JPK Mundo Parts", 16, 921, False, (("China", 16),)),
        ("Tractor Import", 14, 2605, False, (("Estados Unidos", 10), ("Brasil", 4),)),
        ("MODASA", 12, 832, False, (("China", 12),)),
        ("Italtrac Selva", 6, 983, False, (("Estados Unidos", 6),)),
        ("Monsante", 6, 1028, False, (("Estados Unidos", 6),)),
        ("National Air & Motor", 4, 1001, False, (("Estados Unidos", 4),)),
        ("Solutra del Perú", 4, 272, False, (("China", 4),)),
    ],
    "RE48786": [
        ("Repaglas", 2361, 80901, True, (("Estados Unidos", 2301), ("China", 60),)),
        ("IPESA", 772, 59733, False, (("China", 484), ("Emiratos Árabes Unidos", 120), ("Estados Unidos", 102), ("Camerún", 66),)),
        ("Dinámica", 102, 2078, False, (("China", 90), ("Turquía", 12),)),
        ("Suministros Automotrices e Imp.", 98, 1637, False, (("China", 98),)),
        ("Tractor Import", 75, 6373, False, (("Estados Unidos", 75),)),
        ("Maquinarias y Repuestos", 61, 8276, False, (("Estados Unidos", 61),)),
        ("IM Selva", 54, 5963, False, (("China", 48), ("Estados Unidos", 6),)),
        ("Italtrac Selva", 54, 4680, False, (("China", 26), ("Estados Unidos", 16), ("Emiratos Árabes Unidos", 12),)),
        ("Fortrac", 50, 1772, False, (("Turquía", 50),)),
        ("Monsante", 45, 4092, False, (("China", 40), ("Estados Unidos", 5),)),
        ("Inversiones Palmetto", 24, 590, False, (("Estados Unidos", 24),)),
        ("Gamotor Electronic", 20, 330, False, (("China", 20),)),
        ("Mateel", 18, 864, False, (("Turquía", 18),)),
        ("Maquitracto Selva", 16, 485, False, (("China", 16),)),
        ("Tractor House Perú", 16, 379, False, (("China", 16),)),
        ("T&E Import Perú Repuestos", 12, 200, False, (("China", 12),)),
        ("JPK Mundo Parts", 12, 253, False, (("China", 12),)),
        ("Construcción Mecánica J&K", 12, 184, False, (("China", 12),)),
        ("Daxparts", 8, 324, False, (("Estados Unidos", 8),)),
        ("R Y G Rockcat", 8, 376, False, (("Estados Unidos", 8),)),
        ("Cisar", 6, 217, False, (("Turquía", 6),)),
        ("Manserved Dealer", 6, 653, False, (("Estados Unidos", 6),)),
        ("Fabr. y Repar. Mult. e Industriales", 4, 190, False, (("Estados Unidos", 4),)),
        ("Corporación Pesquera Inca", 4, 431, False, (("Estados Unidos", 4),)),
    ],
}


@st.cache_data
def load_importadores_por_oem():
    """Lista completa de importadores por OEM:
    {oem: [{nombre, unidades, fob_total, es_repaglas, origenes}, ...]}.
    `origenes` es una lista [{pais, unidades}, ...] con el desglose de país de
    embarque de ese importador para ese SKU (algunos traen de más de un país)."""
    out = {}
    for oem, rows in _IMPORTADORES_RAW.items():
        out[oem] = [
            {
                "nombre": nombre, "unidades": unidades, "fob_total": fob, "es_repaglas": es_rep,
                "origenes": [{"pais": pais, "unidades": u} for pais, u in origenes],
            }
            for nombre, unidades, fob, es_rep, origenes in rows
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
