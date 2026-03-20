import math
import pandas as pd
from datetime import datetime

EIRP_DBM = 58
SHADOW_MARGIN_DB = 8
VOICE_THRESHOLD_DBM = -100
DATA_THRESHOLD_DBM = -95
BS_HEIGHT_M = 22

def outdoor_path_loss_db(distance_horizontal_m, user_height_m, frequency_mhz, shadow_margin_db=SHADOW_MARGIN_DB):
    """Modelo conservador tipo UMa NLOS con termino de frecuencia en GHz."""
    distance_3d_m = math.sqrt(distance_horizontal_m ** 2 + (BS_HEIGHT_M - user_height_m) ** 2)
    frequency_ghz = frequency_mhz / 1000
    return (
        13.54
        + 39.08 * math.log10(distance_3d_m)
        + 20 * math.log10(frequency_ghz)
        - 0.6 * (user_height_m - 1.5)
        + shadow_margin_db
    )

def classify_service(received_power_dbm):
    if received_power_dbm >= DATA_THRESHOLD_DBM:
        return 'Cumple voz y datos basicos'
    if received_power_dbm >= VOICE_THRESHOLD_DBM:
        return 'Cumple voz, datos justos'
    return 'No cumple objetivo'

def recommendation(received_power_dbm, point_name):
    if received_power_dbm >= DATA_THRESHOLD_DBM:
        if 'Entrada' in point_name:
            return 'Macro suficiente'
        return 'Macro suficiente para el objetivo base'
    if received_power_dbm >= VOICE_THRESHOLD_DBM:
        return 'Revisar refuerzo ligero: repetidor o small cell segun capacidad'
    return 'Refuerzo indoor necesario: small cell o DAS; repetidor solo si la senal donante es estable'

def calculate_coverage(points, bands_mhz, eirp_dbm=EIRP_DBM):
    """Calcula cobertura para todos los puntos y bandas."""
    rows = []
    for band_name, frequency_mhz in bands_mhz.items():
        for point in points:
            outdoor_loss = outdoor_path_loss_db(
                point['dist_h_m'],
                point['altura_m'],
                frequency_mhz,
            )
            indoor_loss = point['fachada_db'] + point['paredes_db'] + point['forjados_db'] + point['extra_db']
            total_loss = outdoor_loss + indoor_loss
            received_power = eirp_dbm - total_loss
            rows.append({
                'banda': band_name,
                'punto': point['nombre'],
                'planta': point['planta'],
                'L_ext_db': round(outdoor_loss, 1),
                'L_fachada_db': point['fachada_db'],
                'L_paredes_db': point['paredes_db'],
                'L_forjados_db': point['forjados_db'],
                'L_extra_db': point['extra_db'],
                'L_total_db': round(total_loss, 1),
                'P_rx_dbm': round(received_power, 1),
                'estado': classify_service(received_power),
                'recomendacion': recommendation(received_power, point['nombre']),
            })
    return pd.DataFrame(rows)

def get_default_points():
    """Retorna los puntos de medida por defecto."""
    return [
        {
            'nombre': 'Entrada principal',
            'planta': 'Baja',
            'altura_m': 1.5,
            'dist_h_m': 180,
            'fachada_db': 14,
            'paredes_db': 0,
            'forjados_db': 0,
            'extra_db': 0,
        },
        {
            'nombre': 'Aula 2a planta',
            'planta': 'Segunda',
            'altura_m': 8.5,
            'dist_h_m': 170,
            'fachada_db': 16,
            'paredes_db': 4,
            'forjados_db': 15,
            'extra_db': 0,
        },
        {
            'nombre': 'Archivo semisotano',
            'planta': 'Semisotano',
            'altura_m': -2.5,
            'dist_h_m': 185,
            'fachada_db': 18,
            'paredes_db': 8,
            'forjados_db': 18,
            'extra_db': 6,
        },
    ]

def get_default_bands():
    """Retorna las bandas de frecuencia por defecto."""
    return {
        'LTE 1800': 1800,
        'UMTS 2100': 2100,
        'LTE 800': 800,
        'LTE 2600': 2600,
    }
