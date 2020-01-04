from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get('https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=Denver%2C%20Colorado%2C%20United%20States&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0')

def see_more_jobs(num_times):
    """
    Scrolls to the bottom of Linkedin page x number of times

    :params: num_times: number of times to scroll to bottom and click see more jobs button

    :returns: None
    """
    for _ in range(num_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        see_more_jobs = driver.find_element_by_class_name('see-more-jobs')
        see_more_jobs.click()
        time.sleep(2)

# see_more_jobs(20)


if __name__ == '__main__':

    jobs = driver.find_elements_by_class_name('result-card__full-card-link')

    job_titles = []
    company_names = []
    locations = []
    num_applicants = []
    descriptions = []

    for job in jobs:
        job.click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, features='lxml')
        job_title_h2 = driver.find_element_by_class_name('topcard__title')
        company_name_a = driver.find_element_by_class_name('topcard__org-name-link')
        locations_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet')]")
        try: 
            num_applicants_span = driver.find_element_by_xpath("//span[contains(@class, 'topcard__flavor--bullet') and contains(@class, 'num-applicants__caption')]")
        except NoSuchElementException as exception:
            num_applicants_span = driver.find_element_by_class_name('num-applicants__caption')
        # descrip_div = soup.find('div', attrs={'class': 'description__text'})
        # print(descrip_div.text)
        description = driver.find_element_by_class_name('description__text')
        job_titles.append(job_title_h2.text)
        company_names.append(company_name_a.text)
        locations.append(locations_span.text)
        num_applicants.append(num_applicants_span.text)
        descriptions.append(description.text)
        # print(num_applicants_span.text)
        # descriptions = driver.find_elements_by_css_selector('p')
        # for descrip in descriptions:
        #     print(descrip.text)
        # print(job_title_h2.text, company_name_a.text)

    df = pd.DataFrame()
    df['Job_Title'] = job_titles
    df['Company'] = company_names
    df['Location'] = locations
    df['Number_of_Applicants'] = num_applicants
    df['Description'] = descriptions

    print(df)
    df.to_csv('test_linkedin_scrape.csv')

    """
    next page clicks = 40
    class = num-applicants__caption
    """