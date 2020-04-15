

from lxml import etree

from fmi_api import WeatherPoint


class HtmlWeatherTable:

    def __init__(self):
        self.root = etree.Element("html")
        self.table_body = self._create_table()

    def _create_table(self) -> etree.Element:
        head = etree.SubElement(self.root, "head")
        style = etree.SubElement(head, "style")
        style.text = """
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }
    
        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }
    
        tr:nth-child(even) {
          background-color: #dddddd;
        }"""
        body = etree.SubElement(self.root, "body")
        etree.SubElement(body, "title").text = "Ensi yön sää "

        table_class = {
            "class": "table table-striped table-dark table-hover"
        }
        table = etree.SubElement(body, "table", attrib=table_class)
        thead = etree.SubElement(table, "thead")
        row = etree.SubElement(thead, "tr")
        etree.SubElement(row, "th", scope="col").text = "aika"
        etree.SubElement(row, "th", scope="col").text = "T"
        etree.SubElement(row, "th", scope="col").text = "tuuli"
        etree.SubElement(row, "th", scope="col").text = "sademäärä [mm]"
        tbody = etree.SubElement(table, "tbody")

        return tbody

    def add_row(self, weather: WeatherPoint, color=None):
        row = etree.SubElement(self.table_body, "tr")
        if color:
            row.attrib["bgcolor"] = color
        etree.SubElement(row, "th", scope="row").text = weather.time.strftime("%H:%m")
        etree.SubElement(row, "td").text = str(int(weather.temp))
        etree.SubElement(row, "td").text = str(int(weather.wind_speed))
        etree.SubElement(row, "td").text = str(int(weather.precipitation_1h))

    def to_string(self):
        return etree.tostring(self.root).decode("utf8")
