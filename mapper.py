#!/bin/python3

import sys
import json


def map():
    # делим дням недели год
    # рабочих дней 5, сб и вск не считаем
    # переделать на stdin для хадупа
    inp = ""
    for s in sys.stdin:
        inp = s

        inp = json.loads(inp)

        for i in range(0, 5):
            day = []
            for j in inp["data"]:
                if j[3] == i:
                    day.append(j)
            to_reduce = {}
            to_reduce["target"] = inp["target"]
            to_reduce["data"] = day
            to_reduce["flag"] = inp["flag"]

            to_reduce = json.dumps(to_reduce)

            print(to_reduce)


map()
