import os
import time
import requests
import pandas as pd

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
API_URL = "[https://api.hypixel.net/v2/skyblock/bazaar](https://api.hypixel.net/v2/skyblock/bazaar)"
TARGET_ITEM = "ENCHANTED_DIAMOND"

def send_alert(msg):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})

def run_monitor():
    last_signal = 0
    while True:
        try:
            res = requests.get(API_URL).json()
            if res.get("success"):
                stats = res["products"][TARGET_ITEM]["quick_status"]
                bp, sp = stats["buyPrice"], stats["sellPrice"]
                
                live_df = pd.DataFrame([{"buy_price": bp, "sell_price": sp, "mid_price": (bp+sp)/2}])
                
                import train
                import importlib
                importlib.reload(train)
                
                sig = train.calculate_signals(live_df).iloc[-1]
                
                if sig == 1 and last_signal != 1:
                    send_alert(f"🟩 **BUY ENTRY OPTION** 🟩\n**Item:** {TARGET_ITEM}\n**Price:** {bp:,.1f} coins\n*Manual Action Required*")
                    last_signal = 1
                elif sig == -1 and last_signal != -1:
                    send_alert(f"🟥 **SELL EXIT OPTION** 🟥\n**Item:** {TARGET_ITEM}\n**Price:** {sp:,.1f} coins\n*Manual Action Required*")
                    last_signal = -1
                elif sig == 0:
                    last_signal = 0
        except Exception as e:
            print(f"Monitor Sync Check Failed: {e}")
        time.sleep(60)

if __name__ == "__main__":
    run_monitor()