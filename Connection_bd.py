import mysql.connector
from mysql.connector import errorcode

class Connection_bd:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        #Alterar plugin de conexão no bando de Dados
        try :
            self.cnt = mysql.connector.connect(user = self.user, password = self.password,
            host = self.host, database = self.database, auth_plugin='mysql_native_password')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def add_silos(self, silos):
        '''
            Cria entrada no banco com base no dicionario de entrada
            PARAMETROS:
                silos: lista com descricao dos silos

        '''
        cursor = self.cnt.cursor()
        add_silo = ("INSERT INTO termosilos.silo "
        "(dsc)"
        "VALUES (%(descricao)s)")
        for i in silos:
            silo_data = {
                'descricao' : str(i)
            }
            try:
                cursor.execute(add_silo, silo_data)
            except mysql.connector.Error as err:
                print("Erros encontrados: {}".format(err))
        self.cnt.commit()
        cursor.close()

    def get_id_silo(self, silo):
        '''
            Obtém o id do silo
            PARAMETROS:
                silo: string de descrição que identifica o silo
            RETORNO:
                lista, na primeira posição o status, e na segunda posição o id 
                    do silo
        '''
        cursor = self.cnt.cursor()
        try:
            query = ("SELECT  id_silo, dsc FROM termosilos.silo "
            "where dsc like %(s)s")
            inf = {'s' : silo}
            cursor.execute(query, inf)
            bd_silos = []
            for i in cursor: bd_silos.append(i)
            if bd_silos == []:
               raise Exception("Não foi encontrado o silo %s no banco!" % silo)
            elif len(bd_silos) > 1:
                raise Exception("Mútiplas referências encontradas a %s!"%silo)
        except Exception as err:
            print(err)
            cursor.close()
            return [False,-1]
        else:
            return [True, bd_silos[0][0]]

    def get_id_pendulo(self, silo, pendulo):
        '''
            Obtém o id do silo
                PARAMETROS:
                    silo: inteiro(id) de identificação do silo
                    pendulo: string de descrição que identifica o pendulo
                RETORNO:
                    lista, na primeira posição o status, e na segunda posição o id 
                        do pendulo
        '''
        cursor = self.cnt.cursor()
        try:
            query = ("SELECT  * FROM termosilos.pendulo "
            "WHERE pen_silo = %(silo)s and dsc like %(pendulo)s")
            inf = {'silo' : silo, 'pendulo' : pendulo}
            cursor.execute(query, inf)
            bd_pendulos = []
            for i in cursor: bd_pendulos.append(i)
            if bd_pendulos == []:
               raise Exception("Não foi encontrado o pendulo %d no banco!" % pendulo)
            elif len(bd_pendulos) > 1:
                raise Exception("Mútiplas referências encontradas a %d!"%pendulo)
        except Exception as err:
            print(err)
            cursor.close()
            return [False,-1]
        else:
            cursor.close()
            return [True, bd_pendulos[0][0]]

    def add_pendulos(self, silo, pendulos):
        '''
            Adiciona os Pendulos nos silos informados
            PARAMETROS:
                silo: string descrição do silo com os pendulos a serem adicionados
                pendulos: lista contendo informacoes quanto a
                    descricao do pendulo e a sua identificacao no silo
        '''
        status, pos = self.get_id_silo(silo)
        if status is False: return
        cursor = self.cnt.cursor()
        add_pendulo = ("INSERT INTO termosilos.pendulo"
            "(pen_silo, dsc)"
            "VALUES(%(silo)s, %(pendulo)s)")
        for i in pendulos:
            data_pendulo = {'silo' : pos, 'pendulo' : i}
            cursor.execute(add_pendulo, data_pendulo)
        self.cnt.commit()
        cursor.close()

    def add_sensor(self, silo, pendulo, ad_sensors):
        '''
            Adiciona o sensor ao banco de dados, com base na sua posição no pêndulo
                e endereço de fabricante
            PARAMETROS:
                silo: string com a descrição do silo
                pendulo: inteiro que identifica o pendulo no silo
                ad_sensors: lista de listas que contem a posição dos sensores nos
                    pendulos e seus respctivos MACS
        '''
        status, id_silo = self.get_id_silo(silo)
        if status != True: return
        status, id_pendulo = self.get_id_pendulo(id_silo, pendulo)
        if status != True: return
        cursor = self.cnt.cursor()
        add_sensor = ("INSERT INTO termosilos.sensor "
        "(pos_sensor, sen_pen, MAC) "
        "VALUES (%(sensor)s, %(pendulo)s, %(MAC)s)" )
        for i in ad_sensors:
            data_sensor = {'sensor' : i[0] , 'pendulo' : id_pendulo,
                'MAC': i[1]}
            cursor.execute(add_sensor, data_sensor)
        self.cnt.commit()
        cursor.close()

    def __del__(self):
        try:    
            self.cnt.close()
        except NameError as err:
            print("Banco não definido!\n")