import csv
from Connection_bd import Connection_bd

def mac2gatm(mac_id):
    '''
        Converte o MAC obtido no arquivo csv no padrao 0x28xxx...
            para o padrao xxx28
    '''
    mac = mac_id.replace("0x", "")
    mac = mac.replace(" ", "")
    mac = mac.split(",")
    mac.reverse()
    return "".join(mac)


def partner_old2new(row):
    '''
        Identifica qual padrao
    '''
    if row.find("0x28")>=0:
        pendulo = mac2gatm(row)
    else:
        pendulo = row
    return pendulo


def csv2dict_sensors(file):
    '''
        Converte os dados do csv em uma dict no padrao posicao_pendulo:MAC
        PARAMETROS:
            file: arquivo.csv
        RETURN:
            dict
    '''
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        filter_list = list(filter(lambda x: (x[1].find('0x28') >= 0), csv_reader))
        id_mac = {}
        for row in filter_list: id_mac[row[5]] = row[1]
        return id_mac


def csv2dict_si_sen(file):
    '''
        Converte os dados do csv em uma dict no padrao silo{posicao_pendulo:MAC}
        PARAMETROS:
            file: arquivo.csv
        RETURN:
            dict{dict}
    '''
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        filter_list = list(filter(lambda x: ((x[0].find('28') >= 0) or 
                (x[5].find('SENSORES') >= 0) ), csv_reader))
        pendulo = 1
        pen_id_m = {}
        for row in filter_list:
            if row[5] == "SENSORES":
                pendulo = int(row[0])
                continue
            if pendulo in pen_id_m.keys():
                pen_id_m[pendulo].update({row[5]: partner_old2new(row[0])})
            else: pen_id_m[pendulo] = {row[5]: partner_old2new(row[0])}
    return pen_id_m
    """
        silo é uma lista com os nomes dos arquivos de extensão .csv
    """
silo = ["silo1", "silo2", "silo3","silo4"]

bd = Connection_bd("root", "pass", "bd.com", "bdName")

bd.add_silos(silo)
for i in silo:
    info = csv2dict_si_sen("./silos/"+i+".csv")
    for pen, sensor in info.items():
        bd.add_pendulos(i, [str(pen)])
        bd.add_sensor(i, pen, sensor.items())
