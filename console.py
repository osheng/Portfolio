# To explore the data in console run the following
# exec(open("console.py").read())
import pandas as pd
import seaborn as sns
from constants import *
WELCOME = "The console is now set up and ready for you to explore data!"
TSX_data = pd.read_csv(RAW + TSX)
XIC_data = pd.read_csv(RAW + XIC)
print(WELCOME)
