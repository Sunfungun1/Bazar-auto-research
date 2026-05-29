import pandas as pd

def calculate_signals(df):
    """
    The AI Agent systematically overwrites this entire function block.
    Return values: 1 (Buy), -1 (Sell), 0 (Hold)
    """
    df['rolling_mean'] = df['mid_price'].rolling(window=5, min_periods=1).mean()
    signals = [1 if m < r * 0.99 else -1 if m > r * 1.01 else 0 for m, r in zip(df['mid_price'], df['rolling_mean'])]
    return pd.Series(signals, index=df.index)