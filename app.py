import streamlit as st
import pandas as pd
import yfinance as yf

# App Title
st.title("Stock Backtesting Engine")

# Sidebar Inputs
st.sidebar.header("1. Select Country & Stock Data")
country = st.sidebar.selectbox("Select Country", ["India", "USA"])
exchange = st.sidebar.selectbox("Select Stock Exchange", ["NSE", "NYSE"])
stock = st.sidebar.text_input("Enter Stock Symbol (e.g., SBIN.NS, AAPL)")

st.sidebar.header("2. Upload Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

st.sidebar.header("3. Backtest Configuration")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Fetch or Load Stock Data
@st.cache
def fetch_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

# Main Section
if st.sidebar.button("Run Backtest"):
    if uploaded_file is not None:
        # Use uploaded data
        data = pd.read_csv(uploaded_file)
        st.success("Using uploaded CSV file for analysis.")
    elif stock:
        # Fetch data from Yahoo Finance
        try:
            data = fetch_stock_data(stock, start_date, end_date)
            st.success(f"Fetched data for {stock}.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter a stock symbol or upload a file.")

    if 'data' in locals():
        # Display data table
        st.subheader(f"Stock Data for {stock}")
        st.write(data)

        # Backtest Logic (Simple Example: Moving Average Crossover)
        st.subheader("Backtesting Results")
        short_window = 10
        long_window = 50

        data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
        data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

        data['Signal'] = 0
        data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
        data.loc[data['Short_MA'] <= data['Long_MA'], 'Signal'] = -1

        st.line_chart(data[['Close', 'Short_MA', 'Long_MA']])
        st.write("Signal Values (1 = Buy, -1 = Sell):")
        st.write(data[['Date', 'Close', 'Short_MA', 'Long_MA', 'Signal']])

else:
    st.write("Configure and click 'Run Backtest' to view results.")

# Footer
st.sidebar.markdown("Developed with ❤️ using Streamlit.")
