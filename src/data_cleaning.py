import pandas as pd

def get_length_of_description(x):
    return len(x)

def senior_or_not(x):
    if 'Senior' in x or 'Sr' in x:
        return 1
    else:
        return 0

def junior_or_not(x):
    if 'Junior' in x or 'Jr' in x:
        return 1
    else:
        return 0

def senior_or_junior_or_not(x):
    if 'Junior' in x or 'Jr' in x:
        return 0
    elif 'Senior' in x or 'Sr' in x:
        return 1
    else:
        return 2

def get_num_applicants_int(x):
    num = str()
    for elem in x:
        if elem == 'B':
            num = 20
            break
        elif elem == 'O':
            num = 200
            break
        elif elem != ' ':
            num += elem
        elif elem == ' ':
            break
    return int(num)

def get_state(x):
    if 'CO' in x or 'Colorado' in x or 'Denver' in x:
        return 'CO'
    elif 'CA' in x or 'California' in x or 'San Francisco' in x or 'Los Angeles' in x or 'Sunnyvale' in x:
        return 'CA'
    elif 'FL' in x or 'Florida' in x or 'Miami' in x:
        return 'FL'
    elif 'NY' in x or 'New York' in x:
        return 'NY'
    elif 'UT' in x or 'Utah' in x or 'Salt Lake City' in x:
        return 'UT'
    elif 'WA' in x or 'Washington' in x or 'Seattle' in x:
        return 'WA'



if __name__ == '__main__':
    #Concatenating indeed data
    df_CO = pd.read_csv('../Datasets/df_indeed_CO.csv', index_col=0)
    df_CA = pd.read_csv('../Datasets/df_indeed_CA.csv', index_col=0)
    df_NY = pd.read_csv('../Datasets/df_indeed_NY.csv', index_col=0)
    df_WA = pd.read_csv('../Datasets/df_indeed_WA.csv', index_col=0)
    df_UT = pd.read_csv('../Datasets/df_indeed_UT.csv', index_col=0)
    df_FL = pd.read_csv('../Datasets/df_indeed_FL.csv', index_col=0)

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

    #Feature engineering
    df_all['Length_of_Description'] = df_all['Description'].apply(get_length_of_description)
    df_all['Senior'] = df_all['Job_Title'].apply(senior_or_not)
    df_all['Junior'] = df_all['Job_Title'].apply(junior_or_not)
    df_all['Senior_Junior_or_not'] = df_all['Job_Title'].apply(senior_or_junior_or_not)
    df_all['num_applicants'] = df_all['Number_of_Applicants'].apply(get_num_applicants_int)
    df_all['State'] = df_all['Location'].apply(get_state)

    df_all.to_csv('../Datasets/df_all_linkedin.csv', index=False)
