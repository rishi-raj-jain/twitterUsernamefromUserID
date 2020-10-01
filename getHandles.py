#!/usr/bin/python

import json
import time
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
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'react-root')))
            # Page is *actually* ready and we can obtain the username from the URL
            print ("Page is ready for -> ", i)
            # Sleep for three seconds for browser to catch up - NO NEED, as page is ready
            # time.sleep(3)
            print(browser.current_url)
            # strip the username from the end of the URL
            endingslash= (str(browser.current_url).split('/'))[-1]
            # Catches cases where username doesn't form part of URL
            if not endingslash==i:
                DictOfUsernames[i] = endingslash
            else:
                print("Account ", i, " Is deactivated. No username retrieved")
                DictOfUsernames[i] = "Dead_Account"

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
            print ("Loading this user's page took too much time!")

    return(DictOfUsernames)

