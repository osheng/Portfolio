import pandas as pd
from pandas import DataFrame

class Asset:
    """An asset object"""
    def __init__(self, name:str, history:DataFrame):
        assert "Date" in history.columns, "history has no Date column"
        assert history["Date"].is_unique, "duplicate dates in history!"
        assert "Value" in history.columns, "history has no Value column"
        # Also check the value history has no nulls
        assert history["Value"].map(lambda x : \
                True if type(x)==float else False, na_action='ignore')\
                    .isnull().sum()==0

        self.name = name
        self.denomination = None
        self.history = history
        self.start_date = min(history["Date"])
        self.start_value = df[df["Date"] ==  min(df["Date"])]["Value"][0]
        self.history["Change"] = df["Value"]/self.start_value
