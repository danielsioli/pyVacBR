# pyVacBR
Pacote para obter os dados de vacinação do Ministério da Saúde disponíveis em https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao

## Use
Importar pacote
```
from pyVacBR import Vacinacao
```
Iniciar instância
```
vac = Vacinacao()
```
Obter dados do município de Macaé/RJ e armazená-los em arquivo CSV no mesmo local do script Python.
```
vac.get_dados_vacinacao(filtro={'estabelecimento_municipio_nome':'MACAE'})
```
Qualquer coluna do arquivo pode ser usada no filtro. Não é possível usar mais de uma coluna de filtro ao mesmo tempo.
O código irá buscar quantas páginas com 10 mil registros cada forem necessárias para obter todos os dados solicitados.
O DataFrame pandas será armanzenada em um arquivo com nome VACINACAO_variavel_valor_PAGINA_x_A_y.csv

Para limitar a memória ocupada pelo DataFrame pandas em 10MB
```
vac.get_dados_vacinacao(filtro={'estabelecimento_municipio_nome':'MACAE'},limite_memoria=10)
```
Cada DataFrame pandas será armanezado em um arquivo com nome VACINACAO_variavel_valor_PAGINA_x_A_y.csv

Para escolher a pasta onde o(s) arquivo(s) serão armazenados
```
vac.get_dados_vacinacao(filtro={'estabelecimento_municipio_nome':'MACAE'},limite_memoria=10,path='C:\')
```
Para limitar a quantidade de páginas de 10 mil registros que serão obtidos
```
vac.get_dados_vacinacao(filtro={'estabelecimento_municipio_nome':'MACAE'},limite_memoria=10,path='C:\',paginas=2)
```