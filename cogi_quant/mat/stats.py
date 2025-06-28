# Helper module for basic sample stats formulas
# Sample data assumed to be np.array
from typing import Union, List

import math
import scipy.stats as scipy
import numpy as np
import pandas as pd

def average(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample mean of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    if len(sample)==0:
        raise Exception("Empty data set.")
    return np.float64(sum(sample)/len(sample))

def variance(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample variance of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    size = len(sample)
    if size==0: raise Exception("Empty data set.")

    sum = 0
    mean = average(sample)
    for value in sample:
        sum += (value - mean)**2
    # return np.float64(np.var(sample))
    return np.float64(sum/(size-1))

def standard_deviation(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample standard deviation of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    # return np.float64(np.std(sample))
    return np.float64(math.sqrt(variance(sample)))

def sup(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample max of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    return np.float64(max(sample))

def inf(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample min of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    return np.float64(min(sample))

def sample_range(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample range of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    return np.float64(sup(sample) - inf(sample))

def frequent(sample: Union[List, np.array, pd.Series]) -> np.float64:
    '''
    Returns sample mode (most frequent value) of a non empty data set.

    :param sample: Non empty array or series of reals
    '''
    return scipy.mode(sample).mode

