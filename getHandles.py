#!/usr/bin/python

import json
# Time and random for random delay
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

def getHandles(user_IDs = None):
    ChromeOptions = webdriver.ChromeOptions()
    # Start Chrome headless so no window popping up
    ChromeOptions.add_argument("--headless")
    # Changed chrome_options to options due to deprecation
    # Setting log_level to 50 effectively silences logging as only fatal errors will be logged
    # SO this is the install - don't / shouldn't install each time so this needs removing somehow
    # Like first time check or take out into separate func
    browser = webdriver.Chrome(ChromeDriverManager(log_level=50).install(), options=ChromeOptions)
    # This dictionary will be populated then returned
    DictOfUsernames = {}
    # iterate over list of user IDs with i as ID
    for i in user_IDs:
        print("\n")
        print(f"Attempting to load Twitter page for user {i}")
        browser.get("https://twitter.com/i/user/"+i)
        # Delay for WebDriverwait. This is maxumum seconds to wait before timeout
        delay = 15
        try:
            # Sleep for random amount so this doesn't look like suspicious activity to Twitter
            time.sleep(random.randint(0, 3))
            # Lambda function here as has to be callable. checks if page redirect has happened.
            # More stable than waiting for page element as we're scraping directly from the URL
            myElem = WebDriverWait(browser, delay).until(lambda urlCheck: browser.current_url != f'https://twitter.com/i/user/{i}')
            # Deprecated: EC.presence_of_element_located((By.ID, 'react-root')))
            print(f"Page is ready for user {i}")
            # strip the username from the end of the URL
            endingslash= (str(browser.current_url).split('/'))[-1]
            # Catches cases where username doesn't form part of URL
            if not endingslash==i:
                DictOfUsernames[i] = endingslash
                print(f"Username for {i} is {endingslash}")
            else:
                print(f"Account {i} may be deactivated. No username retrieved")
                DictOfUsernames[i] = "No_username_retrieved"
            # NOW CLOSE otherwise keeps opening windows and eventually out of memory
            _closeBrowserWindow(browser)
        except TimeoutException:
            print(f"Trying to Load the page for {i} took too much time!")
            print('Used "Timeout" as name')
            DictOfUsernames[i] = "Timeout"
            time.sleep(2)
            # NOW CLOSE otherwise keeps opening windows and eventually out of memory
            _closeBrowserWindow(browser)
    # Finally, totally kill browser so the driver isn't lurking in memory
    browser.quit()
    return(DictOfUsernames)

def _closeBrowserWindow(browser):
    try:
        browser.close
        print("closed headless browser window")
    except:
        print("Couldn't close this headless browser window")
