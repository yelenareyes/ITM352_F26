import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml

X,y = fetch_openml("autos", version=1, as_frame=True, return_X_y=True)
data = X
data['target'] = y

pivot = np.round(pd.pivot_table(data, values='price', 
                                index='num-of-doors', 
                                columns='fuel-type', 
                                aggfunc=np.mean),2)
pivot