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
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def replacer(string):
    a = string.replace(";", "").replace("\n", "")
    return a

### Config Change
file_to_open = "url_course.txt"
csv_to_write = "result.csv"
### Config Change

#open file
with open(file_to_open, 'r', encoding="utf-8") as op:
    links = op.readlines()
    links_count = len(links)

counters = 0

#setup browser
browser = webdriver.Chrome(options=opts)
while counters < links_count:
    try:
        link = links[counters].rstrip()
        browser.get(link)
        sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            view_all_button = browser.find_element(By.XPATH, "//button[@class='cds-149 cds-button-disableElevation cds-button-ghost css-c0avci']")
            view_all_button.click()
        except:
            pass
        subjects = browser.find_elements(By.XPATH, "//a[@class='cds-119 cds-113 cds-115 cds-breadcrumbs-link css-seqyon cds-142']")
        judul = browser.find_element(By.XPATH, "//h1[@class='cds-119 cds-Typography-base css-1xy8ceb cds-121']").text
        desc = browser.find_element(By.XPATH, "//p[@class='cds-119 cds-Typography-base css-80vnnb cds-121']").text
        whatyoulearn = browser.find_element(By.XPATH, "//div[@class='css-15ko5n9']").text
        skillgains = browser.find_elements(By.XPATH, "//span[@class='css-1l1jvyr']")
        skills = ""
        for skill in skillgains:
            skills += f"{skill.text}, "
        all_course = browser.find_elements(By.XPATH, "//a[@data-e2e='sdp-course-list-link']")
        try:
            course_exist = all_course[0].text
        except:
            all_course = browser.find_elements(By.XPATH, "//h3[@class='cds-119 cds-Typography-base css-h1jogs cds-121']")
        courses = ""
        for course in all_course:
            courses += f"{course.text}, "
        with open(csv_to_write, 'a', encoding="utf-8") as csv:
            csv.write(f"{link}; {replacer(subjects[1].text)}; {replacer(judul)}; {replacer(desc)}; {replacer(whatyoulearn)}; {replacer(skills)}; {replacer(courses)};\n")
        print(f"{date_show()} ==> Success : {counters+1}/{links_count} | {link[:75]}... ", end="\r")
    except:
        print(f"{date_show()} ==> Error : {counters+1}/{links_count} | {link[:75]}... ", end="\r")
    counters+= 1