import pandas as pd
from datetime import (datetime, timedelta)
from backtest import backtest

start = datetime(2015,1,1)
end = datetime(2020,1,1)

strategy = [
    {
        "action": "SELL",
        "type": "P",
        "delta": [-0.5,-0.3],
        "frequency": 2,
        "last_price": None,
        "info": pd.Series([],  dtype= float)
    },
    {
        "action": "BUY",
        "type": "P",
        "delta": [-1,-0.7],
        "frequency": 365,
        "last_price": None,
        "info": pd.Series([],  dtype= float)
    },
    {
        "action": "BUY",
        "type": "C",
        "delta": [0.2,0.5],
        "frequency": 30,
        "last_price": None,
        "info": pd.Series([],  dtype= float)
    }
]


def main():
    backtest(strategy, 100, start, end, True, "Tester")
    print("All done!")


if __name__ =="__main__":
    main()
