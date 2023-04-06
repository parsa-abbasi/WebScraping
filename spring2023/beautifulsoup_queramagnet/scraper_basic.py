__author__ = "Parsa Abbasi"
__email__ = "parsa.abbasi1996@gmail.com"
__organization__ = "Quera"
__website__ = "https://parsa-abbasi.github.io/"
__version__ = "1.0.1"
__date__ = "2023-04-05"

import requests
from bs4 import BeautifulSoup
import numpy as np
import json
from tqdm import tqdm

start_page = 1

page = requests.get('https://quera.org/magnet/jobs')
soup = BeautifulSoup(page.content, 'html.parser')
end_page = int(soup.select('.css-1r51i74')[-2].text)
print('The last page number is', end_page)

collected_jobs = []

for page_num in tqdm(range(start_page, end_page+1)):
    # Get the page
    page = requests.get(f'https://quera.org/magnet/jobs?page={page_num}')
    # Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Find each jobs
    jobs = soup.select('.css-1g5o4an')

    for count, job in enumerate(jobs):
        # A dictionary to store information about the job
        result = {}
        
        # Find the title and its link
        title_tag = job.find('h2')
        result['title'] = title_tag.get_text()
        result['url'] = 'https://quera.org/' + title_tag.find('a').get('href')
        
        # Find the date
        result['date'] = job.select('.chakra-stack .css-nm8t2j span')[0].get('title')
        
        # Find the company name
        result['company'] = job.find(class_='chakra-text').get_text()
        
        # Find the location. Make it NaN if not available
        location = job.select('.chakra-stack .css-5ngv18 span')
        if len(location) == 1:
            result['location'] = location[0].get_text()
        else:
            result['location'] = np.nan
        
        # Extract the details spans such as level, type, salary, and remote
        details = job.select('.css-1iyteef span')
        result['level'] = details[0].get_text()
        result['type'] = details[1].get_text()
        result['salary'] = np.nan
        result['remote'] = np.nan
        # the third span is either salary or remote
        if len(details) >= 3:
            if 'دورکاری' in details[2].get_text():
                result['remote'] = details[2].get_text()
            else:
                result['salary'] = details[2].get_text()
        # if the fourth span exists, it is remote
        if len(details) >= 4:
            result['remote'] = details[3].get_text()
        
        # Find all technologies and sub-technologies
        technologies = job.find_all(class_='css-1ljl88f')
        result['technologies'] = [tech.get_text() for tech in technologies]
        sub_technologies = job.find_all(class_='css-1suxakh')
        result['sub_technologies'] = [tech.get_text() for tech in sub_technologies]

        # Append the result to the list
        collected_jobs.append(result)

# Save the results to a json file
with open("quera_magnet_basic.json", "w") as file:
    json.dump(collected_jobs, file)