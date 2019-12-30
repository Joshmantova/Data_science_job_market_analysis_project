import requests
from bs4 import BeautifulSoup
import time
import indeed_web_scrape_script as iwss
import denver_data_science_url_loop as ddsul
import pandas as pd

if __name__ == '__main__':

    list_of_locations = ['CO', 'CA', 'NY', 'WA', 'UT', 'FL']
    counter = 1
    for state in list_of_locations:
        print(f'{counter}/{len(list_of_locations)}: {state} Working')
        starting_url = f'https://www.indeed.com/jobs?q=data+science&l={state}&limit=50&radius=25'
        companies, jobs, locations, easy_apply, ratings, urls, summaries = ddsul.pull_all_allpages(starting_url)
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

    # print(f'The last past of this search is page #: {iwss.get_last_page(starting_url)}')

    # companies, jobs, locations, easy_apply = iwss.pull_jobs_comp_loc_allpages(starting_url)