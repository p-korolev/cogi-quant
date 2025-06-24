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
    Returns simple moving average based on specified window period as a 
    '''
    # work with series to use pd functions
    if isinstance(data, pd.Series):
        struc = series.fill(series=data, filling_type='ffill')
        return struc.rolling(window).mean()
    if  isinstance(data, pairedset.PairedSet):
        data.npfloat_values()
        struc = data.to_series()
        return series.series_to_pairedset(struc.rolling(window).mean())



