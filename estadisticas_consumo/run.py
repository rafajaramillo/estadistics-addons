from influxdb import InfluxDBClient
import json
from datetime import datetime

client = InfluxDBClient(
    host='a0d7b954-influxdb',
    port=8086,
    username='homeassistant',
    password='TU_CONTRASEÑA',
    database='homeassistant'
)

def get_total_consumo_dia():
    query = """SELECT SUM(\"value\") FROM \"sensor.smartplug1_power\" WHERE time >= now() - 1d"""
    result = client.query(query)
    points = list(result.get_points())
    return points[0]['sum'] if points else 0

def get_horas_pico():
    query = """SELECT SUM(\"value\") FROM \"sensor.smartplug1_power\" WHERE time >= now() - 1d GROUP BY time(1h)"""
    result = client.query(query)
    puntos = list(result.get_points())
    puntos.sort(key=lambda x: x['sum'], reverse=True)
    return puntos[:3]

estadisticas = {
    "fecha": datetime.now().strftime('%Y-%m-%d %H:%M'),
    "consumo_total_dia": get_total_consumo_dia(),
    "horas_pico": get_horas_pico()
}

with open("/config/estadisticas.json", "w") as f:
    json.dump(estadisticas, f, indent=4)
