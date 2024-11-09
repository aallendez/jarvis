import os
import requests as req
import json
import threading
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

os.system("clear")



def book_reservation_on_gym(data):
    driver.get('https://ieathleticreservations.ie.edu/sz')
    
    target_day = "Wednesday"
    target_time = "08:00 - 09:00"
    target_activity = "BOXING CORNER"
    
    reservation_link = driver.find_element(By.XPATH, "//div[@class='iconlink ' and .//p[text()='MAKE A RESERVATION']]/a[@class='iconlink__link']")
    reservation_link.click()
    
    tower_div = driver.find_element(By.XPATH, "//div[@class='iconlink' and .//h2[text()='IE TOWER MADRID']]")
    tower_div.click()
    
    if data["activity"] == "Gym":
        individual_choice = driver.find_element(By.ID, "free")
        individual_choice.click()
        
        days = driver.find_elements(By.XPATH, "//div[@class='cal-row-fluid cal-row-head']//span[@ng-bind='day.weekDayLabel']")
        day_index = None
        for index, day in enumerate(days):
            if day.text.strip() == target_day:
                day_index = index
                break
        
        if day_index is None:
            raise Exception(f"Day '{target_day}' not found.")
        
        time_slot_xpath = (f"//div[@class='row ng-scope']//div[@class='cal-cell1 cal-offset0'][{day_index + 1}]"
                   f"//a[contains(text(), '{target_time}') and contains(text(), '{target_activity}')]")
        time_slot = driver.find_element(By.XPATH, time_slot_xpath)
        time_slot.click()
        
        reserve_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✔ Reserve')]"))
        )
        
        reserve_button.click()
        
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(text(), 'Save')]"))
        )

        # Click the "Save" button
        save_button.click()
        
    elif data["activity"] == "Group":
        group_choice = driver.find_element(By.ID, "punt")
        group_choice.click()
    
    return True

def reserve_swim(date):
    print("Reserving swim for date:", date)
    return True
    
def reserve_gym(date):
    print("Reserving gym for date:", date)
    return True


