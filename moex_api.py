import requests
import apimoex
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

BOTH = ("TRADEDATE", "OPEN", "CLOSE", "VOLUME", "VALUE")


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

    def map(self, df):
        # делим дням недели год
        # рабочих дней 5, сб и вск не считаем
        for i in range(0, 5):
            yield df[df["WEEKDAY"] == i]

    def reduce(self, df, target, ):
        # для каждого дня считаем выгодно/невыгодно было вкладываться
        # считаем процент когда было выгодно
        # считаем сколько в среднем заработали бы, вкладываясь удачно
        target_val = target.iloc[0].loc["CLOSE"]
        stonks = pd.DataFrame()
        not_stonks = pd.DataFrame()

        stonks["CLOSE"] = df[target_val - df["CLOSE"] >= 0]["CLOSE"]
        not_stonks["CLOSE"] = df[target_val - df["CLOSE"] < 0]["CLOSE"]

        percent = stonks.shape[0] / df.shape[0]

        print(pd.to_datetime(df.iloc[0]["TRADEDATE"]).strftime("%A"))
        print(
            "Percent of profitable days: {:.2%}, {} out of {}".format(
                percent, stonks.shape[0], df.shape[0]
            )
        )
        print(
            "- Profit days: {:.2%}".format(
                (stonks.shape[0] * target_val - stonks["CLOSE"].sum())
                / stonks["CLOSE"].sum()
            )
        )
        print(
            "- Loss days: {:.2%}".format(
                (not_stonks.shape[0] * target_val - not_stonks["CLOSE"].sum())
                / not_stonks["CLOSE"].sum()
            )
        )
        print(
            "- Overall: {:.2%}".format(
                (df.shape[0] * target_val - df["CLOSE"].sum()) / df["CLOSE"].sum()
            )
        )
        print("- - Investments: {0:0.2f}".format(df["CLOSE"].sum()))
        print("- - Result: {0:0.2f}".format(df.shape[0] * target_val))
        print()

    def user_request(self):
        year = input("DATE: ")
        share = input("SHARE: ")
        df, df_target = self.api.get_year(year, share)

        for i in self.map(df):
            self.reduce(i, df_target)
        print("========================================================")
