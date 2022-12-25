import moex_api
import sys

if __name__ == "__main__":
    trade = moex_api.Trades()
    while True:
        trade.process_request(sys.argv[1], sys.argv[2], sys.argv[3])
