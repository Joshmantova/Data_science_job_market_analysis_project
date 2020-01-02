import pandas as pd

df_CO = pd.read_csv('../Datasets/df_CO.csv', index_col=0)
df_CA = pd.read_csv('../Datasets/df_CA.csv', index_col=0)
df_NY = pd.read_csv('../Datasets/df_NY.csv', index_col=0)
df_WA = pd.read_csv('../Datasets/df_WA.csv', index_col=0)
df_UT = pd.read_csv('../Datasets/df_UT.csv', index_col=0)
df_FL = pd.read_csv('../Datasets/df_FL.csv', index_col=0)

df_all = pd.concat((df_CO, df_CA, df_NY, df_WA, df_UT, df_FL))

df_all.to_csv('../Datasets/df_all.csv')