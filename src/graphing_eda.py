import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
plt.style.use('fivethirtyeight')

df_all = pd.read_csv('../Datasets/df_all_linkedin.csv')

len_descrip_sen = df_all.groupby('Senior_Junior_or_not').mean()['Length_of_Description'].values
senior_junior_or_not = df_all.groupby('Senior_Junior_or_not').mean()['Length_of_Description'].index

fig, ax = plt.subplots(figsize=(13,9))

ax.bar(senior_junior_or_not, len_descrip_sen)
ax.set_xlabel('Senior / Junior Included in Job title or not')
ax.set_ylabel('Length of Description')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Junior', 'Senior', 'Neither'])
ax.set_title('Length of Description for Linkedin Jobs That Include Senior / Junior in Title or Not')
plt.tight_layout()
plt.savefig('../imgs/linkedin_sen_or_not_length_descrip.png')

#Relation Between Number of Applicants and Length of Description on Linkedin

number_applied = df_all['num_applicants'].values
length_of_descrip = df_all['Length_of_Description'].values

fig, ax = plt.subplots(figsize = (13,9))

ax.scatter(length_of_descrip, number_applied)
ax.set_ylabel('Number of Applicants')
ax.set_xlabel('Length of Description')
ax.set_title('Relation Between Number of Applicants and Length of Description on Linkedin')
b, m = polyfit(length_of_descrip, number_applied, 1)
ax.plot(length_of_descrip, b + m * length_of_descrip, '-', linewidth=2, color='k', label='Line of Best Fit')
plt.legend()
plt.tight_layout()
plt.savefig('../imgs/linkedin_num_applicants_len_descrip.png')

#Relation Between Number of Applicants and Length of Description on Linkedin Cleaned

df_cleaned_applicants = df_all[(df_all['num_applicants'] != 20) & (df_all['num_applicants'] != 200)]
num_applied_clean = df_cleaned_applicants['num_applicants'].values
length_of_descrip = df_cleaned_applicants['Length_of_Description'].values
fig, ax = plt.subplots(figsize=(13,9))

ax.scatter(length_of_descrip, num_applied_clean)
ax.set_ylabel('Number of Applicants')
ax.set_xlabel('Length of Description')
ax.set_title('Relation Between Number of Applicants and Length of Description on Linkedin Cleaned')
b, m = polyfit(length_of_descrip, num_applied_clean, 1)
ax.plot(length_of_descrip, b + m * length_of_descrip, '-', linewidth=2, color='k', label='Line of Best Fit')
plt.legend()
plt.tight_layout()
plt.savefig('../imgs/linkedin_num_applicants_len_descrip_cleaned.png')

#Number of job postings for each company on Linkedin

companies = df_all['Company'].value_counts().index[:15]
companies = companies[::-1]

jobs = df_all['Company'].value_counts().values[:15]
jobs = jobs[::-1]

fig, ax = plt.subplots(figsize=(13,9))
# plt.rcParams.update({'font.size': 15})

ax.barh(companies, jobs)

ax.set_xlabel('Number of job postings')
ax.set_ylabel('Companies')
ax.set_title('Number of job postings for each company on Linkedin')
plt.tight_layout()
plt.savefig('../imgs/linkedin_num_postings_for_top_companies.png')

#15 Companies That Post The Longest Descriptions on Linkedin

company_length_descrip = df_all.groupby('Company')['Length_of_Description'].mean().sort_values(ascending=False)
companies = company_length_descrip.index[:15]
avg_len_descrip = company_length_descrip.values[:15]

companies = companies[::-1]
avg_len_descrip = avg_len_descrip[::-1]

fig, ax = plt.subplots(figsize = (13,9))
ax.barh(companies, avg_len_descrip)

ax.set_xlabel('Average Length of Descriptions')
ax.set_ylabel('Company Names')
ax.set_title('15 Companies That Post The Longest Descriptions on Linkedin')
plt.tight_layout()
plt.savefig('../imgs/linkedin_top_companies_longest_descriptions.png')

#Number of job postings for each company on Linkedin in each state

def graph_top10_companies(state_id):
    df_all_state = df_all[df_all['State'] == state_id]
    companies_state = df_all_state['Company'].value_counts().index[:10]
    companies_state = list(companies_state)

    for idx, comp in enumerate(companies_state):
        if len(comp) >= 20:
            comp_temp = comp.split()
            comp_ac = str()
            for word in comp_temp:
                comp_ac += word[0]
            if comp_ac == 'AWS(':
                comp_ac = 'AWS'
            elif comp_ac == 'TCoJCoLS':
                comp_ac = 'LDS Church'
            elif comp_ac == 'IH':
                comp_ac = 'Intermountain Healthcare'
            elif comp_ac == 'RFoTCUoNY':
                comp_ac = 'Research Foundation of NYU'
            elif comp_ac == 'PNNL-P':
                comp_ac = 'PNNL'

            companies_state[idx] = comp_ac
        
    companies_state = companies_state[::-1]

    jobs_state = df_all_state['Company'].value_counts().values[:10]
    jobs_state = jobs_state[::-1]
    # plt.rcParams.update({'font.size': 15})

    fig, ax = plt.subplots(figsize=(13,9))
    ax.barh(companies_state, jobs_state)

    ax.set_xlabel('Number of job postings')
    ax.set_ylabel('Companies')
    ax.set_title(f'Number of job postings for each company on Linkedin in {state_id}')
    
    plt.tight_layout()
    plt.savefig(f'../imgs/linkedin_top_companies_num_job_postings_per_{state_id}.png')

list_of_locs = ['CO', 'CA', 'FL', 'NY', 'UT', 'WA']

for loc in list_of_locs:
    graph_top10_companies(loc)

