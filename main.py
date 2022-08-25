import pandas_datareader as web
import pandas as pd
from yahoo_fin import stock_info as si
import datetime as dt

ticker = "MSFT"

pd.set_option('display.max_columns', None)
ticker_data = si.get_data(ticker, start_date=dt.date(2021, 7, 31), end_date=dt.date(2022, 7, 31))

x = pd.DataFrame(ticker_data)

print(x)




