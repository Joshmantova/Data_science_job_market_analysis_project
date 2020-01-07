import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df_all = pd.read_csv('../Datasets/df_all_linkedin.csv')

print(df_all.columns)