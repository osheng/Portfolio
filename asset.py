import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from constants import *
import datetime
"""
Note: I'm using the word value rather than price because I could imagine
importing an index as an asset as well.
"""
class Asset:
    """An asset object"""

    def __init__(self, name: str, history = None, history_fn = None, denomination = None):

        # check, clean, and set history
        history = history if history_fn is None else pd.read_csv(history_fn)
        assert history is not None, "asset history is None"
        assert DATE in history.columns, "history has no Date column"
        assert history[DATE].is_unique, "duplicate dates in history!"
        assert ACLO in history.columns, "history has no Value column"

        # Convert date data type
        history[DATE] = history[DATE].apply(pd.to_datetime)
        # Later on, perhaps creating Assets with null values would give warnings
        assert history[DATE].isna().any() == False

        self.history = history[[DATE, ACLO]].set_index(DATE).dropna().sort_index()

        # Create daily rate of return
        self.history[DAILY] = 0.0
        vcn = self.history.columns.get_loc(ACLO) #value's column number
        dcn = self.history.columns.get_loc(DAILY) #DAILY's column number

        for i in np.arange(1,len(self.history.index)):
            self.history.iat[i, dcn] = (self.history.iloc[i, vcn] / self.history.iloc[i-1, vcn]) - 1


        #Set other attributes
        self.name = name
        self.denomination = None
        self.start_date = min(self.history.index)
        self.start_value = self.history.loc[self.start_date,ACLO]
        self.end_date = max(self.history.index)
        self.end_value = self.history.loc[self.end_date,ACLO]
        self.mean_daily = self.history[DAILY].mean()
        self.median_daily = self.history[DAILY].median()
        # self.history["Change"] = history[ACLO] / self.start_value # This line is problematic and I'd like to understand why

    def get_value(self, d: datetime) -> float:
        # Note: here I want to test how to input a date
        return self.history.loc[d, ACLO]

    def get_extremes(self, kind="best", n=10) -> Series:
        """
        Return a series of the n most 'kind' changes.
        """
        data = self.history.sort_values(by="DAILY", axis=0, kind='mergesort')
        if kind == "best":
            return data[DAILY].tail(n)
        return data[DAILY].head(n)

    def get_ror(self, from=None, to=None)->float:
        
