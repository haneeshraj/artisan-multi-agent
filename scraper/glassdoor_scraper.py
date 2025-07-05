from selenium.webdriver.common.by import By
from selenium_driver import SeleniumDriver
import time
from datetime import datetime


def scrape_glassdoor_job(url):
    """
    Scrape job details from a Glassdoor job listing page.

    Args:

        url (str): The URL of the Glassdoor job listing page.
    Returns:
        tuple: A tuple containing the paths of the saved JSON and Markdown files.

  
    """
    print("🚀 Starting Glassdoor job details scraper...")

    try:
        with SeleniumDriver(headless=False, stealth_mode=False) as driver:
            print(f"📄 Loading Glassdoor job page: {url}")
            if not driver.get_page(url):
                print("❌ Failed to load Glassdoor job page")
                return None

            print("🔍 Extracting job title...")

            # Title selector class name - heading_Heading__BqX5J heading_Level1__soLZs
            title_element = driver.wait_for_element((By.CSS_SELECTOR, "h1.heading_Heading__BqX5J.heading_Level1__soLZs"))
            title = title_element.text.strip() if title_element else "N/A"

            # Company name selector class name - (div - EmployerProfile_employerNameHeading__bXBYr)
            print("🔍 Extracting company name...")
            company_element = driver.wait_for_element((By.CSS_SELECTOR, "div.EmployerProfile_employerNameHeading__bXBYr"))
            company = company_element.text.strip() if company_element else "N/A"
            
            # Job location - <div data-test="location">Markham</div>
            print("🔍 Extracting job location...")
            location_element = driver.wait_for_element((By.CSS_SELECTOR, "div[data-test='location']"))
            location = location_element.text.strip() if location_element else "N/A"

            # Job salary -  (div - SalaryEstimate_salaryRange__brHFy)
            print("🔍 Extracting job salary...")
            salary_element = driver.wait_for_element((By.CSS_SELECTOR, "div.SalaryEstimate_salaryRange__brHFy"))
            salary = salary_element.text.strip() if salary_element else "N/A"

            # Click "Show more" - <button aria-expanded="false" aria-haspopup="true" class="ShowMoreCTA_showMore__EtZpZ ShowMoreCTA_spacing-md__bS21L" type="button" data-test="show-more-cta"><span>Show more</span><img alt="" aria-hidden="true" class="" src="/job-search-next/assets/chevron.svg"></button>

            show_more_button = driver.wait_for_element((By.CSS_SELECTOR, "button.ShowMoreCTA_showMore__EtZpZ"), timeout=10)
            if show_more_button:
                print("🔍 Clicking 'Show more' to reveal additional job details...")
                show_more_button.click()
            else:
                print("⚠️ 'Show more' button not found, skipping additional details.")

            time.sleep(2)  # Wait for the content to load after clicking "Show more"

            # Job description - (div - class = JobDetails_jobDescription__uW_fK JobDetails_showHidden__C_FOA)
            description_element = driver.wait_for_element((By.CSS_SELECTOR, "div.JobDetails_jobDescription__uW_fK.JobDetails_showHidden__C_FOA"))
            description = description_element.text.strip() if description_element else "N/A"

            print("✅ Successfully extracted job details")

            job_details = {
                "url": url,
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "description": description
            }

            # Write job details as a json file to D:\2025\DS-AI-ML-GEN\ai-artisan\data\scraped-data\raw-json we are currently in D:\2025\DS-AI-ML-GEN\ai-artisan/scraper
            
            file_name = f'glassdoor_{url.split("/job-listing/")[1].split("-JV")[0]}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

            import json
            import os
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-json')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'{file_name}.json')
            # Convert to absolute path
            output_file = os.path.abspath(output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(job_details, f, ensure_ascii=False, indent=4)
            
            # Write job details in md format to D:\2025\DS-AI-ML-GEN\ai-artisan\data\scraped-data\raw-md
            output_md_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-md')
            os.makedirs(output_md_dir, exist_ok=True)
            output_md_file = os.path.join(output_md_dir, f'{file_name}.md')
            # Convert to absolute path
            output_md_file = os.path.abspath(output_md_file)
            with open(output_md_file, 'w', encoding='utf-8') as f:
                f.write(f"# Job Title: {job_details['title']}\n")
                f.write(f"**Company:** {job_details['company']}\n")
                f.write(f"**Location:** {job_details['location']}\n")
                f.write(f"**Salary:** {job_details['salary']}\n")
                f.write("\n## Job Description:\n")
                f.write(job_details['description'])
            print(f"✅ Job details saved to {output_file} and {output_md_file}")
            print("📂 Job details successfully saved to JSON and Markdown files."
                  )
            
            # return the path of the saved json file and md file as a tuple
            return (output_file, output_md_file)
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        return None
