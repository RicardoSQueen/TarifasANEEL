from bot_funks import *
from bot_funks_low_tension import *
from covid_funks import *
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from requests import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# from chromedriver_py import binary_path # this will get you the path variable
import pandas as pd
import time

def get_df(url = 'https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/'):
    driver = webdriver.Chrome(ChromeDriverManager().install())

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
    driver.quit()
    return df


def wrapper(df, tension='high', save_path='.'):
    '''
    Tension is 'high' or 'low' or 'covid'
    '''
    if tension == 'high':
        t0, concess = tariffs_all(df)
        cols = ['Subgrupo', 'Modalidade', 'Acessante','Posto']
        t0[cols] = t0[cols].fillna(method='ffill')
        t0 = t0.sort_values(by=['Validade', 'Agente', 'Subgrupo','Modalidade', 'Acessante', 'Posto'])
        t0.to_excel(f'{save_path}/tarifas_AT.xlsx', index=False)
        t0.drop_duplicates(['Agente', 'Subgrupo','Modalidade', 'Acessante', 'Posto'], 'last').to_excel(f'{save_path}/tarifas_recentes_AT.xlsx', index=False)
        return t0
    elif tension == 'low':
        # reading excels from aneel
        t0, concess = tariffs_all_lt(df)
        cols = ['Subgrupo', 'Modalidade', 'Classe','Subclasse','Posto']
        t0[cols] = t0[cols].fillna(method='ffill')
        t0 = t0.sort_values(by=['Validade', 'Agente', 'Subgrupo','Modalidade', 'Classe','Subclasse','Posto'])
        t0.to_excel(f'{save_path}/tarifas_BT.xlsx', index=False)
        t0.drop_duplicates(['Agente', 'Subgrupo','Classe','Subclasse','Posto'], 'last').to_excel(f'{save_path}/tarifas_recentes_BT.xlsx', index=False)
        return t0
    elif tension == 'covid':
        t0, concess = tariffs_all_covid(df)
        cols = ['Subgrupo', 'Modalidade', 'Classe','Subclasse','Detalhe','UC','Posto']
        t0[cols] = t0[cols].fillna(method='ffill')
        t0 = t0[t0['UNIDADE'].notna()]
        t0.to_excel(f'{save_path}/encargos_covid.xlsx', index=False)

        return t0
    else:
        return("TEnsão é alta ou baixa")

# df = get_df()
# t2 = wrapper(df, tension='covid')
# t2[['Agente','Validade','Subgrupo', 'Modalidade', 'Classe', 'Subclasse', 'Detalhe', 'UC', 'Posto', 'CDE Covid TE']].to_excel('conta_covid.xlsx')