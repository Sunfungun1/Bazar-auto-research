import pandas as pd
import os

DATA_FILE = "bazaar_history.csv"

def load_and_split_data():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError("Data layer missing. Run data_collector.py for a few minutes first!")
        
    df = pd.read_csv(DATA_FILE)
    df = df[df['item_id'] == 'ENCHANTED_DIAMOND'].copy()
    df['mid_price'] = (df['buy_price'] + df['sell_price']) / 2
    
    # Chronological partition to prevent look-ahead bias
    split_idx = int(len(df) * 0.7)
    return df.iloc[:split_idx].reset_index(drop=True), df.iloc[split_idx:].reset_index(drop=True)