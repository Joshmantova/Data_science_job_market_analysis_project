from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
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

def scrape_all_from_linkedin(search_result_url, driver):
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
    delays = np.arange(2,7)
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

    #     job_title_h2 = driver.find_element_by_class_name('topcard__title').text
    #     company_name_a = driver.find_element_by_class_name('topcard__org-name-link').text
    #     locations_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet')]").text
    #     time.sleep(delay)
    #     try: 
    #         # if more than 25 people applied, the number of applicants is located here
    #         num_applicants_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet') and contains(@class, 'num-applicants__caption')]").text
    #     except NoSuchElementException:
    #         # if less than 25 people applied, the number of applicants is located here
    #         num_applicants_span = driver.find_element_by_class_name('num-applicants__caption').text
    #     description = driver.find_element_by_class_name('description__text').text
    #     job_titles.append(job_title_h2)
    #     company_names.append(company_name_a)
    #     locations.append(locations_span)
    #     num_applicants.append(num_applicants_span)
    #     descriptions.append(description)

    # return job_titles, company_names, locations, num_applicants, descriptions

if __name__ == '__main__':
    search_result_url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=Colorado&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

    delays = np.arange(2,5)
    delay = np.random.choice(delays)

    driver = webdriver.Chrome()
    driver.get(search_result_url)
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

    df = pd.DataFrame()
    df['Job_Title'] = job_titles
    df['Company'] = company_names
    df['Location'] = locations
    df['Number_of_Applicants'] = num_applicants
    df['Description'] = descriptions

    print(df)

    """
    <h2 class="topcard__title">Data Science Journalist</h2>
    class="topcard__org-name-link"
    <span class="topcard__flavor topcard__flavor--bullet">Broomfield, CO, US</span>
    <span class="topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption">90 applicants</span>
    <figcaption class="num-applicants__caption">Be among the first 25 applicants</figcaption>
    <div class="description__text description__text--rich">
    """