import os
import sys
import json
from openai import OpenAI
from prepare import load_and_split_data

# --- UPDATED FOR OPENROUTER FREE TIER ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "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") 
)
# ----------------------------------------

def run_backtest(data_slice):
    try:
        import train
        import importlib
        importlib.reload(train)
        
        df = data_slice.copy()
        df['signal'] = train.calculate_signals(df)
        
        balance = 10000000
        inventory = 0
        
        for idx, row in df.iterrows():
            if row['signal'] == 1 and balance >= row['buy_price'] * 100:
                balance -= (row['buy_price'] * 100)
                inventory += 100
            elif row['signal'] == -1 and inventory > 0:
                balance += (row['sell_price'] * inventory)
                inventory = 0
                
        return balance + (inventory * df['sell_price'].iloc[-1]) - 10000000
    except Exception as e:
        print(f"Strategy Compilation Error: {e}")
        return -9999999

def main_research_loop():
    train_data, _ = load_and_split_data()
    best_profit = -float('inf')
    generation = 1
    
    with open("prompt.md", "r") as f:
        system_prompt = f.read()
        
    while True:
        print(f"\n--- AI Research Generation {generation} ---")
        with open("train.py", "r") as f:
            current_code = f.read()
            
        # --- UPDATED MODEL FOR FREE TIER ---
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Enhance this strategy loop:\n\n{current_code}\n\nReturn clean code changes."}
            ]
        )
        # ------------------------------------
        with open("train.py", "r") as f:
            current_code = f.read()
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Enhance this strategy loop:\n\n{current_code}\n\nReturn clean code changes."}
            ]
        )
        
        raw_output = response.choices[0].message.content
        cleaned_code = raw_output.split("```python")[1].split("```")[0].strip() if "```python" in raw_output else raw_output.strip()
        
        with open("train.py", "w") as f:
            f.write(cleaned_code)
            
        profit = run_backtest(train_data)
        print(f"Resulting Strategy Profitability: {profit:,.2f} coins")
        
        if profit > best_profit and profit > -9999999:
            best_profit = profit
            print(f"🔥 Found breakthrough! Preserving Gen {generation} script.")
            with open("best_strategy_current.py", "w") as f:
                f.write(cleaned_code)
        
        generation += 1
        if generation > 5: # Small execution limit cap for test runs
            break

if __name__ == "__main__":
    main_research_loop()