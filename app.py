import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

# Initialize session state variables if they don't exist
if 'stock_data' not in st.session_state:
    # Generate initial stock data (last 60 minutes)
    minutes = 60
    base_time = datetime.now() - timedelta(minutes=minutes)
    times = [base_time + timedelta(minutes=i) for i in range(minutes)]
    
    # Generate slightly upward trending initial data
    initial_price = 100
    noise = np.random.normal(0, 0.5, minutes)
    trend = np.linspace(0, 1, minutes)  # Slight upward trend
    prices = initial_price + noise + trend
    
    st.session_state.stock_data = {
        'times': times,
        'prices': prices.tolist(),
        'last_action': None,
        'last_action_time': None,
        'trend': 'up'  # Track current trend
    }

# Page config
st.set_page_config(page_title="Stock Simulator", layout="wide")
st.title("🚀 Stock Market Simulator")

# Create columns for buy/sell buttons
col1, col2 = st.columns(2)

# Buy button
if col1.button("Buy 📈"):
    current_time = datetime.now()
    st.session_state.stock_data['times'].append(current_time)
    last_price = st.session_state.stock_data['prices'][-1]
    # Generate a sharp increase
    new_price = last_price * (1 + np.random.uniform(0.05, 0.15))
    st.session_state.stock_data['prices'].append(new_price)
    st.session_state.stock_data['last_action'] = 'buy'
    st.session_state.stock_data['last_action_time'] = current_time
    st.session_state.stock_data['trend'] = 'up'

# Sell button
if col2.button("Sell 📉"):
    current_time = datetime.now()
    st.session_state.stock_data['times'].append(current_time)
    last_price = st.session_state.stock_data['prices'][-1]
    # Generate a sharp decrease
    new_price = last_price * (1 - np.random.uniform(0.05, 0.15))
    st.session_state.stock_data['prices'].append(new_price)
    st.session_state.stock_data['last_action'] = 'sell'
    st.session_state.stock_data['last_action_time'] = current_time
    st.session_state.stock_data['trend'] = 'down'

# Add natural price movement
current_time = datetime.now()
last_price = st.session_state.stock_data['prices'][-1]

# Determine movement based on current trend with some randomness
trend_factor = 1.0005 if st.session_state.stock_data['trend'] == 'up' else 0.9995
random_factor = np.random.normal(1, 0.001)  # Small random variations
new_price = last_price * trend_factor * random_factor

# Occasionally change trend
if np.random.random() < 0.05:  # 5% chance to switch trend
    st.session_state.stock_data['trend'] = 'down' if st.session_state.stock_data['trend'] == 'up' else 'up'

# Update data
st.session_state.stock_data['times'].append(current_time)
st.session_state.stock_data['prices'].append(new_price)

# Keep only last 60 minutes of data
if len(st.session_state.stock_data['times']) > 60:
    st.session_state.stock_data['times'] = st.session_state.stock_data['times'][-60:]
    st.session_state.stock_data['prices'] = st.session_state.stock_data['prices'][-60:]

# Create the stock chart
fig = go.Figure()

# Add the stock price line
fig.add_trace(go.Scatter(
    x=st.session_state.stock_data['times'],
    y=st.session_state.stock_data['prices'],
    mode='lines',
    name='Stock Price',
    line=dict(color='#17A2B8', width=2)
))

# Update layout
fig.update_layout(
    title='Live Stock Price Simulation',
    xaxis_title='Time',
    yaxis_title='Price ($)',
    hovermode='x unified',
    showlegend=False,
    height=600,
    template='plotly_white'
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Add some metrics
current_price = st.session_state.stock_data['prices'][-1]
price_change = current_price - st.session_state.stock_data['prices'][-2] if len(st.session_state.stock_data['prices']) > 1 else 0
price_change_percent = (price_change / current_price) * 100

# Display metrics in columns
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} ({price_change_percent:.2f}%)")
col2.metric("Last Action", st.session_state.stock_data['last_action'].upper() if st.session_state.stock_data['last_action'] else "None")
col3.metric("Time Since Last Action", 
            f"{(datetime.now() - st.session_state.stock_data['last_action_time']).seconds}s ago" 
            if st.session_state.stock_data['last_action_time'] else "N/A")

# Refresh every 1 second
time.sleep(1)
st.experimental_rerun() 