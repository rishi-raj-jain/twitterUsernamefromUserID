#!/usr/bin/python

import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getHandles(user_IDs = None):
    ChromeOptions = webdriver.ChromeOptions()
    # Start headless so no window popping up
    ChromeOptions.add_argument("--headless")
    # Changed chrome_options to options due to deprecation
    # MUST be full path to Chromedriver NOT relative. Also must NOT have exe extension here
    browser = webdriver.Chrome('/Users/davidvannen/Desktop/pythonProjects/twitterUsernamefromUserID/chromedriver', options=ChromeOptions)
    # This dictionary will be populated then returned
    DictOfUsernames = {}
    # iterate over array of user IDs with i as ID
    for i in user_IDs:
        # Hardcoded URL - can it be stripped out to calling module and be passed as attr?
        # And / or put alternative URL in here, test and leave available in comment
        browser.get("https://twitter.com/i/user/"+i)
        delay = 15
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'react-root')))
            print ("Page is ready for -> ", i)
            # Sleep for five seconds for browser to catch up
            time.sleep(5)
            print(browser.current_url)
            # strip the username from the end of the URL
            endingslash= (str(browser.current_url).split('/'))[-1]
            # Catches cases where username doesn't form part of URL
            if not endingslash==i:
                DictOfUsernames[i] = endingslash
        except TimeoutException:
            print ("Loading took too much time!")

    return(DictOfUsernames)


returnedDict = getHandles(["80304031","25073877"])
print(returnedDict)