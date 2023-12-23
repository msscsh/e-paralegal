from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = f'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?'\
'consulta=Consultar&'\
'conscsjt=&'\
'numeroTst=0000603&'\
'digitoTst=86&'\
'anoTst=2019&'\
'orgaoTst=5&'\
'tribunalTst=17&'\
'varaTst=0009&'\
'submit=Consultar'

driver.get(url)
print(driver.title)

celulas = driver.find_elements(By.CLASS_NAME, 'historicoProcesso')
print(celulas[0].text)

driver.close()
driver.quit()