import requests
from bs4 import BeautifulSoup

def extract_company_from_result(soup):
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
    jobs = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            jobs.append(a['title'])
    return jobs
 
def extract_locations_from_results(soup):
    locations = []
    for div in soup.find_all('div', attrs={'class': 'recJobLoc'}):
        loc = div['data-rc-loc']
        locations.append(loc)
    return locations

def extract_title_company_location(soup):
    jobs = extract_job_title_from_result(soup)
    companies = extract_company_from_result(soup)
    locations = extract_locations_from_results(soup)
    return jobs, companies, locations

def get_last_page(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, features='lxml')
    pn_list = []
    for pn in soup.find_all('span', attrs={'class': 'pn'}):
        page_number = list(pn.text)
        pn_list.append(page_number)
    last_page = int(pn_list[-2][0])
    return last_page

if __name__ == '__main__':
    pass

