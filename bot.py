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
# import urllib.request
# url = 'https://www.aneel.gov.br/resultado-dos-processos-tarifarios-de-distribuicao'
url = 'https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/'
# fp = urllib.request.urlopen(url)
# mybytes = fp.read()
page = requests.get(url)

# soup = BeautifulSoup(page.content,"html.parser")
# agent_categories = soup.find("select",{"name":"CategoriaAgente"}).findAll("option")
# agent_category = soup.find("select",{"name":"CategoriaAgente"})
# # Agents = soup.find("select",{"name":"Agentes"}).findAll("option")
# # Agents

driver.get(url)

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
sheet_reader = {
    'TA - Aplicação': {
        'skiprows':2,
        'skipcols':1
    },
    'TABELAS REH': {
        'skiprows':1,
        'skipcols':0,
    },
}
driver.close()
concess_not_working = []
tarifas0 = pd.DataFrame()
tarifas1 = pd.DataFrame()
for i in range(df.shape[0]):
    dfloc = df.loc[i]
    test, type = read_links(dfloc, sheet_reader, concess_not_working)
    if type == 0:
        tarifas0=pd.concat([tarifas0, test])
    elif type == 1:
        tarifas0=pd.concat([tarifas1, test])
    else:
        print('bugou')
print('DONE')
cols_to_keep = ['Agente','Validade','SubGrupo','Modalidade_TA','Classe','SubClasse','Detalhe','Posto','unidade','Acessante', 'TotalTUSD', 'TotalTE']
# tarifas[cols_to_keep].to_excel('tarifas.xlsx')

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
