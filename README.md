# Cadastro de sensores DS18B20 em Banco de Dados a partir de arquivos .csv #
Neste repositório, é feito o cadastro de sensores de um arquivo csv, de formato específico para serrem adicionados no Banco de Dados com informações de Silo, Pêndulos e Sensores

## Pré-requisito ##

- Python 3.6;
- pip install mysql-connector-python => Conector MySql para python

## Utilização ##

O arquivo Main, é o Connection_bd.py, ou seja, o ponto de partida da aplicação.

No mesmo diretório da aplicação deve ter uma pasta chamada silos, com os arquivos .csv dentro dela, e os seus nomes dentro da lista na linha 68 do arquivo add_sensors_bd.py.

Após preparado o ambiente para instalação, configurar a conexão do BD na linha 70 e executar:

```shell
python3 add_sensors_bd.py
```