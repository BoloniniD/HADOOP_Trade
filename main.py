import moex_api
from datetime import datetime
import sys

if __name__ == "__main__":
    trade = moex_api.Trades()

    trade.process_request(sys.argv[1], sys.argv[2], sys.argv[3])
