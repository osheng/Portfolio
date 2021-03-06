import pandas as pd
from pandas import Series
import numpy as np
import seaborn as sns
from constants import *
from matplotlib import pyplot as plt
from sys import argv
from LSA import LSA
from sklearn import linear_model
from matplotlib.text import Text

# assert len(argv) == 3 "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
# for i in range(1,3):
#     assert len(argv[1]) > 4 and argv[1][-4:] == ".csv", "Usage: python3 plot.py CSV_NAME.csv CSV_NAME.csv"
testing = False
# TODO: convert this first bit into a function.
if testing:
    # For testing...
    argv = ["plot.py", "SPTSXComp.csv", "XIC.csv"]

    x_name = argv[1][:-4]
    y_name = argv[2][:-4]

    x = pd.read_csv(RAW + argv[1])
    y = pd.read_csv(RAW + argv[2])

    data = x.merge(y, on=DATE).rename(columns={ACLO+"_x": x_name, ACLO+"_y": y_name})
    data = data[[DATE, x_name, y_name]].dropna(axis=0)

    n = 1
    g = sns.FacetGrid(data)
    g = g.map(sns.scatterplot, x_name, y_name)
    x = data[x_name]
    y = data[y_name]
    v = LSA(x, y, n=n)
    min_x = np.floor(min(x))
    max_x = np.ceil(max(x))
    X = np.arange(min_x, max_x)
    Y = np.zeros(int(max_x-min_x))
    for i in np.arange(0, n+1):
        Y = Y + v[n-i]*(X**i)
    plt.plot(X, Y, color="red")
    plt.show(g)
    # TDDO: I'd like to figure out why this doesn't look more linear than it does.


def plot_density(s: Series, n=100, round_to=2, num_quantiles=4, normalize=False):
    """
    Plot the density of values in a series of numeric values
    """
    data = s.value_counts(bins=n, sort=False, normalize=normalize).sort_index()
    mean_index = (((data.index.right - data.index.left) / 2) + data.index.left)
    quantiles = [s.quantile(p/num_quantiles) for p in np.arange(1, num_quantiles)]
    colors = ["red" if any([q in x for q in quantiles]) else "blue" for x in data.index]
    barplot = sns.barplot(x=mean_index, y=data, palette=colors, ci=None)
    new_xlabels = ["" for x in data.index]
    xticklabels = barplot.get_xticklabels()
    i = 0
    q_j = 0
    while i < len(data.index):
        # xticklabels[i].set_rotation("vertical")
        if q_j < len(quantiles) and quantiles[q_j] in data.index[i]:
            new_xlabels[i] = round(quantiles[q_j]*100, round_to)
            q_j += 1
        else:
            i += 1
    barplot.set_xticklabels(new_xlabels)  # This seems unvoidable.
    plt.show()

# aternatively I could just use something like this
# sns.distplot(a.history[DAILY], bins=1000, kde=False)
# plt.show()
