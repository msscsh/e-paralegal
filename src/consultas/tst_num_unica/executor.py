import re, time, requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def criar_driver():
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	return driver

def resolver_processo_pje(numero_processo):
	url_pje_consulta_id = f'https://pje.tst.jus.br/pje-consulta-api/api/processos/dadosbasicos/{numero_processo}'
	headers = {
    	'X-Grau-Instancia': '3',
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
	}
	response = requests.get(url_pje_consulta_id, headers=headers)
	print(response.text)

	dados_ultima_movimentacao.append(' ')
	dados_ultima_movimentacao.append(' ')
	return dados_ultima_movimentacao

def get_dados_da_ultima_movimentacao(numero_processo):

	dados_ultima_movimentacao = []
	driver = criar_driver()

	try:

		texto_formatado = re.sub(r'[^0-9]', '.', numero_processo)
		parte_do_numero_do_processo = texto_formatado.split('.')

		url = f'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?'\
		'consulta=Consultar&'\
		'conscsjt=&'\
		f'numeroTst={parte_do_numero_do_processo[0]}&'\
		f'digitoTst={parte_do_numero_do_processo[1]}&'\
		f'anoTst={parte_do_numero_do_processo[2]}&'\
		f'orgaoTst={parte_do_numero_do_processo[3]}&'\
		f'tribunalTst={parte_do_numero_do_processo[4]}&'\
		f'varaTst={parte_do_numero_do_processo[5]}&'\
		'submit=Consultar'

		driver.get(url)
		time.sleep(2)
		current_url = driver.current_url

		if current_url != url:
			print('Fomos redirecionado')
			return resolver_processo_pje(numero_processo)
		else:
			celulas = driver.find_elements(By.CLASS_NAME, 'historicoProcesso')
			dados_ultima_movimentacao.append(celulas[1].text)
			dados_ultima_movimentacao.append(celulas[2].text)

	except Exception  as e:
		print(f'Erro: {e}')
	finally:
		driver.quit()

	return dados_ultima_movimentacao

def recuperar_processos_do_dataframe(df):
	if 0 in df.columns:
		return df[1].tolist()

def criar_dataframe_da_planilha():
	caminho_do_arquivo = './src/consultas/tst_num_unica/planilha.xlsx'
	df = pd.read_excel(caminho_do_arquivo, header=None, skiprows=4)
	return df

def escrever_dados_na_planilha(dados_data, dados_fase):
	df = pd.DataFrame({'DATA DO ANDAMENTO ': dados_data, 'FASE ATUAL': dados_fase})
	wb = Workbook()
	ws = wb.active
	for r in dataframe_to_rows(df, index=True, header=True):
	    ws.append(r)
	wb.save("./src/consultas/tst_num_unica/planilha-out.xlsx")

def processar_planilha():
	df = criar_dataframe_da_planilha()
	lista_processos = recuperar_processos_do_dataframe(df)
	dados_data = []
	dados_fase = []
	index = 748

	while index < len(lista_processos):
		numero_processo = lista_processos[index]
		print(f'Index: {index} Processo: {numero_processo}')
		numero_processo = numero_processo.zfill(25)

		dados_ultima_movimentacao = get_dados_da_ultima_movimentacao(numero_processo)
		if len(dados_ultima_movimentacao) > 0:
			index += 1
			dados_data.append(dados_ultima_movimentacao[0])
			dados_fase.append(dados_ultima_movimentacao[1])
		else:
			time.sleep(3)

	escrever_dados_na_planilha(dados_data, dados_fase)

tempo_inicial = time.time()
processar_planilha()
tempo_final = time.time()
tempo_total = tempo_final - tempo_inicial
print(f"Tempo de execução: {tempo_total:.5f} segundos")
