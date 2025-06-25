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
    '''
    if isinstance(data, pairedset.PairedSet):
        try:
            as_series = data.to_series()
            macd_info_frame = macd_all_info(data=as_series, fast_period=fast_period, slow_period=slow_period, signal_span=signal_span)
            return series.series_to_pairedset(macd_info_frame["hist"])
        except:
            raise Exception("Paired Set object is invalid.")
    
    return macd_all_info(data, fast_period=fast_period, slow_period=slow_period)["signal"]
