import pandas as pd
import plotly.graph_objects as go

# Define support function
def support(df1, l, n1, n2):
    for i in range(l - n1 + 1, l + 1):
        if df1['Low'][i] > df1['Low'][i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df1['Low'][i] < df1['Low'][i - 1]:
            return 0
    return 1

# Define resistance function
def resistance(df1, l, n1, n2):
    for i in range(l - n1 + 1, l + 1):
        if df1['High'][i] < df1['High'][i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df1['High'][i] > df1['High'][i - 1]:
            return 0
    return 1

# Load data
df = pd.read_csv('TSLA.csv')

# Define parameters
n1 = 2  # Number of candles before
n2 = 2  # Number of candles after

# Create a candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Candlesticks')])

# Initialize lists to store support and resistance levels
support_levels = []
resistance_levels = []

# Find and mark support and resistance levels
for i in range(n1, len(df) - n2):
    if support(df, i, n1, n2):
        support_date = df.loc[i, 'Date']  # Get the date in 'YYYY-MM-DD' format
        support_levels.append({'Date': support_date, 'Price': df['Low'][i], 'Type': 'Support'})
        fig.add_trace(go.Scatter(x=[df.index[i]], y=[df['Low'][i]],
                                mode='markers',
                                name='Support Level',
                                marker=dict(color='green', size=8)))
    elif resistance(df, i, n1, n2):
        resistance_date = df.loc[i, 'Date']  # Get the date in 'YYYY-MM-DD' format
        resistance_levels.append({'Date': resistance_date, 'Price': df['High'][i], 'Type': 'Resistance'})
        fig.add_trace(go.Scatter(x=[df.index[i]], y=[df['High'][i]],
                                mode='markers',
                                name='Resistance Level',
                                marker=dict(color='red', size=8)))

# Customize the layout
fig.update_layout(title='Candlestick Chart with Support and Resistance Levels',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=True)

# Show the chart
fig.show()

# Create DataFrames for support and resistance levels
support_df = pd.DataFrame(support_levels)
resistance_df = pd.DataFrame(resistance_levels)

# Save support and resistance levels to CSV files
support_df.to_csv('support_levels.csv', index=False)
resistance_df.to_csv('resistance_levels.csv', index=False)
