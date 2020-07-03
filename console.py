# To explore the data in console run the following
# exec(open("console.py").read())
import pandas as pd
import datetime
from pandas import Series, Timestamp, DataFrame
import seaborn as sns
from constants import *
import numpy as np
from asset import *
from numpy.linalg import inv
import pdb  # debugger
WELCOME = "The console is now set up and ready for you to explore data!"
TSX_data = pd.read_csv(RAW + TSX)
XIC_data = pd.read_csv(RAW + XIC)


data = TSX_data.merge(XIC_data, on=DATE)

data = data[[DATE, ACLO+"_x", ACLO+"_y"]].dropna(axis=0)
x = data[ACLO + "_x"]
y = data[ACLO + "_y"]


def run(file_name: str) -> None:
    exec(open(file_name).read())


exec(open("asset.py").read())
exec(open("plot.py").read())

a = Asset(name=TSX, history_fn=RAW+TSX)
hyp_data2 = get_returns(a.history, step=1, num_segments="Max", duration=0.5)
sns.set_style("darkgrid")
g = sns.lineplot(data=hyp_data2, x=DATE, y=ROR, palette=["blue"])

title = "Rate of return after 5 years for investments in the TSX from 1979 to 2015\n"
note = "Note: assumes 5 years = 252 times 5 = 1512 trading days\n"
ignores = "Ignores tax, dividens, investment fees, and returns of capital"
# g.axes.text(0.6, 0.95, title + note + ignores, fontsize=16,transform=g.axes.transAxes, va='center', ha='left', bbox=props)
plt.title(title + note + ignores)

# plt.savefig("5yRoRoverTtime1.png", dpi=600)

#
print(WELCOME)
