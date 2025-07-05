# SeleniumDriver Class - Complete Usage Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Basic Usage](#basic-usage)
4. [Configuration Options](#configuration-options)
5. [Core Methods](#core-methods)
6. [Advanced Features](#advanced-features)
7. [Anti-Detection Features](#anti-detection-features)
8. [Real-World Examples](#real-world-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

The `SeleniumDriver` class is a comprehensive wrapper around Selenium WebDriver designed specifically for web scraping. It includes built-in anti-detection features, human-like behavior simulation, and error handling to make your scraping projects more reliable and less detectable.

### Key Features:

- ✅ **Anti-Detection**: Undetected ChromeDriver integration
- ✅ **Human Simulation**: Random delays, realistic typing patterns
- ✅ **Error Handling**: Robust exception handling and retries
- ✅ **Flexibility**: Configurable timeouts, headless/headful modes
- ✅ **Convenience**: Context manager support, utility methods

---

## 🔧 Installation & Setup

### Prerequisites

Make sure you have installed the required packages:

```bash
pip install -r requirements.txt
```

### Import the Class

```python
from scraper.selenium_driver import SeleniumDriver, create_stealth_driver, create_fast_driver
from selenium.webdriver.common.by import By
```

---

## 🚀 Basic Usage

### Method 1: Direct Instantiation

```python
# Create driver instance
driver = SeleniumDriver(headless=False, stealth_mode=True)

# Start the driver
driver.start_driver()

# Navigate to a page
driver.get_page("https://example.com")

# Perform actions...
driver.safe_click((By.ID, "button-id"))

# Close when done
driver.close_driver()
```

### Method 2: Context Manager (Recommended)

```python
# Automatically handles driver startup and cleanup
with SeleniumDriver(headless=False, stealth_mode=True) as driver:
    driver.get_page("https://example.com")
    element = driver.wait_for_element((By.CLASS_NAME, "content"))
    if element:
        print("Element found!")
```

### Method 3: Quick Setup Functions

```python
# For stealth scraping (recommended for LinkedIn, Glassdoor)
with create_stealth_driver(headless=False) as driver:
    driver.get_page("https://linkedin.com")
    # Your scraping logic here

# For fast scraping (good for Indeed, simple sites)
with create_fast_driver(headless=True) as driver:
    driver.get_page("https://indeed.com")
    # Your scraping logic here
```

---

## ⚙️ Configuration Options

### Constructor Parameters

```python
SeleniumDriver(
    headless=False,              # Run browser in background
    stealth_mode=True,           # Use undetected-chromedriver
    window_size="1920,1080",     # Browser window dimensions
    timeout=10,                  # Default element wait timeout
    page_load_timeout=30,        # Page load timeout
    custom_user_agent=None       # Custom user agent string
)
```

### Configuration Examples

```python
# Stealth mode for difficult sites
stealth_driver = SeleniumDriver(
    headless=False,
    stealth_mode=True,
    timeout=15,
    page_load_timeout=45
)

# Fast mode for simple scraping
fast_driver = SeleniumDriver(
    headless=True,
    stealth_mode=False,
    timeout=5,
    page_load_timeout=15
)

# Custom configuration
custom_driver = SeleniumDriver(
    headless=False,
    stealth_mode=True,
    window_size="1366,768",
    custom_user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
```

---

## 🛠️ Core Methods

### Navigation Methods

#### `get_page(url, wait_time=None)`

Navigate to a URL with automatic delays.

```python
# Basic navigation
success = driver.get_page("https://example.com")

# With custom wait time
success = driver.get_page("https://example.com", wait_time=3.0)

if success:
    print("Page loaded successfully")
else:
    print("Failed to load page")
```

### Element Interaction Methods

#### `wait_for_element(locator, timeout=None)`

Wait for a single element to appear.

```python
# Wait for element with default timeout
element = driver.wait_for_element((By.ID, "login-button"))

# Wait with custom timeout
element = driver.wait_for_element((By.CLASS_NAME, "job-card"), timeout=20)

if element:
    print(f"Element text: {element.text}")
else:
    print("Element not found")
```

#### `wait_for_elements(locator, timeout=None)`

Wait for multiple elements.

```python
# Get all job listings
job_elements = driver.wait_for_elements((By.CLASS_NAME, "job-listing"))

print(f"Found {len(job_elements)} job listings")
for job in job_elements:
    print(job.text)
```

#### `safe_click(locator, timeout=None)`

Click an element safely with scrolling and error handling.

```python
# Click login button
success = driver.safe_click((By.ID, "login-btn"))

# Click with custom timeout
success = driver.safe_click((By.XPATH, "//button[text()='Next']"), timeout=15)

if success:
    print("Button clicked successfully")
```

#### `safe_send_keys(locator, text, clear_first=True, timeout=None)`

Type text with human-like behavior.

```python
# Type in username field
success = driver.safe_send_keys((By.ID, "username"), "your_username")

# Type without clearing first
success = driver.safe_send_keys(
    (By.ID, "search-box"),
    "Python Developer",
    clear_first=False
)

# Type with custom timeout
success = driver.safe_send_keys(
    (By.NAME, "email"),
    "user@example.com",
    timeout=10
)
```

### Utility Methods

#### `scroll_to_bottom(pause_time=1.0, max_scrolls=10)`

Scroll to load more content (useful for infinite scroll pages).

```python
# Basic scrolling
driver.scroll_to_bottom()

# Custom scrolling behavior
driver.scroll_to_bottom(pause_time=2.0, max_scrolls=5)
```

#### `take_screenshot(filename)`

Capture screenshots for debugging.

```python
# Take screenshot
success = driver.take_screenshot("debug_screenshot.png")

# Take screenshot with timestamp
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
driver.take_screenshot(f"screenshot_{timestamp}.png")
```

#### `get_page_source()`

Get the HTML source of the current page.

```python
html_content = driver.get_page_source()
if html_content:
    print(f"Page has {len(html_content)} characters")
```

---

## 🔥 Advanced Features

### Locator Strategies

```python
# Common locator patterns
locators = {
    'by_id': (By.ID, "element-id"),
    'by_class': (By.CLASS_NAME, "class-name"),
    'by_xpath': (By.XPATH, "//div[@class='container']//a"),
    'by_css': (By.CSS_SELECTOR, "div.job-card h3"),
    'by_tag': (By.TAG_NAME, "button"),
    'by_text': (By.XPATH, "//button[contains(text(), 'Submit')]"),
    'by_partial_text': (By.XPATH, "//a[contains(text(), 'Next')]")
}

# Use any locator
element = driver.wait_for_element(locators['by_css'])
```

### Chaining Operations

```python
with SeleniumDriver(stealth_mode=True) as driver:
    # Chain multiple operations
    if (driver.get_page("https://example.com") and
        driver.safe_click((By.ID, "login")) and
        driver.safe_send_keys((By.ID, "username"), "user") and
        driver.safe_send_keys((By.ID, "password"), "pass") and
        driver.safe_click((By.ID, "submit"))):

        print("Login successful!")
        # Continue with authenticated actions
    else:
        print("Login failed!")
```

---

## 🥷 Anti-Detection Features

### Built-in Stealth Features

- **Undetected ChromeDriver**: Bypasses most automation detection
- **Random User Agents**: Rotates browser fingerprints
- **Human-like Timing**: Random delays between actions
- **Realistic Typing**: Character-by-character input with delays
- **WebDriver Property Removal**: Hides automation indicators

### Best Practices for Stealth

```python
# 1. Use stealth mode for protected sites
with create_stealth_driver(headless=False) as driver:
    driver.get_page("https://linkedin.com")

    # 2. Add random delays between actions
    time.sleep(random.uniform(1, 3))

    # 3. Use realistic timing for form filling
    driver.safe_send_keys((By.ID, "session_key"), "email@example.com")
    time.sleep(random.uniform(0.5, 1.5))
    driver.safe_send_keys((By.ID, "session_password"), "password")

    # 4. Take screenshots to verify behavior
    driver.take_screenshot("login_page.png")
```

---

## 🌍 Real-World Examples

### Example 1: LinkedIn Job Scraping

```python
def scrape_linkedin_jobs(job_title, location):
    with create_stealth_driver(headless=False) as driver:
        # Navigate to LinkedIn jobs
        base_url = "https://www.linkedin.com/jobs/search"
        params = f"?keywords={job_title}&location={location}"

        if not driver.get_page(base_url + params):
            return []

        # Wait for job cards to load
        job_cards = driver.wait_for_elements((By.CLASS_NAME, "job-card-container"))

        jobs = []
        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, "job-title").text
                company = card.find_element(By.CLASS_NAME, "job-company").text
                location = card.find_element(By.CLASS_NAME, "job-location").text

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location
                })
            except Exception as e:
                print(f"Error extracting job data: {e}")
                continue

        return jobs

# Usage
jobs = scrape_linkedin_jobs("Python Developer", "New York")
print(f"Found {len(jobs)} jobs")
```

### Example 2: Indeed Job Scraping with Pagination

```python
def scrape_indeed_jobs(job_title, location, max_pages=3):
    with create_fast_driver(headless=True) as driver:
        all_jobs = []

        for page in range(max_pages):
            url = f"https://indeed.com/jobs?q={job_title}&l={location}&start={page*10}"

            if not driver.get_page(url):
                break

            # Scroll to load all jobs
            driver.scroll_to_bottom(pause_time=1.0)

            # Extract job information
            job_cards = driver.wait_for_elements((By.CLASS_NAME, "jobsearch-SerpJobCard"))

            for card in job_cards:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, "h2 a span")
                    company_elem = card.find_element(By.CLASS_NAME, "company")

                    all_jobs.append({
                        'title': title_elem.text,
                        'company': company_elem.text,
                        'page': page + 1
                    })
                except Exception as e:
                    continue

            # Random delay between pages
            time.sleep(random.uniform(2, 4))

        return all_jobs

# Usage
jobs = scrape_indeed_jobs("Data Scientist", "San Francisco", max_pages=5)
```

### Example 3: Glassdoor Company Reviews

```python
def scrape_glassdoor_reviews(company_name):
    with create_stealth_driver(headless=False) as driver:
        # Search for company
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company_name}"

        if not driver.get_page(search_url):
            return []

        # Click on first company result
        first_result = driver.wait_for_element((By.CSS_SELECTOR, ".company-tile"))
        if not first_result:
            return []

        if not driver.safe_click((By.CSS_SELECTOR, ".company-tile a")):
            return []

        # Navigate to reviews tab
        reviews_tab = driver.wait_for_element((By.XPATH, "//a[contains(text(), 'Reviews')]"))
        if reviews_tab:
            driver.safe_click((By.XPATH, "//a[contains(text(), 'Reviews')]"))

        # Extract reviews
        reviews = []
        review_elements = driver.wait_for_elements((By.CLASS_NAME, "review"))

        for review in review_elements:
            try:
                rating = review.find_element(By.CLASS_NAME, "rating").get_attribute("title")
                text = review.find_element(By.CLASS_NAME, "review-text").text

                reviews.append({
                    'rating': rating,
                    'text': text
                })
            except Exception as e:
                continue

        return reviews

# Usage
reviews = scrape_glassdoor_reviews("Google")
```

---

## ✅ Best Practices

### 1. Error Handling

```python
def robust_scraping_example():
    try:
        with SeleniumDriver(stealth_mode=True) as driver:
            if not driver.get_page("https://example.com"):
                raise Exception("Failed to load page")

            element = driver.wait_for_element((By.ID, "target"), timeout=30)
            if not element:
                driver.take_screenshot("error_no_element.png")
                raise Exception("Target element not found")

            # Continue with scraping...

    except Exception as e:
        print(f"Scraping failed: {e}")
        # Log error, send notification, etc.
```

### 2. Rate Limiting

```python
import time
import random

def scrape_with_rate_limiting(urls):
    with SeleniumDriver() as driver:
        results = []

        for i, url in enumerate(urls):
            # Add delays between requests
            if i > 0:
                delay = random.uniform(3, 7)  # 3-7 seconds
                print(f"Waiting {delay:.1f} seconds...")
                time.sleep(delay)

            if driver.get_page(url):
                # Extract data...
                results.append(extract_data(driver))

        return results
```

### 3. Data Validation

```python
def validate_scraped_data(data):
    """Validate scraped data before saving."""
    required_fields = ['title', 'company', 'location']

    for item in data:
        # Check required fields
        for field in required_fields:
            if not item.get(field) or item[field].strip() == '':
                print(f"Warning: Missing {field} in {item}")

        # Validate data types
        if 'salary' in item and item['salary']:
            try:
                float(item['salary'].replace('$', '').replace(',', ''))
            except ValueError:
                print(f"Warning: Invalid salary format: {item['salary']}")

    return data
```

### 4. Logging and Monitoring

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_with_logging():
    with SeleniumDriver() as driver:
        logger.info("Starting scraping session")

        try:
            success = driver.get_page("https://example.com")
            logger.info(f"Page load success: {success}")

            elements = driver.wait_for_elements((By.CLASS_NAME, "item"))
            logger.info(f"Found {len(elements)} elements")

            # Process elements...

        except Exception as e:
            logger.error(f"Scraping error: {e}")
            driver.take_screenshot("error_screenshot.png")
            raise

        logger.info("Scraping completed successfully")
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "ChromeDriver not found"

```bash
# Solution: Install webdriver-manager
pip install webdriver-manager

# Or manually download ChromeDriver
# https://chromedriver.chromium.org/
```

#### Issue 2: "Element not found" errors

```python
# Increase timeout
element = driver.wait_for_element((By.ID, "slow-element"), timeout=30)

# Use more specific locators
element = driver.wait_for_element((By.CSS_SELECTOR, "div.container > button.submit"))

# Add explicit waits
time.sleep(2)  # Wait for dynamic content
```

#### Issue 3: Bot detection

```python
# Use stealth mode
with create_stealth_driver(headless=False) as driver:
    # Add human-like behavior
    time.sleep(random.uniform(2, 5))

    # Use realistic typing speeds
    driver.safe_send_keys((By.ID, "input"), "text")

    # Take breaks between actions
    time.sleep(random.uniform(1, 3))
```

#### Issue 4: Memory issues with long-running scripts

```python
# Restart driver periodically
def long_running_scrape(urls):
    batch_size = 50

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]

        with SeleniumDriver() as driver:
            for url in batch:
                # Process URL
                pass

        # Driver automatically closed, memory freed
        print(f"Completed batch {i//batch_size + 1}")
```

### Debug Mode

```python
# Enable debug mode for troubleshooting
def debug_scraping():
    with SeleniumDriver(headless=False, stealth_mode=False) as driver:
        # Take screenshots at each step
        driver.get_page("https://example.com")
        driver.take_screenshot("step1_page_loaded.png")

        element = driver.wait_for_element((By.ID, "target"))
        driver.take_screenshot("step2_element_found.png")

        # Print page source for inspection
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.get_page_source())
```

---

## 📝 Summary

The `SeleniumDriver` class provides a robust foundation for web scraping projects with:

- **Easy Setup**: Simple instantiation with sensible defaults
- **Anti-Detection**: Built-in stealth features for avoiding blocks
- **Error Handling**: Robust exception handling and retries
- **Flexibility**: Configurable for different scraping scenarios
- **Convenience**: Context manager support and utility methods

Start with the basic examples and gradually incorporate advanced features as your scraping needs become more complex. Remember to always respect websites' `robots.txt` files and terms of service when scraping.

---

_Happy Scraping! 🚀_
