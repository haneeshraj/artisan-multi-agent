from selenium.webdriver.common.by import By
from scraper.selenium_driver import SeleniumDriver
import time
from datetime import datetime
import os
import json


def scrape_linkedin_job(url):
    """
    Scrape job details from a LinkedIn job listing page.

    Args:
        url (str): The URL of the LinkedIn job listing page.
    Returns:
        tuple: A tuple containing the paths of the saved JSON and Markdown files.
    
    """

    print("🚀 Starting LinkedIn job details scraper...")

    try:
        with SeleniumDriver(headless=False, stealth_mode=False) as driver:
            print(f"📄 Loading LinkedIn job page: {url}")
            if not driver.get_page(url):
                print("❌ Failed to load LinkedIn job page")
                return None
            

            print("🔍 Extracting job title...")
            title_element = driver.wait_for_element((By.CSS_SELECTOR, "h1.top-card-layout__title"), timeout=20)
            title = title_element.text.strip() if title_element else "N/A"

            print("🔍 Extracting company name...")
            # div.job-details-jobs-unified-top-card__company-name
            company_element = driver.wait_for_element((By.CSS_SELECTOR, "span.topcard__flavor"), timeout=20)
            company = company_element.text.strip() if company_element else "N/A"

            print("🔍 Extracting job location..."
                  )
            # topcard__flavor topcard__flavor--bullet
            location_element = driver.wait_for_element((By.CSS_SELECTOR, "span.topcard__flavor--bullet"), timeout=20)
            location = location_element.text.strip() if location_element else "N/A"

            print("🔍 Looking for and removing any overlays...")
            try:
                driver.driver.execute_script("""
                    const overlays = document.getElementsByClassName('modal__overlay--visible');
                    if (overlays.length > 0) {
                        for (let i = 0; i < overlays.length; i++) {
                            overlays[i].remove();
                        }
                        return "✅ Overlay removed successfully";
                    }
                    return "No overlays found";
                """)
                time.sleep(1)  # Small wait after removing overlay
            except Exception as e:
                print(f"⚠️ Error while attempting to remove overlay: {e}")

            

            # Click "Show more" to reveal the full job description
            print("🔍 Clicking 'Show more' to reveal additional job details..." )
            show_more_button = driver.wait_for_element(
                (By.CSS_SELECTOR, "button.show-more-less-html__button--more"),
                timeout=10
            )
            if show_more_button:
                show_more_button.click()
            else:
                print("⚠️ 'Show more' button not found")
            

            time.sleep(2)  # Wait for the content to load after clicking "Show more"

            print("🔍 Extracting complete job description using JavaScript...")
            description = "N/A"
            try:
                js_description = driver.driver.execute_script("""
                    const descriptionElement = document.getElementsByClassName('show-more-less-html__markup')[0];
                    if (descriptionElement) {
                        return descriptionElement.innerText;
                    } else {
                        return "N/A";
                    }
                """)
                
                if js_description == "N/A":
                    print("⚠️ Could not find description element with JavaScript")
                    # Fall back to the previous method
                    description_element = driver.wait_for_element(
                        (By.CSS_SELECTOR, "div.show-more-less-html__markup"), 
                        timeout=20
                    )
                    description = description_element.text.strip() if description_element else "N/A"
                else:
                    print("✅ Successfully extracted complete job description with JavaScript")
                    description = js_description
            except Exception as e:
                print(f"⚠️ JavaScript extraction failed: {e}")
                # Fall back to the previous method
                try:
                    description_element = driver.wait_for_element(
                        (By.CSS_SELECTOR, "div.show-more-less-html__markup"), 
                        timeout=20
                    )
                    description = description_element.text.strip() if description_element else "N/A"
                except Exception as e2:
                    print(f"❌ Both extraction methods failed. Error: {e2}")
                    description = "N/A"

            print("✅ Successfully extracted job details")

            job_details = {
                "url": url,
                "title": title,
                "company": company,
                "location": location ,

                "description": description
            }

            print(f"📄 Job details extracted!")

            # Save job details to JSON and Markdown files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            import json
            import os
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-json')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'linkedin_{title.replace(" ", "_")}_{timestamp}.json')
            output_file = os.path.abspath(output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(job_details, f, ensure_ascii=False, indent=4)
            # Write job details in Markdown format
            output_md_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-md')
            os.makedirs(output_md_dir, exist_ok=True)
            output_md_file = os.path.join(output_md_dir, f'linkedin_{title.replace(" ", "_")}_{timestamp}.md')
            output_md_file = os.path.abspath(output_md_file)
            with open(output_md_file, 'w', encoding='utf-8') as f:
                f.write(f"# Job Title: {job_details['title']}\n")
                f.write(f"**Company:** {job_details['company']}\n")
                f.write(f"**Location:** {job_details['location']}\n")
                f.write("\n## Job Description:\n")
                f.write(job_details['description'])

            print(f"✅ Job details saved to {output_file} and {output_md_file}")
            print("📂 Job details successfully saved to JSON and Markdown files.")
            # Return the paths of the saved files
            return (output_file, output_md_file)



    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        return None
    

