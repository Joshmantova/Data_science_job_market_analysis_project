import pandas as pd

if __name__ == '__main__'
#Concatenating indeed data
df_CO = pd.read_csv('../Datasets/df_CO.csv', index_col=0)
df_CA = pd.read_csv('../Datasets/df_CA.csv', index_col=0)
df_NY = pd.read_csv('../Datasets/df_NY.csv', index_col=0)
df_WA = pd.read_csv('../Datasets/df_WA.csv', index_col=0)
df_UT = pd.read_csv('../Datasets/df_UT.csv', index_col=0)
df_FL = pd.read_csv('../Datasets/df_FL.csv', index_col=0)

df_all = pd.concat((df_CO, df_CA, df_NY, df_WA, df_UT, df_FL))

df_all.to_csv('../Datasets/df_all_indeed.csv')

#Concatenating linkedin data
df_CA = pd.read_csv('../Datasets/df_linkedin_California.csv')
df_CO = pd.read_csv('../Datasets/df_linkedin_Colorado.csv')
df_FL = pd.read_csv('../Datasets/df_linkedin_Florida.csv')
df_NY = pd.read_csv('../Datasets/df_linkedin_New%20york.csv')
df_UT = pd.read_csv('../Datasets/df_linkedin_Utah.csv')
df_WA = pd.read_csv('../Datasets/df_linkedin_Washington.csv')

df_all = pd.concat((df_CO, df_CA, df_NY, df_WA, df_UT, df_FL))
df_all.to_csv('../Datasets/df_all_linkedin.csv')