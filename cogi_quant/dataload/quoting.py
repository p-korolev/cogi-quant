import cogi_quant.dataload.company_profile as profile
from datetime import datetime

import yfinance as fin
import numpy as np
import pandas as pd

class Quote(profile.CompanyProfile):
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.load = fin.Ticker(ticker)
    
    def get_current_price(self) -> np.float64:
        '''
        Returns last updated price of the stock.   

        **Examples**

        >>> Quote("AAPL").get_current_price()
        >>> 198.91 
        '''
        return np.float64(self.load.info.get("currentPrice"))

    def overall_risk(self) -> np.float64:
        return np.float64(self.load.info.get("overallRisk"))
    
    def get_previous_close(self) -> np.float64:
        '''
        Returns previous day close price.

        **Examples**

        >>> Quote("AAPL").get_previous_close()
        >>> 198.71
        '''
        return np.float64(self.load.info.get("previousClose"))
    
    def get_current_day_open(self) -> np.float64:
        '''
        Returns current day open price.

        **Examples**

        >>> Quote("AAPL").get_current_day_open()
        >>> 198.77
        '''
        return np.float64(self.load.info.get("open"))
    
    def get_current_day_low(self) -> np.float64:
        '''
        Returns current day low price.

        **Examples**

        >>> Quote("AAPL").get_current_day_low()
        >>> 197.90
        '''
        return np.float64(self.load.info.get("dayLow"))
    
    def get_current_day_high(self) -> np.float64:
        '''
        Returns current day high price.

        **Examples**

        >>> Quote("AAPL").get_current_day_high()
        >>> 199.52
        '''
        return np.float64(self.load.info.get("dayHigh"))
    
    def get_beta(self) -> np.float64:
        '''
        Returns current beta value for stock.

        **Examples**
        
        >>> Quote("AAPL").get_beta()
        >>> 1.2
        '''
        return np.float64(self.load.info.get("beta"))
    
    def get_PE_trailing(self) -> np.float64:
        '''
        Returns current trailing P/E value for stock.

        **Examples**
        
        >>> Quote("AAPL").get_PE_trailing()
        >>> 30.70
        '''
        return np.float64(self.load.info.get("trailingPE"))
    
    def get_PE_forward(self) -> np.float64:
        '''
        Returns current forward P/E value for stock.

        **Examples**
        
        >>> Quote("AAPL").get_PE_forward()
        >>> 28.57
        '''
        return np.float64(self.load.info.get("forwardPE"))
    
    def get_current_day_volume(self) -> np.float64:
        return np.float64(self.load.info.get("volume"))
    
    def get_regular_volume(self) -> np.float64:
        return np.float64(self.load.info.get("regularMarketVolume"))
    
    def get_average_ten_day_volume(self) -> np.float64:
        return np.float64(self.load.info.get("averageDailyVolume10Day"))
    
    def get_year_low(self) -> np.float64:
        return np.float64(self.load.info.get("fiftyTwoWeekLow"))
    
    def get_year_high(self) -> np.float64:
        return np.float64(self.load.info.get("fiftyTwoWeekHigh"))
    
    def get_quote_frame(self, start=None, end=None, period=None, interval=None) -> pd.DataFrame:
        '''
        Returns data frame of general quantitative quote attributes for selected dates and interval.

        :param start: Date range start
        :param end: Date range end
        :param period: If start, end are left as None, use period ('1d', '1w' '1mo', '3mo', '6mo', '1y', '2y')
        :param interval: Time interval between quotes ('1m', '1d')

        **Examples**

        >>> quoting = Quote(ticker='aapl')
        >>> quoting.get_quote_frame(start=None, end=None, period='6mo', interval=None)
                                         Open        High         Low       Close    Volume  Dividends  Stock Splits
        Date
        2024-12-30 00:00:00-05:00  251.623020  252.889969  250.146586  251.593094  35557500        0.0           0.0
        2024-12-31 00:00:00-05:00  251.832526  252.670501  248.829760  249.817383  39480700        0.0           0.0
        2025-01-02 00:00:00-05:00  248.330961  248.500565  241.238085  243.263199  55740700        0.0           0.0
        2025-01-03 00:00:00-05:00  242.774368  243.592387  241.307905  242.774368  40244100        0.0           0.0
        2025-01-06 00:00:00-05:00  243.722074  246.734810  242.614744  244.410416  45045600        0.0           0.0
        ...                               ...         ...         ...         ...       ...        ...           ...
        2025-06-23 00:00:00-04:00  201.630005  202.300003  198.960007  201.500000  55814300        0.0           0.0
        2025-06-24 00:00:00-04:00  202.589996  203.440002  200.199997  200.300003  54064000        0.0           0.0
        2025-06-25 00:00:00-04:00  201.449997  203.669998  200.619995  201.559998  39525700        0.0           0.0
        2025-06-26 00:00:00-04:00  201.429993  202.639999  199.460007  201.000000  50799100        0.0           0.0
        2025-06-27 00:00:00-04:00  201.889999  203.220001  200.000000  201.080002  73114100        0.0           0.0

        [123 rows x 7 columns]

        >>> quoting.get_quote_frame(start='2025-01-01', end='2025-06-10')
                                         Open        High         Low       Close    Volume  Dividends  Stock Splits
        Date
        2025-01-02 00:00:00-05:00  248.330961  248.500565  241.238085  243.263199  55740700        0.0           0.0
        2025-01-03 00:00:00-05:00  242.774368  243.592387  241.307905  242.774368  40244100        0.0           0.0
        2025-01-06 00:00:00-05:00  243.722074  246.734810  242.614744  244.410416  45045600        0.0           0.0
        2025-01-07 00:00:00-05:00  242.395272  244.959095  240.769205  241.627136  40856000        0.0           0.0
        2025-01-08 00:00:00-05:00  241.337830  243.123531  239.472335  242.115952  37628900        0.0           0.0
        ...                               ...         ...         ...         ...       ...        ...           ...
        2025-06-03 00:00:00-04:00  201.350006  203.770004  200.960007  203.270004  46381600        0.0           0.0
        2025-06-04 00:00:00-04:00  202.910004  206.240005  202.100006  202.820007  43604000        0.0           0.0
        2025-06-05 00:00:00-04:00  203.500000  204.750000  200.149994  200.630005  55126100        0.0           0.0
        2025-06-06 00:00:00-04:00  203.000000  205.699997  202.050003  203.919998  46607700        0.0           0.0
        2025-06-09 00:00:00-04:00  204.389999  206.000000  200.020004  201.449997  72862600        0.0           0.0

        [108 rows x 7 columns]

        '''
        # using start, end dates as date range
        if (start!=None and end!=None and period==None and interval!=None):
            return pd.DataFrame(self.load.history(start=start, end=end, interval=interval))
        
        # using start, end dates without interval
        if (start!=None and end!=None and period==None and interval==None):
            return pd.DataFrame(self.load.history(start=start, end=end))
        
        # using period as date range with interval
        if (start==None and end==None and period!=None and interval!=None):
            return pd.DataFrame(self.load.history(period=period, interval=interval))
        
        # using period as date range without interval
        if (start==None and end==None and period!=None and interval==None):
            return pd.DataFrame(self.load.history(period=period))
        
        else:
            return ValueError(
                "Parameters are entered incorrectly. Here is a list of time range options:\n" \
                "1. start, end\n" \
                "2. start, end, interval\n" \
                "3. period\n" \
                "4. period, interval"
                )