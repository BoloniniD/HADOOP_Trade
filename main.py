import moex_api
import pandas as pd


class Trades:
    def __init__(self):
        self.api = moex_api.MOEXData()

    def user_request(self):
        year = int(input("YEAR: "))
        share = input("SHARE: ")
        df = self.api.get_year_evening(year, share)
        print(df)


if __name__ == "__main__":
    trade = Trades()
    while True:
        trade.user_request()
