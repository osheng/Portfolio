import pandas as pd
import seaborn as sb
from constants import *
from matplotlib import pyplot as plt
from sys import argv

# assert len(argv) == 3 "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
# for i in range(1,3):
#     assert len(argv[1]) > 4 and argv[1][-4:] == ".csv", "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
x_name = argv[1][:-4]
y_name = argv[2][:-4]

x = pd.read_csv(RAW + argv[1])
y = pd.read_csv(RAW + argv[2])

data = x.merge(y, on=DATE)
plot = sb.scatterplot(x=data[ACLO + "_x"], y=data[ACLO + "_y"],data=data)
plt.xlabel(x_name)
plt.ylabel(y_name)
plt.show(plot)
