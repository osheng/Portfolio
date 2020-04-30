import pandas as pd
import seaborn as sns
from constants import *
from matplotlib import pyplot as plt
from sys import argv
from LSA import LSA
from sklearn import linear_model

# assert len(argv) == 3 "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
# for i in range(1,3):
#     assert len(argv[1]) > 4 and argv[1][-4:] == ".csv", "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"

# For testing...
argv = ["plot.py", "SPTSXComp.csv", "XIC.csv"]

x_name = argv[1][:-4]
y_name = argv[2][:-4]

x = pd.read_csv(RAW + argv[1])
y = pd.read_csv(RAW + argv[2])

data = x.merge(y, on=DATE).rename(columns={ACLO+"_x": x_name, ACLO+"_y": y_name})
data = data[[DATE, x_name, y_name]].dropna(axis=0)


g = sns.FacetGrid(data)
g = g.map(sns.scatterplot, x_name, y_name, edgecolor="white")
x = data[x_name]
y = data[y_name]
v = LSA(x, y, n=1)
X = np.arange(min(x), max(x))
Y = v[0]*X+v[1]
plt.plot(X,Y,color="red")
plt.show(g)
