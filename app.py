import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Advanced Stock Dashboard", layout="wide")

st.title("📈 Advanced Stock Market Dashboard")

# ------------------ SIDEBAR ------------------
st.sidebar.header("Settings")

# Multi-select stocks
stocks = st.sidebar.multiselect(
    "Select Stocks",
    ["AAPL", "TSLA", "GOOGL", "INFY.NS", "RELIANCE.NS", "TCS.NS"],
    default=["AAPL"]
)

# Time interval
interval = st.sidebar.selectbox(
    "Select Interval",
    ["1m", "5m", "15m", "1h", "1d"]
)

# Auto refresh
refresh = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)

# ------------------ AUTO REFRESH ------------------
st.experimental_rerun()

# ------------------ FETCH DATA ------------------
if stocks:
    data = yf.download(stocks, period="1d", interval=interval)

    # ------------------ GRAPH ------------------
    st.subheader("📊 Candlestick Chart")

    for stock in stocks:
        try:
            df = yf.download(stock, period="1d", interval=interval)

            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=stock
            ))

            # Moving Averages
            df['MA50'] = df['Close'].rolling(window=50).mean()
            df['MA200'] = df['Close'].rolling(window=200).mean()

            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['MA50'],
                mode='lines',
                name='MA 50'
            ))

            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['MA200'],
                mode='lines',
                name='MA 200'
            ))

            fig.update_layout(
                title=f"{stock} Live Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.error(f"Error loading {stock}")

    # ------------------ METRICS ------------------
    st.subheader("📊 Key Metrics")

    cols = st.columns(len(stocks))

    for i, stock in enumerate(stocks):
        try:
            df = yf.download(stock, period="1d", interval=interval)
            price = df['Close'].iloc[-1]
            high = df['High'].max()
            low = df['Low'].min()

            cols[i].metric(stock, round(float(price), 2))
            cols[i].write(f"High: {round(float(high), 2)}")
            cols[i].write(f"Low: {round(float(low), 2)}")

        except:
            cols[i].write("No Data")

else:
    st.warning("Please select at least one stock")