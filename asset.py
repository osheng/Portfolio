import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from constants import *
import datetime
from typing import Union, Iterable
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
        """Return the rate of return on a asset

        start_date (str or Timestamp): when the asset was placed
        end_date (str or Timestamp): when the asset was sold

        """
        start = self.start_value if start_date is None else self.history.loc[start_date, ACLO]
        end = self.end_value if end_date is None else self.history.loc[end_date, ACLO]
        return start/end


def annualize(ror: Union[Iterable[float], float], n: int, periodicity=DAYS) -> Union[Iterable[float], float]:
    """
    Takes in a rate or return or a list of rates of return and returns them annualized

    n (int): the number of observed periods
    periodicity (str): whether the observed periods are in DAYS or YEARS
    """
    assert periodicity in [YEARS, DAYS], "periodicity must be '{}' or '{}'".format(YEARS, DAYS)
    if isinstance(ror, float) and periodicity == DAYS:
        return (1 + ror)**(YEAR/n) - 1
    elif isinstance(ror, float) and periodicity == YEARS:
        return (1 + ror)**(1/n) - 1
    else:
        return Series(data=[annualize(x, n, periodicity) for x in ror], index=ror.index)


# hypothesis 1


def get_returns(history: DataFrame, start_date=None, step=20, duration=5, num_segments=10) -> DataFrame:
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
    length = round(duration*YEAR)
    while i < len(history.index) and i+length < len(history.index) and \
            (want_max or len(output) < num_segments):
        ror = history.iloc[i+length, col_index]/history.iloc[i, col_index]
        output.append((history.index[i], ror - 1))
        i += step
    return DataFrame(output, columns=[DATE, ROR])


def fill_nans(history: DataFrame, col=ACLO) -> None:
    """
    Fill in place the NaNs in col of history with the average of the nearest non-NaN value.
    """
    c = history.columns.get_loc(ACLO)
    n = len(history.index)
    for i in np.arange(1, n):
        if np.isnan(history.iloc[i, c]):
            ante_i = i - 1
            post_i = i + 1
            while np.isnan(history.iloc[ante_i, c]):
                ante_i -= 1
            while np.isnan(history.iloc[post_i, c]):
                post_i += 1
            dif = post_i + ante_i
            before = history.iloc[ante_i, c]
            after = history.iloc[post_i, c]
            history.iloc[i, c] = before + (i - ante_i)*(after - before)/dif

def quantile(s: Series, value: float) -> float:
    """
    Return which quantile of s value is in.
    """
    n = sum([1 for x in s if x < value])
    return n/s.size
