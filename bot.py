from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from requests import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from chromedriver_py import binary_path # this will get you the path variable
import pandas as pd
import time
driver = webdriver.Chrome(executable_path=binary_path)
from bot_funks import *
url = 'https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/'
page = requests.get(url)

driver.get(url)
status = 0
while status==0:
    try:

        agent_category = Select(driver.find_element_by_name('CategoriaAgente'))
        # select by visible text
        agent_category.select_by_visible_text('Todos')

        time.sleep(0.5)
        agent = Select(driver.find_element_by_name('Agentes'))
        agent.select_by_visible_text('Todos')

        time.sleep(0.5)
        agent = Select(driver.find_element_by_name('TipoProcesso'))
        agent.select_by_visible_text('Todos')

        time.sleep(0.5)
        agent = Select(driver.find_element_by_name('Ano'))
        agent.select_by_visible_text('Todos')
        # get element
        time.sleep(0.5)
        element = driver.find_element_by_xpath('//input[@value="Procurar"]')
        # click the element
        element.click()
        time.sleep(10)
        ## criando df
        html_source = driver.page_source
        # dfs = pd.read_html(html_source, skiprows=[0,3])
        # dfs[1]

        soup = BeautifulSoup(html_source, 'html.parser')
        table = soup.findAll('table')[1]
        status=1
        print('\r foi')
    except Exception as e:
        print('\r nao foi')
        time.sleep(1)

records = []
columns = []
for tr in table.findAll("tr"):
    ths = tr.findAll("th")
    if ths != []:
        for each in ths:
            columns.append(each.text)
    else:
        trs = tr.findAll("td")
        record = []
        for each in trs:
            try:
                links = each.find('a')['href']
                text = each.text
                record.append([links])
                # record.append(text)
            except:
                text = each.text
                record.append(text)
        records.append(record)

columns.insert(1, 'Link')
df = pd.DataFrame(data=records[2:], columns=records[1])
df = df.replace('\n','', regex=True).replace('\t','', regex=True).replace('\xa0','', regex=True)
df = df.drop(index=0).reset_index(drop=True)
df['Data de Aniversário'] = pd.to_datetime(df['Data de Aniversário'], dayfirst=True)
remove_filter = (df['Estrutura Tarifária'].apply(lambda x: len(x)) >0) & (df['Data de Aniversário'].dt.year >= datetime.now().year -1)
df = df[remove_filter].reset_index(drop=True)
df['Estrutura Tarifária'] = df['Estrutura Tarifária'].apply(lambda x: x[0]).str.replace(' ', '%20')
cols = ['Agente', 'Categoria do Agente', 'Tipo de Processo', 'Data de Aniversário', 'Status Resultado', 'Estrutura Tarifária']
df = df[cols]
driver.close()

# reading excels from aneel
t0, concess = tariffs_all(df)
t0 = t0.fillna(method='ffill')
t0 = t0.sort_values(by=['Validade', 'Agente', 'Subgrupo','Modalidade', 'Acessante', 'Posto'])
t0.to_excel('tarifas.xlsx')
t0.drop_duplicates(['Agente', 'Subgrupo','Modalidade', 'Acessante', 'Posto'], 'last').to_excel('tarifas_recentes.xlsx')

# concess_not_working = []
# o_list = []

# tarifas = pd.DataFrame()
# print(df.shape[0])
# for i in range(df.shape[0]):
#     print(f'{i+1} de {df.shape[0]}')
#     dfloc = df.loc[i]
#     test = read_links(dfloc, o_list, concess_not_working)
#     # read_links(zipfile, o_list, o_list, concess_not_working)
#     # break
#     # tarifas=pd.concat([tarifas, test])
# print('DONE')
# tarifas = pd.DataFrame([item for sublist in o_list for item in sublist])
# tarifas = tarifas.fillna(method='ffill')
# cols_to_keep = ['Agente','Validade','SubGrupo','Modalidade_TA','Classe','SubClasse','Detalhe','Posto','unidade','Acessante', 'TotalTUSD', 'TotalTE']
# # tarifas[cols_to_keep].to_excel('tarifas.xlsx')




#    print(df.loc[i,'Agente'])
    # try:
    #     sheet_name = 'TA - Aplicação'
    #     test = pd.read_excel(df.loc[i,'Estrutura Tarifária'], sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
    #     test['Agente'] = df.loc[i,'Agente']
    #     test['Validade'] = pd.to_datetime(df.loc[i,'Data de Aniversário']) + pd.offsets.DateOffset(days=-1, years=1)
    #     tarifas = pd.concat([tarifas, test])
    # except Exception as e:
    #     concess_not_working.append(df.loc[i,'Agente'])
    # finally:
    #     pass
