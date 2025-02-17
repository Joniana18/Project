from requests_html import HTMLSession
import pandas as pd

def scrape_all_jobs_requests_html(base_url, site_type, start_page=1, end_page=5):
    session = HTMLSession()
    all_jobs = []

    page = start_page
    while True:
        if site_type == "duapune":
            url = f"{base_url}?page={page}"
        elif site_type == "punajuaj":
            url = f"{base_url}/page/{page}/"
        
        response = session.get(url)
        response.html.render(sleep=5)  # Render the JavaScript

        if site_type == "duapune":
            job_elements = response.html.find("div.job-listing")
        elif site_type == "punajuaj":
            job_elements = response.html.find("div.loop-item-content")

        print(f"Page {page}: Found {len(job_elements)} jobs")  # Debugging

        if not job_elements:
            print("No job elements found, stopping...")
            break  # Stop if no more jobs found

        for job_element in job_elements:
            try:
                if site_type == "duapune":
                    title = job_element.find("h1.job-title a", first=True).text.strip()
                    company = job_element.find("small a[style]", first=True).text.strip() if job_element.find("small a[style]", first=True) else "No company found"
                    job_type = job_element.find("span.time", first=True).text.strip() if job_element.find("span.time", first=True) else "No job type"
                    location = job_element.find("span.location", first=True).text.strip() if job_element.find("span.location", first=True) else "No location found"
                    expire = job_element.find("span.expire", first=True).text.strip() if job_element.find("span.expire", first=True) else "No expire date"
                    job_data = {
                        "Title": title,
                        "Company": company,
                        "Job Type": job_type,
                        "Location": location,
                        "Expire": expire
                    }
                elif site_type == "punajuaj":
                    title = job_element.find("h3.loop-item-title a", first=True).text.strip()
                    company = job_element.find("span.job-company", first=True).text.strip() if job_element.find("span.job-company", first=True) else "No company found"
                    job_type = job_element.find("span.job-type", first=True).text.strip() if job_element.find("span.job-type", first=True) else "No job type"
                    location = job_element.find("span.job-location", first=True).text.strip() if job_element.find("span.job-location", first=True) else "No location found"
                    category = job_element.find("span.job-category", first=True).text.strip() if job_element.find("span.job-category", first=True) else "No category"
                    language = job_element.find("span.job-language", first=True).text.strip() if job_element.find("span.job-language", first=True) else "No language"
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

        # Check for the presence of a "Next" button
        next_button = response.html.find("a.next.page-numbers", first=True)
        if not next_button:
            print("No next button found, stopping...")
            break  # Stop if no "Next" button is found

        page += 1

    return pd.DataFrame(all_jobs)
