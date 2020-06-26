import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from constants import
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

        # Convert price data type
        history[ACLO] = history[ACLO].map(lambda x: True if type(x) == float else False, na_action='ignore')
        # Confirm no null values
        assert 0 == history[ACLO].isnull().sum()

        # Convert date data type
        history[DATE] = history[DATE].apply(pd.to_datetime)
        self.history = history[[DATE, ACLO]]
        self.history.set_index(DATE)
        self.history.sort_values(by="index", axis=0, inplace=True, kind='mergesort')

        # Create daily rate of return
        self.history[DAILY] = 1
        vcn = self.history.columns.get_loc(ACLO) #value's column number
        dcn = self.history.columns.get_loc(DAILY) #DAILY's column number
        for i np.arange(1,len(self.history.index)-1):
            self.history[DAILY].iat[i, dcn] = self.history.iloc[i, ACLO] / self.history.iloc[i-1, ACLO]


        #Set other attributes
        self.name = name
        self.denomination = None
        self.start_date = min(history[DATE])
        self.start_value = history[history[DATE] == self.start_date][ACLO][0]
        self.end_date = max(history[DATE])
        self.end_value = history[history[DATE] == self.end_date][ACLO][0]
        # I'm including both of these for the moment to remind myself of the syntax.
        assert self.end_value == self.history.loc[self.end_date, ACLO]

        self.mean_daily = self.history[DAILY].mean
        self.median_daily = self.history[DAILY].median

        self.history["Change"] = history[ACLO] / self.start_value

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
