#preprocess.py
# this script used to clean and preprocess the dataframe.

import pandas as pd

#Convert date to datetime
def convert_date(df):
    df["Date"] = pd.to_datetime(df["Date"])
    return df

#setting date as index
def set_index(df):
    df.set_index("Date", inplace=True)
    return df

#handle missing values
def handle_missing_value(df):
    df.ffill(inplace=True)
    df.dropna(inplace=True)
    return df

def preprocess(df):
    df = convert_date(df)
    df = set_index(df)
    df= handle_missing_value(df)
    return df

