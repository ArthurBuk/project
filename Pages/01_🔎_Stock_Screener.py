# FRONT
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# BACK
import pandas_datareader as web
import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf
import datetime as dt


# LOTTIE ICON
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_icon_2 = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_zzm0zttt.json")
st_lottie(lottie_icon_2)


# FILTER 1 - Select ETF
st.header("Select a benchmark ETF")
etf_list = ['S&P 500', 'DOW', 'NASDAQ', 'IBOVESPA', 'NIFTY 50']
etf_selectbox = st.selectbox("Choose index", options=etf_list)

# FILTER 2 - Select TIMEFRAME
st.header("Select a timeframe for analysis")
x = st.slider('From 1 to 365 days',
              min_value=1, max_value=365, step=1)


start = dt.datetime.now() - dt.timedelta(days=x)
end = dt.datetime.now()

tickers = ''
etf_selected = ''

if etf_selectbox == 'S&P 500':
    tickers = si.tickers_sp500()
    etf_selected = '^GSPC'
elif etf_selectbox == 'DOW':
    tickers = si.tickers_dow()
    etf_selected = '^DJI'
elif etf_selectbox == 'NASDAQ':
    tickers = si.tickers_nasdaq()
    etf_selected = '^IXIC'
elif etf_selectbox == 'IBOVESPA':
    tickers = si.tickers_ibovespa()
    etf_selected = '^BVSP'
elif etf_selectbox == 'NIFTY 50':
    tickers = si.tickers_nifty50()
    etf_selected = '^NSEI'

etf_df = web.DataReader(etf_selected, 'yahoo', start, end)
etf_df['Pct Change'] = etf_df['Adj Close'].pct_change()
etf_return = (etf_df['Pct Change'] + 1).cumprod()[-1]


# EXPANDER 1 - START
expander = st.expander(f"{etf_selectbox} index historical performance")

# PLOT 1 - ETF historical data /yfinance/
expander.header(f"{etf_selectbox} performance - past {x} days")

plot1_etf_symbol = etf_selected  # Ticker symbol of ETF - selected from checkbox
plot1_etf_data = yf.Ticker(plot1_etf_symbol)
plot1_etf_df = plot1_etf_data.history(period='1d', start=start, end=end)

expander.line_chart(plot1_etf_df["Close"])
if expander.checkbox("Show plot data"):
    expander.dataframe(plot1_etf_df['Close'], height=int(250))
# EXPANDER 1 - END


# FILTER 3 - FILTERING STOCK KPI
# Score - key indicator to compare to S&P500 performance, calculated below
# NOTE: order of selection influences order inside the list
columns_original = [
    'Ticker',
    'Latest_Price',
    'Score',  # KeyError: 'Score' - solved, it was called in the end by final_df.sort_values(...)
    'PE_Ratio',
    'PEG_Ratio',
    'SMA_150',
    'SMA_200',
    '52_Week_Low',
    '52_Week_High']

st.header("Select stock KPIs for analysis")
columns_selected = st.multiselect(label="Desired KPIs", options=columns_original)

return_list = []
final_df = pd.DataFrame(columns=[columns_selected])
st.write(final_df)  # NOTE: order of selection influences order inside the list
st.write("testing")

# create CSV file OR ignore and keep just in memory,
# adjust code below if not using csv


# for ticker in tickers:
#     df = web.DataReader(ticker, 'yahoo', start, end)
# #   df.to_csv(f'C:/Users/Munich2018/PycharmProjects/project/Stock_Data/stock_data/{ticker}.csv')
#
#     # calculating % change in stock price
#     df['Pct Change'] = df['Adj Close'].pct_change()
#     stock_return = (df['Pct Change'] + 1).cumprod()[-1]
#
#     # calculating relative returns of 1 stock to ETF
#     returns_compared = round((stock_return / etf_return), 2)
#     return_list.append(returns_compared)
#
# # FILTERS for identifying TOP performers (> than ETF)
# best_performers = pd.DataFrame(list(zip(tickers, return_list)),
#                                columns=[
#                                    'Ticker',
#                                    'Returns Compared'
#                                ])
#
# # rank TOP stock performers
# # multiply by 100 to get actual % values
# best_performers['Score'] = best_performers['Returns Compared'].rank(pct=True) * 100


# FILTER 4 - Choose % of TOP stock
# Specify TOP performers in %, 0.8 = TOP 20 %, 0.7 = TOP 30 %, etc.
st.header("TOP performing stocks vs selected ETF")
top_stocks_selectbox = st.selectbox("Choose desired of TOP performers", options=['1.0 %', '1.5 %', '2.0 %', '2.5 %'])

top_stocks_pct = ''

if top_stocks_selectbox == '1.0 %':
    top_stocks_pct = 0.99
elif top_stocks_selectbox == '1.5 %':
    top_stocks_pct = 0.985
elif top_stocks_selectbox == '2.0 %':
    top_stocks_pct = 0.98
elif top_stocks_selectbox == '2.5 %':
    top_stocks_pct = 0.975

# best_performers = best_performers[best_performers['Score'] >= best_performers['Score'].quantile(top_stocks_pct)]


# for ticker in best_performers['Ticker']:
#     try:
#         # uploading the CSV file
#         df = pd.read_csv(f'C:/Users/Munich2018/PycharmProjects/project/Stock_Data/stock_data/{ticker}.csv', index_col=0)
#         moving_averages = [150, 200]
#         for ma in moving_averages:
#             # window defines timeframe (e.g. 150 dats, 200 days, etc.)
#             df['SMA_' + str(ma)] = round(df['Ads Close'].rolling(window=ma).mean(), 2) # rounded to 2 decimal places
#
#         latest_price = df['Adj Close'][-1]
#         # check documentation + function description for adding other statistics
#         # check stock.info() OR print(si.get_quote_data(ticker)) to see a DICT and choose
#         # some other field for more information
#         pe_ratio = float(si.get_quote_data(ticker)['PE Ratio (TTM)'])
#         # accessing individual fields
#         peg_ratio = float(si.get_stats_valuation(ticker)[1][4])
#         moving_average_150 = df('SMA_150')[-1]
#         moving_average_200 = df('SMA_200')[-1]
#         low_52week = round(min(df['Low'][-(52*5):]), 2)
#         high_52week = round(max(df['Low'][-(52*5):]), 2)
#         score = round(best_performers[best_performers['Ticker'] == ticker]['Score'].tolist())
#
#         # conditions for picking the stock
#
#         KPI_1 = latest_price > moving_average_150 > moving_average_200
#         KPI_2 = latest_price >= (1.3 * low_52week)
#         KPI_3 = latest_price >= (0.75 * high_52week)
#         KPI_4 = pe_ratio < 40
#         KPI_5 = peg_ratio < 2
#
#         if KPI_1 and KPI_2 and KPI_3 and KPI_4 and KPI_5:
#             final_df = final_df.append({'Ticker': ticker,
#                                         'Latest_Price': latest_price,
#                                         'Score': score,
#                                         'PE_Ratio': pe_ratio,
#                                         'SMA_150': moving_average_150,
#                                         'SMA_200': moving_average_200,
#                                         '52_Week_Low': low_52week,
#                                         '52_Week_High': high_52week}, ignore_index=True)
#     except Exception as e:
#         print(f"{e} for {ticker}")

# final_df.sort_values(by='Score', ascending=False)
# pd.set_option('display.max_columns', 10)

#print(final_df)
#final_df.to_csv()




