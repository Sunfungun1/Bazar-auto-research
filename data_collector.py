import requests
import pandas as pd
import time
import os

API_URL = "https://api.hypixel.net/v2/skyblock/bazaar"
DATA_FILE = "bazaar_history.csv"

def fetch_bazaar_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                products = data.get("products", {})
                timestamp = time.time()
                
                rows = []
                for item_id, details in products.items():
                    quick_status = details.get("quick_status", {})
                    rows.append({
                        "timestamp": timestamp,
                        "item_id": item_id,
                        "sell_price": quick_status.get("sellPrice", 0),
                        "buy_price": quick_status.get("buyPrice", 0),
                        "sell_volume": quick_status.get("sellVolume", 0),
                        "buy_volume": quick_status.get("buyVolume", 0)
                    })
                
                df = pd.DataFrame(rows)
                if not os.path.isfile(DATA_FILE):
                    df.to_csv(DATA_FILE, index=False)
                else:
                    df.to_csv(DATA_FILE, mode='a', header=False, index=False)
                print(f"Data snapshot added: {time.strftime('%H:%M:%S')}")
        else:
            print(f"API Connection Issue: {response.status_code}")
    except Exception as e:
        print(f"Error logging data: {e}")

if __name__ == "__main__":
    print("Starting background data collector. Press Ctrl+C to exit.")
    while True:
        fetch_bazaar_data()
        time.sleep(60)