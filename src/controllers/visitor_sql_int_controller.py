from src.controllers.action_controller import ActionController
from src.models.repository.sql_int_repository import SqlIntRepository
from datetime import datetime, date, timedelta, timezone

class VisitorSqlIntController:
    '''Classe Controller ATENDIMENTO - MYSQL Integrador'''
    def __init__(self):
        self.sql = str
        self.query_sql = None



    def insert_line_visitor_in_sql_int(self, line_captured:dict): # VOUCHER 2.0 -> grava retorno do insert do fortigate
        ''' Recebe dicionário com 12 chaves e valor de Status da transação 
            Atualiza status no dicionário com chave e valor
            Cria linha na tabela CARE_MV / MYSQL INTEGRADOR
            :line_captured: Dicionário com chaves e valores para inserção
            ___________________________________________________________________
            VOUCHER 2.O (process)     junho-2024
        '''
        # INSTANCIANDO Classes
        sql_int_repository = SqlIntRepository()
        action_controller = ActionController()
    
        _status_insert = ""
        list_tuple = []        
        # procura a chave(key_name) com valor(key_value) no dicionário passada e retorna tupla achada, caso exista
        list_value = []
        list_keys = []                    


        for k, v in line_captured.items():
            list_keys.append(k)
            list_value.append(v)

        for index, value in enumerate(list_keys):
            if value == "user-id":
                list_keys[index] = "`user-id`"
                
        _keys = ", ".join(list_keys)
        # print(f"\ncare_sql_int_controller - linha 163 - {_keys}")
        # print(f"\ncare_sql_int_controller - linha 164 - {list_value}")
        # ENVIAR QUERY DO ATENDIMENTO
        create_query = sql_int_repository.create_line_in_mysql(_keys, list_value, "contingency")
        return create_query
        #------------------------------------------------------------
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


    def update_visitor_auto_in_sql_int(self, status_insert, init_interval = 1, end_interval = 500, expiration = 28800): # VOUCHER 2.0 CRIAÇÃO DE USUÁRIOS
        '''   
            CRIA registros baseados no RANGE informado na tabela contingency - MYSQL INTEGRADOR
            ___________________________________________________________________
            VOUCHER 2.0 --> Applicant: visitor_sql_int_applicant
        '''
        # INSTANCIA Classe - SqlIntRepository
        sql_int_repository = SqlIntRepository()
        action_controller = ActionController()
        # Parâmentros para geração de x usuários
        # -----------------------------------------------------
        # "user_id, password, nr_cpf, id, tp_atendimento, cd_multi_empresa, itera_fortigate,  
        # expiration, dt_update, dt_remove, cd_atendimento, dt_atendimento, dh_criacao"
        # PARÂMETROS PARA O BANCO:
        table_name = 'contingency'
        primary_key = "`user-id`" 
        list_keys = "`user-id`, password, sponsor, user_id, password, tp_atendimento, itera_fortigate, expiration"
        _abbr_init = 'uni'
        tp_atendimento = 'V1'
        _sponsor = "VOUCHER-VISITANTE"
        itera_fortigate = status_insert
        list_value = []
        list_return = []
        tuple_value = ()
            # ------------------------------------------------------------
        for i in range(init_interval, end_interval+1):
            # Criando registros baseado em parãmentros passados   
            password = action_controller.number_random()
            number_pass = str(i) # converte em string
            user_id = _abbr_init+number_pass.zfill(5) #preencher com zeros a esquerda
            dict_create = {}
            list_value.clear()
            list_value.append(user_id)
            list_value.append(password)
            list_value.append(_sponsor)
            list_value.append(user_id)
            list_value.append(password)
            list_value.append(tp_atendimento)
            list_value.append(itera_fortigate)
            list_value.append(expiration)
            # insere a lista de valores acima em uma nova lista de tuplas
            tuple_value = tuple(list_value)
            # list_tuple.append(tuple(list_value))
            try:
                # ENVIAR QUERY para atualizar o banco INTEGRADOR
                create_query = sql_int_repository.create_duplicate_key_mysql(tuple_value, list_keys, table_name, primary_key, f"'{user_id}'")
                # ------------------------------------------------------------
                # print(f"\n Retorno ==> visitor_sql_int_controller => create_duplicate_key_mysql: {create_query}")
                # ------------------------------------------------------------

            except Exception as exception:
                list_return.append({"status": "error"}) 
                return list_return
        list_return.append({"status": "success"})    
        return list_return

    def select_filter_cd_atendimento_in_visitor_dic(self, line_captured:dict, table_name, where_key_name="name", where_operator="==", where_key_type=None, key_dict=None): # VOUCHER 2.0  
        ''' RECEBE DICIONÁRIO, Parâmentro do WHERE  e chave para selecionar valor do dicionário recebido
            Utilizado inicialmente para SETS
            ### Recebe LINHA DO DICIONÁRIO() RESAPI para selecionar a chave informada e buscar no SQL"
            ### RETORNA LISTA VAZIA OU COM DICIONÁRIO atualizado com novas chaves e valores de acordo com o retorno do RESTAPI\n
            :line_captured: Dicionário com chaves:valor
            :table_name: Tabela do banco para realizar a consulta
            :where_key_name: Nome do CAMPO existente no DICIONÁRIO recebido como parâmetro para usar na consulta 
            :where_operator: Operador de comparação ( == , >= , <= , !=, <>, 'IS NOT NULL', 'IS NULL' ) 
            :where_key_type: Tipo do valor da chave :where_key_name:
            :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n
            ___________________________________________________________________
            VOUCHER 2.0  (process.py / )  - julho/2024
        '''
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        table = table_name
        colummns ='*' 
        order = None
        asc = True
        # print(f"\n\n CARE_SQL_INT_CONTROLER 51  ----> {line_captured[key_dict]}\n\n")
        # passa o valor da chave para a variável DE FILTRO.
        if where_key_type == "str":
            _value_key = f"'{line_captured[key_dict]}'"
        else:    
            _value_key = line_captured[key_dict]
    
        where = f"{where_key_name} {where_operator} {_value_key} "
        # print(f"\n\n where ----> {where}\n\n")
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        query_sql = sql_int_repository.read_fetchall_mysql_dic(table, colummns, where, order, asc)
        
        return query_sql


    def select_visitor_modify_title_sql_int(self, where=None) : # VOUCHER 2.0  - 
        ''' Consulta contingency com títulos REFERENCIADOS aos CAMPOS do FORTIGATE!
            ___________________________________________________________________
            VOUCHER 2.0 
            Utilizado por: process        
        '''
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        _table = 'contingency'
        _colummns ="id as id, user_id as `user-id`, password as password, nr_cpf as name, (select expire from forti_group where tp_atendimento = contingency.tp_atendimento) as 'expiration', sponsor, cd_multi_empresa as 'company',  CONCAT('Tipo: ', tp_atendimento,' | Cod.Empresa: ', cd_multi_empresa, ' | Data Criação: ', dt_update) as 'comment', itera_fortigate"
        _where = where
        _order = "`user-id`"
        _asc = True
        # Instancia MODEL - CARE_SQL_IN_
        sql_int_repository = SqlIntRepository()

        # GERAR QUERY DO ATENDIMENTO
        # print("\n Start => Class GroupSqlIntController!!! \n") 
        self.query_sql = sql_int_repository.read_query_mysql_dic(_table, _colummns, _where, _order, _asc)
        return self.query_sql
        # ------------------------------------------------------        

    def select_user_id_sql_int_dic(self): # applicant TESTADO
        ''' CONSULTA id do usuário e Intera_Fortigate <=> Visitante - MYSQL Integrador
            Utilizado inicialmente para SETS
            ___________________________________________________________________
            Applicant: visitor_sql_int_applicant
        '''
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        _table = 'contingency'
        _colummns ="*"
        _where = None
        _order = "`user-id`"
        _asc = True

        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        
        try:
            # GERAR QUERY DO ATENDIMENTO
            self.query_sql = sql_int_repository.read_query_mysql_dic(_table, _colummns, _where, _order, _asc)

            # print("\n END => Method select_cd_atendimento_sql_int_dic <==> Class CareSqlIntController \n")        # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return self.query_sql
        except Exception as exception:
            # print("\n END => Method select_cd_atendimento_sql_int_dic <==> Class CareSqlIntController \n")        # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return [{ "status": "error", "erro de exceção": str(exception) }]


    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def update_visitor_return_forti_for_sql_int(self, list_dict:list) -> list: # VOUCHER 2.0    ATUALIZA MYSQL COM STATUS DA DATA DE REMOÇÃO
        ''' RECEBE LISTA COM DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA apenas a linha onde o user-id exist do contrário inseri NOVO
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'contingency'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()

        # INSERT INTO fortinet_voucher.contingency () VALUES ('uni00016', 'uni00016', 17, 'REMOVED', 0, '') ON DUPLICATE KEY UPDATE `user-id`='uni00016'
        for dict_line in list_dict:
            # Lista de valores com 8 colunas, repetir user-id na 8º COLUNA
            _list_value = [dict_line["user-id"], dict_line["user-id"], dict_line["id"], dict_line["itera_fortigate"], dict_line["expiration"], dict_line["dt_remove"], None, dict_line["user-id"]]
            _tuple_value= tuple(_list_value) 
            _list_value.clear()
            # print(f"\n Tupla criada a partir da lista criada ---------------\n {_tuple_value}")               
            # _value_key = f"'{dict_line["user-id"]}'"
            _insert = sql_int_repository.update_visitor_return_fortigate_mysql(_tuple_value, _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
            # print(f"\n Retorno SQL ---------------\n {_insert}")               

        return _insert


    def update_visitor_expiration_forti_for_sql_int(self, dict_line:dict) -> list: # VOUCHER 2.0    ATUALIZA MYSQL COM STATUS DA DATA DE REMOÇÃO
        ''' RECEBE LINHA DO DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA COM INFORMAÇÕES DO FORTIGATE
            Retorna LISTA C/ DICIONÁRIO com status da operação
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'contingency'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        _itera_fortigate = "EXPIRATION" 
        _dt_remove = datetime.now()
        # Lista de valores com 8 colunas, repetir user-id na 8º COLUNA
        _list_value = [dict_line["user-id"], dict_line["user-id"], dict_line["id"], _itera_fortigate, dict_line["expiration"], _dt_remove, None, dict_line["user-id"]]
        # converte lista em tupla e envia para sql
        _tuple_value= tuple(_list_value) 

        _insert = sql_int_repository.update_visitor_return_fortigate_mysql(_tuple_value, _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
        # print(f"\n Retorno SQL ---------------\n {_insert}")               

        return _insert

    def delete_expiration_visitor_sql_int(self, dict:dict) -> list: # VOUCHER 2.0    ATUALIZA MYSQL COM STATUS DA DATA DE REMOÇÃO
        ''' RECEBE DICIONÁRIO para DELETAR NO MYSQL
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'contingency'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        # print(f"3333333333333333333333333333333333 visitor_sql_controller - linha 208 {dict}")
        _delete = sql_int_repository.delete_care_mysql("`user-id`", dict["user-id"], _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
        return _delete    
    
    # def delete_expiration_visitor_sql_int(self, list_dict:list) -> list: # VOUCHER 2.0    ATUALIZA MYSQL COM STATUS DA DATA DE REMOÇÃO
    #     ''' RECEBE LISTA COM DICIONÁRIO: (itera_fortigate) para DELETAR NO MYSQL
    #         ATUALIZA apenas a linha onde o user-id exist do contrário inseri NOVO
    #         Retorna LISTA DICIONÁRIO com status operação - MYSQL
    #         ___________________________________________________________________
    #         VOUCHER 2.0  ==> Applicant: process    02/07/24
    #     '''    
    #     _table_name = 'contingency'
    #     # Classes sendo instanciadas
    #     sql_int_repository = SqlIntRepository()

    #     for dict_line in list_dict:
    #         _delete = sql_int_repository.delete_care_mysql("`user-id`", dict_line["user-id"], _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
    #     return _delete        