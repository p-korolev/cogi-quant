# Helper module for basic sample stats formulas
# Sample data assumed to be np.array

import math
import scipy.stats as S
import numpy as np

def average(sample: np.array) -> np.float64:
    '''
    Returns sample mean of a non empty data set.

    :param sample: Non empty array of reals
    '''
    if len(sample)==0:
        raise Exception("Empty data set.")
    return np.float64(sum(sample)/len(sample))

def variance(sample: np.array) -> np.float64:
    size = len(sample)
    if size==0: raise Exception("Empty data set.")

    sum = 0
    mean = average(sample)
    for value in sample:
        sum += (value - mean)**2
    
    # return np.float64(np.var(sample))
    return np.float64(sum/(size-1))

def standard_deviation(sample: np.array) -> np.float64:
    # return np.float64(np.std(sample))
    return np.float64(math.sqrt(variance(sample)))

def sup(sample: np.array) -> np.float64:
    return np.float64(max(sample))

def inf(sample: np.array) -> np.float64:
    return np.float64(min(sample))

def sample_range(sample: np.array) -> np.float64:
    return np.float64(sup(sample) - inf(sample))


