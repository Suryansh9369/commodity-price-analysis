#features.py

# this script will return dataframe with new feature like returns, volatility(Risk) and moving average.
import pandas as pd

#calculate returns
def calculate_return(df):
    return df.pct_change(fill_method=None)

#calculate volatility(Risk) or rolling window of 30 days
def calculate_volatility(df, window=30):
    return df.pct_change(fill_method=None).rolling(window).std()

# calculating moving averages
def moving_average(df, window=30):
    return df.rolling(window).mean()

# Master feature function to be called.

def create_features(df):
    returns = calculate_return(df)
    volatility = calculate_volatility(df)
    ma = moving_average(df)
    
    # Rename columns properly
    returns.columns = [col + "_Returns" for col in df.columns]
    volatility.columns = [col + "_Volatility" for col in df.columns]
    ma.columns = [col + "_MA30" for col in df.columns]
    
    df = pd.concat([df, returns, volatility, ma], axis=1)
    
    return df

