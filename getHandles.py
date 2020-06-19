import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument("--start-maximized")
browser = webdriver.Chrome('./chromedriver', chrome_options=ChromeOptions)
with open('./listIDS.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]  #Array of all id's
data = {}
data["people"]= []
for i in content:
    browser.get("https://twitter.com/i/user/"+i)
    delay = 15
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'react-root')))
        print ("Page is ready for -> ", i)
        time.sleep(5)
        print(browser.current_url)
        endingslash= (str(browser.current_url).split('/'))[-1]
        if not endingslash==i:
            data['people'].append({
                i: endingslash
            })
    except TimeoutException:
        print ("Loading took too much time!")
with open('twitterHandles.txt', 'w') as outfile:
    json.dump(data, outfile)