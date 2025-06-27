import yfinance as fin
import numpy as np
import pandas as pd
from datetime import datetime

import cogi_quant.dataload.company_profile as profile

class Stock(profile.CompanyProfile):
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.load = fin.Ticker(ticker)
    
    def get_current_price(self) -> np.float64:
        '''
        Returns last updated price of the stock.   

        **Examples**

        >>> Stock("AAPL").get_current_price()
        >>> 198.91 
        '''
        return np.float64(self.load.info.get("currentPrice"))

    def overall_risk(self) -> np.float64:
        return np.float64(self.load.info.get("overallRisk"))
    
    def get_previous_close(self) -> np.float64:
        '''
        Returns previous day close price.

        **Examples**

        >>> Stock("AAPL").get_previous_close()
        >>> 198.71
        '''
        return np.float64(self.load.info.get("previousClose"))
    
    def get_current_day_open(self) -> np.float64:
        '''
        Returns current day open price.

        **Examples**

        >>> Stock("AAPL").get_current_day_open()
        >>> 198.77
        '''
        return np.float64(self.load.info.get("open"))
    
    def get_current_day_low(self) -> np.float64:
        '''
        Returns current day low price.

        **Examples**

        >>> Stock("AAPL").get_current_day_low()
        >>> 197.90
        '''
        return np.float64(self.load.info.get("dayLow"))
    
    def get_current_day_high(self) -> np.float64:
        '''
        Returns current day high price.

        **Examples**

        >>> Stock("AAPL").get_current_day_high()
        >>> 199.52
        '''
        return np.float64(self.load.info.get("dayHigh"))
    
    def get_beta(self) -> np.float64:
        '''
        Returns current beta value for stock.

        **Examples**
        
        >>> Stock("AAPL").get_beta()
        >>> 1.2
        '''
        return np.float64(self.load.info.get("beta"))
    
    def get_PE_trailing(self) -> np.float64:
        '''
        Returns current trailing P/E value for stock.

        **Examples**
        
        >>> Stock("AAPL").get_PE_trailing()
        >>> 30.70
        '''
        return np.float64(self.load.info.get("trailingPE"))
    
    def get_PE_forward(self) -> np.float64:
        '''
        Returns current forward P/E value for stock.

        **Examples**
        
        >>> Stock("AAPL").get_PE_forward()
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

        >>> stock.get_quote_frame(start=None, end=None, period='6mo', interval=None)
        >>> stock.get_quote_frame(start='2025-01-01', end='2025-06-10')
        '''
        # using start, end dates as date range
        if (start!=None and end!=None and period==None):
            return pd.DataFrame(self.load.history(start=start, end=end, interval=interval))
        
        # using period as date range with interval
        if (start==None and end==None and period!=None and interval!=None):
            return pd.DataFrame(self.load.history(period=period, interval=interval))
        
        # using period as date range without interval
        if (start==None and end==None and period!=None and interval==None):
            return pd.DataFrame(self.load.history(period=period))
        
        return "Must parameterize quote data date range."

