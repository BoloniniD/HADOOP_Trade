import requests
import apimoex
import pandas as pd

MORNING = ("TRADEDATE", "OPEN", "VOLUME", "VALUE")
EVENING = ("TRADEDATE", "CLOSE", "VOLUME", "VALUE")
BOTH = ("TRADEDATE", "OPEN", "CLOSE", "VOLUME", "VALUE")


class MOEXData:
    def __init__(self):
        self.session = requests.Session()

    def get_year(self, year, share, cols):
        data = apimoex.get_board_history(
            self.session,
            share,
            columns=cols,
            start="{}-01-01".format(year),
            end="{}-01-01".format(year + 1),
        )
        df = pd.DataFrame(data)
        df.set_index("TRADEDATE", inplace=True)
        return df

    def get_year_morning(self, year, share):
        return self.get_year(year, share, MORNING)

    def get_year_evening(self, year, share):
        return self.get_year(year, share, EVENING)

    def get_year_both(self, year, share):
        return self.get_year(year, share, BOTH)
