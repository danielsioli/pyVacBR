import requests
import pandas as pd

class Vacinacao():

    url = 'https://imunizacao-es.saude.gov.br/_search?scroll=1m'
    url_scroll = 'https://imunizacao-es.saude.gov.br/_search/scroll'
    usuario = 'imunizacao_public'
    senha = 'qlto5t&7r_@+#Tlstigi'

    def __init__(self):
        pass

    def _arruma_colunas(self,data_frame):
        data_frame.drop(['_index', '_type', '_id', '_score'], axis=1, inplace=True)
        colunas = data_frame.columns
        colunas = [coluna.replace('_source.', '') for coluna in colunas]
        data_frame.columns = colunas
        data_frame.set_index('document_id', inplace=True)
        return data_frame

    def get_dados_vacinacao(self,filtro=None,limite_memoria=None,path='',paginas=None):
        arquivo_nome_parte = 'VACINACAO_'
        data = {'size': '10000'}
        if filtro:
            if type(filtro) == dict:
                data = {'size': '10000', 'query': {'match': filtro}}
                for key, value in filtro.items():
                    arquivo_nome_parte += str(key) + '_' + str(value) + '_'
            else:
                print(f'O argumento filtro deve ser um dicionário. Foi recebido {type(filtro)}')
                exit()

        pagina = 1
        primeira_pagina = 1
        estouro_memoria = False
        reposta_ok = False
        r = requests.post(self.url, json=data, auth=(self.usuario, self.senha))
        if r.ok:
            resposta_ok = True
            resposta = r.json()
            hits = resposta['hits']['hits']
            if not hits or len(hits) == 0:
                print(f'Nenhum valor retornado para o filtro {filtro}')
                exit()
            df = pd.json_normalize(resposta, ['hits', 'hits'])
            df = self._arruma_colunas(df)
            memory_usage = df.memory_usage().sum() / (1024 ** 2)
            print(f'Página {pagina} - Memory Usage:{"{:3.2f}".format(memory_usage)}MB')
            pagina += 1
            hits = resposta['hits']['hits']
            data = {'scroll_id': resposta['_scroll_id'], 'scroll': '1m'}
            while r.ok and hits != None and len(hits) > 0 and (not paginas or pagina <= paginas):
                r = requests.post(self.url_scroll, json=data, auth=(self.usuario, self.senha))
                if r.ok:
                    resposta = r.json()
                    try:
                        hits = resposta['hits']['hits']
                        data = {'scroll_id': resposta['_scroll_id'], 'scroll': '1m'}
                        if limite_memoria and memory_usage > limite_memoria:
                            arquivo = arquivo_nome_parte + 'PAGINA_' + str(primeira_pagina) + '_A_' + str(
                                pagina - 1) + '.csv'
                            df.to_csv(path + arquivo, sep=';', decimal=',', encoding='latin1')
                            print(f'Arquivo {arquivo} salvo em {path}')
                            df = pd.json_normalize(resposta, ['hits', 'hits'])
                            df = self._arruma_colunas(df)
                            primeira_pagina = pagina
                            estouro_memoria = True
                        else:
                            temp = pd.json_normalize(resposta, ['hits', 'hits'])
                            temp = self._arruma_colunas(temp)
                            df = pd.concat([df, temp])
                        memory_usage = df.memory_usage().sum() / (1024 ** 2)
                        print(f'Página {pagina} - Memory Usage:{"{:3.2f}".format(memory_usage)}MB')
                        estouro_memoria = False
                    except:
                        hits = None
                    pagina += 1
                else:
                    print(f'Erro obtendo página {pagina}: {r.text}')
                    break
        else:
            print(f'Erro obtendo página {pagina}: {r.text}')

        if not estouro_memoria and resposta_ok:
            arquivo = arquivo_nome_parte + 'PAGINA_' + str(primeira_pagina) + '_A_' + str(
                pagina - 1) + '.csv'
            df.to_csv(path + arquivo, sep=';', decimal=',', encoding='latin1')
            print(f'Arquivo {arquivo} salvo em {path}')