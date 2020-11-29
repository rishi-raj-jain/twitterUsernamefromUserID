#!/usr/bin/python

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
    # This dictionary will be populated if user IDs in correct format, then returned. Otherwise returned empty.
    DictOfUsernames = {}
    # Proceed only if a list has been passed
    if user_IDs != None and type(user_IDs) == list:
        # Only use IDs if they solely contain digits
        legalUser_IDs = [s for s in user_IDs if s.isdigit()]
        # Alert for dropped illegal IDs
        if len(legalUser_IDs) < len(user_IDs):
            print(f"IDs dropped for containing invalid characters: {len(user_IDs) - len(legalUser_IDs)}  User IDs must contain digits only")
        ChromeOptions = webdriver.ChromeOptions()
        # Start Chrome headless so no window popping up
        ChromeOptions.add_argument("--headless")
        # Changed chrome_options to options due to deprecation
        # Setting log_level to 50 effectively silences logging as only fatal errors will be logged
        browser = webdriver.Chrome(ChromeDriverManager(log_level=50).install(), options=ChromeOptions)
        # iterate over list of user IDs with i as ID
        for i in legalUser_IDs:
            print("\n")
            print(f"Attempting to load Twitter page for user {i}")
            browser.get("https://twitter.com/i/user/"+i)
            # Delay for WebDriverwait. This is maxumum seconds to wait before timeout
            delay = 10
            try:
                # Sleep for random amount so this doesn't look like suspicious activity to Twitter
                time.sleep(random.randint(0, 2))
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
                    print("No username retrieved")
                    DictOfUsernames[i] = "No_username_retrieved"
                # NOW CLOSE otherwise keeps opening windows and eventually out of memory
                _closeBrowserWindow(browser)
            except TimeoutException:
                print(f"Trying to Load the page for {i} took too much time!")
                print('Using "_Timeout" as name')
                DictOfUsernames[i] = "_Timeout"
                # NOW CLOSE otherwise keeps opening windows and eventually out of memory
                _closeBrowserWindow(browser)
        # Finally after parsing all user IDs, totally kill browser so the driver isn't lurking in memory
        browser.quit()
        return(DictOfUsernames)
    else:
        print("No usernames provided")
        # Return empty dictionary
        return(DictOfUsernames)

def _closeBrowserWindow(browser):
    try:
        browser.close
        print("closed headless browser window")
    except:
        print("Couldn't close this headless browser window")
