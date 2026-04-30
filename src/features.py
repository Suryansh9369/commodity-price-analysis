import pandas as pd

#calculate returns
def calculate_return(df):
    return df.pct_change()

#calculate volatility(Risk) or rolling window of 30 days
def calculate_volatility(df, window=30):
    return df.pct_change().rolling(window).std()

# calculating moving averages
def moving_average(df, window=30):
    return df.rolling(window).mean()

# Master feature function to be called.

def create_features(df):
    df["Returns"] = calculate_return(df)
    df["Volatility"] = calculate_volatility(df,window=30)
    df["Moving_Average_30_Days"] = moving_average(df, window=30)
    
    return df

# this script will return dataframe with new feature like returns, volatility(Risk) and moving average.