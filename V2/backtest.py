from functions import *
from datetime import (timedelta, datetime)
import pandas as pd

from grapher import graph_this_please

file_prefix = "UnderlyingOptionsEODCalcs_"

def backtest(strategy, start_cash, start, end, graph=False, output_name="output"):
    starting_value = 100
    cash = starting_value
    current = start
    assets = 0
    y = []
    logs = []
    while current < end:
        logs.append("*****************")
        logs.append(str(current.date()))
        try:
            data = pd.read_csv("data/" + file_prefix + str(current.date()) + ".csv")
            assets = 0

            for leg in strategy:
                if leg["info"].empty:
                    leg["info"] = grand_selector(data, leg["type"], leg["delta"], current + timedelta(days=leg["frequency"]))
                    BAM = bidAskMean(leg["info"]["bid_1545"], leg["info"]["ask_1545"])
                    logs.append(leg["action"] + "ing " + leg["info"]["expiration"] + " " + str(leg["info"]["strike"]) + " for " + str(BAM))
                    if leg["action"] == "BUY":
                        cash -= BAM
                        assets += BAM
                    if leg["action"] == "SELL":
                        cash += BAM
                        assets -= BAM
                    leg["last_price"] = BAM
                    
                else:
                    contract = selectContract(data, leg["type"], leg["info"]["expiration"], leg["info"]["strike"])
                    BAM = bidAskMean(contract["bid_1545"], contract["ask_1545"])
                    logs.append("Asset ("+leg["type"] + leg["info"]["expiration"] + "-" + str(leg["info"]["strike"]) + ") change from " + str(leg["last_price"]) + " to " + str(BAM))
                    leg["last_price"] = BAM
                    # logs.append(leg["action"] + "ing " + leg["info"]["expiry"] + " " + leg["info"]["strike"] + " for " + str(BAM))
                    if leg["action"] == "BUY":
                        assets += BAM
                    if leg["action"] == "SELL":
                        assets -= BAM
                    if (datetime.strptime(leg["info"]["expiration"] , "%Y-%m-%d") - current).days <= 1:
                        if leg["action"] == "BUY":
                            logs.append("SELLing " + leg["type"] + leg["info"]["expiration"] + "-" + str(leg["info"]["strike"]))
                            cash += BAM
                            assets -= BAM
                        if leg["action"] == "SELL":
                            logs.append("BUYing " + leg["type"] + leg["info"]["expiration"] + "-" + str(leg["info"]["strike"]))
                            cash -= BAM
                            assets += BAM
                        try:
                            leg["info"] = grand_selector(data, leg["type"], leg["delta"], current + timedelta(days=leg["frequency"]))
                            BAM = bidAskMean(leg["info"]["bid_1545"], leg["info"]["ask_1545"])
                            logs.append(leg["action"] + "ing " + leg["info"]["expiration"] + " " + str(leg["info"]["strike"]) + " for " + str(BAM))
                        except IndexError:
                            logs.append("The grand selector failed... Leaving this leg emtpy")
                            leg["info"] = pd.Series([],  dtype= float)
                        if leg["action"] == "BUY":
                            cash -= BAM
                            assets += BAM
                        if leg["action"] == "SELL":
                            cash += BAM
                            assets -= BAM
                        leg["last_price"] = BAM
                        
            logs.append("Assets=" + str(assets) + " Cash=" + str(cash))
            pl = (cash + assets) - (starting_value)
            logs.append("Current p/l: " + str(pl))
        except FileNotFoundError:
            logs.append("Could not find data")
        if graph:
            networth = cash + assets
            y.append(networth)
        current += timedelta(days = 1)
    
    f = open(output_name + ".txt", "w")
    f.write("\n".join(logs))
    f.close()

    if graph:
        graph_this_please(start, end, y, output_name)