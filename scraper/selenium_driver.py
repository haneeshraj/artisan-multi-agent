"""
Selenium WebDriver wrapper class for web scraping.
Provides a reusable driver with common configurations and anti-detection features.
"""

import time
import random
from typing import Optional, List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import undetected_chromedriver as uc


class SeleniumDriver:
    """
    A comprehensive Selenium WebDriver wrapper class for web scraping.
    Includes anti-detection features and common scraping utilities.
    """
    
    def __init__(self, 
                 headless: bool = False,
                 stealth_mode: bool = True,
                 window_size: str = "1920,1080",
                 timeout: int = 10,
                 page_load_timeout: int = 30,
                 custom_user_agent: Optional[str] = None):
        """
        Initialize the Selenium driver with anti-detection features.
        
        Args:
            headless: Run browser in headless mode
            stealth_mode: Use undetected-chromedriver for better stealth
            window_size: Browser window size as "width,height"
            timeout: Default wait timeout for elements
            page_load_timeout: Page load timeout
            custom_user_agent: Custom user agent string
        """
        self.headless = headless
        self.stealth_mode = stealth_mode
        self.window_size = window_size
        self.timeout = timeout
        self.page_load_timeout = page_load_timeout
        self.custom_user_agent = custom_user_agent
        self.driver = None
        self.wait = None
        
    def _get_chrome_options(self) -> Options:
        """Configure Chrome options for web scraping."""
        options = Options()
        
        # Basic options
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--window-size={self.window_size}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Anti-detection options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Performance options
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")  # Remove if JS is needed
        
        # User agent
        if self.custom_user_agent:
            options.add_argument(f"--user-agent={self.custom_user_agent}")
        else:
            ua = UserAgent()
            options.add_argument(f"--user-agent={ua.random}")
        
        return options
    
    def start_driver(self) -> webdriver.Chrome:
        """Start and configure the Chrome WebDriver."""
        try:
            if self.stealth_mode:
                # Use undetected-chromedriver for better stealth
                options = uc.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                
                self.driver = uc.Chrome(options=options)
            else:
                # Use regular ChromeDriver
                options = self._get_chrome_options()
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.driver.implicitly_wait(self.timeout)
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return self.driver
            
        except Exception as e:
            raise Exception(f"Failed to start WebDriver: {str(e)}")
    
    def get_page(self, url: str, wait_time: Optional[float] = None) -> bool:
        """
        Navigate to a URL with random delay and error handling.
        
        Args:
            url: The URL to navigate to
            wait_time: Optional custom wait time after loading
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.driver:
                self.start_driver()
            
            self.driver.get(url)
            
            # Random delay to mimic human behavior
            delay = wait_time if wait_time else random.uniform(2, 5)
            time.sleep(delay)
            
            return True
            
        except Exception as e:
            print(f"Error loading page {url}: {str(e)}")
            return False
    
    def wait_for_element(self, locator: tuple, timeout: Optional[int] = None) -> Any:
        """
        Wait for an element to be present and return it.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, "locator_value")
            timeout: Optional custom timeout
            
        Returns:
            WebElement or None
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None
    
    def wait_for_elements(self, locator: tuple, timeout: Optional[int] = None) -> List[Any]:
        """
        Wait for elements to be present and return them.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, "locator_value")
            timeout: Optional custom timeout
            
        Returns:
            List of WebElements
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def safe_click(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """
        Safely click an element with wait and error handling.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, "locator_value")
            timeout: Optional custom timeout
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.wait_for_element(locator, timeout)
            if element:
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.5)
                
                # Try regular click first
                try:
                    element.click()
                except:
                    # If regular click fails, try JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                
                return True
            return False
        except Exception as e:
            print(f"Error clicking element: {str(e)}")
            return False
    
    def safe_send_keys(self, locator: tuple, text: str, clear_first: bool = True, timeout: Optional[int] = None) -> bool:
        """
        Safely send keys to an element with human-like typing.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, "locator_value")
            text: Text to type
            clear_first: Clear field before typing
            timeout: Optional custom timeout
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.wait_for_element(locator, timeout)
            if element:
                if clear_first:
                    element.clear()
                
                # Human-like typing with random delays
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                return True
            return False
        except Exception as e:
            print(f"Error sending keys: {str(e)}")
            return False
    
    def scroll_to_bottom(self, pause_time: float = 1.0, max_scrolls: int = 10) -> None:
        """
        Scroll to the bottom of the page gradually.
        
        Args:
            pause_time: Time to pause between scrolls
            max_scrolls: Maximum number of scroll attempts
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(max_scrolls):
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            
            # Check if we've reached the bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Path to save the screenshot
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.driver:
                self.driver.save_screenshot(filename)
                return True
            return False
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return False
    
    def get_page_source(self) -> Optional[str]:
        """Get the current page source."""
        try:
            return self.driver.page_source if self.driver else None
        except Exception as e:
            print(f"Error getting page source: {str(e)}")
            return None
    
    def close_driver(self) -> None:
        """Close the WebDriver and clean up resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
        except Exception as e:
            print(f"Error closing driver: {str(e)}")
    
    def __enter__(self):
        """Context manager entry."""
        self.start_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()


# Example usage functions
def create_stealth_driver(headless: bool = False) -> SeleniumDriver:
    """Create a stealth driver optimized for avoiding detection."""
    return SeleniumDriver(
        headless=headless,
        stealth_mode=True,
        timeout=15,
        page_load_timeout=30
    )

def create_fast_driver(headless: bool = True) -> SeleniumDriver:
    """Create a fast driver optimized for performance."""
    return SeleniumDriver(
        headless=headless,
        stealth_mode=False,
        timeout=10,
        page_load_timeout=20
    )