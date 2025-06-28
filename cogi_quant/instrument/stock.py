import pandas as pd
import numpy as np
import yfinance as yf 

from cogi_quant.dataload import quoting
from cogi_quant.dataload import company_profile
from cogi_quant.dataload import snp
from typing import Union, Optional, List

class Stock():
    def __init__(self, ticker: Optional[str] = None, company_name: Optional[str] = None) -> None:
        '''
        Initialize stock object. Enter etiher the company's publically traded stock ticker symbol, or name of company.
        '''
        # parameter checks
        if (ticker!=None and company_name!=None):
            raise ValueError(
                "Expected either ticker parameter or company_name parameter to be provided, not both."
                )
        if (ticker==None and company_name==None):
            raise ValueError(
                "Either ticker or company_name must be provided."
            )
        # initialize ticker and enable quoting
        if ticker!=None:
            try:
                self.ticker = ticker
                self.q = quoting.Quote(ticker)
            except:
                raise ValueError("Ticker is invalid or does not exist.")
        if company_name!=None:
            try:
                tick = search_ticker(company_name=company_name)
            except:
                raise ValueError("Company does not have a publically traded ticker or input is invalid.")
            self.ticker = tick
            self.q = quoting.Quote(self.ticker)
        self.profile = company_profile.CompanyProfile(self.ticker)

    def __repr__(self):
        return self.ticker, self.q.get_current_price()

    def get_company_summary(self) -> str:
        return self.profile.summary()


# helper queries
# search endpoint for ticker given company name
import requests
def search_ticker(company_name: Union[List, str]) -> Union[List, str]:
    '''
    Return ticker symbol(s) of inputted company name(s).

    :param company_name: Name of public company.

    **Usage**

    Miscellaneous stock symbol matching and searching.

    **Examples**
    
    >>> search_ticker("Apple Inc.")
    "AAPL"

    >>> search_ticker("Apple")
    "AAPL"

    >> search_ticker(["Apple", "Tesla"])
    ["AAPL", "TSLA"]
    '''
    
    if isinstance(company_name, List):
        result = []
        for company in company_name:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company}"
            response = requests.get(url).json()
            for result in response.get("quotes", []):
                if result.get("quoteType")=="EQUITY":
                    result.append(result.get("symbol"))
            result.append("")
    if isinstance(company_name, str):
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
        response = requests.get(url).json()
        for result in response.get("quotes", []):
            if result.get("quoteType")=="EQUITY":
                return result.get("symbol")
        return None 
    else: 
        raise TypeError("Expected company_name to be a list or individual string")

    
