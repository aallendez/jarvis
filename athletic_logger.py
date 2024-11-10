# import os
# import requests as req
# import json
# import threading
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# os.system("clear")



# def book_reservation_on_gym(data):
#     driver.get('https://ieathleticreservations.ie.edu/sz')
    
#     target_day = "Wednesday"
#     target_time = "08:00 - 09:00"
#     target_activity = "BOXING CORNER"
    
#     reservation_link = driver.find_element(By.XPATH, "//div[@class='iconlink ' and .//p[text()='MAKE A RESERVATION']]/a[@class='iconlink__link']")
#     reservation_link.click()
    
#     tower_div = driver.find_element(By.XPATH, "//div[@class='iconlink' and .//h2[text()='IE TOWER MADRID']]")
#     tower_div.click()
    
#     if data["activity"] == "Gym":
#         individual_choice = driver.find_element(By.ID, "free")
#         individual_choice.click()
        
#         days = driver.find_elements(By.XPATH, "//div[@class='cal-row-fluid cal-row-head']//span[@ng-bind='day.weekDayLabel']")
#         day_index = None
#         for index, day in enumerate(days):
#             if day.text.strip() == target_day:
#                 day_index = index
#                 break
        
#         if day_index is None:
#             raise Exception(f"Day '{target_day}' not found.")
        
#         time_slot_xpath = (f"//div[@class='row ng-scope']//div[@class='cal-cell1 cal-offset0'][{day_index + 1}]"
#                    f"//a[contains(text(), '{target_time}') and contains(text(), '{target_activity}')]")
#         time_slot = driver.find_element(By.XPATH, time_slot_xpath)
#         time_slot.click()
        
#         reserve_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✔ Reserve')]"))
#         )
        
#         reserve_button.click()
        
#         save_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(text(), 'Save')]"))
#         )

#         # Click the "Save" button
#         save_button.click()
        
#     elif data["activity"] == "Group":
#         group_choice = driver.find_element(By.ID, "punt")
#         group_choice.click()
    
#     return True

# def reserve_swim(date):
#     print("Reserving swim for date:", date)
#     return True
    
# def reserve_gym(date):
#     print("Reserving gym for date:", date)
#     return True


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/Users/juanalonso-allende/Library/Application Support/Google/Chrome")
chrome_options.add_argument("--profile-directory=Profile 6")  # Use the profile directory for your account
chrome_options.add_argument("--disable-extensions")  # Disable extensions to avoid conflicts
chrome_options.add_experimental_option("detach", True)  # Keeps Chrome open
chrome_options.add_argument("--start-maximized")

# Explicit path to Chrome (optional but may help)
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)

# Navigate to a website to test if the browser is responsive
# driver.get("https://www.instagram.com")


def login(email, password):
    # Open the login page
    driver.get('https://ieathleticreservations.ie.edu/sz')
    
    time.sleep(5)  # Wait for the page to load
    
    # Wait for the email input field, enter the email, and click "Next"
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "i0116"))
    )
    email_input.send_keys(email)
    
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    )
    next_button.click()
    
    # Wait and enter the password
    time.sleep(3)  # Wait for the password page to load
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "i0118"))
    )
    password_input.send_keys(password)
    
    # Click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    )
    login_button.click()


def start_reservation():
    driver.get('https://ieathleticreservations.ie.edu/sz')
    
    auth = False
    
    if auth is True:
        login("jalonsoallen.ieu2023@student.ie.edu", "t0P1%m3N")
        time.sleep(30)
    else:
        time.sleep(5)
    
    # Wait until the reservation link is clickable
    reservation_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='iconlink ' and .//p[text()='MAKE A RESERVATION']]/a[@class='iconlink__link']"))
    )
    reservation_link.click()
    
    ie_tower_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='iconlink' and .//h2[text()='IE TOWER MADRID']]/a"))
    )
    ie_tower_link.click()
    
    
# Function to reserve a gym session
def reserve_gym(target_day, target_time):
    start_reservation()
    
    print("Reserving gym session...")
    
    individual_choice = driver.find_element(By.ID, "free")
    individual_choice.click()
    
    print("Individual choice selected.")
    
    days = driver.find_elements(By.XPATH, "//div[@class='cal-row-fluid cal-row-head']//span[@ng-bind='day.weekDayLabel']")
    day_index = None
    for index, day in enumerate(days):
        if day.text.strip() == target_day:
            day_index = index
            break
        
    print("Day index:", day_index)
    
    if day_index is None:
        raise Exception(f"Day '{target_day}' not found.")
    
    time_slot_xpath = f"//div[@class='row ng-scope']//div[@class='cal-cell1 cal-offset0'][{day_index + 1}]//a[contains(text(), '{target_time}')]"
    time_slot = driver.find_element(By.XPATH, time_slot_xpath)
    time_slot.click()
    
    
    
    reserve_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✔ Reserve')]"))
    )
    reserve_button.click()
    
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(text(), 'Save')]"))
    )
    save_button.click()
    
    return True


# Function to reserve a group swim session
def reserve_swim(target_day, target_time):
    start_reservation()
    
    print("Reserving swim session...")
    
    group_choice = driver.find_element(By.ID, "punt")
    group_choice.click()
    
    print("Group choice selected.")
    
    days = driver.find_elements(By.XPATH, "//div[@class='cal-row-fluid cal-row-head']//span[@ng-bind='day.weekDayLabel']")
    day_index = None
    for index, day in enumerate(days):
        if day.text.strip() == target_day:
            day_index = index
            break
        
    print("Day index:", day_index)
    
    if day_index is None:
        raise Exception(f"Day '{target_day}' not found.")
    
    time_slot_xpath = f"//div[@class='row ng-scope']//div[@class='cal-cell1 cal-offset0'][{day_index + 1}]//a[contains(text(), '{target_time}')]"
    time_slot = driver.find_element(By.XPATH, time_slot_xpath)
    time_slot.click()
    
    reserve_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✔ Reserve')]"))
    )
    reserve_button.click()
    
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(text(), 'Save')]"))
    )
    save_button.click()
    
    return True

