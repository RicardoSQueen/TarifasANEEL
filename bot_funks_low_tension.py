import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from support_funks import *
import traceback

def read_links(dfloc,o_list, concess_not_working):
    try:
        url = dfloc['Estrutura Tarifária']
        agent = dfloc['Agente']
        validity = pd.to_datetime(dfloc['Data de Aniversário']) + pd.offsets.DateOffset(days=-1, years=1)
    except Exception as e:
        print('Something went wrong in pre-processing of dfloc')
    sheet_reader = {
    'TA - Aplicação': {
        'skiprows':2,
        'skipcols':1
    },
    'TABELAS REH': {
        'skiprows':4,
        'skipcols':0,
        'columns': ['Subgrupo','Modalidade','Classe','Subclasse','Posto','TUSDFio','TUSDEnc','TE']
    },
    }
    # try:
    #     sheets, excbits = get_sheets_n_excel(url)
    # except Exception as e:
    #     print(f'Something went wrong downloading from {url}')
    try:
        sheet_name = 'TABELAS REH'
        test = pd.read_excel(url, sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'],usecols="L:S", header=None, names=sheet_reader[sheet_name]['columns'], engine='openpyxl', na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null'], keep_default_na = False)
        # test = pd.ExcelFile(dfloc['Estrutura Tarifária'], engine='openpyxl',encoding='latin1').parse(sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
        test = test[~test.isna().all(axis=1)]
        test['Agente'] = agent
        test['Validade'] = validity
        # return test, 0
        o_list.append(test.to_dict('records'))
        print(f'{agent} ok!\n') 
        return(None)
    except Exception as e:
        concess_not_working.append(agent)
        print(f'{agent}  Not Working')
        return(None)
def tariffs_runner(df):
    threads= []
    o_list= []
    o_list= []
    concess_not_working = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(df.shape[0]):
            dfloc = df.loc[i]
            threads.append(executor.submit(read_links, dfloc, o_list, concess_not_working))
            
    return [item for sublist in o_list for item in sublist], concess_not_working
def tariffs_all(df):
    t0, concess = tariffs_runner(df)
    t0 = pd.DataFrame(t0)
    return t0, concess
# def tariffs_to_df(df, sheet_reader):
#     concess_not_working = []
#     tarifas = pd.DataFrame()
#     for i in range(df.shape[0]):
#         print(df.loc[i,'Agente'])
#         try:
#             sheet_name = 'TA - Aplicação'
#             test = pd.read_excel(df.loc[i,'Estrutura Tarifária'], sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
#             test['Agente'] = df.loc[i,'Agente']
#             test['Validade'] = pd.to_datetime(df.loc[i,'Data de Aniversário']) + pd.offsets.DateOffset(days=-1, years=1)
#             tarifas = pd.concat([tarifas, test])
#         except Exception as e:
#             concess_not_working.append(df.loc[i,'Agente'])
#         finally:
#             pass
#     print('DONE')
#     cols_to_keep = ['Agente','Validade','SubGrupo','Modalidade_TA','Classe','SubClasse','Detalhe','Posto','unidade','Acessante', 'TotalTUSD', 'TotalTE']
#     tarifas[cols_to_keep].to_excel('tarifas.xlsx')
