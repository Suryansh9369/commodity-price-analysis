import yfinance as yf

gold = yf.download("GC=F", start="2015-01-01")
silver = yf.download("SI=F", start="2015-01-01")
oil = yf.download("CL=F", start="2015-01-01")

gold.to_csv("data/gold.csv")
silver.to_csv("data/silver.csv")
oil.to_csv("data/oil.csv")
