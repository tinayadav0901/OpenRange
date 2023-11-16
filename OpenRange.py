import pandas as pd

# Sample data (you should replace this with actual historical data)
data = {
    'timestamp': ['2020-01-01 09:15', '2020-01-01 09:30', '2020-01-01 15:15'],
    'open': [30000, 30500, 31000],
    'high': [31000, 31500, 32000],
    'low': [29500, 30000, 30500],
    'close': [30800, 31200, 31500]
}

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Strategy parameters
stop_loss_percentage = 0.005
trade_start_time = pd.to_datetime('09:15')
trade_end_time = pd.to_datetime('15:15')

# Initialize variables
position = None
entry_price = 0
stop_loss_price = 0
pnl = 0

# Implement the strategy
for index, row in df.iterrows():
    if index.time() == trade_start_time.time():
        # Reset position at the start of the day
        position = None

    if position is None:
        # Check for entry signals
        if row['high'] > row['open']:
            position = 'buy'
            entry_price = row['high']
            stop_loss_price = entry_price * (1 - stop_loss_percentage)
        elif row['low'] < row['open']:
            position = 'sell'
            entry_price = row['low']
            stop_loss_price = entry_price * (1 + stop_loss_percentage)

    elif position == 'buy':
        # Check for stop-loss or square off conditions
        if row['low'] < stop_loss_price or index.time() >= trade_end_time.time():
            pnl += row['close'] - entry_price
            position = None

    elif position == 'sell':
        # Check for stop-loss or square off conditions
        if row['high'] > stop_loss_price or index.time() >= trade_end_time.time():
            pnl += entry_price - row['close']
            position = None

# Print the profit and loss
print(f"Profit and Loss for 2020: {pnl}")