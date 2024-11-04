from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_driver():
    # Use your specific user profile directory path
    user_data_path = "/Users/juanalonso-allende/Library/Application Support/Google/Chrome/Default"
    
    # Configure Chrome options to use the specified user profile directory
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={user_data_path}")
    
    # Initialize Chrome driver with the user data directory
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

driver = init_driver()

