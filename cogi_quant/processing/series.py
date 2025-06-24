# Module for series handling and cleaning

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Union, Any 

from cogi_quant.objects import pairedset

def get_series_values(series: pd.Series) -> np.ndarray:
    '''
    Returns numpy array of series values.
    '''
    return series.to_numpy()

def get_series_index(series: pd.Series) -> np.ndarray:
    '''
    Returns numpy array of series date indexing values.
    '''
    return series.index.to_numpy()

def fill(series: pd.Series, filling_type: str = 'ffill') -> pd.Series:
    '''
    Return a series with all values filled using the following filling rules:
        1. If filling_type is ffill, fill NaN value using previous cell value. If first item is NaN, fill it using series mean.
        2. If filling_type is bfill, fill NaN value using next cell value. If last item is NaN, fill it using series mean.
    
    **Usage**
    
    Cleaning large series without harming series mean or variance.

    **Examples**

    >>> from price_fetching import get_price_open_series
    >>> stock = dataload.micinfo.Stock('AAPL')
    >>> s = get_price_open_series(stock, period='3mo')
    >>> front_filled = fill(s)
    >>> back_filled = fill(s, filling_type='bfill)
    '''
    series_copy = series.copy()
    mean_series = series.mean(skipna=True)
    # back-filling option selected
    if filling_type=='bfill':
        if pd.isna(series_copy.iloc[-1]):
            series_copy.ilioc[-1] = mean_series
            return series_copy.bfill()   
    # front fill, use series mean if first value NaN
    if pd.isna(series_copy.iloc[0]):
        series_copy.iloc[0] = mean_series
    return series_copy.ffill()


from typing import Optional
def normalize_series(series: pd.Series, normalization_method: Optional[str]) -> pd.Series:
    '''
    Return normalized series where values range from [0,1] inclusive using minmax method. If 'z' is specified as normalization_method, use z-score method.

    :param series: Pandas series
    :param normalization_method: Optional parameter. Indicate 'z' to use z-score normalization as the normalization method. 

    **Usage**

    Normalizing a series before using for ML models.

    **Examples**

    >>> test_series = pd.Series([98.0, 100.33, 101, 105.4, 110.12, 109.2], index=pd.date_range("2024-01-01", periods=6, freq="D"))
    >>> print(test_series)
    2024-01-01     98.00
    2024-01-02    100.33
    2024-01-03    101.00
    2024-01-04    105.40
    2024-01-05    110.12
    2024-01-06    109.20

    >>> print(normalize_series(test_series))
    2024-01-01    0.000000
    2024-01-02    0.192244
    2024-01-03    0.247525
    2024-01-04    0.610561
    2024-01-05    1.000000
    2024-01-06    0.924092

    >>> print(normalize_series(test_series, normalization_method='z'))
    2024-01-01   -1.202038
    2024-01-02   -0.735894
    2024-01-03   -0.601852
    2024-01-04    0.278419
    2024-01-05    1.222711
    2024-01-06    1.038654
    '''
    if series.empty: 
        return None 
    if normalization_method=='z':
        try:
            return (series - series.mean())/series.std()
        except: 
            raise ValueError("Try filling series")
    if normalization_method==None or (normalization_method in ['minmax', 'mm', 'm']):
        try:
            return (series-series.min())/(series.max()-series.min())
        except: 
            raise ValueError("Try filling series.")
    else:
        raise ValueError("Use an appropriate normalization method.")


def series_to_pairedset(series: pd.Series) -> pairedset.PairedSet:
    '''
    Returns paired set structure of a given series. paired_set.X holds the series index, paired_set.Y holds the series values.
    
    **Usage**

    Prepare a pandas series for graphing, splitting the index and value into X, Y pairs within a paired set object.

    **Examples**

    >>> stock = dataload.micinfo..Stock("AAPL")
    >>> open_price_series = get_price_open_series(stock=stock, period='1mo')
    >>> open_price_pairedset = series_to_pairedset(open_price_series)
    >>> open_price_pairedset.X
    [Timestamp('2025-05-23 00:00:00-0400', tz='America/New_York')
     Timestamp('2025-05-27 00:00:00-0400', tz='America/New_York')
     ...
     Timestamp('2025-06-23 00:00:00-0400', tz='America/New_York')]

    >>> open_price_pairedset.Y
    [193.66999817 
     198.30000305 
     ... 
     201.53199768]

    >>> type(open_price_pairedset.Y[0])
    np.float64
    '''
    # error handling
    if series.empty:
        raise IndexError("Empty Series.")
    if (len(get_series_index(series=series))!=len(get_series_values(series=series))):
        raise Exception("Index-Value match error.")
    
    # final paired set
    return pairedset.PairedSet(indexing_array=get_series_index(series), value_array=get_series_values(series))
