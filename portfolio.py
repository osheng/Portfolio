import sys
import asset

class Portfolio:
    """A portfolio object"""

    def __init__(self, name: str, asset_allocation: dict[Asset:float]):
        assert sum(asset_allocation.values()) == 1, "asset_allocation does not sum to 1"
        self.name = name
        self.asset_allocation = asset_allocation
