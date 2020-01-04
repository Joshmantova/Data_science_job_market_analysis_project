from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/jobs/search?keywords=data%20science&location=Denver%2C%20Colorado%2C%20United%20States&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0')

time.sleep(1)

# jobs = driver.find_elements_by_class_name("result-card__full-card-link")
# for posting in jobs:
#     posting.click()
#     time.sleep(2)

# see_more_jobs = driver.find_element_by_class_name("see-more-jobs")
# see_more_jobs.click()

jobs = driver.find_elements_by_class_name("result-card__full-card-link")
job_titles = []
for posting in jobs:
    posting.click()
    time.sleep(1)
    title = driver.find_element_by_class_name("topcard__title").text
    print(title)
    job_titles.append(title)
    time.sleep(1)

print(job_titles)
'''
class="result-card__full-card-link" 
class="see-more-jobs"
class="topcard__title" .text
class="topcard__org-name-link"  .text
class="topcard__flavor topcard__flavor--bullet"  .text
'''