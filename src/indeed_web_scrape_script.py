import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def extract_company_from_result(soup):
    """
    Outputs list of company names for each job posting from Indeed

    :params: soup object from Indeed search
    
    :returns: list of cleaned company names
    """
    companies = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        company = div.find_all(name='span', attrs={'class': 'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={'class': 'result-link-source'})
            for span in sec_try:
                companies.append(span.text.strip())
    return companies

def extract_job_title_from_result(soup): 
    """
    Outputs list of job titles for each posting from Indeed

    :params: soup object from Indeed search

    :returns: list of cleaned job titles
    """
    jobs = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            jobs.append(a['title'])
    return jobs

def extract_locations_from_results(soup):
    """
    Outputs list of locations for each job posting from Indeed

    :params: soup object from Indeed search

    :returns: list of cleaned locations for each job posting
    """
    locations = []
    for div in soup.find_all('div', attrs={'class': 'recJobLoc'}):
        loc = div['data-rc-loc']
        locations.append(loc)
    return locations

def extract_comprating_from_results(soup):
    """
    Outputs list of company ratings for each job posting from Indeed.
    If no company rating is available, returns None

    :params: soup object from Indeed search

    :returns: list of company ratings (floats) for each job posting
    """
    ratings = []
    for div in soup.find_all('div', attrs={'class': 'sjcl'}):
        span = div.find('span', attrs={'class': 'ratingsContent'})
        if span:
            rating = span.text.strip()
            ratings.append(float(rating))
        else:
            ratings.append(None)
    return ratings

def extract_easyapply_from_results(soup):
    """
    Outputs list consisting of whether or not the job can be easily applied for

    :params: soup object from Indeed search

    :returns: list consisting of whether or not the job can be easily applied for
    Easy Apply if the job is easy apply and Not Easy Apply if it is not
    """
    easy_apply = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        if div.find('span', attrs={'class': 'iaLabel'}):
            easy_apply.append('Easy Apply')
        elif div.find('span', attrs={'class': 'iaLabel'}) == None:
            easy_apply.append('Not Easy Apply')
    return easy_apply

def extract_url_from_results(soup):
    """
    Outputs list of urls for each job posting

    :params: soup object from Indeed search

    :returns: list of urls for each job posting
    """
    links = []
    final_links = []
    for div in soup.find_all('div', attrs={'class': 'title'}):
        for a in div.find_all('a', attrs={'target': '_blank'}):
            links.append(a['href'])

    for link in links:
        final_link = 'indeed.com' + link
        final_links.append(final_link)
    return final_links

def extract_summary_from_results(soup):
    """
    Outputs list of summaries for each job posting. Only includes the brief
    summary available on the search result page. Does not include the complete
    job summary.

    :params: soup object from Indeed search

    :returns: list of cleaned summaries for each job posting
    """
    summary_list = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        summary_div = div.find('div', attrs={'class': 'summary'})
        summary_list_temp = str()
        for li in summary_div.find_all('li'):
            summary_list_temp += f' {li.text.strip()}'
        summary_list.append(summary_list_temp)
    return summary_list

def extract_title_company_location_ea(soup):
    """
    Outputs jobs, company names, locations, easy apply or not, company ratings,
    and summaries from Indeed search page

    :params: soup object from Indeed search

    :returns: six lists: job titles, company names, locations, easy apply or not,
    company ratings, and search page summaries
    """
    jobs = extract_job_title_from_result(soup)
    companies = extract_company_from_result(soup)
    locations = extract_locations_from_results(soup)
    easy_apply = extract_easyapply_from_results(soup)
    ratings = extract_comprating_from_results(soup)
    summary = extract_summary_from_results(soup)
    return jobs, companies, locations, easy_apply, ratings, summary

def get_last_page(URL):
    """
    Outputs the last page number of a given search. Allows automation
    of checking how many pages a search yields

    :params: URL of Indeed search

    :returns: Last page number of search
    """

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, features='lxml')
    pn_list = []
    for pn in soup.find_all('span', attrs={'class': 'pn'}):
        page_number = list(pn.text)
        pn_list.append(page_number)
    if len(pn_list[-2]) > 1:
        last_page = int(pn_list[-2][0] + pn_list[-2][1])
    else:
        last_page = int(pn_list[-2][0])
    return last_page

def get_url_list(starting_url):
    """
    Outputs list of URLs for each available page of the search

    :params: starting_url: URL of first page of the search

    :returns: list of URLs for each page of the search
    """
    last_page = get_last_page(starting_url)
    ending_range = (last_page - 1) * 50
    start = [num for num in range(50, ending_range + 1, 50)]
    url_list = [starting_url]
    for i in start:
        base_url = starting_url
        page_num = f'&start={i}'
        base_url += page_num
        url_list.append(base_url)
    return url_list

def pull_all_allpages(url):
    """
    Pulls all information from entire Indeed search

    :params: URL from initial search page

    :returns: six lists: companies, jobs, locations, easy_apply, ratings,
    urls, summaries
    """
    url_list = get_url_list(url)
    companies = []
    jobs = []
    locations = []
    easy_apply = []
    ratings = []
    urls = []
    summaries = []
    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features='html.parser')
        jobs_temp = extract_job_title_from_result(soup)
        companies_temp = extract_company_from_result(soup)
        locations_temp = extract_locations_from_results(soup)
        easy_apply_temp = extract_easyapply_from_results(soup)
        ratings_temp = extract_comprating_from_results(soup)
        url_temp = extract_url_from_results(soup)
        summary_temp = extract_summary_from_results(soup)
        
        companies.extend(companies_temp)
        jobs.extend(jobs_temp)
        locations.extend(locations_temp)
        easy_apply.extend(easy_apply_temp)
        ratings.extend(ratings_temp)
        urls.extend(url_temp)
        summaries.extend(summary_temp)
        time.sleep(2)
    return companies, jobs, locations, easy_apply, ratings, urls, summaries

if __name__ == '__main__':
    list_of_locations = ['CO', 'CA', 'NY', 'WA', 'UT', 'FL']
    counter = 1
    for state in list_of_locations:
        print(f'{counter}/{len(list_of_locations)}: {state} Working')
        starting_url = f'https://www.indeed.com/jobs?q=data+science&l={state}&limit=50&radius=25'
        companies, jobs, locations, easy_apply, ratings, urls, summaries = pull_all_allpages(starting_url)
        df = pd.DataFrame()
        df['Companies'] = companies
        df['Jobs'] = jobs
        df['Locations'] = locations
        df['Easy_Apply'] = easy_apply
        df['Rating'] = ratings
        df['Summary'] = summaries
        df.to_csv(f'df_{state}')
        print(f'{counter}/{len(list_of_locations)}: {state} Complete!')
        counter += 1
    print('DONE!!!!')

