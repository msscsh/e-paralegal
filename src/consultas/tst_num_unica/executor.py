from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import time

from datetime import datetime

def get_dados_da_ultima_movimentacao(numero_processo):
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

	dados_ultima_movimentacao = []
	dados_ultima_movimentacao.append(celulas[1].text)
	dados_ultima_movimentacao.append(celulas[2].text)

	return dados_ultima_movimentacao

def recuperar_processos_do_dataframe(df):
	if 0 in df.columns:
		return df[1].tolist()

def criar_dataframe_da_planilha(criar_dataframe_da_planilha):
	caminho_do_arquivo = './src/consultas/tst_num_unica/planilha.xlsx'
	df = pd.read_excel(caminho_do_arquivo, header=None, skiprows=criar_dataframe_da_planilha)
	return df

def escrever_dados_na_linha_da_planilha(dados, df, index, coluna_nome):
	caminho_do_arquivo = './src/consultas/tst_num_unica/planilha.xlsx'
	df.at[index, coluna_nome] = dados
	df.to_excel(caminho_do_arquivo, index=False)

linhas_offset = 4
df = criar_dataframe_da_planilha(linhas_offset)
lista_processos = recuperar_processos_do_dataframe(df)
index = linhas_offset;

print(df)

for numero_processo in lista_processos:
	index += 1
	if len(numero_processo) == 25:
		dados_ultima_movimentacao = get_dados_da_ultima_movimentacao(numero_processo)
		escrever_dados_na_linha_da_planilha(dados_ultima_movimentacao[0], df, index, 'E')
		escrever_dados_na_linha_da_planilha(dados_ultima_movimentacao[1], df, index, 'F')
	else:
		print(f'Numero de processo inválido: {numero_processo}')
