import pandas as pd


class XlsParser:
    def __init__(self, filename):
        self.filename = filename
        self.time = None
        self.millisecond = None
        self.status = None
        self._parse_file()

    def _parse_file(self):
        data = pd.ExcelFile(self.filename)
        sheet = data.parse(0)
        self.time = sheet['tijdstip'].to_numpy()
        self.millisecond = sheet['msec'].to_numpy()
        self.status = sheet['status'].to_numpy()