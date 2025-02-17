from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def scrape_all_jobs_selenium(base_url, site_type, start_page=1, end_page=5):
    options = webdriver.ChromeOptions()
    # Remove headless mode to see the browser
    # options.add_argument('--headless')  # Comment this line to keep it visible

    driver = webdriver.Chrome(options=options)
    all_jobs = []

    try:
        if site_type == "punajuaj":
            start_page = end_page = 1  # Force to only scrape the first page

        for page in range(start_page, end_page + 1):
            if site_type == "duapune":
                url = f"{base_url}?page={page}"
            elif site_type == "punajuaj":
                url = f"{base_url}/page/{page}/"
            
            driver.get(url)
            time.sleep(5)  # Increase time to allow full page load

            if site_type == "duapune":
                job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-listing")
            elif site_type == "punajuaj":
                job_elements = driver.find_elements(By.CSS_SELECTOR, "div.loop-item-content")

            print(f"Page {page}: Found {len(job_elements)} jobs")  # Debugging

            if not job_elements:
                print("No job elements found, stopping...")
                break  # Stop if no more jobs found

            for job_element in job_elements:
                try:
                    title = job_element.find_element(By.CSS_SELECTOR, "h3.loop-item-title a").text.strip()
                    company = job_element.find_element(By.CSS_SELECTOR, "span.job-company").text.strip() if job_element.find_elements(By.CSS_SELECTOR, "span.job-company") else "No company found"
                    job_type = job_element.find_element(By.CSS_SELECTOR, "span.job-type").text.strip() if job_element.find_elements(By.CSS_SELECTOR, "span.job-type") else "No job type"
                    location = job_element.find_element(By.CSS_SELECTOR, "span.job-location").text.strip() if job_element.find_elements(By.CSS_SELECTOR, "span.job-location") else "No location found"
                    category = job_element.find_element(By.CSS_SELECTOR, "span.job-category").text.strip() if job_element.find_elements(By.CSS_SELECTOR, "span.job-category") else "No category"
                    language = job_element.find_element(By.CSS_SELECTOR, "span.job-language").text.strip() if job_element.find_elements(By.CSS_SELECTOR, "span.job-language") else "No language"

                    job_data = {
                        "Title": title,
                        "Company": company,
                        "Job Type": job_type,
                        "Location": location,
                        "Category": category,
                        "Language": language
                    }

                    all_jobs.append(job_data)
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue
    
    finally:
        driver.quit()

    return pd.DataFrame(all_jobs)
