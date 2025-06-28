# Module for market indicator formulas
import math
import numpy as np
import pandas as pd

from datetime import datetime
from typing import Union, List, Any
from cogi_quant.objects import pairedset
from cogi_quant.processing import series

def simple_moving_average(data: Union[pd.Series, pairedset.PairedSet], window: int) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns simple moving average based on specified window period as type pd.Series if data was type pd.Series, and PairedSet if data was type PairedSet.

    :param data: Series or PairedSet data.
    :param window: Period cycle for moving average. Defines how many observations to aggregate (average) at each step.

    **Usage**
    
    Getting a moving average for a stock prices series for plotting.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> simple_moving_average(data=data, window=3)
    Date
    2025-05-28 00:00:00-04:00           NaN
    2025-05-29 00:00:00-04:00           NaN
    2025-05-30 00:00:00-04:00    200.406667
    2025-06-02 00:00:00-04:00    200.833333
    2025-06-03 00:00:00-04:00    201.940002
    2025-06-04 00:00:00-04:00    202.596670
    2025-06-05 00:00:00-04:00    202.240005
    ...
    2025-06-26 00:00:00-04:00    200.953334
    2025-06-27 00:00:00-04:00    201.213333
    Name: Close, dtype: float64
    '''
    # work with series to use pd functions
    if isinstance(data, pd.Series):
        struc = series.fill(series=data, filling_type='ffill')
        return struc.rolling(window).mean()
    if  isinstance(data, pairedset.PairedSet):
        data.npfloat_values()
        struc = data.to_series()
        return series.series_to_pairedset(struc.rolling(window).mean())

def ema(data: Union[pd.Series, pairedset.PairedSet], lookback: int = 12, adjust: bool = False) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns exponential moving average of a price series or PairedSet.

    :param data: Price data in from of Series or PairedSet.
    :param lookback: Look-back period span. 
    :param adjust: Adjustable pass through for Pandas

    **Usage**

    Plotting exponential moving average against a stock's open prices as a time series plot.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> ema(data=data)
    Date
    2025-05-28 00:00:00-04:00    200.419998
    2025-05-29 00:00:00-04:00    200.347690
    2025-05-30 00:00:00-04:00    200.424970
    2025-06-02 00:00:00-04:00    200.621128
    2025-06-03 00:00:00-04:00    201.028647
    2025-06-04 00:00:00-04:00    201.304241
    2025-06-05 00:00:00-04:00    201.200512
    ...
    2025-06-25 00:00:00-04:00    199.974783
    2025-06-26 00:00:00-04:00    200.132509
    2025-06-27 00:00:00-04:00    200.278277
    Name: Close, dtype: float64
    '''
    if isinstance(data, pairedset.PairedSet):
        as_series = data.to_series()
        return series.series_to_pairedset(as_series.ewm(span=lookback, adjust=adjust).mean())
    return data.ewm(span=lookback, adjust=adjust).mean()

def rsi(data: Union[pd.Series, pairedset.PairedSet], period: int = 14) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns relative strength index over a given period. Returns same type as type of paramater data entered.

    :param data: Series or PairedSet data.
    :param period: Look-back window for rsi

    **Usage**

    Plotting an RSI against a stock's price as a time series. 

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> rsi(data=data, period=7) # period normally set at 14
    Date
    2025-05-28 00:00:00-04:00          NaN
    2025-05-29 00:00:00-04:00     0.000000
    2025-05-30 00:00:00-04:00    24.193687
    2025-06-02 00:00:00-04:00    40.148486
    2025-06-03 00:00:00-04:00    58.823756
    2025-06-04 00:00:00-04:00    53.266034
    2025-06-05 00:00:00-04:00    34.668345
    ...
    2025-06-25 00:00:00-04:00    56.876480
    2025-06-26 00:00:00-04:00    53.967379
    2025-06-27 00:00:00-04:00    54.356483
    Name: Close, dtype: float64
    '''
    copy = data
    if isinstance(data, pairedset.PairedSet):
        copy = data.to_series()
    
    gain = copy.diff().clip(lower=0)
    loss = -(copy.diff().clip(upper=0))

    # use Wilder's smoothed moving averages
    alpha = 1/period 
    avg_gain = gain.ewm(alpha=alpha, adjust=False).mean()
    avg_loss = loss.ewm(alpha=alpha, adjust=False).mean()
    rsi = 100 - (100/(1+(avg_gain/avg_loss)))

    if isinstance(data, pairedset.PairedSet):
        return series.series_to_pairedset(rsi)
    return rsi 

def macd_all_info(data: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_span: int = 9) -> pd.DataFrame:
    '''
    General moving average convergence divergence information scope. Returns dataframe containing columns for:
        "macd": fast EMA - slow EMA
        "signal": EMA(MACD)
        "hist": macd - signal

    :param data: quantitative series data.
    :param fast_period: period span for shorter EMA.
    :param slow_period: period span for longer EMA.
    :param signal_span: period span for the signal line.

    **Usage** 

    Pulling all required moving average con/div data, or returing individual columns as a series for time series plotting.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> macd_all_info(data=data)
                                macd    signal      hist
    Date
    2025-05-28 00:00:00-04:00  0.000000  0.000000  0.000000
    2025-05-29 00:00:00-04:00 -0.037493 -0.007499 -0.029994
    2025-05-30 00:00:00-04:00  0.005355 -0.004928  0.010283
    2025-06-02 00:00:00-04:00  0.106670  0.017392  0.089278
    2025-06-03 00:00:00-04:00  0.310075  0.075928  0.234147
    2025-06-04 00:00:00-04:00  0.430007  0.146744  0.283263
    2025-06-05 00:00:00-04:00  0.344369  0.186269  0.158100
    ...
    2025-06-25 00:00:00-04:00 -0.172773 -0.325501  0.152728
    2025-06-26 00:00:00-04:00 -0.078191 -0.276039  0.197848
    2025-06-27 00:00:00-04:00  0.003184 -0.220194  0.223379
    '''
    macd_line = (data.ewm(span=fast_period, adjust=False).mean()) - (data.ewm(span=slow_period, adjust=False).mean())
    signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()
    hist = macd_line - signal_line

    return pd.DataFrame(
        {"macd": macd_line, 
         "signal": signal_line, 
         "hist": hist},
        index=data.index
    )

def macd(data: Union[pd.Series, pairedset.PairedSet], fast_period: int = 12, slow_period: int = 26) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns the moving average convergence divergence as a Series or PairedSet depending on data input type.

    :param data: series or paired set price/returns data.
    :param fast_period: period for short-span EMA.
    :param slow_period: period for long-span EMA.
    
    **Usage**

    Pulling moving average con/div values to plot macd line against stock prices or returns.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> macd(data=data)  
    Date
    2025-05-28 00:00:00-04:00  0.000000
    2025-05-29 00:00:00-04:00 -0.037493
    2025-05-30 00:00:00-04:00  0.005355
    2025-06-02 00:00:00-04:00  0.106670
    2025-06-03 00:00:00-04:00  0.310075
    2025-06-04 00:00:00-04:00  0.430007
    2025-06-05 00:00:00-04:00  0.344369
    ...
    2025-06-25 00:00:00-04:00 -0.172773
    2025-06-26 00:00:00-04:00 -0.078191
    2025-06-27 00:00:00-04:00  0.003184
    Name: macd, dtype: float64
    '''
    if isinstance(data, pairedset.PairedSet):
        try:
            as_series = data.to_series()
            macd_info_frame = macd_all_info(data=as_series, fast_period=fast_period, slow_period=slow_period)
            return series.series_to_pairedset(macd_info_frame["macd"])
        except:
            raise Exception("Paired Set object is invalid.")
    
    return macd_all_info(data, fast_period=fast_period, slow_period=slow_period)["macd"]

def macd_signal(data: Union[pd.Series, pairedset.PairedSet], fast_period: int = 12, slow_period: int = 26, signal_span: int = 9) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns the moving average convergence divergence signal as a Series or PairedSet depending on data input type.

    :param data: series or paired set price/returns data.
    :param fast_period: period for short-span EMA.
    :param slow_period: period for long-span EMA.
    :param signal_span: period for signal line.
    
    **Usage**

    Pulling moving average con/div signal to plot against stock prices or returns.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> macd_signal(data=data)
    Date
    2025-05-28 00:00:00-04:00  0.000000
    2025-05-29 00:00:00-04:00 -0.007499
    2025-05-30 00:00:00-04:00 -0.004928
    2025-06-02 00:00:00-04:00  0.017392
    2025-06-03 00:00:00-04:00  0.075928
    2025-06-04 00:00:00-04:00  0.146744
    2025-06-05 00:00:00-04:00  0.186269
    ...
    2025-06-25 00:00:00-04:00 -0.325501
    2025-06-26 00:00:00-04:00 -0.276039
    2025-06-27 00:00:00-04:00 -0.220194
    Name: signal, dtype: float64
    '''
    if isinstance(data, pairedset.PairedSet):
        try:
            as_series = data.to_series()
            macd_info_frame = macd_all_info(data=as_series, fast_period=fast_period, slow_period=slow_period, signal_span=signal_span)
            return series.series_to_pairedset(macd_info_frame["signal"])
        except:
            raise Exception("Paired Set object is invalid.")
    
    return macd_all_info(data, fast_period=fast_period, slow_period=slow_period)["signal"]

def macd_hist(data: Union[pd.Series, pairedset.PairedSet], fast_period: int = 12, slow_period: int = 26, signal_span: int = 9) -> Union[pd.Series, pairedset.PairedSet]:
    '''
    Returns macd minus signal as a Series or PairedSet depending on data input type.

    :param data: series or paired set price/returns data.
    :param fast_period: period for short-span EMA.
    :param slow_period: period for long-span EMA.
    :param signal_span: period for signal line.
    
    **Usage**

    Pulling macd, signal difference series to plot against stock prices or returns.

    **Examples**

    >>> from cogi_quant.processing import price_history
    >>> from cogi_quant.instrument import stock
    >>> aapl = stock.Stock(ticker="aapl")
    >>> data = price_history.get_price_close_series(aapl, period='1mo')
    >>> macd_hist(data=data)
    Date
    2025-05-28 00:00:00-04:00    0.000000
    2025-05-29 00:00:00-04:00   -0.029994
    2025-05-30 00:00:00-04:00    0.010283
    2025-06-02 00:00:00-04:00    0.089278
    2025-06-03 00:00:00-04:00    0.234147
    2025-06-04 00:00:00-04:00    0.283263
    2025-06-05 00:00:00-04:00    0.158100
    ...
    2025-06-25 00:00:00-04:00    0.152728
    2025-06-26 00:00:00-04:00    0.197848
    2025-06-27 00:00:00-04:00    0.223379
    Name: hist, dtype: float64
    '''
    if isinstance(data, pairedset.PairedSet):
        try:
            as_series = data.to_series()
            macd_info_frame = macd_all_info(data=as_series, 
                                            fast_period=fast_period, 
                                            slow_period=slow_period, 
                                            signal_span=signal_span)
            return series.series_to_pairedset(macd_info_frame["hist"])
        except:
            raise Exception("Paired Set object is invalid.")
    
    return macd_all_info(data, fast_period=fast_period, slow_period=slow_period)["hist"]
