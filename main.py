from functions import *
import pandas as pd
import datetime


filePrefix = "UnderlyingOptionsEODCalcs_"

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2021, 1, 1)

x = []
y = []



def main():
  print("Beggining Backtest...")
  current = start
  pl = 0
  holding = pd.Series([])
  while current < end:
    print("**********************")
    print(str(current.date()))
    try:
      # Read in the data
      data = pd.read_csv("./data/" + filePrefix + str(current.date()) + ".csv")

      # Buy the option we have sold
      if not holding.empty:
        contractToSell = selectContract(data, "P", data["expiration"],data["strike"])
        profit = bidAskMean((holding["bid_1545"], holding["ask_1545"])) - bidAskMean(contractToSell["bid_1545"], contractToSell["ask_1545"])
        print("Buying " + str(holding["expiration"]) + " " + str(holding["strike"]) + " for: " + str(((contractToSell["bid_1545"] + contractToSell["ask_1545"]) / 2)))
        holding = pd.Series([])
        
        # Calculate and track p/l
        print("Profit on trade: " + str(profit))
        pl += profit
        x.append(str(current.date()))
        y.append(pl)
        print("Current P/L: " + str(pl))

      # Try Selling one two days out
      overATM = pd.DataFrame()
      n = 2
      while len(overATM) == 0 and current + datetime.timedelta(days=n) < end:
        print(str(n), end=",")
        targetExpiration = current + datetime.timedelta(days=n)
        twoDaysOut = data[(data["expiration"] == str(targetExpiration.date())) & (data["option_type"] == 'P')]
        overATM = twoDaysOut[twoDaysOut["delta_1545"] >= -0.5]
        overATM.sort_values(by="delta_1545", axis=0, ascending=True,  inplace=True)
        n += 1
      if len(overATM) > 0:
        holding = overATM.iloc[0]
        print("Selling " + str(holding["expiration"]) + " " + str(holding["strike"]) + " for " + str((holding["bid_1545"] + holding["ask_1545"]) / 2))
      current += datetime.timedelta(days= n - 1)
    except FileNotFoundError:
      print("No data found today")
      if (current - start).days > 1:
        print("going back in time...")
        current -= datetime.timedelta(days=1)
      else:
        current += datetime.timedelta(days=1)

if __name__ == "__main__":
  main()
  print(x)
  print(y)
