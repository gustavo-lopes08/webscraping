import time, requests, json, mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from credentials import zenUsr, zenPass, kenUsr, kenPass
from connectdb import conn, cursor

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

divDadosPrincipais = soup.find_all('div', attrs={'class':'col-sm-8 ng-binding'})
requisitante = divDadosPrincipais[3].get_text()
cargo = soup.find('span', attrs={'id':'position-position-template-name'}).get_text()
codigoVaga = soup.find('span', attrs={'class': 'info-value'}).get_text()

cursor = conn.cursor()

cursor.execute("INSERT INTO vaga (codigo, cargo, requisitante) VALUES ( "+codigoVaga+", '"+cargo+"' , '"+requisitante+"' )")

conn.commit()

dados = []
cursor.execute("SELECT * FROM vaga")
for x in cursor:
    dados.append(x)

for d in dados:
    codVaga = d[0]
    cargo = d[1]
    requisitante = d[2]

cursor.close()
conn.close()

t_body = "Codigo da Vaga: {}\nCargo: {} \nRequisitante: {}".format(codVaga,cargo,requisitante)
subject = "Solicitação de Ativo - "+str(cargo)

zenUrl = ''
headers = {'Content-Type': 'application/json'}
data =  {
    'ticket': {'subject':'Solicitação de Ativo - '+cargo, 'comment': {'body':t_body} }
}

response = requests.post(url=zenUrl, data=json.dumps(data), auth=(zenUsr, zenPass), headers=headers)

print(response.text)