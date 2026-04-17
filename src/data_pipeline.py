import pandas as pd 
from sqlalchemy import create_engine
import time
import os
import logging
import yfinance as yf

logging.basicConfig(
    filename='../logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Fetching gold data...")

engine = create_engine('sqlite:///inventory.db')

def fetch_data(ticker, name):
    """fetch data from yfinance"""
    try:
        logging.info(f"Fetching data from {name}({ticker})")
        
        df = yf.download(ticker, start='2025-10-10')
        
        if df.empty:
            logging.warning(f"No data returned from {name}")
        else:
            logging.info(f"fetched {len(df)} rows of {name}")
        return df
    
    except Exception as e:
        logging.error(f"Error fetching {name}: {e}")
        return None
    
def store_data(df, table_name):
    """store dataframe into sqlite3"""
    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=True)
        logging.info(f"stored data in table: {table_name}")
        
    except Exception as e:
        logging.error(f"Error storing {table_name}: {e}")
        
def run_pipeline():
    start = time.time()
    
    commodities = {
        "GC=F": "gold",
        "SI=F": "silver",
        "CL=F": "oil"
    }
    
    for ticker, name in commodities.items():
        df = fetch_data(ticker, name)
        
        if df is not None:
            store_data(df, name)
            
    end = time.time()
    total_time = (end-start)/60
    
    logging.info("PIPELINE COMPLETED")
    logging.info(f"Total time taken: {total_time: .2f} minutes")
    
if __name__ == "__main__":
    run_pipeline()

