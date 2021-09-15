from functions import *
import pandas as pd
import datetime

filePrefix = "UnderlyingOptionsEODCalcs_"

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2021, 1, 1)


y = []


holdings = [
  { #Sell ATM puts every 2 days
    "action": "SELL",
    "type": "P",
    "delta": -0.5,
    "frequency": 2,
    "last_price": None,
    "info": pd.Series([])
  }
]



def main():
  cash = 0
  assets = 0
  pl = 0
  current = start
  print("Beginning Backtest...")
  while current < end:
    print("**********************")
    print(str(current.date()))
    try:
      # Read in the data
      data = pd.read_csv("./data/" + filePrefix + str(current.date()) + ".csv")

      for holding in holdings:
        # print(holding)
        if not holding["info"].empty:
          contract = selectContract(data, holding["info"]["option_type"], holding["info"]["expiration"], holding["info"]["strike"])
          BAM = bidAskMean(contract["bid_1545"], contract["ask_1545"])
          # if holding["action"] == "BUY": pl += (BAM - holding["last_price"])
          # if holding["action"] == "SELL": pl += (holding["last_price"] - BAM)
          print("holding was at " + str(holding["last_price"]) + " but is not at " + str(BAM) + " (" + str(contract["strike"]) +  ") leaving p/l at " + str(pl))
          holding["last_price"] = BAM
          if holding["info"]["expiration"] == str(current.date()):
            # Expiration has come so unload the option
            BAM = bidAskMean(contract["bid_1545"], contract["ask_1545"])
            print("BUYing " + contract["expiration"] + " for " + str(BAM))
            if holding["action"] == "BUY": cost = -BAM
            if holding["action"] == "SELL": cost = BAM
            pl -= BAM
            print(pl)

            holding["info"] = grand_selector(data, holding["type"], holding["delta"],current + datetime.timedelta(days = holding["frequency"]))
            BAM = bidAskMean(holding["info"]["bid_1545"], holding["info"]["ask_1545"])
            
            print(holding["action"] + "ing " + holding["info"]["expiration"] + " for " + str(BAM))
            if holding["action"] == "BUY": cost = BAM
            if holding["action"] == "SELL": cost = -BAM
            pl -= cost
            holding["last_price"] = BAM
        else:
          holding["info"] = grand_selector(data, holding["type"], holding["delta"],current + datetime.timedelta(days = holding["frequency"]))
          BAM = bidAskMean(holding["info"]["bid_1545"], holding["info"]["ask_1545"])
          print(holding["action"] + "ing " + holding["info"]["expiration"] + " " + str(holding["info"]["strike"]) + " for " + str(BAM))
          if holding["action"] == "BUY": 
            cash -= BAM
            assets += BAM
          if holding["action"] == "SELL": 
            cash += BAM
            assets -= BAM
          holding["last_price"] = BAM
    except FileNotFoundError:
      print("count not find data")

    print(pl)
    y.append(pl)
    current += datetime.timedelta(days=1)


if __name__ == "__main__":
  main()
  print(y)
    
