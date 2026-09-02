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
# Tupla: (nombre, unidades, fob_total, cif_total, es_repaglas, origenes) — origenes es una
# tupla (país, unidades) por país de embarque. cif_total = FOB + flete + seguro (costo
# puesto en el puerto de Callao antes de aranceles/agente/almacenaje).
_IMPORTADORES_RAW = {
    "RE65966": [
        ("Repaglas", 657, 45825, 47723, True, (("Estados Unidos", 609), ("India", 40), ("Reino Unido", 8),)),
        ("IPESA", 51, 7907, 8253, False, (("Estados Unidos", 51),)),
        ("Corporación Pesquera Inca", 4, 1078, 1143, False, (("Estados Unidos", 4),)),
        ("Nuevo Concepto de Maquinarias Agro Industrial", 1, 29, 49, False, (("China", 1),)),
    ],
    "R116383": [
        ("Repaglas", 1110, 28916, 30535, True, (("Estados Unidos", 1098), ("Reino Unido", 12),)),
        ("Suministros Automotrices e Imp.", 36, 360, 397, False, (("China", 36),)),
        ("R & T Rockcat", 30, 880, 912, False, (("Estados Unidos", 30),)),
        ("Agritractor", 12, 101, 113, False, (("China", 12),)),
        ("R Y G Rockcat", 12, 380, 388, False, (("Estados Unidos", 12),)),
        ("Pro & Ma Nuevo Horizonte", 4, 45, 48, False, (("China", 4),)),
    ],
    "RE536083": [
        ("Repaglas", 422, 34971, 36097, True, (("Estados Unidos", 418), ("Reino Unido", 4),)),
        ("IPESA", 60, 7830, 8061, False, (("Estados Unidos", 60),)),
        ("Dinámica", 32, 1942, 1995, False, (("China", 32),)),
        ("Fortrac", 24, 4536, 4771, False, (("Estados Unidos", 24),)),
        ("R Y G Rockcat", 12, 1272, 1303, False, (("Estados Unidos", 12),)),
        ("JPK Mundo Parts", 8, 524, 537, False, (("China", 8),)),
    ],
    "RE500734": [
        ("Repaglas", 846, 65395, 66766, True, (("Estados Unidos", 746), ("India", 40), ("Turquía", 20), ("China", 20), ("Reino Unido", 20),)),
        ("Suministros Automotrices e Imp.", 65, 1611, 1714, False, (("China", 65),)),
        ("Dinámica", 55, 2686, 2779, False, (("Turquía", 50), ("Italia", 5),)),
        ("P&G Repuestos", 40, 1023, 1041, False, (("China", 40),)),
        ("Fortrac", 31, 1938, 2142, False, (("Estados Unidos", 21), ("Turquía", 10),)),
        ("R & T Rockcat", 24, 2170, 2228, False, (("Estados Unidos", 24),)),
        ("Repuestos y Accesorios El Paraíso", 17, 979, 1000, False, (("Brasil", 17),)),
        ("T&E Import Perú Repuestos", 15, 368, 377, False, (("China", 15),)),
        ("R Y G Rockcat", 12, 1233, 1254, False, (("Estados Unidos", 12),)),
        ("Tralex", 7, 300, 327, False, (("Estados Unidos", 4), ("Turquía", 3),)),
        ("Guerrero Motor's", 7, 137, 139, False, (("China", 7),)),
        ("Maquitracto Selva", 6, 231, 236, False, (("China", 6),)),
        ("Construcción Mecánica J&K", 5, 125, 129, False, (("China", 5),)),
        ("Amazon Motors", 4, 689, 703, False, (("Estados Unidos", 4),)),
        ("Autorepuestos A&T", 3, 84, 86, False, (("China", 3),)),
        ("Agroindustrias San Jacinto", 3, 490, 526, False, (("Brasil", 3),)),
        ("Agritractor", 2, 61, 68, False, (("China", 2),)),
        ("Serviagri de Ica", 2, 184, 190, False, (("Estados Unidos", 2),)),
        ("Pitahaya Servicios Integrales", 2, 61, 76, False, (("China", 2),)),
        ("Tractus Implementos y Partes", 2, 65, 66, False, (("Turquía", 2),)),
        ("Cisar", 1, 54, 59, False, (("China", 1),)),
    ],
    "RE66820": [
        ("Repaglas", 4910, 61909, 62532, True, (("Estados Unidos", 4680), ("China", 230),)),
        ("Dinámica", 300, 3486, 3548, False, (("China", 300),)),
        ("Suministros Automotrices e Imp.", 288, 1348, 1402, False, (("China", 288),)),
        ("R Y G Rockcat", 80, 1328, 1350, False, (("Estados Unidos", 80),)),
        ("T&E Import Perú Repuestos", 50, 192, 198, False, (("China", 50),)),
        ("Mateel", 46, 701, 755, False, (("Estados Unidos", 46),)),
        ("Fortrac", 42, 617, 654, False, (("Estados Unidos", 42),)),
        ("Tractorandinas Parts", 10, 56, 69, False, (("Brasil", 10),)),
        ("JPK Mundo Parts", 8, 105, 107, False, (("China", 8),)),
        ("AG Import Parve", 8, 40, 41, False, (("China", 8),)),
        ("Rinai Repuestos", 1, 10, 12, False, (("Italia", 1),)),
    ],
    "RE507850": [
        ("Repaglas", 1296, 92294, 95754, True, (("Estados Unidos", 1196), ("Reino Unido", 60), ("India", 40),)),
        ("IPESA", 207, 21406, 22036, False, (("Estados Unidos", 203), ("Argentina", 4),)),
        ("Fortrac", 194, 13868, 14439, False, (("Estados Unidos", 194),)),
        ("Dinámica", 60, 3358, 3492, False, (("China", 60),)),
        ("Cisar", 50, 4390, 4478, False, (("Brasil", 50),)),
        ("Maquinarias y Repuestos", 36, 9998, 10183, False, (("Estados Unidos", 36),)),
        ("Mateel", 18, 793, 934, False, (("Estados Unidos", 18),)),
        ("Tractor Import", 8, 1721, 1869, False, (("Estados Unidos", 8),)),
        ("MODASA", 8, 555, 587, False, (("China", 8),)),
        ("IM Selva", 7, 3585, 3734, False, (("Estados Unidos", 7),)),
        ("Italtrac Selva", 6, 1105, 1192, False, (("Estados Unidos", 6),)),
        ("ITM Tractor", 6, 743, 831, False, (("Estados Unidos", 6),)),
        ("Monsante", 6, 1399, 1494, False, (("Estados Unidos", 6),)),
        ("R Y G Rockcat", 4, 334, 341, False, (("Estados Unidos", 4),)),
        ("R & T Rockcat", 2, 152, 156, False, (("Estados Unidos", 2),)),
    ],
    "RE501455": [
        ("Repaglas", 738, 57211, 57749, True, (("Estados Unidos", 692), ("India", 20), ("Reino Unido", 15), ("Brasil", 11),)),
        ("Dinámica", 82, 4182, 4250, False, (("China", 78), ("Reino Unido", 4),)),
        ("Guerrero Motor's", 40, 390, 404, False, (("Turquía", 40),)),
        ("Suministros Automotrices e Imp.", 36, 1695, 1808, False, (("China", 36),)),
        ("IPESA", 35, 7510, 7774, False, (("Estados Unidos", 35),)),
        ("Fortrac", 13, 840, 936, False, (("Estados Unidos", 7), ("Turquía", 6),)),
        ("R Y G Rockcat", 12, 1163, 1192, False, (("Estados Unidos", 12),)),
        ("Mateel", 8, 668, 732, False, (("Estados Unidos", 8),)),
        ("JPK Mundo Parts", 8, 427, 437, False, (("China", 8),)),
        ("Construcción Mecánica J&K", 6, 123, 127, False, (("China", 6),)),
        ("MODASA", 5, 321, 331, False, (("China", 5),)),
        ("Monsante", 4, 845, 885, False, (("Estados Unidos", 4),)),
        ("Agritractor", 4, 88, 99, False, (("China", 4),)),
        ("Repuestos y Accesorios El Paraíso", 4, 390, 434, False, (("Italia", 4),)),
        ("P&G Repuestos", 3, 122, 142, False, (("Turquía", 3),)),
        ("Solutra del Perú", 2, 81, 84, False, (("Reino Unido", 1), ("China", 1),)),
        ("Pro & Ma Nuevo Horizonte", 2, 43, 46, False, (("China", 2),)),
        ("National Air & Motor", 1, 356, 367, False, (("Estados Unidos", 1),)),
        ("R & T Rockcat", 1, 88, 90, False, (("Estados Unidos", 1),)),
        ("Geprocem", 1, 345, 368, False, (("Estados Unidos", 1),)),
        ("Corporación Pesquera Inca", 1, 370, 393, False, (("Estados Unidos", 1),)),
    ],
    "RE504914": [
        ("Repaglas", 819, 71042, 71986, True, (("Estados Unidos", 776), ("China", 25), ("Reino Unido", 13), ("Brasil", 5),)),
        ("IPESA", 130, 29426, 30101, False, (("Argentina", 66), ("Estados Unidos", 48), ("Argelia", 16),)),
        ("Fortrac", 73, 15039, 15955, False, (("Estados Unidos", 63), ("Argentina", 6), ("Reino Unido", 4),)),
        ("Suministros Automotrices e Imp.", 70, 1554, 1592, False, (("China", 70),)),
        ("Dinámica", 40, 2019, 2076, False, (("Reino Unido", 40),)),
        ("Maquinarias y Repuestos", 29, 17146, 17508, False, (("Estados Unidos", 29),)),
        ("R Y G Rockcat", 20, 2213, 2266, False, (("Estados Unidos", 20),)),
        ("T&E Import Perú Repuestos", 15, 341, 350, False, (("China", 15),)),
        ("Mateel", 15, 1422, 1570, False, (("Estados Unidos", 15),)),
        ("Monsante", 13, 6481, 6719, False, (("Estados Unidos", 5), ("Argelia", 3), ("India", 3), ("Argentina", 2),)),
        ("P&G Repuestos", 10, 455, 529, False, (("Turquía", 10),)),
        ("IM Selva", 9, 5991, 6130, False, (("Estados Unidos", 6), ("Argentina", 3),)),
        ("Italtrac Selva", 6, 2488, 2843, False, (("Argentina", 6),)),
        ("R & T Rockcat", 6, 629, 646, False, (("Estados Unidos", 6),)),
        ("JPK Mundo Parts", 6, 524, 537, False, (("China", 6),)),
        ("Agritractor", 5, 173, 193, False, (("China", 5),)),
        ("MODASA", 5, 504, 513, False, (("China", 5),)),
        ("Tractor Import", 4, 2509, 2649, False, (("Estados Unidos", 4),)),
        ("Geprocem", 3, 1525, 1542, False, (("Estados Unidos", 3),)),
        ("Solutra del Perú", 3, 33, 34, False, (("China", 3),)),
        ("(Persona natural — dato protegido)", 2, 782, 806, False, (("Estados Unidos", 1), ("Reino Unido", 1),)),
        ("Cisar", 2, 155, 169, False, (("Italia", 2),)),
        ("Corporación Pesquera Inca", 2, 1206, 1287, False, (("Estados Unidos", 2),)),
        ("Baustelle", 1, 1369, 1409, False, (("Estados Unidos", 1),)),
        ("World Motors", 1, 742, 767, False, (("Estados Unidos", 1),)),
        ("National Air & Motor", 1, 726, 747, False, (("Estados Unidos", 1),)),
        ("Parts and Services BVC", 1, 820, 856, False, (("Argentina", 1),)),
        ("Guerrero Motor's", 1, 42, 45, False, (("China", 1),)),
        ("Repadiesel Repuestos", 1, 111, 123, False, (("Estados Unidos", 1),)),
        ("Emimaq", 1, 595, 607, False, (("Reino Unido", 1),)),
    ],
    "RE507920": [
        ("Repaglas", 1676, 125602, 130013, True, (("Estados Unidos", 1595), ("Reino Unido", 41), ("India", 40),)),
        ("IPESA", 202, 13830, 14262, False, (("Estados Unidos", 202),)),
        ("Fortrac", 79, 11974, 12506, False, (("Estados Unidos", 79),)),
        ("Dinámica", 61, 3406, 3480, False, (("China", 61),)),
        ("R Y G Rockcat", 28, 2583, 2754, False, (("Estados Unidos", 28),)),
        ("Mateel", 24, 1516, 1687, False, (("Estados Unidos", 24),)),
        ("R & T Rockcat", 24, 2008, 2062, False, (("Estados Unidos", 24),)),
        ("JPK Mundo Parts", 16, 921, 942, False, (("China", 16),)),
        ("Tractor Import", 14, 2605, 2804, False, (("Estados Unidos", 10), ("Brasil", 4),)),
        ("MODASA", 12, 832, 880, False, (("China", 12),)),
        ("Italtrac Selva", 6, 983, 1150, False, (("Estados Unidos", 6),)),
        ("Monsante", 6, 1028, 1054, False, (("Estados Unidos", 6),)),
        ("National Air & Motor", 4, 1001, 1030, False, (("Estados Unidos", 4),)),
        ("Solutra del Perú", 4, 272, 283, False, (("China", 4),)),
    ],
    "RE48786": [
        ("Repaglas", 2361, 80901, 81338, True, (("Estados Unidos", 2301), ("China", 60),)),
        ("IPESA", 772, 59733, 61533, False, (("China", 484), ("Emiratos Árabes Unidos", 120), ("Estados Unidos", 102), ("Camerún", 66),)),
        ("Dinámica", 102, 2078, 2135, False, (("China", 90), ("Turquía", 12),)),
        ("Suministros Automotrices e Imp.", 98, 1637, 1688, False, (("China", 98),)),
        ("Tractor Import", 75, 6373, 6785, False, (("Estados Unidos", 75),)),
        ("Maquinarias y Repuestos", 61, 8276, 8556, False, (("Estados Unidos", 61),)),
        ("IM Selva", 54, 5963, 6612, False, (("China", 48), ("Estados Unidos", 6),)),
        ("Italtrac Selva", 54, 4680, 5251, False, (("China", 26), ("Estados Unidos", 16), ("Emiratos Árabes Unidos", 12),)),
        ("Fortrac", 50, 1772, 2282, False, (("Turquía", 50),)),
        ("Monsante", 45, 4092, 4250, False, (("China", 40), ("Estados Unidos", 5),)),
        ("Inversiones Palmetto", 24, 590, 665, False, (("Estados Unidos", 24),)),
        ("Gamotor Electronic", 20, 330, 332, False, (("China", 20),)),
        ("Mateel", 18, 864, 881, False, (("Turquía", 18),)),
        ("Maquitracto Selva", 16, 485, 495, False, (("China", 16),)),
        ("Tractor House Perú", 16, 379, 386, False, (("China", 16),)),
        ("T&E Import Perú Repuestos", 12, 200, 205, False, (("China", 12),)),
        ("JPK Mundo Parts", 12, 253, 259, False, (("China", 12),)),
        ("Construcción Mecánica J&K", 12, 184, 191, False, (("China", 12),)),
        ("Daxparts", 8, 324, 335, False, (("Estados Unidos", 8),)),
        ("R Y G Rockcat", 8, 376, 384, False, (("Estados Unidos", 8),)),
        ("Cisar", 6, 217, 237, False, (("Turquía", 6),)),
        ("Manserved Dealer", 6, 653, 671, False, (("Estados Unidos", 6),)),
        ("Fabr. y Repar. Mult. e Industriales", 4, 190, 215, False, (("Estados Unidos", 4),)),
        ("Corporación Pesquera Inca", 4, 431, 457, False, (("Estados Unidos", 4),)),
    ],
}


@st.cache_data
def load_importadores_por_oem():
    """Lista completa de importadores por OEM:
    {oem: [{nombre, unidades, fob_total, cif_total, es_repaglas, origenes}, ...]}.
    `origenes` es una lista [{pais, unidades}, ...] con el desglose de país de
    embarque de ese importador para ese SKU (algunos traen de más de un país)."""
    out = {}
    for oem, rows in _IMPORTADORES_RAW.items():
        out[oem] = [
            {
                "nombre": nombre, "unidades": unidades, "fob_total": fob, "cif_total": cif,
                "es_repaglas": es_rep,
                "origenes": [{"pais": pais, "unidades": u} for pais, u in origenes],
            }
            for nombre, unidades, fob, cif, es_rep, origenes in rows
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


# Unidades importadas por año por OEM — Repaglas y sus 2 rivales más cercanos por volumen
# histórico (no "resto" agregado) — calculado 2026-09-01 desde los mismos 10 reportes ADEX
# reales. share_pct = % del FOB total 2022-jul.2026 de ese rival (mismo criterio que _RAW).
# precio_vs_repaglas_pct = FOB/unidad del rival como % del FOB/unidad de Repaglas, full periodo
# (100% = mismo precio; <75% = rival claramente más barato; >110% = más caro/premium).
# lectura = interpretación de precio + trayectoria de compras, hecha a mano cruzando ambos ejes
# (un rival "barato y creciendo" importa mucho más que uno "caro y en retirada", aunque el
# share agregado de Repaglas no distinga entre ambos). 2026 es parcial (solo hasta julio).
_TENDENCIA_IMPORTADOR_RAW = {
    "RE65966": {
        "repaglas": {2022: 80, 2023: 164, 2024: 161, 2025: 152, 2026: 100},
        "rivales": [
            ("IPESA", 14.4, 222, "Se retira (47→4→0→0) y siempre pagó 2.2x el precio de Repaglas — no compite en precio.",
             {2022: 47, 2023: 4}),
            ("Corporación Pesquera Inca", 2.0, 386, "Comprador ocasional a precio muy alto (3.9x) — no es amenaza de precio.",
             {2026: 4}),
        ],
    },
    "R116383": {
        "repaglas": {2022: 250, 2023: 190, 2024: 300, 2025: 238, 2026: 132},
        "rivales": [
            ("R & T Rockcat", 2.9, 113, "Volumen marginal y precio a la par — no mueve el mercado.",
             {2022: 12, 2024: 18}),
            ("Suministros Automotrices e Imp.", 1.2, 38, "Compró barato (38% del precio) una sola vez (2022) y no volvió en 4 años — dormido, no confirmado como retiro.",
             {2022: 36}),
        ],
    },
    "RE536083": {
        "repaglas": {2022: 56, 2023: 72, 2024: 132, 2025: 98, 2026: 64},
        "rivales": [
            ("IPESA", 15.3, 157, "Compró una sola vez (2022) a precio alto (1.6x) y no repitió.",
             {2022: 60}),
            ("Dinámica", 3.8, 73, "Más barato (73%) pero volumen chico y estable, sin señal de crecer.",
             {2022: 10, 2023: 12, 2025: 10}),
        ],
    },
    "RE500734": {
        "repaglas": {2022: 139, 2023: 93, 2024: 242, 2025: 242, 2026: 130},
        "rivales": [
            ("Dinámica", 3.4, 63, "Barato (63%) y reactivado en 2025 (30u) tras un hueco de 2 años — vigilar si sigue en 2026.",
             {2022: 25, 2025: 30}),
            ("Suministros Automotrices e Imp.", 2.0, 32, "Muy barato (32%) pero cayó fuerte (55→10 parcial) — hoy no es volumen relevante.",
             {2022: 55, 2026: 10}),
        ],
    },
    "RE66820": {
        "repaglas": {2022: 1270, 2023: 970, 2024: 1170, 2025: 1050, 2026: 450},
        "rivales": [
            ("Dinámica", 5.0, 92, "A la par de precio (92%) y bajando (180→120) — no es el riesgo principal aquí.",
             {2022: 180, 2024: 120}),
            ("Suministros Automotrices e Imp.", 1.9, 37, "Muy barato (37%) y casi triplicó su volumen (72→216) — el rival de precio más agresivo de toda la canasta, y va creciendo.",
             {2022: 72, 2024: 216}),
        ],
    },
    "RE507850": {
        "repaglas": {2022: 150, 2023: 184, 2024: 328, 2025: 402, 2026: 232},
        "rivales": [
            ("IPESA", 13.7, 145, "Se retira (103→104→0→0→0) pagando 1.45x el precio de Repaglas — no compite en precio.",
             {2022: 103, 2023: 104}),
            ("Fortrac", 8.9, 100, "Precio idéntico al de Repaglas (100%) y su volumen se cuadruplicó en 2025 (33→139) — la señal más seria de la canasta, no subir precio todavía.",
             {2022: 33, 2025: 139, 2026: 22}),
        ],
    },
    "RE501455": {
        "repaglas": {2022: 135, 2023: 105, 2024: 192, 2025: 191, 2026: 115},
        "rivales": [
            ("Dinámica", 5.4, 66, "Barato (66%) con presencia en 4 de 5 años, pero sin tendencia clara de crecimiento.",
             {2022: 24, 2023: 8, 2024: 30, 2025: 20}),
            ("Guerrero Motor's", 0.5, 13, "Extremadamente barato (13% del precio) una sola vez (2022) y no volvió en 4 años — dormido, vigilar.",
             {2022: 40}),
        ],
    },
    "RE504914": {
        "repaglas": {2022: 135, 2023: 96, 2024: 184, 2025: 238, 2026: 166},
        "rivales": [
            ("IPESA", 17.5, 261, "Caro (2.6x) y en declive sostenido y consistente (66→50→9→5→0) — no es un problema de precio.",
             {2022: 66, 2023: 50, 2024: 9, 2025: 5}),
            ("Fortrac", 8.9, 238, "Caro (2.4x), con un repunte en 2025 (30u) pero sin competir en precio.",
             {2022: 14, 2023: 8, 2024: 9, 2025: 30, 2026: 12}),
        ],
    },
    "RE507920": {
        "repaglas": {2022: 330, 2023: 252, 2024: 365, 2025: 473, 2026: 256},
        "rivales": [
            ("IPESA", 8.2, 91, "A la par de precio (91%) y en retirada total (93→87→22→0→0) — el caso más limpio de los 10 SKU.",
             {2022: 93, 2023: 87, 2024: 22}),
            ("Fortrac", 7.1, 202, "Caro (2x) y marginal — no es amenaza de precio.",
             {2022: 19, 2023: 16, 2025: 28, 2026: 16}),
        ],
    },
    "RE48786": {
        "repaglas": {2022: 380, 2023: 439, 2024: 620, 2025: 592, 2026: 330},
        "rivales": [
            ("IPESA", 33.0, 226, "Caro (2.3x) pero con volumen históricamente grande (526, 246 unidades) — se retiró 3 años (0 en 2024-2026); confirmar si no vuelve antes de asumirlo ganado.",
             {2022: 526, 2023: 246}),
            ("Dinámica", 1.1, 59, "Barato (59%) pero también se retiró — sin compras en 3 años.",
             {2022: 42, 2023: 60}),
        ],
    },
}

# Semáforo de riesgo por SKU — síntesis manual de la tendencia + precio de arriba, para no
# obligar al lector a leer las 2 lecturas de cada SKU para sacar la conclusión general.
# vía libre = subir precio con poco riesgo · vigilar = revisar antes de decidir ·
# no subir = hay una señal concreta de rival barato y activo/creciendo.
_SEMAFORO_RAW = {
    "RE65966":  ("🟢 Vía libre", "Los 2 rivales se retiraron o compran caro."),
    "R116383":  ("🟡 Vigilar", "Rival barato (38%) dormido 4 años, no confirmado como retiro."),
    "RE536083": ("🟡 Vigilar", "Rival caro se fue, pero el barato (73%) sigue activo aunque chico."),
    "RE500734": ("🟡 Vigilar", "2 rivales baratos, uno reactivado en 2025 — confirmar en 2026."),
    "RE66820":  ("🔴 No subir aún", "El rival más barato de la canasta (37%) casi triplicó su volumen."),
    "RE507850": ("🔴 No subir aún", "Rival a precio idéntico cuadruplicó su volumen en 2025."),
    "RE501455": ("🟡 Vigilar", "Rival extremadamente barato (13%) dormido 4 años."),
    "RE504914": ("🟡 Vigilar", "Rivales caros, pero share bajo (42%) por fragmentación en 30 importadores."),
    "RE507920": ("🟢 Vía libre", "El único rival a la par de precio está en retirada total."),
    "RE48786":  ("🟡 Vigilar", "Rival caro con historial de volumen grande se retiró — confirmar antes de asumirlo."),
}


@st.cache_data
def load_tendencia_por_importador():
    """Unidades por año, por OEM: Repaglas y sus 2 rivales más cercanos por volumen histórico,
    con precio relativo y lectura cualitativa de cada uno.
    {oem: {"repaglas": {anio: u},
           "rivales": [{"nombre", "share_pct", "precio_vs_repaglas_pct", "lectura", "por_anio": {anio: u}}, ...],
           "semaforo", "semaforo_resumen"}}.
    2026 es parcial (solo hasta julio)."""
    out = {}
    for oem, v in _TENDENCIA_IMPORTADOR_RAW.items():
        semaforo, resumen = _SEMAFORO_RAW[oem]
        out[oem] = {
            "repaglas": dict(v["repaglas"]),
            "rivales": [
                {
                    "nombre": nombre, "share_pct": share, "precio_vs_repaglas_pct": precio_pct,
                    "lectura": lectura, "por_anio": dict(por_anio),
                }
                for nombre, share, precio_pct, lectura, por_anio in v["rivales"]
            ],
            "semaforo": semaforo,
            "semaforo_resumen": resumen,
        }
    return out


_EVOLUCION_ANUAL_RAW = {
    "RE65966": [
        ("Repaglas", {2022: 80, 2023: 164, 2024: 161, 2025: 152, 2026: 100}),
        ("IPESA", {2022: 47, 2023: 4}),
        ("Corporación Pesquera Inca", {2026: 4}),
        ("Nuevo Concepto de Maquinarias Agro Industrial", {2022: 1}),
    ],
    "R116383": [
        ("Repaglas", {2022: 250, 2023: 190, 2024: 300, 2025: 238, 2026: 132}),
        ("Suministros Automotrices e Imp.", {2022: 36}),
        ("R & T Rockcat", {2022: 12, 2024: 18}),
        ("Agritractor", {2022: 12}),
        ("R Y G Rockcat", {2024: 12}),
        ("Pro & Ma Nuevo Horizonte", {2024: 4}),
    ],
    "RE536083": [
        ("Repaglas", {2022: 56, 2023: 72, 2024: 132, 2025: 98, 2026: 64}),
        ("IPESA", {2022: 60}),
        ("Dinámica", {2022: 10, 2023: 12, 2025: 10}),
        ("Fortrac", {2023: 20, 2024: 4}),
        ("R Y G Rockcat", {2023: 12}),
        ("JPK Mundo Parts", {2025: 8}),
    ],
    "RE500734": [
        ("Repaglas", {2022: 139, 2023: 93, 2024: 242, 2025: 242, 2026: 130}),
        ("Suministros Automotrices e Imp.", {2022: 55, 2026: 10}),
        ("Dinámica", {2022: 25, 2025: 30}),
        ("P&G Repuestos", {2026: 40}),
        ("Fortrac", {2023: 10, 2025: 16, 2026: 5}),
        ("R & T Rockcat", {2024: 24}),
        ("Repuestos y Accesorios El Paraíso", {2022: 6, 2024: 10, 2026: 1}),
        ("T&E Import Perú Repuestos", {2023: 15}),
        ("R Y G Rockcat", {2022: 12}),
        ("Tralex", {2022: 3, 2023: 2, 2026: 2}),
        ("Guerrero Motor's", {2023: 5, 2026: 2}),
        ("Maquitracto Selva", {2025: 6}),
        ("Construcción Mecánica J&K", {2025: 5}),
        ("Amazon Motors", {2026: 4}),
        ("Autorepuestos A&T", {2024: 1, 2025: 2}),
        ("Agroindustrias San Jacinto", {2025: 3}),
        ("Agritractor", {2022: 2}),
        ("Serviagri de Ica", {2022: 1, 2023: 1}),
        ("Pitahaya Servicios Integrales", {2023: 2}),
        ("Tractus Implementos y Partes", {2025: 2}),
        ("Cisar", {2023: 1}),
    ],
    "RE66820": [
        ("Repaglas", {2022: 1270, 2023: 970, 2024: 1170, 2025: 1050, 2026: 450}),
        ("Dinámica", {2022: 180, 2024: 120}),
        ("Suministros Automotrices e Imp.", {2022: 72, 2024: 216}),
        ("R Y G Rockcat", {2022: 80}),
        ("T&E Import Perú Repuestos", {2023: 50}),
        ("Mateel", {2024: 46}),
        ("Fortrac", {2025: 32, 2026: 10}),
        ("Tractorandinas Parts", {2022: 10}),
        ("JPK Mundo Parts", {2025: 8}),
        ("AG Import Parve", {2025: 8}),
        ("Rinai Repuestos", {2025: 1}),
    ],
    "RE507850": [
        ("Repaglas", {2022: 150, 2023: 184, 2024: 328, 2025: 402, 2026: 232}),
        ("IPESA", {2022: 103, 2023: 104}),
        ("Fortrac", {2022: 33, 2025: 139, 2026: 22}),
        ("Dinámica", {2022: 20, 2024: 40}),
        ("Cisar", {2024: 50}),
        ("Maquinarias y Repuestos", {2023: 18, 2024: 12, 2026: 6}),
        ("Mateel", {2023: 6, 2026: 12}),
        ("Tractor Import", {2022: 4, 2024: 4}),
        ("MODASA", {2023: 8}),
        ("IM Selva", {2024: 6, 2025: 1}),
        ("Italtrac Selva", {2023: 6}),
        ("ITM Tractor", {2024: 6}),
        ("Monsante", {2025: 6}),
        ("R Y G Rockcat", {2024: 4}),
        ("R & T Rockcat", {2024: 2}),
    ],
    "RE501455": [
        ("Repaglas", {2022: 135, 2023: 105, 2024: 192, 2025: 191, 2026: 115}),
        ("Dinámica", {2022: 24, 2023: 8, 2024: 30, 2025: 20}),
        ("Guerrero Motor's", {2022: 40}),
        ("Suministros Automotrices e Imp.", {2022: 18, 2024: 18}),
        ("IPESA", {2022: 35}),
        ("Fortrac", {2023: 6, 2025: 5, 2026: 2}),
        ("R Y G Rockcat", {2022: 12}),
        ("Mateel", {2023: 1, 2024: 5, 2026: 2}),
        ("JPK Mundo Parts", {2025: 8}),
        ("Construcción Mecánica J&K", {2025: 6}),
        ("MODASA", {2023: 5}),
        ("Monsante", {2022: 4}),
        ("Agritractor", {2022: 4}),
        ("Repuestos y Accesorios El Paraíso", {2024: 4}),
        ("P&G Repuestos", {2026: 3}),
        ("Solutra del Perú", {2024: 1, 2026: 1}),
        ("Pro & Ma Nuevo Horizonte", {2024: 2}),
        ("National Air & Motor", {2023: 1}),
        ("R & T Rockcat", {2024: 1}),
        ("Geprocem", {2025: 1}),
        ("Corporación Pesquera Inca", {2026: 1}),
    ],
    "RE504914": [
        ("Repaglas", {2022: 135, 2023: 96, 2024: 184, 2025: 238, 2026: 166}),
        ("IPESA", {2022: 66, 2023: 50, 2024: 9, 2025: 5}),
        ("Fortrac", {2022: 14, 2023: 8, 2024: 9, 2025: 30, 2026: 12}),
        ("Suministros Automotrices e Imp.", {2023: 70}),
        ("Dinámica", {2022: 20, 2024: 20}),
        ("Maquinarias y Repuestos", {2022: 9, 2023: 1, 2024: 12, 2025: 4, 2026: 3}),
        ("R Y G Rockcat", {2022: 12, 2023: 8}),
        ("T&E Import Perú Repuestos", {2023: 15}),
        ("Mateel", {2024: 10, 2026: 5}),
        ("Monsante", {2022: 4, 2023: 1, 2024: 8}),
        ("P&G Repuestos", {2026: 10}),
        ("IM Selva", {2022: 3, 2023: 1, 2024: 2, 2025: 3}),
        ("Italtrac Selva", {2022: 4, 2023: 2}),
        ("R & T Rockcat", {2024: 6}),
        ("JPK Mundo Parts", {2025: 6}),
        ("Agritractor", {2022: 5}),
        ("MODASA", {2023: 5}),
        ("Tractor Import", {2023: 2, 2024: 1, 2025: 1}),
        ("Geprocem", {2025: 3}),
        ("Solutra del Perú", {2026: 3}),
        ("(Persona natural — dato protegido)", {2024: 1, 2025: 1}),
        ("Cisar", {2025: 2}),
        ("Corporación Pesquera Inca", {2026: 2}),
        ("Baustelle", {2022: 1}),
        ("World Motors", {2022: 1}),
        ("National Air & Motor", {2023: 1}),
        ("Parts and Services BVC", {2023: 1}),
        ("Guerrero Motor's", {2024: 1}),
        ("Repadiesel Repuestos", {2025: 1}),
        ("Emimaq", {2026: 1}),
    ],
    "RE507920": [
        ("Repaglas", {2022: 330, 2023: 252, 2024: 365, 2025: 473, 2026: 256}),
        ("IPESA", {2022: 93, 2023: 87, 2024: 22}),
        ("Fortrac", {2022: 19, 2023: 16, 2025: 28, 2026: 16}),
        ("Dinámica", {2022: 20, 2023: 7, 2024: 21, 2025: 13}),
        ("R Y G Rockcat", {2022: 12, 2023: 16}),
        ("Mateel", {2023: 8, 2024: 8, 2026: 8}),
        ("R & T Rockcat", {2024: 24}),
        ("JPK Mundo Parts", {2025: 16}),
        ("Tractor Import", {2022: 4, 2023: 4, 2024: 6}),
        ("MODASA", {2023: 12}),
        ("Italtrac Selva", {2022: 6}),
        ("Monsante", {2023: 6}),
        ("National Air & Motor", {2023: 4}),
        ("Solutra del Perú", {2024: 4}),
    ],
    "RE48786": [
        ("Repaglas", {2022: 380, 2023: 439, 2024: 620, 2025: 592, 2026: 330}),
        ("IPESA", {2022: 526, 2023: 246}),
        ("Dinámica", {2022: 42, 2023: 60}),
        ("Suministros Automotrices e Imp.", {2022: 12, 2023: 36, 2024: 50}),
        ("Tractor Import", {2022: 10, 2023: 16, 2024: 36, 2025: 9, 2026: 4}),
        ("Maquinarias y Repuestos", {2022: 6, 2023: 12, 2024: 10, 2025: 15, 2026: 18}),
        ("IM Selva", {2022: 24, 2023: 6, 2024: 6, 2025: 18}),
        ("Italtrac Selva", {2022: 16, 2023: 38}),
        ("Fortrac", {2023: 50}),
        ("Monsante", {2022: 20, 2024: 20, 2025: 5}),
        ("Inversiones Palmetto", {2023: 24}),
        ("Gamotor Electronic", {2026: 20}),
        ("Mateel", {2022: 18}),
        ("Maquitracto Selva", {2025: 16}),
        ("Tractor House Perú", {2026: 16}),
        ("T&E Import Perú Repuestos", {2023: 12}),
        ("JPK Mundo Parts", {2025: 12}),
        ("Construcción Mecánica J&K", {2025: 12}),
        ("Daxparts", {2022: 8}),
        ("R Y G Rockcat", {2023: 8}),
        ("Cisar", {2023: 6}),
        ("Manserved Dealer", {2023: 6}),
        ("Fabr. y Repar. Mult. e Industriales", {2025: 4}),
        ("Corporación Pesquera Inca", {2026: 4}),
    ],
}


@st.cache_data
def load_evolucion_anual():
    """Unidades por año, TODOS los importadores (no solo los 2 rivales principales), por OEM —
    para inspección numérica de detalle. {oem: [{"nombre", "por_anio": {anio: u}, "total"}, ...]},
    ordenado de mayor a menor por unidades totales. 2026 es parcial (solo hasta julio)."""
    out = {}
    for oem, rows in _EVOLUCION_ANUAL_RAW.items():
        out[oem] = [
            {"nombre": nombre, "por_anio": dict(por_anio), "total": sum(por_anio.values())}
            for nombre, por_anio in rows
        ]
    return out


# Importadores que traen genuinamente marca MAXIFORCE (no un equivalente/otra marca) en al
# menos uno de los 10 SKU ancla — detectado 2026-09-02 buscando el texto "MAXIFORCE" en los 5
# campos de Descripción Comercial de los 10 reportes ADEX reales, deduplicado por
# DUA+RUC+cantidad+FOB. Repaglas sigue siendo 96.6% de todas las unidades con esa etiqueta,
# pero 4 empresas (R Y G Rockcat, Fortrac, Mateel, R & T Rockcat) la importan de forma
# repetida en 5-9 de los 10 códigos — no es un lote suelto, es competencia directa de marca.
# Tupla: (nombre, {anio: unidades} agregado en los 10 SKU, [(oem, unidades, fob_total), ...]
# desglose por SKU en el que aparece, ordenado de mayor a menor).
_MAXIFORCE_REPAGLAS_RAW = {2022: 2920, 2023: 2565, 2024: 3536, 2025: 3585, 2026: 1856}

_MAXIFORCE_RIVALES_RAW = [
    ("R Y G Rockcat", {2022: 116, 2023: 44, 2024: 16},
     [("RE66820", 80, 1328), ("RE507920", 28, 2583), ("RE536083", 12, 1272), ("R116383", 12, 380),
      ("RE501455", 12, 1163), ("RE500734", 12, 1233), ("RE48786", 8, 375), ("RE504914", 8, 926),
      ("RE507850", 4, 334)]),
    ("Fortrac", {2022: 7, 2025: 99, 2026: 42},
     [("RE66820", 42, 617), ("RE507850", 36, 2833), ("RE507920", 24, 2002), ("RE500734", 21, 1586),
      ("RE504914", 18, 1458), ("RE501455", 7, 641)]),
    ("Mateel", {2023: 14, 2024: 68},
     [("RE66820", 46, 701), ("RE507920", 16, 1206), ("RE504914", 9, 715), ("RE507850", 6, 318),
      ("RE501455", 5, 444)]),
    ("R & T Rockcat", {2022: 12, 2024: 69},
     [("R116383", 30, 880), ("RE507920", 24, 2008), ("RE500734", 18, 1701), ("RE504914", 6, 629),
      ("RE507850", 2, 152), ("RE501455", 1, 88)]),
    ("Daxparts", {2022: 8}, [("RE48786", 8, 324)]),
    ("Fabr. y Repar. Mult. e Industriales", {2025: 4}, [("RE48786", 4, 190)]),
    ("Amazon Motors", {2026: 4}, [("RE500734", 4, 689)]),
]


@st.cache_data
def load_competencia_maxiforce():
    """Importadores que traen marca MAXIFORCE genuina (no equivalente) en al menos uno de los
    10 SKU ancla. Devuelve:
    {
      "repaglas": {anio: unidades},
      "rivales": [{"nombre", "por_anio": {anio: u}, "total",
                   "detalle_sku": [{"oem", "unidades", "fob_total"}, ...]}, ...]
                 ordenado de mayor a menor por unidades totales,
    }
    2026 es parcial (solo hasta julio)."""
    rivales = []
    for nombre, por_anio, detalle in _MAXIFORCE_RIVALES_RAW:
        rivales.append(
            {
                "nombre": nombre,
                "por_anio": dict(por_anio),
                "total": sum(por_anio.values()),
                "detalle_sku": [{"oem": oem, "unidades": u, "fob_total": fob} for oem, u, fob in detalle],
            }
        )
    rivales.sort(key=lambda r: -r["total"])
    return {"repaglas": dict(_MAXIFORCE_REPAGLAS_RAW), "rivales": rivales}
