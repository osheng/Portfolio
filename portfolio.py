from asset import Asset
from typing import Dict
from pandas import DataFrame
from transaction import Transaction


class Portfolio:
    """A portfolio object"""

    def __init__(self, name: str, value: float, assets: Dict[str:Asset],
                 asset_allocation: Dict[str:float]):
        # assert asset_allocation.keys().all(lambda x: x in POSSIBLE_ASSETS),\
        #     "asset_allocation contains mislabeled asset"
        assert sum(asset_allocation.values()) == 1, \
            "asset_allocation does not sum to 1"
        assert assets.keys().sort() == asset_allocation.keys().sort(), \
            "assets and asset_allocation don't match"
        self.name = name
        self.start_value = value
        self.assets = assets
        self.asset_allocation = asset_allocation
        self.transactions = []
        # TODO: add rate or return
        # Note the rate of return for an investment is its value at a later date
        # divided by its value at the earlier date
        # Also, note withdrawals decrease the rate of return by a proportion
        # equal to how much they are of the initial Investment
        # Perhaps it would be more accurate to day that investments lose a proportion of their RoR
        # when a portion of them is withdrawn
        # rate of return of the portfolio should be the sum of the rates for
        # each of the investments
        # I should maybe have a list of Transactions

        # TODO the return of value should likely just be an attribute of portfolio

    def value(self):
        """
        Return DataFrame giving the value and %-change of the portfolio over time
        """
        wc = "Weighted Change"
        df = DataFrame()
        for a in self.assets:
            if df.empty:
                df = self.assets[a]
                df[wc] = df["Change"] * self.asset_allocation[a]
            else:
                df.merge(self.assets[a], on="Date")
        df["Portfolio Change"] = \
            df.filter(regex=".*" + wc + ".*").sum(axis=1)
        df["Portfolio Value"] = self.start_value * df["Portfolio Change"]
        return df["Date", "Portfolio Value", "Portfolio Change"]

    def invest(self, date: str, amount: float, asset: Asset):
        """invest in a portfolio at some point in time"""
        pass

    def withdraw(self, date: str, amount: float, asset: Asset):
        """withdraw some amount from a port at a certain time"""
        pass

    def rebalance(self, date: str, allocation: Dict[str:float]):
        """rebalance portfolio"""
        pass

    def trade(self, date: str, to_be_sold: Asset, to_be_bought: Asset, value: float):
        """Make a trade within a portfolio"""
        pass

    def add_transaction(self, t: Transaction):
        # TODO: make this update the value history of the portfolio currently return
        # by value()
        pass
