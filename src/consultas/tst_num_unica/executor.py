from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import time

def get_data_ultima_movimentacao(numero_processo):
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	parte_do_numero_do_processo = numero_processo.split('.')

	url = f'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?'\
	'consulta=Consultar&'\
	'conscsjt=&'\
	f'numeroTst={parte_do_numero_do_processo[0].split("-")[0]}&'\
	f'digitoTst={parte_do_numero_do_processo[0].split("-")[1]}&'\
	f'anoTst={parte_do_numero_do_processo[1]}&'\
	f'orgaoTst={parte_do_numero_do_processo[2]}&'\
	f'tribunalTst={parte_do_numero_do_processo[3]}&'\
	f'varaTst={parte_do_numero_do_processo[4]}&'\
	'submit=Consultar'

	driver.get(url)
	time.sleep(5)
	celulas = driver.find_elements(By.CLASS_NAME, 'historicoProcesso')
	return celulas[1].text

def recuperar_processos_no_arquivo():
	caminho_do_arquivo = './src/consultas/tst_num_unica/planilha.xlsx'
	df = pd.read_excel(caminho_do_arquivo, header=None, skiprows=4)
	if 0 in df.columns:
		return df[1].tolist()

lista_processos = recuperar_processos_no_arquivo()
for numero_processo in lista_processos:
	if len(numero_processo) == 25:
		data_ultima_movimentacao = get_data_ultima_movimentacao(numero_processo)
		print(data_ultima_movimentacao)
	else:
		print(f'Numero de processo inválido: {numero_processo}')
