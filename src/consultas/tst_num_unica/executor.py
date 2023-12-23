from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

def get_data_ultima_movimentacao(numero_processo):
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
	return celulas[1].text

	driver.close()
	driver.quit()

def recuperar_processos_no_arquivo():
	caminho_do_arquivo = './src/consultas/tst_num_unica/planilha.xlsx'
	df = pd.read_excel(caminho_do_arquivo, header=None, skiprows=4)
	if 0 in df.columns:
		return df[1].tolist()

lista_processos = recuperar_processos_no_arquivo()
print(len(lista_processos))

numero_processo = ''
data_ultima_movimentacao = get_data_ultima_movimentacao(numero_processo)
print(data_ultima_movimentacao)