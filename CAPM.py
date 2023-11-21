import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Disable the PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Adj Close']

def get_market_data(start_date, end_date):
    market_data = yf.download('^NSEI', start=start_date, end=end_date)  # Use the symbol for Nifty 50
    return market_data['Adj Close']

def calculate_expected_return(risk_free_rate, market_return, beta):
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return expected_return

def main():
    st.title("Capital Asset Pricing Model (CAPM) Calculator and Visualization")

    risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=2.0)
    market_return = st.number_input("Market Return (%)", min_value=0.0, max_value=100.0, step=0.1, value=8.0)
    beta = st.number_input("Enter Beta", min_value=0.0, step=0.1, value=1.0)
    stock_ticker = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS)", value="RELIANCE.NS")  # Use the symbol for the Indian stock
    start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    if st.button("Calculate Expected Return"):
        try:
            # Fetch stock and market data
            stock_data = get_stock_data(stock_ticker, start_date, end_date)
            market_data = get_market_data(start_date, end_date)

            # Calculate historical stock and market returns
            stock_returns = stock_data.pct_change()
            market_returns = market_data.pct_change()

            # Set a common color palette for better visualization
            sns.set_palette("husl")

            # Visualization 1: Historical Price Chart
            st.subheader("1. Historical Price Chart")
            fig_price_chart, ax_price_chart = plt.subplots(figsize=(12, 6))
            ax_price_chart.plot(stock_data, label=f"{stock_ticker} Stock Price", linewidth=2)
            ax_price_chart.plot(market_data, label="Nifty 50 Index", linewidth=2)
            ax_price_chart.set_title("Historical Price Chart", fontsize=16)
            ax_price_chart.set_xlabel("Date", fontsize=12)
            ax_price_chart.set_ylabel("Adjusted Close Price", fontsize=12)
            ax_price_chart.legend(fontsize=10)
            st.pyplot(fig_price_chart)

            # Visualization 2: Beta Comparison
            st.subheader("2. Beta Comparison with Market")
            fig_beta_comparison, ax_beta_comparison = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=market_returns, y=stock_returns, label=f"{stock_ticker} vs Market", ax=ax_beta_comparison, s=50)
            ax_beta_comparison.axhline(0, color='black', linestyle='--', linewidth=2)
            ax_beta_comparison.axvline(0, color='black', linestyle='--', linewidth=2)
            ax_beta_comparison.set_title("Beta Comparison with Market", fontsize=16)
            ax_beta_comparison.set_xlabel("Nifty 50 Returns", fontsize=12)
            ax_beta_comparison.set_ylabel(f"{stock_ticker} Returns", fontsize=12)
            ax_beta_comparison.legend(fontsize=10)
            st.pyplot(fig_beta_comparison)

            # Visualization 3: CAPM Expected Return
            st.subheader("3. CAPM Expected Return")
            expected_return = calculate_expected_return(risk_free_rate / 100, market_return / 100, beta)
            st.success(f"The expected return is: {expected_return * 100:.2f}%")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
