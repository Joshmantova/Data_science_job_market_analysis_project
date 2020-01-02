from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://www.google.com/search?q=data+science&rlz=1C5CHFA_enUS875US875&oq=google+jobs&aqs=chrome..69i57j0l4j69i60l3.1489j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwi8ocOV8uPmAhXEBc0KHUA_Dt0QiYsCKAB6BAgIEAM#fpstate=tldetail&htivrt=jobs&htidocid=7wbZ6K1a4VsVyeEyAAAAAA%3D%3D')
# driver.get('https://www.wikipedia.org/')

def scroll_to_bottom(driver):
    # driver = self.browser
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
 
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
 
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

jobs = driver.find_elements_by_class_name('BjJfJf')
scroll_to_bottom(driver)
job_list = []
for job in jobs:
    job_list.append(job.text)
    time.sleep(.5)

# driver.execute_script('window.scrollTo()')
# driver.

print(job_list)

# driver.close()

'''
"BjJfJf cPd5d gsrt"
'''