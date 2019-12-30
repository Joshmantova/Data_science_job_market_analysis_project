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

def extract_comprating_from_results(soup):
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
    easy_apply = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        if div.find('span', attrs={'class': 'iaLabel'}):
            easy_apply.append('Easy Apply')
        elif div.find('span', attrs={'class': 'iaLabel'}) == None:
            easy_apply.append('Not Easy Apply')
    return easy_apply

def extract_url_from_results(soup):
    links = []
    final_links = []
    # for div in soup.find_all('div', attrs={'class': 'row'}):
    for div in soup.find_all('div', attrs={'class': 'title'}):
        for a in div.find_all('a', attrs={'target': '_blank'}):
            links.append(a['href'])

    for link in links:
        final_link = 'indeed.com' + link
        final_links.append(final_link)
    return final_links

def extract_summary_from_results(soup):
    summary_list = []
    for div in soup.find_all('div', attrs={'class': 'row'}):
        summary_div = div.find('div', attrs={'class': 'summary'})
        summary_list_temp = str()
        for li in summary_div.find_all('li'):
            summary_list_temp += f' {li.text.strip()}'
        summary_list.append(summary_list_temp)
    return summary_list

def extract_title_company_location_ea(soup):
    jobs = extract_job_title_from_result(soup)
    companies = extract_company_from_result(soup)
    locations = extract_locations_from_results(soup)
    easy_apply = extract_easyapply_from_results(soup)
    ratings = extract_comprating_from_results(soup)
    summary = extract_summary_from_results(soup)
    return jobs, companies, locations, easy_apply, ratings, summary

def get_last_page(URL):
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

if __name__ == '__main__':
    URL = 'https://www.indeed.com/jobs?q=data+science&l=NY&limit=50&radius=25'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, features='lxml')
    companies = extract_company_from_result(soup)
    jobs = extract_job_title_from_result(soup)
    urls = extract_url_from_results(soup)
    summaries = extract_summary_from_results(soup)
    print(f'Company len: {len(companies)}, jobs len: {len(jobs)}, url len: {len(urls)} summary len: {len(summaries)}')
