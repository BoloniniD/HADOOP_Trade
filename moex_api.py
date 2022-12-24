import requests
import apimoex
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import mapper
import reducer
import json
import sys
import multiprocessing

BOTH = ("TRADEDATE", "OPEN", "CLOSE")


class MOEXData:
    def __init__(self):
        self.session = requests.Session()

    def get_year(self, date, share):
        date = datetime.strptime(date, "%Y-%m-%d")

        data_year = apimoex.get_board_history(
            self.session,
            share,
            columns=BOTH,
            start="{}".format(
                (date - relativedelta(years=1, days=1)).strftime("%Y-%m-%d")
            ),
            end="{}".format((date - relativedelta(days=1)).strftime("%Y-%m-%d")),
        )
        df = pd.DataFrame(data_year)
        df = df[df.notna()["CLOSE"]]
        df = df[df.notna()["OPEN"]]
        df["WEEKDAY"] = pd.to_datetime(df["TRADEDATE"]).apply(lambda x: x.weekday())

        data_target_day = apimoex.get_board_history(
            self.session,
            share,
            columns=BOTH,
            start="{}".format(date.strftime("%Y-%m-%d")),
            end="{}".format(date.strftime("%Y-%m-%d")),
        )
        df_target = pd.DataFrame(data_target_day)

        return df, df_target


class Trades:
    def __init__(self):
        self.api = MOEXData()

    def user_request(self):
        year = input("DATE: ")
        share = input("SHARE: ").upper()
        flag = input("OPEN/CLOSE: ").upper()
        df, df_target = self.api.get_year(year, share)

        inp = {}

        inp["target"] = df_target.iloc[0][flag]
        inp["data"] = json.loads(df.to_json())
        inp["flag"] = flag

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=mapper.map, args=(q,))
        q.put(json.dumps(inp, cls=mapper.NpEncoder))
        p.start()
        p.join()
        p.close()

        print("========================================================")
