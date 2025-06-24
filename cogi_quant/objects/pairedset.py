from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Union, Optional, Any

class PairedSet():
    def __init__(self, indexing_array: Any = None, value_array: Any = None):
        # handle array length issues
        if len(indexing_array)!=len(value_array):
            raise Exception("Arrays differ in length.")
        # populate primary properties
        self.X = np.array(indexing_array)
        self.Y = np.array(value_array)

    @property
    def combined(self) -> np.ndarray:
        return np.array([self.X, self.Y])
    
    def __repr__(self) -> np.ndarray:
        return self.combined
    
    def __str__(self) -> str:
        return str(self.combined)

    def get_array_X(self) -> np.ndarray:
        '''
        Return indexing array of the combined pair array. 

        Returns self.X
        '''
        return self.X
    
    def get_array_Y(self) -> np.ndarray:
        '''
        Return value array of the combined pair array. 

        Returns self.Y
        '''
        return self.Y
    
    def get_pair_at_index(self, index: int) -> np.ndarray:
        '''
        Returns 1D array [indexing_array[index], value_array[index]]

        :param index: index of value from either X or Y.

        **Usage**

        >>> set_pair = PairedSet(indexing_array=[1,2,3], value_array=[2,4,6])
        >>> set_pair.get_pair_at_index(1)
        [2 4]
        '''
        try:
            return np.array([self.X[index], self.Y[index]])
        except:
            Exception("Index out of range.")

    def append_paired_set(self, other: PairedSet) -> None:
        '''
        Appends another PairedSet to the PairedSet object. other.X appends to self.X and other.Y appends to self.Y

        If self.    

        **Examples**

        >>> pair1 = PairedSet(indexing_array=[1,2], value_array=[5,10])
        >>> pair2 = PairedSet(indexing_array=[3,4], value_array=[15,20])
        >>> pair1.append_paired_set(pair2)
        >>> pair1
        [[1,2,3,4] [5,10,15,20]]
        '''
        self.X = np.append(self.X, other.X)
        self.Y = np.append(self.Y, other.Y)

    def append_single_pair(self, *args: Union[PairedSet, Any, Any]) -> None:
        '''
        Append a single (x,y) pair to the PairedSet object. Size of X and Y arrays increases by one element.
        
        X -> X.append(x), Y -> Y.append(y)

        :param args: Either a 1x1 PairedSet object or two values.

        **Examples**

        >>> P = PairedSet([1,2], [5,6])
        >>> to_append = PairedSet([3], [7])
        >>> P.append_single_pair(to_append)
        >>> print(P)
        [[1,2,3]
         [5,6,7]]
        
        >>> P.append_single_pair(4,8)
        >>> print(P)
        [[1,2,3,4]
         [5,6,7,8]]
        '''
        # PairedSet was given
        if len(args)==1 and isinstance(args[0], PairedSet):
            self.append_paired_set(args[0])

        # Two values (x, y) were given
        if len(args)==2 and (not isinstance(arg, PairedSet) for arg in args):
            self.append_paired_set(PairedSet([args[0]], args[1]))
        else:
            raise TypeError("Expected PairedSet or two values.")
        
    def get_corresponding_Yvalue(self, X_value: np.float64) -> np.float64:
        '''
        Returns corresponding Y value to first appearing X_value.

        **Usage**
        If a paired set contains dates as indexing_list X, and instrument price as value_list Y, get the instrument price of date X_value = '2025-12-05'.

        **Examples**

        >>> P = PairedSet(indexing_array=['2025-12-03', '2025-11-03', '2025-10-03'], value_array=[110.33, 108.61, 101.99])
        >>> P.get_corresponding_Yvalue(X_value='2025-11-03')
        108.61
        '''
        exists = False
        if self.X==None or self.Y==None: 
            return None
        for index_value in self.X:
            if index_value == X_value:
                pass
    
    def to_series(self, indexing_name: Optional[str] = None) -> pd.Series:
        '''
        Returns PairedSet object as a pd.Series object, where self.X becomes the series index.

        **Usage**
        Easing conversion process of PairedSet data structures and printing views.

        **Examples**

        >>> P = PairedSet(['2025-12-01', '2025-12-02', '2025-12-03', '2025-12-04'], [100.0, 101.0, 102.0, 103.0])
        >>> print(P.to_series(indexing_name='Date'))
        Date
        2025-12-01    100.0
        2025-12-02    101.0
        2025-12-03    102.0
        2025-12-04    103.0
        '''
        idx = pd.Index(self.X, name=indexing_name)
        return pd.Series(self.Y, index=idx)
    
    def npfloat_values(self) -> None:
        '''
        Converts all values in the value array to npfloat64.

        **Usage**

        Cleaning dtype of time series data.
        '''
        self.Y = self.Y.astype(np.float64, copy=False)

                