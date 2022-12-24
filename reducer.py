import sys
import json
import pandas as pd


def reduce(q):
    # для каждого дня считаем выгодно/невыгодно было вкладываться
    # считаем процент когда было выгодно
    # считаем сколько в среднем заработали бы, вкладываясь удачно
    inp = q.get()

    inp = json.loads(inp)

    df = pd.DataFrame(inp["data"])

    target_val = inp["target"]
    stonks = pd.DataFrame()
    not_stonks = pd.DataFrame()

    stonks["CLOSE"] = df[target_val - df["CLOSE"] >= 0]["CLOSE"]
    not_stonks["CLOSE"] = df[target_val - df["CLOSE"] < 0]["CLOSE"]

    percent = stonks.shape[0] / df.shape[0]

    with open(pd.to_datetime(df.iloc[0]["TRADEDATE"]).strftime("%A"), "w") as fil:
        fil.writelines(
            [
                pd.to_datetime(df.iloc[0]["TRADEDATE"]).strftime("%A"),
                "\n",
                "Percent of profitable days: {:.2%}, {} out of {}".format(
                    percent, stonks.shape[0], df.shape[0]
                ),
                "\n",
                "- Profit days: {:.2%}".format(
                    (stonks.shape[0] * target_val - stonks["CLOSE"].sum())
                    / stonks["CLOSE"].sum()
                ),
                "\n",
                "- Loss days: {:.2%}".format(
                    (not_stonks.shape[0] * target_val - not_stonks["CLOSE"].sum())
                    / not_stonks["CLOSE"].sum()
                ),
                "\n",
                "- Overall: {:.2%}".format(
                    (df.shape[0] * target_val - df["CLOSE"].sum()) / df["CLOSE"].sum()
                ),
                "\n",
                "- - Investments: {0:0.2f}".format(df["CLOSE"].sum()),
                "\n",
                "- - Result: {0:0.2f}".format(df.shape[0] * target_val),
            ]
        )
