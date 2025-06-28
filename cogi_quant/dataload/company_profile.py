from __future__ import annotations
from datetime import datetime

import yfinance as fin
import numpy as np
import pandas as pd

class CompanyProfile():
    def __init__(self, ticker: str):
        self.ticker_name = ticker
        self.load = fin.Ticker(ticker) 
    
    def get_company(self) -> str:
        return self.load.info.get("longName")

    def get_company_industry(self, display_industry_key=False) -> str:
        '''
        Returns the industry which the company is in.

        :param display_industry_key: Use 'industryKey' attribute instead of general 'sector' from stock.load.info
        '''
        
        if (display_industry_key):
            return self.load.info.get("industryKey")
        return self.load.info.get("industry")
    
    def same_industry(self, other: CompanyProfile) -> bool:
        return self.get_company_industry==other.get_company_industry()

    def get_company_sector(self, display_sector_key=False) -> str:
        '''
        Returns industry sector of company. 

        :param display_sector_key: Use 'sectorKey' attribute instead of general 'sector' from stock.load.info    
        '''

        if (display_sector_key):
            return self.load.get("sectorKey")
        return self.load.info.get("sector")
    
    def eq_sector(self, other: CompanyProfile) -> bool:
        return self.get_company_sector()==other.get_company_sector()
    
    def view_sector(self, viewlen: int = 5) -> bool:
        '''
        Returns a list of companies in the same sector
        '''
        pass

    def get_chair(self) -> pd.DataFrame:
        '''
        Returns top four company officers with Name, Age, Title, and Pay info.

        **Usage**

        >>> stock.get_chair()
                               name  age                                       title    totalPay
        0      Mr. Timothy D. Cook   63                              CEO & Director  16520856.0
        1  Mr. Jeffrey E. Williams   60                     Chief Operating Officer   5020737.0
        2   Ms. Katherine L. Adams   60      Senior VP, General Counsel & Secretary   5022182.0
        3     Ms. Deirdre  O'Brien   57  Chief People Officer & Senior VP of Retail   5022182.0
        '''
        
        chair_raw = self.load.info.get("companyOfficers")
        df = pd.DataFrame(chair_raw).head(4)

        # type handling
        df['age'] = df['age'].astype(np.int64)
        df['totalPay'] = df['totalPay'].astype(np.float64)

        return df[['name', 'age', 'title', 'totalPay']]
    
    def get_company_number_employees(self) -> np.int64:
        return np.int64(self.load.info.get("employees"))
    
    def summary(self) -> str:
        return self.load.info.get("longBusinessSummary")

