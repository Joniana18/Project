import asyncio
from pyppeteer import launch
import pandas as pd

async def scrape_all_jobs_pyppeteer(base_url, site_type, start_page=1, end_page=5):
    browser = await launch(headless=True)
    page = await browser.newPage()
    all_jobs = []

    current_page = start_page
    while True:
        if site_type == "duapune":
            url = f"{base_url}?page={current_page}"
        elif site_type == "punajuaj":
            url = f"{base_url}/page/{current_page}/"
        
        await page.goto(url)
        await page.waitForSelector("body")  # Wait for the page to load

        if site_type == "duapune":
            job_elements = await page.querySelectorAll("div.job-listing")
        elif site_type == "punajuaj":
            job_elements = await page.querySelectorAll("div.loop-item-content")

        print(f"Page {current_page}: Found {len(job_elements)} jobs")  # Debugging

        if not job_elements:
            print("No job elements found, stopping...")
            break  # Stop if no more jobs found

        for job_element in job_elements:
            try:
                if site_type == "duapune":
                    title = await page.evaluate('(element) => element.querySelector("h1.job-title a").innerText', job_element)
                    company = await page.evaluate('(element) => element.querySelector("small a[style]").innerText', job_element) if await page.querySelector("small a[style]") else "No company found"
                    job_type = await page.evaluate('(element) => element.querySelector("span.time").innerText', job_element) if await page.querySelector("span.time") else "No job type"
                    location = await page.evaluate('(element) => element.querySelector("span.location").innerText', job_element) if await page.querySelector("span.location") else "No location found"
                    expire = await page.evaluate('(element) => element.querySelector("span.expire").innerText', job_element) if await page.querySelector("span.expire") else "No expire date"
                    job_data = {
                        "Title": title,
                        "Company": company,
                        "Job Type": job_type,
                        "Location": location,
                        "Expire": expire
                    }
                elif site_type == "punajuaj":
                    title = await page.evaluate('(element) => element.querySelector("h3.loop-item-title a").innerText', job_element)
                    company = await page.evaluate('(element) => element.querySelector("span.job-company").innerText', job_element) if await page.querySelector("span.job-company") else "No company found"
                    job_type = await page.evaluate('(element) => element.querySelector("span.job-type").innerText', job_element) if await page.querySelector("span.job-type") else "No job type"
                    location = await page.evaluate('(element) => element.querySelector("span.job-location").innerText', job_element) if await page.querySelector("span.job-location") else "No location found"
                    category = await page.evaluate('(element) => element.querySelector("span.job-category").innerText', job_element) if await page.querySelector("span.job-category") else "No category"
                    language = await page.evaluate('(element) => element.querySelector("span.job-language").innerText', job_element) if await page.querySelector("span.job-language") else "No language"
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
        next_button = await page.querySelector("a.next.page-numbers")
        if not next_button:
            print("No next button found, stopping...")
            break  # Stop if no "Next" button is found

        current_page += 1

    await browser.close()
    return pd.DataFrame(all_jobs)

def scrape_all_jobs(base_url, site_type, start_page=1, end_page=5):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(scrape_all_jobs_pyppeteer(base_url, site_type, start_page, end_page))
