from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import numpy as np

def see_more_jobs(driver, num_times=40):
    """
    Scrolls to the bottom of Linkedin page x number of times

    :params: num_times: number of times to scroll to bottom and click see more jobs button

    :returns: None
    """
    if num_times == 0:
        return None
    for _ in range(num_times):
        time.sleep(.5)
        see_more_jobs = driver.find_element_by_class_name('see-more-jobs')
        driver.execute_script('return arguments[0].scrollIntoView();', see_more_jobs)
        see_more_jobs.click()
        time.sleep(3)

def scrape_all_from_linkedin(driver):
    """
    Scrapes several features of jobs from linkedin search.

    :params: \n
    search_result_url: initial search page for job \n
    driver: selenium webdriver to use to scrape

    :returns: \n
    job_titles: list of job titles of each job \n
    company_names: list of company names for each job \n
    locations: list of locations of each job \n
    num_applicants: list of number of applicants for each job \n
    descriptions: list of descriptions of each job
    """
    delays = np.arange(2,5)
    delay = np.random.choice(delays)

    jobs = driver.find_elements_by_class_name('result-card__full-card-link')

    job_titles = []
    company_names = []
    locations = []
    num_applicants = []
    descriptions = []

    for job in jobs:
        driver.execute_script('return arguments[0].scrollIntoView();', job)
        time.sleep(delay)
        job.click()
        time.sleep(delay)

        page = driver.page_source
        soup = BeautifulSoup(page, features='lxml')
        job_title_h2 = soup.find('h2', attrs={'class': 'topcard__title'})
        job_title = job_title_h2.text

        company_name_a = soup.find('a', attrs={'class': 'topcard__org-name-link'})
        company_name = company_name_a.text

        locations_span = soup.find('span', attrs={'class': 'topcard__flavor--bullet'})
        location = locations_span.text

        if soup.find('span', attrs={'class': 'num-applicants__caption'}):
            num_applicants_cont = soup.find('span', attrs={'class': 'num-applicants__caption'})
        else:
            num_applicants_cont = soup.find('figcaption', attrs={'class': 'num-applicants__caption'})
        num_applicants_temp = num_applicants_cont.text

        description_div = soup.find('div', attrs={'class': 'description__text--rich'})
        description = description_div.text

        job_titles.append(job_title)
        company_names.append(company_name)
        locations.append(location)
        num_applicants.append(num_applicants_temp)
        descriptions.append(description)

    return job_titles, company_names, locations, num_applicants, descriptions

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
        see_more_jobs(driver, num_times=20)

        time.sleep(delay)

        job_titles, company_names, locations, num_applicants, descriptions = scrape_all_from_linkedin(driver)

        df = pd.DataFrame()
        df['Job_Title'] = job_titles
        df['Company'] = company_names
        df['Location'] = locations
        df['Number_of_Applicants'] = num_applicants
        df['Description'] = descriptions

        df.to_csv(f'df_linkedin_{loc}.csv')
        print(f'{loc} scraping is done!')
        time.sleep(60)
    print('Finished scraping all locations!!!!')
    driver.close()
