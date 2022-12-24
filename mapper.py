import sys
import reducer
import json
import numpy as np
import pandas as pd
import multiprocessing


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def map(q):
    # делим дням недели год
    # рабочих дней 5, сб и вск не считаем
    # переделать на stdin для хадупа
    inp = q.get()
    prcs = []
    inp = json.loads(inp)

    df = pd.DataFrame(inp["data"])
    for i in range(0, 5):
        s = df[df["WEEKDAY"] == i].to_json()
        to_reduce = {}
        to_reduce["target"] = inp["target"]
        to_reduce["data"] = json.loads(s)
        to_reduce["flag"] = inp["flag"]

        qq = multiprocessing.Queue()
        qq.put(json.dumps(to_reduce))
        p = multiprocessing.Process(target=reducer.reduce, args=(qq,))
        prcs.append(p)
        p.start()

    for i in prcs:
        i.join()
        i.close()
