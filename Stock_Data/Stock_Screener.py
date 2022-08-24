import pandas_datareader as web
import pandas as pd
from yahoo_fin import stock_info as si
import datetime as dt


############################################################################################################## FILTER 1
# or another ETF (DOW, NASDAQ)
tickers = si.tickers_sp500()

############################################################################################################## FILTER 2

# T=1Y (365 days)
start = dt.datetime.now() - dt.timedelta(days=365)
end = dt.datetime.now()

# return of ETF in 1Y
sp500_df = web.DataReader('^GSPC', 'yahoo', start, end)   # make argument dynamic
sp500_df['Pct Change'] = sp500_df['Adj Close'].pct_change()
sp500_return = (sp500_df['Pct Change'] + 1).cumprod()[-1]

# parameters for FILTERING
return_list = []
final_df = pd.DataFrame(columns=[
    'Ticker',
    'Latest_Price',
    'Score',
    'PE_Ratio',
    'PEG_Ratio',
    'SMA_150',
    'SMA_200',
    '52_Week_Low',
    '52_Week_High',
    ])

# create CSV file OR ignore and keep just in memory,
# adjust code on a line 62
for ticker in tickers:
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.to_csv(f'stock_data/{ticker}.csv')

    # calculating % change in stock price
    df['Pct Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Pct Change'] + 1).cumprod()[-1]

    # calculating relative returns of 1 stock to ETF
    returns_compared = round((stock_return / sp500_return), 2)
    return_list.append(returns_compared)

# FILTERS for identifying TOP performers (> than ETF)
best_performers = pd.DataFrame(list(zip(tickers, return_list)),
                               columns=[
                                   'Ticker',
                                   'Returns Compared'
                               ])
# rank TOP performers
# multiply by 100 to get actual % values
best_performers['Score'] = best_performers['Returns Compared'].rank(pct=True) * 100
# specify TOP performers in %, 0.8 = TOP 20 %, 0.7 = TOP 30 %, etc.
best_performers = best_performers[best_performers['Score'] >= best_performers['Score'].quantile(0.7)]


for ticker in best_performers['Ticker']:
    try:
        # uploading the CSV file
        df = pd.read_csv(f'stock_data/{ticker}.csv', index_col=0)
        moving_averages = [150, 200]
        for ma in moving_averages:
            # window defines timeframe (e.g. 150 dats, 200 days, etc.)
            df['SMA_' + str(ma)] = round(df['Ads Close'].rolling(window=ma).mean(), 2) # rounded to 2 decimal places

        latest_price = df['Adj Close'][-1]
        # check documentation + function description for adding other statistics
        # check stock.info() OR print(si.get_quote_data(ticker)) to see a DICT and choose
        # some other field for more information
        pe_ratio = float(si.get_quote_data(ticker)['PE Ratio (TTM)'])
        # accessing individual fields
        peg_ratio = float(si.get_stats_valuation(ticker)[1][4])
        moving_average_150 = df('SMA_150')[-1]
        moving_average_200 = df('SMA_200')[-1]
        low_52week = round(min(df['Low'][-(52*5):]), 2)
        high_52week = round(max(df['Low'][-(52*5):]), 2)
        score = round(best_performers[best_performers['Ticker'] == ticker]['Score'].tolist())

        # conditions for picking the stock

        condition_1 = latest_price > moving_average_150 > moving_average_200
        condition_2 = latest_price >= (1.3 * low_52week)
        condition_3 = latest_price >= (0.75 * high_52week)
        condition_4 = pe_ratio < 40
        condition_5 = peg_ratio < 2

        if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
            final_df = final_df.append({'Ticker': ticker,
                                        'Latest_Price': latest_price,
                                        'Score': score,
                                        'PE_Ratio': pe_ratio,
                                        'SMA_150': moving_average_150,
                                        'SMA_200': moving_average_200,
                                        '52_Week_Low': low_52week,
                                        '52_Week_High': high_52week}, ignore_index=True)
    except Exception as e:
        print(f"{e} for {ticker}")

final_df.sort_values(by='Score', ascending=False)
pd.set_option('display.max_columns', 10)

print(final_df)
final_df.to_csv()





