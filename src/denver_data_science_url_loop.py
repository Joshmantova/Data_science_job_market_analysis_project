import indeed_web_scrape_script as iwss
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_url_list(starting_url):
    last_page = iwss.get_last_page(starting_url)
    ending_range = (last_page - 1) * 50
    start = [num for num in range(50, ending_range + 1, 50)]
    url_list = [starting_url]
    for i in start:
        base_url = starting_url
        page_num = f'&start={i}'
        base_url += page_num
        url_list.append(base_url)
    return url_list

def pull_jobs_comp_loc_allpages(url):
    url_list = get_url_list(url)
    companies = []
    jobs = []
    locations = []
    easy_apply = []
    ratings = []
    urls = []
    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features='html.parser')
        jobs_temp = iwss.extract_job_title_from_result(soup)
        companies_temp = iwss.extract_company_from_result(soup)
        locations_temp = iwss.extract_locations_from_results(soup)
        easy_apply_temp = iwss.extract_easyapply_from_results(soup)
        ratings_temp = iwss.extract_comprating_from_results(soup)
        url_temp = iwss.extract_url_from_results(soup)
        # jobs_temp, companies_temp, locations_temp, easy_apply_temp, ratings_temp = iwss.extract_title_company_location_ea(soup)
        
        companies.extend(companies_temp)
        jobs.extend(jobs_temp)
        locations.extend(locations_temp)
        easy_apply.extend(easy_apply_temp)
        ratings.extend(ratings_temp)
        urls.extend(url_temp)
        time.sleep(2)
    return companies, jobs, locations, easy_apply, ratings, urls

if __name__ == '__main__':

    starting_url = 'https://www.indeed.com/jobs?q=data+science&l=CO&limit=50&radius=25'

    companies, jobs, locations, easy_apply, ratings, urls = pull_jobs_comp_loc_allpages(starting_url)

    # df = pd.DataFrame()
    # df['Company_Name'] = companies
    # df['Job_Title'] = jobs
    # df['Location'] = locations
    # df['Easy_Apply'] = easy_apply
    # df['Rating'] = ratings
    # # df['URL'] = urls

    print(f'Company len: {len(companies)}, jobs len: {len(jobs)}, url len: {len(urls)}')
