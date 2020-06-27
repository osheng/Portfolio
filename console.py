# To explore the data in console run the following
# exec(open("console.py").read())
import pandas as pd
import datetime
from pandas import Series
import seaborn as sns
from constants import *
import numpy as np
from asset import Asset
from numpy.linalg import inv
WELCOME = "The console is now set up and ready for you to explore data!"
TSX_data = pd.read_csv(RAW + TSX)
XIC_data = pd.read_csv(RAW + XIC)
print(WELCOME)

data = TSX_data.merge(XIC_data, on=DATE)

data = data[[DATE, ACLO+"_x", ACLO+"_y"]].dropna(axis=0)
x = data[ACLO + "_x"]
y = data[ACLO + "_y"]


def run(file_name: str) -> None:
    exec(open(file_name).read())


a = Asset(name=TSX, history_fn=RAW+TSX)
