import selenium_linkedin_jobs_test as sljt
import pandas as pd

if __name__ == '__main__':
    list_of_locations = ['Colorado', 'California', 'New%20york', 'Washington', 'Utah', 'Florida']
    # for loc in list_of_locations:
    #     print(f'starting to scrape {loc[1]} jobs from Linkedin')
    #     search_result_url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science&location={loc}&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
    #     job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url)

    #     df = pd.DataFrame()
    #     df['Job_Title'] = job_titles
    #     df['Company'] = company_names
    #     df['Location'] = locations
    #     df['Number_of_Applicants'] = num_applicants
    #     df['Description'] = descriptions

    #     df.to_csv(f'df_linkedin_{loc}.csv')
    #     print(f'{loc} scraping is done!')
    # print('Finished scraping all locations!!!!')

    loc = list_of_locations[1]
    print(f'starting to scrape {loc} jobs from Linkedin')
    search_result_url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science&location={loc}&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
    job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url)

    df = pd.DataFrame()
    df['Job_Title'] = job_titles
    df['Company'] = company_names
    df['Location'] = locations
    df['Number_of_Applicants'] = num_applicants
    df['Description'] = descriptions

    df.to_csv(f'df_linkedin_{loc}.csv')
    print(f'{loc} scraping is done!')