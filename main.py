import moex_api

if __name__ == "__main__":
    trade = moex_api.Trades()
    while True:
        trade.user_request()
