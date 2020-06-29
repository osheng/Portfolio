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

    def __init__(self, name: str, history=None, history_fn=None, denomination=None):

        # check, clean, and set history
        history = history if history_fn is None else pd.read_csv(history_fn)
        assert history is not None, "asset history is None"
        assert DATE in history.columns, "history has no Date column"
        assert history[DATE].is_unique, "duplicate dates in history!"
        assert ACLO in history.columns, "history has no " + ACLO + " column"

        # Convert date data type
        history[DATE] = history[DATE].apply(pd.to_datetime)
        # Later on, perhaps creating Assets with null values would give warnings
        assert history[DATE].isna().any() == False

        self.history = history[[DATE, ACLO]].set_index(DATE).dropna().sort_index()

        # Create daily rate of return
        self.history[DAILY] = 0.0
        vcn = self.history.columns.get_loc(ACLO)  # value's column number
        dcn = self.history.columns.get_loc(DAILY)  # DAILY's column number

        for i in np.arange(1, len(self.history.index)):
            self.history.iat[i, dcn] = (self.history.iloc[i, vcn] / self.history.iloc[i-1, vcn]) - 1

        # Set other attributes
        self.name = name
        self.denomination = None
        self.start_date = min(self.history.index)
        self.start_value = self.history.loc[self.start_date, ACLO]
        self.end_date = max(self.history.index)
        self.end_value = self.history.loc[self.end_date, ACLO]
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

    def get_ror(self, start_date=None, end_date=None) -> float:
        start = self.start_value if start_date is None else self.history.loc[start_date, ACLO]
        end = self.end_value if end_date is None else self.history.loc[end_date, ACLO]
        return start/end

# hypothesis 1


def hyp1(history: DataFrame, start_date=None, step=20, duration=5, num_segments=10) -> DataFrame:
    """
    Split a dataframe with price history into num_segments segments of equal
    duration, each starting step days after the previous,
    and return a dataframe with start dates of each segment and the RoR
    for investments with the recorded start_date.

    Assume history is indexed and sorted by date.

    They key to memory management here will be to never actually split history,
    instead just create the dataframe of values required.
    """
    output = []
    want_max = str(num_segments).lower() == "max"
    start_index = 0 if start_date is None else history.index.get_loc(start_date)
    col_index = history.columns.get_loc(ACLO)
    i = start_index
    length = duration*YEAR
    while i < len(history.index) and i+length < len(history.index) and \
    (want_max or len(output) < num_segments):
        ror =  history.iloc[i+length, col_index]/history.iloc[i, col_index]
        output.append((history.index[i],ror - 1))
        i += step
    return DataFrame(output, columns=[DATE, ROR])
