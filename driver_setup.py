from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(level=logging.INFO)

# Function to initialize the Chrome WebDriver
def get_chrome_driver():
    try:
        logging.info("Opening Chrome Driver")
        user_agent = ""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={user_agent}")

        return webdriver.Chrome(options=chrome_options)
    
    except Exception as e:
        logging.error(f"Error initializing Chrome driver: {e}")
        raise
