from datetime import datetime
import pandas as pd
import numpy as np
from cogi_quant.dataload.quote import Stock 

from typing import Union, Any 

def get_price_open_series(stock: Stock,
                          start_date: Union[pd.Timestamp, datetime, str] = None, 
                          end_date: Union[pd.Timestamp, datetime, str] = None, 
                          period: str = None,
                          time_interval: str = None) -> pd.Series:
    '''
    Return series data type of a stock's open price during a specified time. 

    *Either start_date AND end_date are specified, OR period alone. time_interval may be specified in either case.*

    :param stock: Stock object
    :param start_date: (Optional) time period start
    :param end_date: (Optional) time period end
    :param period: (Optional) period length ('1w', '1mo', '3mo', '6mo', '1y', '2y', '5y')
    :param time_interval: (Optional) time interval between quotes. Taken as 24 hours (1d) if not specified.

    **Examples**
    >>> aapl = Stock("AAPL")
    >>> get_price_open_series(stock=aapl, period='6mo')

    Date

    2024-12-23 00:00:00-05:00    254.156919                                                                                     
    2024-12-24 00:00:00-05:00    254.875189                                        
    2024-12-26 00:00:00-05:00    257.568678                                        
    2024-12-27 00:00:00-05:00    257.209530                                        
    2024-12-30 00:00:00-05:00    251.623005                                         
    ...                                                                                
    2025-06-16 00:00:00-04:00    197.300003                                        
    2025-06-17 00:00:00-04:00    197.199997                                        
    2025-06-18 00:00:00-04:00    195.940002                                        
    2025-06-20 00:00:00-04:00    198.240005                                        
    2025-06-23 00:00:00-04:00    201.531998                                        
    '''
    frame = stock.get_quote_frame(start=start_date, end=end_date, period=period, interval=time_interval)
    return frame['Open']

def get_price_close_series(stock: Stock, 
                           start_date: Union[pd.Timestamp, datetime, str] = None, 
                           end_date: Union[pd.Timestamp, datetime, str] = None, 
                           period: str = None,
                           time_interval: str = None) -> pd.Series:
    '''
    Return series data type of a stock's close price during a specified time. 

    *Either start_date AND end_date are specified, OR period alone. time_interval may be specified in either case.*

    :param stock: Stock object
    :param start_date: (Optional) time period start
    :param end_date: (Optional) time period end
    :param period: (Optional) period length ('1w', '1mo', '3mo', '6mo', '1y', '2y', '5y')
    :param time_interval: (Optional) time interval between quotes. Taken as 24 hours (1d) if not specified.

    **Examples**
    >>> aapl = Stock("AAPL")
    >>> get_price_close_series(stock=aapl, period='6mo')

    Date

    2024-12-23 00:00:00-05:00    254.156919                                                                                     
    2024-12-24 00:00:00-05:00    254.875189                                        
    2024-12-26 00:00:00-05:00    257.568678                                        
    2024-12-27 00:00:00-05:00    257.209530                                        
    2024-12-30 00:00:00-05:00    251.623005                                         
    ...                                                                                
    2025-06-16 00:00:00-04:00    197.300003                                        
    2025-06-17 00:00:00-04:00    197.199997                                        
    2025-06-18 00:00:00-04:00    195.940002                                        
    2025-06-20 00:00:00-04:00    198.240005                                        
    2025-06-23 00:00:00-04:00    201.531998                                        
    '''
    frame = stock.get_quote_frame(start=start_date, end=end_date, period=period, interval=time_interval)
    return frame['Close']

def get_price_high_series(stock: Stock, 
                          start_date: Union[pd.Timestamp, datetime, str] = None, 
                          end_date: Union[pd.Timestamp, datetime, str] = None, 
                          period: str = None,
                          time_interval: str = None) -> pd.Series:
    '''
    Return series of a stock's daily high price during a specified date range. *If interval is specified, it will take
    the stock's high price during that time interval*.

    *Either start_date AND end_date are specified, OR period alone. time_interval may be specified in either case.*

    :param stock: Stock object
    :param start_date: (Optional) time period start
    :param end_date: (Optional) time period end
    :param period: (Optional) period length ('1w', '1mo', '3mo', '6mo', '1y', '2y', '5y')
    :param time_interval: (Optional) time interval between quotes. Taken as 24 hours (1d) if not specified.

    **Examples**
    >>> aapl = dataload.micinfo..Stock("AAPL")
    >>> get_price_high_series(stock=aapl, period='6mo')

    Date

    2024-12-23 00:00:00-05:00    254.156919                                                                                     
    2024-12-24 00:00:00-05:00    254.875189                                        
    2024-12-26 00:00:00-05:00    257.568678                                        
    2024-12-27 00:00:00-05:00    257.209530                                        
    2024-12-30 00:00:00-05:00    251.623005                                         
    ...                                                                                
    2025-06-16 00:00:00-04:00    197.300003                                        
    2025-06-17 00:00:00-04:00    197.199997                                        
    2025-06-18 00:00:00-04:00    195.940002                                        
    2025-06-20 00:00:00-04:00    198.240005                                        
    2025-06-23 00:00:00-04:00    201.531998                                        
    '''
    frame = stock.get_quote_frame(start=start_date, end=end_date, period=period, interval=time_interval)
    return frame['High']

def get_price_low_series(stock: Stock,
                         start_date: Union[pd.Timestamp, datetime, str] = None, 
                         end_date: Union[pd.Timestamp, datetime, str] = None, 
                         period: str = None,
                         time_interval: str = None) -> pd.Series:
    '''
    Return series of a stock's daily low price during a specified date range. *If interval is specified, it will take
    the stock's high price during that time interval*.

    *Either start_date AND end_date are specified, OR period alone. time_interval may be specified in either case.*

    :param stock: Stock object
    :param start_date: (Optional) time period start
    :param end_date: (Optional) time period end
    :param period: (Optional) period length ('1w', '1mo', '3mo', '6mo', '1y', '2y', '5y')
    :param time_interval: (Optional) time interval between quotes. Taken as 24 hours (1d) if not specified.

    **Examples**
    >>> aapl = Stock("AAPL")
    >>> get_price_low_series(stock=aapl, period='6mo')

    Date

    2024-12-23 00:00:00-05:00    254.156919                                                                                     
    2024-12-24 00:00:00-05:00    254.875189                                        
    2024-12-26 00:00:00-05:00    257.568678                                        
    2024-12-27 00:00:00-05:00    257.209530                                        
    2024-12-30 00:00:00-05:00    251.623005                                         
    ...                                                                                
    2025-06-16 00:00:00-04:00    197.300003                                        
    2025-06-17 00:00:00-04:00    197.199997                                        
    2025-06-18 00:00:00-04:00    195.940002                                        
    2025-06-20 00:00:00-04:00    198.240005                                        
    2025-06-23 00:00:00-04:00    201.531998                                        
    '''
    frame = stock.get_quote_frame(start=start_date, end=end_date, period=period, interval=time_interval)
    return frame['Low']
