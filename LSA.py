# This module implements Least Squared Approximation as explained in
# Friedberg, Insel, and Spence's Linear Algebra, section 6.3
import pandas
from pandas import Series
import numpy as np
from numpy.linalg import inv

def LSA(x: Series, y: Series, n=1) -> Series:
    """

    """
    assert x.size == y.size, "x and y do not have the same size!"
    A = np.ones( (x.size, 1), dtype=np.float )
    for i in range(1,n+1):
        temp = np.ndarray((x.size,1), buffer=x.to_numpy(), dtype=np.float)
        A = np.concatenate((temp,A), axis=1)
    print(A)
    Y = np.ndarray((x.size,1), buffer=y.to_numpy(), dtype=np.float)
    print(Y)
    return list(inv(A.T.dot(A)).dot(A.T.dot(Y)).flatten())
