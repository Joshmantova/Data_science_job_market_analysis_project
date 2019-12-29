import requests
from bs4 import BeautifulSoup
import time
import indeed_web_scrape_script as iwss
import denver_data_science_url_loop as ddsul
import pandas as pd

if __name__ == '__main__':

    list_of_locations = ['CO', 'CA', 'NY', 'WA', 'UT', 'FL']

    for state in list_of_locations:
        starting_url = f'https://www.indeed.com/jobs?q=data+science&l={state}&limit=50&radius=25'
        companies, jobs, locations, easy_apply, ratings = ddsul.pull_all_allpages(starting_url)
        df_name = f'df_{state}'
        df_name = pd.DataFrame()
        df_name['Companies'] = companies
        df_name['Jobs'] = jobs
        df_name['Locations'] = locations
        df_name['easy_apply'] = easy_apply
        print(df_name)
    
    print('DONE!!!!')

    # print(f'The last past of this search is page #: {iwss.get_last_page(starting_url)}')

    # companies, jobs, locations, easy_apply = iwss.pull_jobs_comp_loc_allpages(starting_url)