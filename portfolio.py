import sys
from asset import Asset
from typing import Dict
from pandas import DataFrame

POSSIBLE_ASSETS = ["S&P500","S&P/TSX Comp"]

class Portfolio:
    """A portfolio object"""

    def __init__(self, name: str, value: float, assets: Dict[str:Asset], \
        asset_allocation: Dict[str:float]):
        # assert asset_allocation.keys().all(lambda x: x in POSSIBLE_ASSETS),\
        #     "asset_allocation contains mislabled asset"
        assert sum(asset_allocation.values()) == 1,\
            "asset_allocation does not sum to 1"
        assert assets.keys().sort()==asset_allocation.keys().sort(),\
            "assets and asset_allocation don't match"
        self.name = name
        self.start_value = value
        self.assets = assets
        self.asset_allocation = asset_allocation

    def value(self):
        """Return the value of the portfolio over time"""
        df = DataFrame()
        for a in assets:
            if df.empty:
                df = assets[a]
            else:
                df.merge(assets[a], on="Date")
        df["Portfolio Value"] = start_value # times the change in assets for the given weight
        df["Portfolio Change"] = df["Portfolio Value"]/start_value
        return df["Date", "Portfolio Value", "Portfolio Change"]
