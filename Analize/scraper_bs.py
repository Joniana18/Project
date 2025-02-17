# scraper_bs.py
import requests
from bs4 import BeautifulSoup

def scrape_jobs_from_pages(base_url, site_type, start_page=1, end_page=5):
    jobs = []
    
    if site_type == "punajuaj":
        start_page = end_page = 1  # Restrict to only the first page
    
    for page in range(start_page, end_page + 1):
        if site_type == "duapune":
            url = f"{base_url}?page={page}"
        elif site_type == "punajuaj":
            url = f"{base_url}/page/{page}/"
        
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        if site_type == "duapune":
            results = soup.find_all('div', class_='job-listing')
            for result in results:
                try:
                    job_title = result.find('h1', class_='job-title').find('a').text.strip()
                    company = result.find('small').find('a', style=True).text.strip()
                    location = result.find('span', class_='location').text.strip()
                    job_type = result.find('span', class_='time').text.strip()
                    expire = result.find('span', class_='expire').text.strip()
                    jobs.append([job_title, company, location, job_type, expire])
                except AttributeError:
                    continue

        elif site_type == "punajuaj":
            results = soup.find_all('div', class_='loop-item-content')
            for result in results:
                try:
                    job_title = result.find('h3', class_='loop-item-title').find('a').text.strip()
                    company = result.find('span', class_='job-company').text.strip() if result.find('span', class_='job-company') else 'No company found'
                    job_type = result.find('span', class_='job-type').text.strip() if result.find('span', class_='job-type') else 'No job type'
                    location = result.find('span', class_='job-location').text.strip() if result.find('span', class_='job-location') else 'No location found'
                    category = result.find('span', class_='job-category').text.strip() if result.find('span', class_='job-category') else 'No category'
                    language = result.find('span', class_='job-language').text.strip() if result.find('span', class_='job-language') else 'No language'
                    jobs.append([job_title, company, job_type, location, category, language])
                except AttributeError:
                    continue

        if not results:
            break  # Stop if no more jobs found

    return jobs
