#!/usr/bin/python

# Time and random for random delay
import time
import random
import numpy as np
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Inherited class from Thread class to get return values from threads
class GetThreadValue(threading.Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return


def get_driver():
    ChromeOptions = webdriver.ChromeOptions()
    # Basic user agent ensures headless mode works. Chrome version number doesn't need to be exact
    ChromeOptions.add_argument("user-agent=Chrome/89")
    # Start Chrome headless so no window popping up
    ChromeOptions.add_argument("--headless")
    # Changed chrome_options to options due to deprecation
    # Setting log_level to 50 effectively silences logging as only fatal errors will be logged
    browser = webdriver.Chrome(
        ChromeDriverManager(log_level=50).install(), options=ChromeOptions
    )
    return browser


def getUsername(ids, browser, delayTime=5):
    # iterate over list of user IDs with i as ID
    localDictUserID = dict()
    for i in ids:
        print("\n")
        print(f"Attempting to load Twitter page for user {i}")
        browser.get("https://twitter.com/i/user/" + i)
        # Delay for WebDriverwait. This is maxumum seconds to wait before timeout
        delay = delayTime
        try:
            # Sleep for random amount so this doesn't look like suspicious activity to Twitter
            time.sleep(random.randint(0, 2))
            # Lambda function here as has to be callable. checks if page redirect has happened.
            # More stable than waiting for page element as we're scraping directly from the URL
            myElem = WebDriverWait(browser, delay).until(
                lambda urlCheck: browser.current_url
                != f"https://twitter.com/i/user/{i}"
            )
            # Deprecated: EC.presence_of_element_located((By.ID, 'react-root')))
            print(f"Page is ready for user {i}")
            # strip the username from the end of the URL
            endingslash = (str(browser.current_url).split("/"))[-1]
            # NOW CLOSE otherwise keeps opening windows and eventually out of memory
            _closeBrowserWindow(browser)
            # Catches cases where username doesn't form part of URL
            if not endingslash == i:
                print(f"Username for {i} is {endingslash}")
                localDictUserID[i] = endingslash
            else:
                print("No username retrieved")
                localDictUserID[i] = "No_username_retrieved"

        except TimeoutException:
            print(f"Trying to Load the page for {i} took too much time!")
            print('Using "_Timeout" as name')
            # NOW CLOSE otherwise keeps opening windows and eventually out of memory
            _closeBrowserWindow(browser)
            localDictUserID[i] = "_Timeout"
    # Finally after parsing all user IDs, totally kill browser so the driver isn't lurking in memory
    browser.quit()
    return localDictUserID


def getHandles(user_IDs=None, delayTime=5):
    # This dictionary will be populated if user IDs in correct format, then returned. Otherwise returned empty.
    DictOfUsernames = dict()
    # Proceed only if a list has been passed
    if user_IDs != None and type(user_IDs) == list:
        # Only use IDs if they solely contain digits
        legalUser_IDs = [s for s in user_IDs if s.isdigit()]
        # Alert for dropped illegal IDs
        if len(legalUser_IDs) < len(user_IDs):
            print(
                f"IDs dropped for containing invalid characters: {len(user_IDs) - len(legalUser_IDs)}  User IDs must contain digits only"
            )
        num_ids = len(legalUser_IDs)
        # Check for duplicate user ids
        legalUser_IDs = list(set(legalUser_IDs))
        if len(legalUser_IDs) < num_ids:
            print(
                f"Duplicate IDs dropped: {num_ids - len(legalUser_IDs)}  User IDs must be unique"
            )
            num_ids = len(legalUser_IDs)
        # Splitting IDs into multiple arrays for multithreading (Upto 10 splits if userids more than 10)
        splits = min(num_ids, 10)
        ids = np.array_split(legalUser_IDs, splits)
        # Creating and Starting Multiple Threads
        driver = []
        processes = []
        for i in range(len(ids)):
            driver.append(get_driver())
            processes.append(
                GetThreadValue(target=getUsername, args=(ids[i], driver[i], delayTime))
            )
        for p in processes:
            p.start()
        # This list will store dictionaries returned by individual threads
        dictList = []
        # Getting return values from threads while pausing the main thread
        for p in processes:
            dictList.append(p.join())
        # Combining the list of dictionaries to a single dictionary
        DictOfUsernames = dict((key, d[key]) for d in dictList for key in d)
        return DictOfUsernames
    else:
        print("No usernames provided")
        # Return empty dictionary
        return DictOfUsernames


def _closeBrowserWindow(browser):
    try:
        browser.close
        print("closed headless browser window")
    except:
        print("Couldn't close this headless browser window")
