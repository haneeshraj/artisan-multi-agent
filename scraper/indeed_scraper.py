from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium_driver import SeleniumDriver
import time
from datetime import datetime

def scrape_indeed_job(url):
    """
    Scrape job details from an Indeed job listing page.
    Args:
        url (str): The URL of the Indeed job listing page.
    Returns:
        tuple: A tuple containing the paths of the saved JSON and Markdown files.
    
    """

    print("🚀 Starting indeed job details scraper...")

    try:
        with SeleniumDriver(headless=False, stealth_mode=True) as driver:  # Try stealth mode to bypass some detection
            print(f"📄 Loading Indeed job page: {url}")
            
            if not driver.get_page(url):
                print("❌ Failed to load Indeed job page")
                return None
                
            # Check for CAPTCHA and wait for manual solving
            print("⏳ Waiting for page to load and checking for CAPTCHA...")
            print("💡 If you see a CAPTCHA, please solve it manually in the browser window.")
            print("💡 You'll have 60 seconds to solve any CAPTCHA before the script continues.")
            
            # Give user time to solve CAPTCHA if it appears
            time.sleep(30)
            
            # Try to detect if we're still on a CAPTCHA page
            try:
                # Look for title element as indication we've passed CAPTCHA
                driver.wait_for_element((By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title"), timeout=5)
                print("✅ Page loaded successfully!")
            except TimeoutException:
                print("⚠️ Still waiting for job page to load fully...")
                print("💡 You have 30 more seconds to solve any CAPTCHA if present.")
                time.sleep(30)  # Additional time if needed
                
            # Extract job title
            print("🔍 Extracting job title..." )
            #<h1 class="jobsearch-JobInfoHeader-title css-1lipiqt e1tiznh50" lang="en" dir="ltr" data-testid="jobsearch-JobInfoHeader-title"><span>Principal AI/ML Scientist</span></h1>
            title_element = driver.wait_for_element((By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title"), timeout=20)
            if not title_element:
                print("❌ Failed to find job title element")
                print("📸 Taking screenshot for debugging...")
                driver.take_screenshot("indeed_scraper_no_title.png")
                print("⚠️ This could be due to a CAPTCHA or the page structure has changed.")
                print("💡 Check the screenshot to see if a CAPTCHA is present.")
                return None
            title = title_element.text.strip()
            print(f"✅ Successfully extracted job title: {title}")
            
           
            company_element = driver.wait_for_element((By.CSS_SELECTOR, "div[data-company-name='true'] a"), timeout=20)
            company = company_element.text.strip() if company_element else "N/A"

            # <div data-testid="inlineHeader-companyLocation" class="css-1vysp2z eu4oa1w0"><div data-testid="job-location" class="css-dgqgie eu4oa1w0">22 Adelaide Street West, Suite 2500, Toronto, ON M5H 4E3</div></div>
            location_element = driver.wait_for_element((By.CSS_SELECTOR, "div[data-testid='inlineHeader-companyLocation'] div[data-testid='job-location']"), timeout=20)
            location = location_element.text.strip() if location_element else "N/A"

            # <div id="jobDescriptionText" class="jobsearch-JobComponent-description css-1rybqxq eu4oa1w0">
            description_element = driver.wait_for_element((By.ID, "jobDescriptionText"), timeout=20)
            description = description_element.text.strip() if description_element else "N/A"

            print("✅ Successfully extracted job details")

            job_details = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": url,
            }

            # Write job details as a json file to D:\2025\DS-AI-ML-GEN\ai-artisan\data\scraped-data\raw-json we are currently in D:\2025\DS-AI-ML-GEN\ai-artisan/scraper
            
            file_name = f'indeed_{url.split("&jk=")[1].split("&")[0]}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

            import json
            import os
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-json')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'{file_name}.json')
            output_file = os.path.abspath(output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(job_details, f, ensure_ascii=False, indent=4)

            # Write job details in md format to D:\2025\DS-AI-ML-GEN\ai-artisan\data\scraped-data\raw-md
            output_md_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-md')
            os.makedirs(output_md_dir, exist_ok=True)
            output_md_file = os.path.join(output_md_dir, f'{file_name}.md')
            output_md_file = os.path.abspath(output_md_file)
            with open(output_md_file, 'w', encoding='utf-8') as f:
                f.write(f"# Job Title: {job_details['title']}\n")
                f.write(f"**Company:** {job_details['company']}\n")
                f.write(f"**Location:** {job_details['location']}\n")
                f.write("\n## Job Description:\n")
                f.write(job_details['description'])
            print(f"✅ Job details saved to {output_file} and {output_md_file}")
            print("📂 Job details successfully saved to JSON and Markdown files."
                  )
            
            # For now, just returning the job title as a proof of concept
            return (output_file, output_md_file)
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        return None
    

def main():
    """Main function to run the Indeed job scraper"""
    print("Indeed Job Scraper")
    print("=" * 40)
    
    # Example Indeed job URL
    url = "https://ca.indeed.com/viewjob?from=app-tracker-saved-appcard&hl=en&jk=e2feb32ddb471717&tk=1ivcfuj5vg2ao800"
    
    job_title = scrape_indeed_job(url)
    if job_title:
        print(f"\n🎉 Successfully extracted job details")
    else:
        print("\n💔 Failed to extract job details")
    
if __name__ == "__main__":
    main()