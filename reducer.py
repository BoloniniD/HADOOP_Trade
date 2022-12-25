#!/bin/python3

import sys
import json
import datetime


def reduce():
    inp = ""
    for s in sys.stdin:
        inp = s

        inp = json.loads(inp)
        target_val = inp["target"]
        flag = inp["flag"]

        if flag == "OPEN":
            flag = 1
        else:
            flag = 2

        stonks = []
        not_stonks = []
        for i in inp["data"]:
            if target_val - i[flag] >= 0:
                stonks.append(i)
            else:
                not_stonks.append(i)

        percent = len(stonks) / len(inp["data"])

        sum_stonks = 0
        sum_not_stonks = 0
        total_sum = 0

        for i in stonks:
            sum_stonks += i[flag]

        for i in not_stonks:
            sum_not_stonks += i[flag]

        for i in inp["data"]:
            total_sum += i[flag]

        try:
            stonks_percent = (len(stonks) * target_val - sum_stonks) / sum_stonks
        except:
            stonks_percent = -1

        try:
            not_stonks_percent = (
                len(not_stonks) * target_val - sum_not_stonks
            ) / sum_not_stonks
        except:
            not_stonks_percent = -1

        try:
            total_percent = (len(inp["data"]) * target_val - total_sum) / total_sum
        except:
            total_percent = -1

        print(
            "{},{},{},{},{},{},{}".format(
                datetime.datetime.strptime(inp["data"][0][0], "%Y-%m-%d").strftime(
                    "%A"
                ),
                percent,
                stonks_percent,
                not_stonks_percent,
                total_percent,
                total_sum,
                len(inp["data"]) * target_val,
            )
        )


reduce()
