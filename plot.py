import pandas as pd
import seaborn as sb
from constants import *
from matplotlib import pyplot as plt
from sys import argv
from LSA import LSA

# assert len(argv) == 3 "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
# for i in range(1,3):
#     assert len(argv[1]) > 4 and argv[1][-4:] == ".csv", "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
argv = ["plot.py","SPTSXComp.csv","XIC.csv"]

x_name = argv[1][:-4]
y_name = argv[2][:-4]

x = pd.read_csv(RAW + argv[1])
y = pd.read_csv(RAW + argv[2])

data = x.merge(y, on=DATE)
data = data[[DATE, ACLO+"_x", ACLO+"_y"]].dropna(axis=0)
plot = sb.scatterplot(x=data[ACLO + "_x"], y=data[ACLO + "_y"], data=data, color="orange")
plt.xlabel(x_name)
plt.ylabel(y_name)
x = data[ACLO+"_x"]
y = data[ACLO + "_y"]
v = LSA(x, y)

plt.plot([min(x), max(x)], [v[0]*min(x)+v[1],v[0]*max(x)+v[1]] , linewidth=2,color="blue")
plt.show(plot)
