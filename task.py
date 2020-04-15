from datetime import timedelta, datetime

from email_handler.gmail import send_html
from email_handler.html_builder import HtmlWeatherTable
from fmi_api.get_forecast import hirlam_forecast


def warn_severe_weather():
    forecast = hirlam_forecast(location="Vantaa")

    html_builder = HtmlWeatherTable()
    warnings_found = False
    for ts, weather in forecast.items():
        if ts > datetime.now() + timedelta(hours=12):
            color = None
            if weather.temp < 1:
                color = "#B3B9F2"
                warnings_found = True
            elif weather.temp > 25:
                color = "#F2B3B3"
                warnings_found = True
            elif weather.wind_speed > 10:
                color = "#B3B9F2"
            html_builder.add_row(weather, color=color)

    if warnings_found:
        send_html(
            subject=f"Säävaroitus {datetime.now().strftime('%Y-%m-%d %H:%m')}",
            msg=html_builder.to_string()
        )


def daily():
    warn_severe_weather()


if __name__ == '__main__':
    daily()
