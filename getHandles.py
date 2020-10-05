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
            print ("Page is ready for -> ", i)
            print(browser.current_url)
            # strip the username from the end of the URL
            endingslash= (str(browser.current_url).split('/'))[-1]
            # Catches cases where username doesn't form part of URL
            if not endingslash==i:
                DictOfUsernames[i] = endingslash
            else:
                print("Account ", i, "may be deactivated. No username retrieved")
                DictOfUsernames[i] = "No_username_retrieved"

            # <Deprecated? This threw an error, the line below doesn't.> print(browser.getPageSource())
            # print(browser.page_source)

            # NOW CLOSE otherwise keeps opening windows and eventually out of memory
            try:
                browser.close
                # Removing as too verbose
                # print("Closed browser instance")
            except:
                print("Couldn't close this browser instance")
        except TimeoutException:
            print(f"Loading the page for {i} took too much time!")
            DictOfUsernames[i] = "Timeout"

    return(DictOfUsernames)

