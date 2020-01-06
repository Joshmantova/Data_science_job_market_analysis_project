from selenium import webdriver
import selenium_linkedin_jobs_test as sljt
import Selenium_and_BS4_linkedin as sbs4
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    delays = np.arange(2,5)
    delay = np.random.choice(delays)

    list_of_locations = ['Colorado','California', 'New%20york', 'Washington', 'Utah', 'Florida']
    for loc in list_of_locations:
        print(f'Starting to scrape {loc} jobs from Linkedin')
        search_result_url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science&location={loc}&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
        driver.get(search_result_url)
        sljt.see_more_jobs(driver, num_times=40)

        time.sleep(delay)

        job_titles, company_names, locations, num_applicants, descriptions = sbs4.scrape_all_from_linkedin(driver)


        # try:
        #     job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url, driver)
        # except NoSuchElementException:
        #     print('There was a No Such Element Exception error!! Waiting two minutes.')
        #     time.sleep(120)
        #     print('Continuing')
        #     job_titles, company_names, locations, num_applicants, descriptions = sljt.scrape_all_from_linkedin(search_result_url, driver)

        df = pd.DataFrame()
        df['Job_Title'] = job_titles
        df['Company'] = company_names
        df['Location'] = locations
        df['Number_of_Applicants'] = num_applicants
        df['Description'] = descriptions

        df.to_csv(f'df_linkedin_{loc}_40.csv')
        print(f'{loc} scraping is done!')
        time.sleep(60)
    print('Finished scraping all locations!!!!')
    driver.close()
