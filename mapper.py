#!/bin/python

import sys
import json
import numpy as np
import pandas as pd


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def map():
    # делим дням недели год
    # рабочих дней 5, сб и вск не считаем
    # переделать на stdin для хадупа
    inp = ""
    for s in sys.stdin:
        inp = s

        inp = json.loads(inp)

        df = pd.DataFrame(inp["data"])
        for i in range(0, 5):
            s = df[df["WEEKDAY"] == i].to_json()
            to_reduce = {}
            to_reduce["target"] = inp["target"]
            to_reduce["data"] = json.loads(s)
            to_reduce["flag"] = inp["flag"]

            to_reduce = json.dumps(to_reduce)

            print(to_reduce)


map()
