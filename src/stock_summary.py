#stock_summary.py

# this script will fetch stocks data from inventory.db and after preprocessing and featuring will restore in database (inventory.db)

import pandas as pd
import sqlite3
from preprocessing import preprocess
from features import create_features
import logging

logging.basicConfig(
    filename='../logs/stock_summary.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
conn = sqlite3.connect("inventory.db")
# this function will fetch stocks data from inventory.db
def fetch_data(conn):
    try:
        logging.info("Fetchimg data...")
        gold = pd.read_sql_query("SELECT * FROM gold", conn)
        silver = pd.read_sql_query("SELECT * FROM silver", conn)
        oil = pd.read_sql_query("SELECT * FROM oil", conn)
        
        logging.info("creating copy of data...")
        gold_copy = gold.copy()
        silver_copy = silver.copy()
        oil_copy = oil.copy() 
        
        logging.info("preprocessing..")
        # Preprocess individually
        gold = preprocess(gold)
        silver = preprocess(silver)
        oil = preprocess(oil)
        
        
        df = pd.concat([
            gold["Close"].rename("Gold"),
            silver["Close"].rename("Silver"),
            oil["Close"].rename("Oil")
        ], axis=1)
        # Feature engineering
        
        logging.info("adding some new features...")
        df = create_features(df)
        df.dropna(inplace=True)
        print(df.head())
        
        return df
    except Exception as e:
        logging.error(f"fetching error: {e}")
        return None

def store_summary(df, conn):
    try:
        logging.info("Storing data...")
        df.reset_index(inplace=True)   # convert index → column
        df.to_sql("stock_summary", conn, if_exists="replace", index=False)
        logging.info("Stock summary stored in database")
        
    except Exception as e:
        logging.error(f"fetching error: {e}")
    
if __name__ == "__main__":
    conn = sqlite3.connect("inventory.db")

    df = fetch_data(conn)

    if df is not None:
        store_summary(df, conn)
        logging.info("stock_summary table is stored in database...")
    else:
        logging.error("Dataframe is None, skipping storage")

    conn.close()