import time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from credentials import kenUsr, kenPass

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options,executable_path='')
url = ""

def login(url):
    browser.get(url)
    time.sleep(2)
    usrfield = browser.find_element_by_id("email")
    pwdfield = browser.find_element_by_id("password")
    btn = browser.find_element_by_class_name("btn.btn-success.ng-binding")

    usrfield.send_keys(kenUsr)
    pwdfield.send_keys(kenPass)
    btn.click()

login(url)

time.sleep(2)

soup = BeautifulSoup(browser.page_source, 'html.parser')

time.sleep(2)

links = []

table = soup.find('table', attrs={'class': 'table table-positions table-hover u-no-margin ng-scope'})

for link in table.findAll('a', attrs={'href': re.compile("progresso$")}):
    links.append((link.get('href')))

links = [l.replace("progresso", "detalhes") for l in links]

print(links)