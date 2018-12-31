import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('f150_XLT_cars.csv')

#sns.jointplot('Year', 'odometer', data=data)
sns.heatmap(data.corr())
# adding something new to see what happens
