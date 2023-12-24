from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import time

from datetime import datetime

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def get_dados_da_ultima_movimentacao(numero_processo):

	dados_ultima_movimentacao = []

	try:
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
		time.sleep(2)
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

def recuperar_processos_ignorados():
	lista_de_ignorados = []
	return lista_de_ignorados

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
	lista_processos_ignorados = recuperar_processos_ignorados()
	dados_data = []
	dados_fase = []
	index = 0

	while index < len(lista_processos):
		numero_processo = lista_processos[index]
		print(f'Index: {index} Processo: {numero_processo}')
		if numero_processo in lista_processos_ignorados:
			print(f'Ignorando processo: {numero_processo}')
			dados_data.append(' ')
			dados_fase.append(' ')
		elif len(numero_processo) == 25:
			dados_ultima_movimentacao = get_dados_da_ultima_movimentacao(numero_processo)
			if len(dados_ultima_movimentacao) > 0:
				index += 1
				dados_data.append(dados_ultima_movimentacao[0])
				dados_fase.append(dados_ultima_movimentacao[1])
			else:
				time.sleep(5)
		else:
			print(f'Numero de processo inválido: {numero_processo}')

	escrever_dados_na_planilha(dados_data, dados_fase)

processar_planilha()