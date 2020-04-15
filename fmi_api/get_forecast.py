import logging
from collections import OrderedDict
from datetime import datetime
from typing import Iterable, Dict

from lxml import etree
from requests import request, models
from requests.exceptions import RequestException

from . import WeatherPoint
from ._timed_cache import timed_cache

CONFIG_FILE = 'configs.ini'
FMI_URL = "http://opendata.fmi.fi/wfs"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



@timed_cache(minutes=60)
def _make_api_request(location: str) -> models.Response:

    logger.info("Creating new weather request to FMI")
    params = {
        "request": "getFeature",
        "service": "WFS",
        "version": "2.0.0",
        "storedquery_id": "fmi::forecast::hirlam::surface::point::multipointcoverage",
        "place": location
    }
    return request(url=FMI_URL, params=params, method="get")


def _parse_weather_report(content: bytes) -> Dict[datetime, WeatherPoint]:  # FIXME later:
    # OrderedDict typing would cause problems: https://tinyurl.com/y6wwtre7

    xml_tree = etree.XML(content)

    # Define namespaces
    ns_positions = ".//{http://www.opengis.net/gmlcov/1.0}positions"
    ns_data = ".//{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList"
    ns_datafields = ".//{http://www.opengis.net/swe/2.0}field"

    # Parse data
    positions_raw: str = xml_tree.findtext(ns_positions)
    weather_data_raw: str = xml_tree.findtext(ns_data)
    field_details: Iterable = xml_tree.findall(ns_datafields)

    # Combine data and labels to dicts, weather data
    field_labels = [x.get('name') for x in field_details]
    weather_data = list()
    for row in weather_data_raw.splitlines():
        weather_data.append(dict(zip(field_labels, row.split())))

    # Combine data and labels to dicts, location(s)
    point_labels = ("lat", "lon", "timestamp")
    positions = list()
    for row in positions_raw.splitlines():
        positions.append(dict(zip(point_labels, row.split())))

    # Convert data to WeatherPoint dataclasses
    result_weather = OrderedDict()
    for point, datum in zip(positions, weather_data):
        if not point and not datum:  # skip empty rows
            continue

        this_timestamp = datetime.fromtimestamp(int(point["timestamp"]))
        weather_point = WeatherPoint(
            lat=float(point["lat"]),
            lon=float(point["lon"]),
            time=this_timestamp,
            temp=float(datum["Temperature"]),
            pressure=float(datum["Pressure"]),
            humidity=float(datum["Humidity"]),
            dew_point=float(datum["DewPoint"]),
            precipitation_1h=float(datum["Precipitation1h"]),
            precipitation_total=float(datum["PrecipitationAmount"]),
            wind_dir=float(datum["WindDirection"]),
            wind_speed=float(datum["WindSpeedMS"]),
        )

        result_weather[this_timestamp] = weather_point

    return result_weather


def _parse_api_error_response(result: models.Response) -> None:
    logger.error(f"API connection failed.")
    logger.error(f"Code: {result.status_code}, reason: {result.reason}")
    logger.error("Check DEBUG for full response.")
    logger.debug(result.text)

    xml_tree = etree.XML(result.content)
    error_message = xml_tree.findtext(".//{http://www.opengis.net/ows/1.1}ExceptionText")
    logger.error(error_message)


def hirlam_forecast(location: str) -> Dict[datetime, WeatherPoint]:
    try:
        result = _make_api_request(location)
    except RequestException:
        logger.exception("Unexpected error connecting to FMI API, see log for details")
        raise ConnectionError("Unable to connect to FMI API")

    if result.ok:
        return _parse_weather_report(result.content)
    else:
        _parse_api_error_response(result)
        raise ConnectionRefusedError("FMI API refused connection, see log for details")

