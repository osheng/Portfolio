class Transaction:
    """Define various types of Transaction"""
    def __init__(self, date: str):
        self.date = date
# Maybe transaction history should just be a dataframe as well?
# Rebalancing doesn't make sense. There should only be trades from one asset to another,
# Withdrawals and investments. Actually even trades are maybe unnecessary. Since a trade is just
# where you withdraw from one asset then invest in another.
# Withdrawals and investments can also be the same thing. Investments will just be positive value
# and withdrawals will be negative.
# Maybe a portfolio is just a history of transactions?
#
# class Trade(Transaction):
#
# class Withdrawal(Transaction):
#
# class Investment(Transaction):
#
# class Rebalance(Transaction):


# TODO: I should have a way to read and write an array of transactions to CSV
