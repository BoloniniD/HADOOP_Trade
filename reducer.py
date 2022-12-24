import sys
import json
import pandas as pd


def reduce():
    # для каждого дня считаем выгодно/невыгодно было вкладываться
    # считаем процент когда было выгодно
    # считаем сколько в среднем заработали бы, вкладываясь удачно
    inp = ""
    for s in sys.stdin:
        inp = inp + "\n" + s

    inp = json.loads(inp)

    df = pd.DataFrame(inp["data"])

    target_val = inp["target"]
    flag = inp["flag"]
    stonks = pd.DataFrame()
    not_stonks = pd.DataFrame()

    stonks[flag] = df[target_val - df[flag] >= 0][flag]
    not_stonks[flag] = df[target_val - df[flag] < 0][flag]

    percent = stonks.shape[0] / df.shape[0]

    print(
        "{},{},{},{},{}".format(
            pd.to_datetime(df.iloc[0]["TRADEDATE"]).strftime("%A"),
            percent,
            (stonks.shape[0] * target_val - stonks[flag].sum()) / stonks[flag].sum(),
            (not_stonks.shape[0] * target_val - not_stonks[flag].sum())
            / not_stonks[flag].sum(),
            (df.shape[0] * target_val - df[flag].sum()) / df[flag].sum(),
            df[flag].sum(),
            df.shape[0] * target_val,
        )
    )
