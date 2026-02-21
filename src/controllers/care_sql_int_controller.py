from src.env import table_in_lists_env # Arquivo de grupos do fortigate
from src.view.bash_view import BashView
from src.controllers.action_controller import ActionController
from src.models.repository.sql_int_repository import SqlIntRepository
from datetime import datetime, timedelta
from pytz import timezone

class CareSqlIntController:
    '''Classe Controller ATENDIMENTO - MYSQL Integrador'''
    def __init__(self):
        self.sql = str
        self.query_sql = None
        self.bash_view = BashView()
        
    def select_all_cd_atendimento_not_dt_remove_int_dic(self): # VOUCHER 2.0  
        ''' CONSULTA Código atendimento e Intera_Fortigate <=> CARE_MV - MYSQL Integrador
            Utilizado inicialmente para SETS
            RETORNA LISTA VAZIA ou LISTA COM STATUS
            ___________________________________________________________________
            VOUCHER 2.0  (process.py / )  - julho/2024
        '''
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        table = 'care_mv'
        colummns ="*" 
        # colummns ="cd_atendimento, `user-id`, name, tp_atendimento, sponsor, cd_multi_empresa, company, dt_atendimento, itera_fortigate, dt_remove, expiration, id" 
        where = "care_mv.dt_remove IS NULL "
        order = 'cd_atendimento'
        asc = True

        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        query_sql = sql_int_repository.read_query_mysql_dic(table, colummns, where, order, asc)
        return query_sql

    def select_filter_cd_atendimento_in_care_mv_dic(self, line_captured:dict, table_name, where_key_name="name", where_operator="==", where_key_type=None, key_dict=None): # VOUCHER 2.0  
        ''' RECEBE DICIONÁRIO, Parâmentro do WHERE  e chave para selecionar valor do dicionário recebido
            Utilizado inicialmente para SETS
            ### Recebe LINHA DO DICIONÁRIO() ORA-MV para selecionar a chave informada e buscar no FORTIGATE"
            ### RETORNA LISTA VAZIA OU COM DICIONÁRIO, atualizado com novas chaves e valores de acordo com o retorno do RESTAPI\n
            :guest_dict: Dicionário com chaves:valor
            :where_key_name: Nome do CAMPO existente no FORTIGATE como parâmetro para consultar na RESTAPI 
            :where_operator: Operador de comparação ( == , >= , <= , !=, <>, 'IS NOT NULL', 'IS NULL' ) 
            :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n
            ___________________________________________________________________
            VOUCHER 2.0  (process.py / )  - 24/07/2024
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


    def select_all_reg_in_table_int(self, table): # applicant TESTADO!
        ''' Seleciona todos os registros da TABELA informada no MYSQL-Integrador \n
            :table: 
            RETORNA DICIONÁRIO DA TABELA
            ______________________________________________________
            VOUCHER 2.0
        '''
        
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        _table = table
        _colummns ="*"
        where = None
        order = None
        asc = True

        # Instancia MODEL - CARE_SQL_IN_
        sql_int_repository = SqlIntRepository()
        try:
            # GERAR QUERY DO ATENDIMENTO
            self.query_sql = sql_int_repository.read_query_mysql_dic(_table, _colummns, where, order, asc)
            # print("\n END => Class GroupSqlIntController!!! \n")        # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return self.query_sql
        except Exception as exception:
            return { "success": False, "error": str(exception) }    

    def select_modify_title_care_sql_int(self) :  # VOUCHER 2.0
        ''' Consulta CARE_MV com títulos REFERENCIADOS aos CAMPOS do FORTIGATE!
            ___________________________________________________________________
            VOUCHER 2.0       
        '''
        # PARÃMETROS PARA QUERY SQL INTEGRADOR
        table = 'care_mv'
        colummns =" as `user-id`, cd_atendimento as 'name', id as id, password as 'password', cd_multi_empresa as 'company', 'expiration', 'sponsor', dt_atendimento as 'comment', itera_fortigate"
        where = None
        order = None
        asc = True

        # Instancia MODEL - CARE_SQL_IN_
        sql_int_repository = SqlIntRepository()

        try:
            # GERAR QUERY DO ATENDIMENTO
            self.query_sql = sql_int_repository.read_query_mysql_dic(table, colummns, where, order, asc)
            return self.query_sql
            # ------------------------------------------------------        
        except Exception as exception:
            return [{ "success": False}, {"error": str(exception)}]

    def insert_removed_not_found_forti_for_sql_int(self, line_captured:dict) -> list: # VOUCHER 2.0  - ATUALIZA STATUS NO MYSQL APÓS REMOÇÃO DO FORTIGATE
        ''' RECEBE DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA apenas a linha onde o user-id exist do contrário inseri NOVO
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        _table_name = 'care_mv'
        dt_remove = datetime.now()
        list_keys = ['cd_atendimento', "`user-id`", 'nr_cpf', 'name', 'sponsor', 'company', 'dt_remove', 'expiration', 'id', 'itera_fortigate']
        list_value = [line_captured["name"], line_captured["user-id"], line_captured["user-id"], line_captured["name"], line_captured["sponsor"], line_captured["company"], dt_remove, line_captured["expiration"], line_captured["id"], "REMOVED"]

        _keys = ", ".join(list_keys)

        create_query = sql_int_repository.create_line_in_mysql(_keys, list_value, "care_mv")
        return create_query

    def insert_line_care_ora_in_sql_int(self, line_captured:dict): # VOUCHER 2.0 -> grava retorno do insert do fortigate
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
        create_query = sql_int_repository.create_line_in_mysql(_keys, list_value, "care_mv")
        return create_query
        #------------------------------------------------------------
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
    def insert_return_forti_in_sql_int(self, line_captured): # VOUCHER 2.0 -> grava Registro ERRO FORTIGATE no CARE_MV - SQL
        ''' Recebe dicionário com 20 chaves e valor de Status da transação 
            Insere DT_REMOVE no dicionário com chave e valor
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
        # ENVIAR QUERY DO ATENDIMENTO
        create_query = sql_int_repository.create_line_in_mysql(_keys, list_value, "care_mv")
        return create_query
    #------------------------------------------------------------
        
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def update_return_delete_forti_for_sql_int(self, list_dict:list) -> list: # VOUCHER 2.0  - ATUALIZA STATUS NO MYSQL APÓS REMOÇÃO DO FORTIGATE
        ''' RECEBE LISTA COM DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA A DT_REMOVE = AGORA(), 
            ATUALIZA apenas a linha onde o user-id exist do contrário inseri NOVO
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'care_mv'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()

        for dict_line in list_dict:
            # Lista de valores com 8 colunas, repetir user-id na 8º COLUNA
            _list_value = [dict_line["user-id"], dict_line["id"], dict_line["itera_fortigate"], dict_line["expiration"], dict_line["dt_remove"], dict_line["name"]]
            _tuple_value= tuple(_list_value) 
            _list_value.clear()
            _insert = sql_int_repository.update_return_fortigate_care_mv(_tuple_value, _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
            # print(f"\n Retorno SQL ---------------\n {_insert}")               
        return _insert

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def update_return_insert_forti_for_sql_int(self, list_dict:list) -> list: # VOUCHER 2.0  - ATUALIZA STATUS NO MYSQL APÓS REMOÇÃO DO FORTIGATE
        ''' RECEBE LISTA COM DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA DT_REMOVE = None, 
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'care_mv'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()

        for dict_line in list_dict:
            _list_value = [dict_line["user-id"], dict_line["id"], dict_line["itera_fortigate"], dict_line["expiration"], None, dict_line["name"]]
            _tuple_value= tuple(_list_value) 
            _list_value.clear()
            _insert = sql_int_repository.update_return_fortigate_care_mv(_tuple_value, _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL
            # print(f"\n Retorno SQL ---------------\n {_insert}")               
        return _insert

    def delete_return_delete_forti_for_sql_int(self, dict:dict) -> list: # VOUCHER 2.0  - ATUALIZA STATUS NO MYSQL APÓS REMOÇÃO DO FORTIGATE
        ''' RECEBE LISTA COM DICIONÁRIO: (itera_fortigate) para ATUALIZAR NO MYSQL
            ATUALIZA A DT_REMOVE = AGORA(), 
            ATUALIZA apenas a linha onde o user-id exist do contrário inseri NOVO
            Retorna LISTA DICIONÁRIO com status operação - MYSQL
            ___________________________________________________________________
            VOUCHER 2.0  ==> Applicant: process    02/07/24
        '''    
        _table_name = 'care_mv'
        # Classes sendo instanciadas
        sql_int_repository = SqlIntRepository()
        _delete = sql_int_repository.delete_care_mysql("cd_atendimento", dict["cd_atendimento"], _table_name) # VOUCHER 2.0 Insere vários registro passados no MYSQL

        return _delete   