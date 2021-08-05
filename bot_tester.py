from bot_funks import *

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
save_path = './'
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

concess=[]
o_list = []

for i in range(df.shape[0]):
    read_links(df.loc[i], o_list, concess)

