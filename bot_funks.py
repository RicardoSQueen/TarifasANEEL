import pandas as pd

def read_links(dfloc, sheet_reader, concess_not_working):
    try:
        agent = dfloc['Agente']
        validity = pd.to_datetime(dfloc['Data de Aniversário']) + pd.offsets.DateOffset(days=-1, years=1)
        sheet_name = list(sheet_reader.keys())[0]
        test = pd.read_excel(dfloc['Estrutura Tarifária'], sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
        test['Agente'] = agent
        test['Validade'] = validity
        return test, 0
    except Exception as e:
        try:
            sheet_name = list(sheet_reader.keys())[1]
            test = pd.read_excel(dfloc['Estrutura Tarifária'], sheet_name=sheet_name, skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
            test['Agente'] = agent
            test['Validade'] = validity
            return test, 1
        except Exception as e1:
            concess_not_working.append
            return f'{agent} Not Working'

def tariffs_to_df(df, sheet_reader):
    concess_not_working = []
    tarifas = pd.DataFrame()
    for i in range(df.shape[0]):
        print(df.loc[i,'Agente'])
        try:
            sheet_name = 'TA - Aplicação'
            test = pd.read_excel(df.loc[i,'Estrutura Tarifária'], sheet_name=sheet_name,skiprows=sheet_reader[sheet_name]['skiprows'], usecols=lambda x: 'Unnamed' not in x)
            test['Agente'] = df.loc[i,'Agente']
            test['Validade'] = pd.to_datetime(df.loc[i,'Data de Aniversário']) + pd.offsets.DateOffset(days=-1, years=1)
            tarifas = pd.concat([tarifas, test])
        except Exception as e:
            concess_not_working.append(df.loc[i,'Agente'])
        finally:
            pass
    print('DONE')
    cols_to_keep = ['Agente','Validade','SubGrupo','Modalidade_TA','Classe','SubClasse','Detalhe','Posto','unidade','Acessante', 'TotalTUSD', 'TotalTE']
    tarifas[cols_to_keep].to_excel('tarifas.xlsx')
