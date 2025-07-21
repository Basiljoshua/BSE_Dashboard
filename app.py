import streamlit as st
import pandas as pd
import yfinance as yf
import os

st.set_page_config(page_title="BSE Dashboard", layout="wide")

st.title("📈 BSE Stock Data Dashboard")

# ----------- Section 1: Bhav Copy CSV -----------
st.header("📂 Bhav Copy (Local CSV Data)")

try:
    sample_file = os.path.join("data", "bhav_copy.CSV")
    df = pd.read_csv(sample_file)

    st.subheader("Raw Data (Top 5 Rows)")
    st.dataframe(df.head())

    if all(col in df.columns for col in ["FinInstrmNm", "OpnPric", "ClsPric"]):
        selected_bhav_stock = st.selectbox(
            "Select a stock from Bhav Copy", df["FinInstrmNm"].unique(), key="bhav"
        )

        stock_row = df[df["FinInstrmNm"] == selected_bhav_stock].iloc[0]

        open_price = stock_row["OpnPric"]
        close_price = stock_row["ClsPric"]
        percent_change = ((close_price - open_price) / open_price) * 100

        st.subheader(f"📊 {selected_bhav_stock} (Bhav Copy Data)")
        st.metric(
            label="Percentage Change",
            value=f"{percent_change:.2f}%",
            delta=f"{percent_change:.2f}%",
        )

        st.bar_chart(
            pd.DataFrame({"Price": [open_price, close_price]}, index=["Open", "Close"])
        )
except Exception as e:
    st.error(f"⚠️ Could not load Bhav Copy: {e}")

# ----------- Section 2: yFinance Real-Time -----------
st.header("🌐 Live BSE Stock (via Yahoo Finance)")

# Sample stock list (you can expand this)
bse_stocks = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK",
    "ICICIBANK", "SBIN", "LT", "ITC", "BHARTIARTL", "AXISBANK"
]

selected_live_stock = st.selectbox("Select a live BSE stock", bse_stocks, key="live")

yf_ticker = selected_live_stock + ".BO"

try:
    stock = yf.Ticker(yf_ticker)
    stock_info = stock.info

    current_price = stock_info.get("regularMarketPrice", None)
    prev_close = stock_info.get("regularMarketPreviousClose", None)
    open_price = stock_info.get("regularMarketOpen", None)

    if current_price is None:
        raise ValueError("No price data available")

    percent_change = (
        ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
    )

    st.subheader(f"📡 {selected_live_stock} (Real-Time via yFinance)")
    st.metric(
        label="Current Price",
        value=f"₹ {current_price:.2f}",
        delta=f"{percent_change:.2f}%"
    )

    st.bar_chart(
        pd.DataFrame(
            {"Price": [open_price, prev_close, current_price]},
            index=["Open", "Prev Close", "Current"]
        )
    )

except Exception as e:
    st.error(f"⚠️ Could not fetch data for `{yf_ticker}`: {e}")
