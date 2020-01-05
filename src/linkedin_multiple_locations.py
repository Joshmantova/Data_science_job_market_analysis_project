from selenium import webdriver
import selenium_linkedin_jobs_test as sljt
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    list_of_locations = ['Colorado','California', 'New%20york', 'Washington', 'Utah', 'Florida']
    for loc in list_of_locations:
        print(f'Starting to scrape {loc} jobs from Linkedin')
        search_result_url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science&location={loc}&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
        driver.get(search_result_url)
        sljt.see_more_jobs(driver, num_times=2)
        try:
            job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url, driver)
        except NoSuchElementException:
            print('There was a No Such Element Exception error!! Waiting two minutes.')
            time.sleep(120)
            print('Continuing')
            job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url, driver)

        df = pd.DataFrame()
        df['Job_Title'] = job_titles
        df['Company'] = company_names
        df['Location'] = locations
        df['Number_of_Applicants'] = num_applicants
        df['Description'] = descriptions

        df.to_csv(f'../Datasets/df_linkedin_{loc}_TEST.csv')
        print(f'{loc} scraping is done!')
        time.sleep(60)
    print('Finished scraping all locations!!!!')
    driver.close()

    # loc = list_of_locations[1]
    # print(f'starting to scrape {loc} jobs from Linkedin')
    # search_result_url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science&location={loc}&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
    # job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url)

    # df = pd.DataFrame()
    # df['Job_Title'] = job_titles
    # df['Company'] = company_names
    # df['Location'] = locations
    # df['Number_of_Applicants'] = num_applicants
    # df['Description'] = descriptions

    # df.to_csv(f'df_linkedin_{loc}.csv')
    # print(f'{loc} scraping is done!')