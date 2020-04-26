import pandas as pd
from sys import argv

assert len(argv) >= 3, "Usage: python3 clean.py path/to/output/ CSV_NAME.csv"
# n most recent data points
n = 24
# column to select
col = "Adj Close"
for arg in argv[2:]:
    assert len(arg) >= 5 and arg[-4:] == ".csv", "Usage: python3 clean.py path/to/output/ CSV_NAME.csv"

    curr_df = pd.read_csv(arg)
    curr_df["Date"] = curr_df["Date"].apply(pd.to_datetime)
    curr_df["EndOfMonth"] = pd.to_datetime(curr_df["Date"], format="%Y-%m-%d") + pd.tseries.offsets.BusinessMonthEnd(0)
    curr_df.loc[(curr_df["Date"] == curr_df["EndOfMonth"])][["Date", col]].\
        tail(n).to_csv("{path}{name}_{n}.csv".format(path=argv[1], name=arg[:-4], n=n))

