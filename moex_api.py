import requests
import apimoex
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import json
import numpy as np
import subprocess
from os import listdir


BOTH = ("TRADEDATE", "OPEN", "CLOSE")


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


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

    def process_request(self, year, share, flag):
        df, df_target = self.api.get_year(year, share)

        inp = {}

        inp["target"] = df_target.iloc[0][flag]
        inp["data"] = df.values.tolist()
        inp["flag"] = flag

        to_hadoop = json.dumps(inp, cls=NpEncoder)

        with open("inp.txt", "w") as file:
            file.write(to_hadoop)

        try:
            subprocess.run("hadoop fs -rm -r -f proj", shell=True)
        except:
            pass

        subprocess.run("hadoop fs -mkdir proj", shell=True)

        subprocess.run("hadoop fs -copyFromLocal ./inp.txt ./proj", shell=True)

        subprocess.run(
            "mapred streaming -input ./proj/inp.txt -output ./proj/output -mapper mapper.py -file ./mapper.py -reducer reducer.py -file ./reducer.py",
            shell=True,
        )

        try:
            subprocess.run("rm -rf proj", shell=True)
        except:
            pass

        subprocess.run("hadoop fs -get ./proj/output ./proj", shell=True)

        out_files = listdir("./proj")

        result = []
        for i in out_files:
            if i.startswith("part"):
                with open("./proj/{}".format(i), "r") as fil:
                    result.append(fil.readline())

        return result
