def selectContract(df, type, expiration, strike):
  temp = df[(df["expiration"] == expiration) & (df["strike"] == strike) & (df["option_type"] == type)]
  # print(">>>>" + type + "," +  expiration + "," + str(strike))
  return temp.iloc[0]

def bidAskMean(bid, ask):
  return (bid + ask) / 2

def grand_selector(df, type, delta, expiry):
  correct_type_delta_and_expiration = df[(df["option_type"] == type) & (df["delta_1545"] >= delta[0]) & (df["delta_1545"] <= delta[1]) & (df["expiration"] >= str(expiry.date()))]
  sorted = correct_type_delta_and_expiration.sort_values(by=["expiration","delta_1545"]) 
  return sorted.iloc[0]
