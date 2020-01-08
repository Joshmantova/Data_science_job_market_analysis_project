import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd as tukeyhsd

df_all = pd.read_csv('../Datasets/df_all_linkedin.csv')

# Anova for senior, junior, and neither level jobs 

senior_df = df_all[df_all['Senior_Junior_or_not'] == 1]
junior_df = df_all[df_all['Senior_Junior_or_not'] == 0]
neither_df = df_all[df_all['Senior_Junior_or_not'] == 2]

senior = senior_df['Length_of_Description'].values
junior = junior_df['Length_of_Description'].values
neither = neither_df['Length_of_Description'].values

# Proportion of each group. Small number of Junior jobs and most (88%) are neither senior nor junior

df_between = 3 - 1
df_within = df_all.shape[0] - df_between
print(f'degrees of freedom: ({df_between}, {df_within})')

prop_senior = len(senior) / df_all.shape[0]
prop_junior = len(junior) / df_all.shape[0]
prop_neither = len(neither) / df_all.shape[0]

print(f'The percentage of Senior level jobs is: {prop_senior * 100:0.2f}')
print(f'The percentage of Junior level jobs is: {(prop_junior * 100):0.2f}')
print(f"The percentage of jobs that didn't mention Junior or Senior in the title is: {prop_neither * 100:0.2f}")

# Nonsignificant ANOVA

anova = stats.f_oneway(senior, junior, neither)
print(anova)

num_applicants = df_all['num_applicants'].values
len_descrip = df_all['Length_of_Description'].values

# Correlation between number of applicants and length of description. It's negative and significant but 
# I think it's weighing too heavily on < 25 applicants. Very small effect size

r = stats.pearsonr(num_applicants, len_descrip)
# print(r)

# Taking out the < 25 and > 200s and redoing the correlation. Correlation is no longer significant. Probably due to
# Sample size issues. Effect size is ultra small too but still negative.

df_all_applicants_cleaned = df_all[(df_all['num_applicants'] != 20) & (df_all['num_applicants'] != 200)]
num_applicants_cleaned = df_all_applicants_cleaned['num_applicants'].values
len_descrip_cleaned = df_all_applicants_cleaned['Length_of_Description'].values

r_cleaned = stats.pearsonr(num_applicants_cleaned, len_descrip_cleaned)
# print(r_cleaned)

# Comparing the length of description for senior jobs vs jobs that don't mention senior or junior. Nonsignificant.

t_test = stats.ttest_ind(senior, neither)
# print(t_test)

# Comparing the length of description for senior level jobs vs all others. Nonsignificant.

senior_or_not_senior_df = df_all[df_all['Senior'] == 1]
senior_or_not_senior = senior_or_not_senior_df['Length_of_Description'].values

senior_or_not_not_df = df_all[df_all['Senior'] == 0]
senior_or_not_not = senior_or_not_not_df['Length_of_Description'].values

t_test2 = stats.ttest_ind(senior_or_not_senior, senior_or_not_not)
# print(t_test2)
