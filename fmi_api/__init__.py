from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherPoint(object):
    lat: float
    lon: float
    time: datetime

    temp: float
    pressure: float
    humidity: float
    dew_point: float

    precipitation_1h: float
    precipitation_total: float

    wind_dir: float
    wind_speed: float
