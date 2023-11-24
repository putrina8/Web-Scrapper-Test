from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import warnings,os,time
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep

warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()
opts = Options()
opts.add_argument('log-level=3')
#opts.add_argument('--headless=chrome')
prefs = {"profile.default_content_setting_values.notifications" : 2}
opts.add_experimental_option("prefs",prefs)
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])

def date_show():
    date = f"[{time.strftime('%d-%m-%y %X')}]\n"
    return date

### Config Change
link_store = f'data.txt'
keywords = [
    "Business",  #1
    "Data Science", #2 
    "Language Learning", #3 
    "Physical Science and Engineering",  #4
    "Arts and Humanities",  #5
    "Health", #6
    "Math and Logic", #7
    "Social Sciences",  #8
    "Computer Science",  #9
    "Information Technology",  #10
    "Personal Development"  #11
]
### Config Change

# start browser
browser = webdriver.Chrome(options=opts)

# Looping through each keyword
for pilihan_keyword, keyword in enumerate(keywords, start=1):
    print(f"\n{date_show()} ==> Scraping for Keyword: {keyword}\n")

    # Get Max Page
    browser.get(f"https://www.coursera.org/search?topic={keyword}&page=1")
    max_page = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Go to last page']"))).text
    print(f"Max Page {max_page}")

    # looping search page
    for item in range(int(max_page)):
        print(f"{date_show()} ==> Scraping Page : {item+1}", end="\r")
        url = f"https://www.coursera.org/search?topic={keyword}&page={item+1}"
        browser.get(url)

        # Menunggu hingga elemen-elemen link muncul
        links = wait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142']"))
        )

        for link in links:
            single_link = link.get_attribute('href')
            with open(link_store, 'a', encoding="utf-8") as res:
                res.write(f"{single_link}\n")

# Close the browser
browser.quit()