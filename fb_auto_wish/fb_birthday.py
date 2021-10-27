""" 
Task: Send automated birthday wished to a facebook friend on birthday
Inputs:
    1. CredFile Path (in given format with base64 encoded values)
    2. Chrome Driver Path
Created By: Shayon Deb Roy
Date: 16-10-2021
Version:1 
Source Code
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import json
import base64
import random


################################# INPUT VALUES (CHANGE VALUES HERE) ###############################

cred_file_path = 'fb_auto_wish/creds.json'
driver_file_path = "/home/shayon/Documents/Python Projects/virtenv/fb_auto_wish/chromedriver_linux64/chromedriver"
log_path = '/home/shayon/Documents/Python Projects/virtenv/fb_auto_wish/autowish.log'



###################################################################################################
#                               DO NOT CHANGE THE CODE BELOW                                      #
###################################################################################################

#log file creation
try:
    logFile = open(log_path, "a")
except:
    print("could not create log")
    exit()

#get creds
try:
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: execution started")
    creds = open(cred_file_path,"r")
    data = json.loads(creds.read())
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: credentials read")

except:
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[ERROR]: not able to open the credentials file")
    logFile.close()
    exit()

try:
    option1 = Options()
    option1.add_argument("--disable-notifications") #block alert
    option1.add_argument("headless") #hide screen
    driver =  webdriver.Chrome(driver_file_path,chrome_options=option1)
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: driver initialized")
except:
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[ERROR]: not able to initialize driver with the give chrome driver path")
    logFile.close()
    exit()

#facebook login
try: 
    #open facebook login page
    driver.get("https://www.facebook.com")  
    email = driver.find_element_by_id("email")
    email.send_keys(base64.b64decode(data["username"]).decode('utf-8'))
    password = driver.find_element_by_id("pass")
    password.send_keys(base64.b64decode(data["password"]).decode('utf-8'))
    creds.close()
    password.send_keys(Keys.RETURN)
    time.sleep(3)
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: facebook login success")

except:
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[ERROR]: login attempt failed")
    driver.close()
    creds.close()
    logFile.close()
    exit()

#send message
try:
    wish_counter = 0
    driver.get("https://www.facebook.com/events/birthdays/?acontext=%7B%22event_action_history%22%3A[%7B%22mechanism%22%3A%22left_rail%22%2C%22surface%22%3A%22bookmark%22%7D]%2C%22ref_notif_type%22%3Anull%7D")
    time.sleep(3)
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: at birthday event page")
    elements = driver.find_elements_by_xpath("//*[@class='_1mf _1mj']")
    if len(elements) == 0:
        logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: There are no birthdays today!")
        driver.close()
    # send birthday wishes
    else:
        list_of_wishes = ["Happy Birthday! Have a great one, enjoy!", "Happy birthday, wishing you and your family good health, happiness and prosperity. Have a good one. Enjoy.", "Happy birthday, wishing you a wonderful year ahead filled with new experience. Enjoy the day.", "Happy birthday, always wishing the best for you, have a good one."]
        for element in elements:
            element.send_keys(random.choice(list_of_wishes))
            element.send_keys(Keys.RETURN)
            wish_counter = wish_counter + 1
        driver.close()
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: " + str(wish_counter) + " wishe(s) sent")
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[INFO]: execution complete")
    logFile.close()

except Exception as err:
    logFile.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "[ERROR]: not able to add birthday note in the event page. " + err)
    driver.close()
    logFile.close()
    exit()


