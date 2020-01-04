from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def see_more_jobs(driver, num_times=40):
    """
    Scrolls to the bottom of Linkedin page x number of times

    :params: num_times: number of times to scroll to bottom and click see more jobs button

    :returns: None
    """
    if num_times == 0:
        return None
    for _ in range(num_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        see_more_jobs = driver.find_element_by_class_name('see-more-jobs')
        see_more_jobs.click()
        time.sleep(2)

# see_more_jobs(20)

def scrape_all_from_linkedin(search_result_url, driver, num_pages=40):
    """
    Scrapes several features of jobs from linkedin search.

    :params: \n
    search_result_url: initial search page for job \n
    num_pages: the number of times the user would like to press the 'see more jobs' button

    :returns: \n
    job_titles: list of job titles of each job \n
    company_names: list of company names for each job \n
    locations: list of locations of each job \n
    num_applicants: list of number of applicants for each job \n
    descriptions: list of descriptions of each job
    """

    jobs = driver.find_elements_by_class_name('result-card__full-card-link')

    job_titles = []
    company_names = []
    locations = []
    num_applicants = []
    descriptions = []

    for job in jobs:
        job.click()
        time.sleep(2)
        job_title_h2 = driver.find_element_by_class_name('topcard__title')
        company_name_a = driver.find_element_by_class_name('topcard__org-name-link')
        locations_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet')]")
        try: 
            # if more than 25 people applied, the number of applicants is located here
            num_applicants_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet') and contains(@class, 'num-applicants__caption')]")
        except NoSuchElementException as exception:
            # if less than 25 people applied, the number of applicants is located here
            num_applicants_span = driver.find_element_by_class_name('num-applicants__caption')
        description = driver.find_element_by_class_name('description__text')
        job_titles.append(job_title_h2.text)
        company_names.append(company_name_a.text)
        locations.append(locations_span.text)
        num_applicants.append(num_applicants_span.text)
        descriptions.append(description.text)

    return job_titles, company_names, locations, num_applicants, descriptions

if __name__ == '__main__':
    search_result_url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=Colorado&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
    job_titles, company_names, locations, num_applicants, descriptions = scrape_all_from_linkedin(search_result_url, num_pages=0)

    df = pd.DataFrame()
    df['Job_Title'] = job_titles
    df['Company'] = company_names
    df['Location'] = locations
    df['Number_of_Applicants'] = num_applicants
    df['Description'] = descriptions

    print(df)
    # df.to_csv('test_linkedin_scrape.csv')

    """
    next page clicks = 40
    class = num-applicants__caption
    """