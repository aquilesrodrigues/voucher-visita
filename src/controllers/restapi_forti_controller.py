from src.view.bash_view import BashView
from src.env import table_in_lists_env # Arquivo de grupos do fortigate
from src.controllers.action_controller import ActionController
from src.models.repository.restapi_forti_repository import RestFortiRepository
from datetime import datetime, date, time, timedelta
import copy
from pytz import timezone


class RestAPIFortiController:
    """_summary_
        Classe Controller RestAPI FORTIGATE
        TODOS OS MÉTODOS AQUI RETORNA LISTA
    """
    def __init__(self):
        self.sql = str
        self.query_sql = None
        self.child_name = dict() 
        self.filter_param = ""
        self.bash_view = BashView()
        self.time_difference = timedelta(hours=-3)

    def get_all_groups_from_rest_forti(self) -> list: # VOUCHER 2.0 ==> todos registros
        ''' 
        #### Seleciona Todos os REGISTROS COM SEUS GRUPOS no fortigate
        RETORNA LISTA Dicionário AGRUPANDO os registros de cada grupo. 
        ___________________________________________________________________
        Voucher 2.0  03-07-24
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        # action_controller = ActionController()
        self._method = "get"
        self._mkey = ""
        self.child_name=""
        self.child_key=""
        response = rest_forti_repository.all_methods_in_forti(self._method, self._mkey, self.child_name, self.child_key)
        return response



    def get_all_guest_by_groups_in_rest_forti(self, list_groups:list) -> list: # VOUCHER 2.0 ==> todos registros
        ''' 
        #### Seleciona Todos os registros do fortigate baseado na lista dos GRUPOS passados
        :list_groups: lista dos grupos para consulta
        RETORNA LISTA Dicionário AGRUPANDO os registros de cada grupo. 
        :list_group: Lista com nome dos grupos para procura no fortigate
        ___________________________________________________________________
        Voucher 2.0  03-07-24
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        # action_controller = ActionController()
        self._method = "get"
        self.child_name="/guest"
        self.child_key=""
        _list_dict = []
        for i in list_groups:
            self._mkey= f"/{i}" # nome do grupo Iterado
            # response = rest_forti_repository.get_all_guest_in_groups(self._mkey, self.child_name, self.child_key)
            response = rest_forti_repository.all_methods_in_forti(self._method, self._mkey, self.child_name, self.child_key)
            payload = response
            if payload["http_status"] == 200:
                if "results" in payload:
                    if len(payload["results"]) != 0:
                        for line_dic in payload["results"]:
                            _list_dict.append(line_dic)
            else:
                _list_dict.append(payload)
                return _list_dict

        return _list_dict

    def get_all_guest_groups_filter_rest_forti(self, list_groups:list, filter_param) -> list: # VOUCHER 2.0  ==> Expiration <= 0
        ''' 
        Lista Todos os registros do FORTIGATE baseado na lista dos GRUPOS com valor para a chave passada
        RETORNA LISTA Dicionário com [chave:'valor'] OU LISTA vazia caso náo consiga. 
        :list_group: Lista com nome dos grupos para procura no fortigate
        Exemplo: todos com chave expiration <= hora atual
        ___________________________________________________________________
        Voucher 2.0 (process / )    junho-2024
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        # action_controller = ActionController()
        _method = "get-filter"

        self.child_name="/guest"
        self.child_key=""

        _filter_param = f"filter={filter_param}" # filtro para consulta após gravação no fortigate 
        _list_dict = []
        # Executa método de GET-FILTER para procurar o atendimento inserido usando o FILTER_PARAM e retorna o PAYLOAD 

        for i in list_groups:
            _mkey= f"/{i}" # nome do grupo Iterado
            # _mkey= f"/Ambulatorio" # nome do grupo Iterado
            response = rest_forti_repository.all_methods_in_forti(_method, _mkey, self.child_name, self.child_key, None, _filter_param)
            payload = response
            if payload["http_status"] == 200:
                if len(payload["results"]) != 0:
                    for line_list in payload["results"]:
                        _list_dict.append(line_list)
            else:
                _list_dict.append(payload)
                return _list_dict
        return _list_dict

    def get_care_mv_filter_key_rest_forti(self, care_mv_dict:dict, filter_key_name="name", filter_operator="==", filter_key_type='str', key_dict=None) -> list: # VOUCHER 2.0  ==> Busca atendimento 
        ''' ### Recebe LINHA DO DICIONÁRIO() CARE_MV para selecionar a chave informada e buscar no FORTIGATE"
            ### RETORNA O DICIONÁRIO, atualizado com novas chaves e valores de acordo com o retorno do RESTAPI\n
            :guest_dict: Dicionário com chaves:valor
            :filter_key_name: Nome do CAMPO existente no FORTIGATE como parâmetro para consultar na RESTAPI 
            :filter_operator: Operador de comparação ( == , >= , <= , != ) 
            :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n

        VOUCHER 2.0  - USAR PARA ATENDIMENTO / VISITANTES   julho-2024
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        _method = "get-filter"
        _itera_fortigate = "IN.FORTIGATE"
        _child_name="/guest"
        _child_key=""
        _list_dict = []
        
        # CRIA DICIONÁRIO COM CHAVES DO FORTIGATE
        stamp_care_mv_dict = action_controller.stamp_from_ora_mv_to_guest_forti(care_mv_dict, _itera_fortigate, "*") 
        # print(f"{stamp_care_mv_dict}")
        
        _group = f"/{stamp_care_mv_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        # passa o valor da chave para a variável DE FILTRO.
        if filter_key_type == "str":
            _value_key = f"'{care_mv_dict[key_dict]}'"
        else:    
            _value_key = care_mv_dict[key_dict]
            
        _filter_str = f"{filter_key_name}{filter_operator}{_value_key}"
        _filter_param = f"filter={_filter_str}" # filtro para consulta   
        # Executa método de GET para procurar o atendimento usando o FILTER_PARAM e retornando o PAYLOAD 
        payload = rest_forti_repository.all_methods_in_forti(_method, _group, _child_name, _child_key, None, _filter_param)
        # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
        if "status" in payload:
            if payload['http_status'] == 200:          
                for results in payload["results"]:
                    if "id" in results:
                        stamp_care_mv_dict.update(id = results["id"])
                    if "expiration" in results:  
                        stamp_care_mv_dict.update(expiration = results["expiration"])
                    stamp_care_mv_dict.update(itera_fortigate = 'IN.FORTIGATE')
                    stamp_care_mv_dict.update(status = payload['status'])    
                    stamp_care_mv_dict.update(http_status = payload['http_status'])      
                    _code = payload['http_status']
                    resp = action_controller.request_response(_code)
                    stamp_care_mv_dict.update(status_message = resp)          
                    # -----------------------------------------------------------
                    _list_dict.append(stamp_care_mv_dict)
            else:
                stamp_care_mv_dict.update(itera_fortigate = 'NOT.FORTIGATE')
                stamp_care_mv_dict.update(status = payload['status'])    
                stamp_care_mv_dict.update(http_status = payload['http_status'])
                _code = payload['http_status']
                resp = action_controller.request_response(_code)
                stamp_care_mv_dict.update(status_message = resp)          
                # -----------------------------------------------------------
                _list_dict.append(stamp_care_mv_dict)
        return _list_dict 
    
    # # NOVO MÉTODO PARA CARIMBAR E FILTRAR NO FORTIGATE 13/08/2024
    # # --------------------------------------------------------------------
    # def get_atendime_for_filter_key_in_rest_forti(self, guest_dict:dict, filter_key_name="name", filter_operator="==", filter_key_type=None, key_dict=None) -> list: # VOUCHER 2.0  ==> BUSCA LINHA DICIONÁRIO() ORA-MV DENTRO FORTIGATE 
    #     ''' ### Recebe DICIONÁRIO{} contendo a chave e valor a ser procurado dentro do FORTIGATE"
    #         ### RETORNA O DICIONÁRIO, com chaves em caixa-baixa e atualizadas com novas chaves e valores de acordo com o retorno do RESTAPI\n
    #         :guest_dict: Dicionário com chaves:valor (precisa ter a chave informada no parâmetro - key_dict - )
    #         :filter_key_name: Nome do CAMPO existente no FORTIGATE como parâmetro para consultar na RESTAPI
    #         :filter_operator: Operador de comparação ( == , >= , <= , != ) 
    #         :filter_key_type: Se informado  "str", converterá o valor do parâmetro - key_dict - em string
    #         :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n
    #     _________________________________________________________________________________\n
    #     VOUCHER 2.0  - USAR PARA ATENDIMENTOS DO MV   13/08/2024 - Agosto-2024
    #     '''           
    #     # Instancia MODEL - UsersRestFortiRepository
    #     # --------------------------------------------------------------------
    #     rest_forti_repository = RestFortiRepository() 
    #     action_controller = ActionController()
    #     # ---------------------------------------------------------------------
    #     _method = "get-filter"
    #     _itera_fortigate = "IN.FORTIGATE"
    #     _child_name="/guest"
    #     _child_key=""
    #     list_dict = []

    #     # ATUALIZAR DICIONÁRIO COM CHAVES PARA O FORTIGATE
    #     stamp_dict = action_controller.stamp_dict_ora_mv_to_guest_forti(guest_dict, _itera_fortigate, "*")        

    #     # print(f"\n\n gest_atendimento_ora_filter_key_rest_forti == DICT_JOIN --> {dict_join} \n")   

    #     if stamp_dict['itera_fortigate'] == "INVALID":
    #         stamp_dict.update(status = "error")
    #         stamp_dict.update(http_status = 000)
    #         resp = action_controller.request_response(000) # Desc código erro
    #         stamp_dict.update(status_message = resp)
    #         # ---------------------------------------------------------------            
    #         list_dict.append(stamp_dict)
    #         return list_dict

    #     _group = f"/{stamp_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
    #     # passa o valor da chave para a variável DE FILTRO.
    #     if filter_key_type == "str":
    #         _value_key = f"'{stamp_dict[key_dict]}'"
    #     else:    
    #         _value_key = stamp_dict[key_dict]
    #     _filter_str = f"{filter_key_name}{filter_operator}{_value_key}"
    #     _filter_param = f"filter={_filter_str}" # filtro para consulta   

    #     # Executa método de GET para procurar o atendimento usando o FILTER_PARAM e retornando o PAYLOAD 
    #     payload = rest_forti_repository.all_methods_in_forti(_method, _group, _child_name, _child_key, None, _filter_param)
    #     # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
    #     # print(f"\n Linha 224 - restapi_forti_controller ==> {payload}")
    #     # if "http_status" in payload:
    #     if payload['http_status'] == 200:
    #         # print(f"\nIMPRIMIR PAYLOAD DEPOIS DO IF HTTP_STATUS \n {payload} \n\n")          
    #         if len(payload["results"]) > 0:
    #             for results in payload["results"]:
    #                 if "id" in results:
    #                     stamp_dict.update(id = results["id"])
    #                 if "expiration" in results:  
    #                     stamp_dict.update(expiration = results["expiration"])
    #                 # -----------------------------------------------------------
    #                 stamp_dict.update(itera_fortigate = 'IN.FORTIGATE')
    #         else:
    #             stamp_dict.update(id = None)
    #             stamp_dict.update(itera_fortigate = 'NOT.FORTIGATE')

    #         stamp_dict.update(status = payload['status'])    
    #         stamp_dict.update(http_status = payload['http_status'])      
    #         _code = payload['http_status']
    #         resp = action_controller.request_response(_code)
    #         stamp_dict.update(status_message = resp)
            
    #         list_dict.append(stamp_dict)
    #     else:
    #         stamp_dict.update(id = None)
    #         stamp_dict.update(itera_fortigate = 'ERROR.FORTIGATE')
    #         stamp_dict.update(status = payload['status'])    
    #         stamp_dict.update(http_status = payload['http_status'])
    #         _code = payload['http_status']
    #         resp = action_controller.request_response(_code)
    #         stamp_dict.update(status_message = resp)          
    #         # -----------------------------------------------------------
    #         list_dict.append(stamp_dict)
    #     # else:
    #     #     stamp_dict.update(itera_fortigate = 'ERROR.RESTAPI')
    #     #     stamp_dict.update(status = payload['status'])    
    #     #     stamp_dict.update(http_status = payload['http_status'])
    #     #     list_dict.append(stamp_dict)
        
    #     return list_dict





    # ANTIGO MÉTODO PARA CARIMBAR E FILTRAR NO FORTIGATE
    # --------------------------------------------------------------------
    def get_atendime_ora_filter_key_rest_forti(self, guest_dict:dict, filter_key_name="name", filter_operator="==", filter_key_type=None, key_dict=None) -> list: # VOUCHER 2.0  ==> BUSCA LINHA DICIONÁRIO() ORA-MV DENTRO FORTIGATE 
        ''' ### Recebe LINHA DO DICIONÁRIO() ORA-MV para selecionar a chave informada e buscar no FORTIGATE"
            ### RETORNA O DICIONÁRIO, atualizado com novas chaves e valores de acordo com o retorno do RESTAPI\n
            :guest_dict: Dicionário com chaves:valor
            :filter_key_name: Nome do CAMPO existente no FORTIGATE como parâmetro para consultar na RESTAPI 
            :filter_operator: Operador de comparação ( == , >= , <= , != ) 
            :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n
        ___________________________________________________________________\n
        VOUCHER 2.0  - USAR PARA ATENDIMENTO / VISITANTES   junho-2024
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        _method = "get-filter"
        _itera_fortigate = "IN.FORTIGATE"
        _child_name="/guest"
        _child_key=""
        list_dict = []

        # CRIA DICIONÁRIO COM CHAVES DO FORTIGATE
        stamp_dict = action_controller.stamp_from_ora_mv_to_guest_forti(guest_dict, _itera_fortigate, "*")        
        # JUNTA OS DOIS DICIONÁRIOS
        dict_join = action_controller.join_dict(guest_dict, stamp_dict)
        dict_join.pop('comment')

        # print(f"\n\n gest_atendimento_ora_filter_key_rest_forti == DICT_JOIN --> {dict_join} \n")   

        if stamp_dict['itera_fortigate'] == "NOT.FORTIGATE":
            dict_join.update(id = None)
            dict_join.update(user_id = None)
            dict_join.update(password = None)
            dict_join.update(status = "error")
            dict_join.update(http_status = 000)
            resp = action_controller.request_response(000) # Desc código erro
            dict_join.update(status_message = resp)
            # ---------------------------------------------------------------            
            list_dict.append(dict_join)
            return list_dict

        _group = f"/{stamp_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        # passa o valor da chave para a variável DE FILTRO.
        if filter_key_type == "str":
            _value_key = f"'{guest_dict[key_dict]}'"
        else:    
            _value_key = guest_dict[key_dict]
        _filter_str = f"{filter_key_name}{filter_operator}{_value_key}"
        _filter_param = f"filter={_filter_str}" # filtro para consulta   

        # Executa método de GET para procurar o atendimento usando o FILTER_PARAM e retornando o PAYLOAD 
        payload = rest_forti_repository.all_methods_in_forti(_method, _group, _child_name, _child_key, None, _filter_param)
        # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
        # print(f"\n Linha 208 - restapi_forti_controller ==> {payload}")
        # if "http_status" in payload:
        if payload['http_status'] == 200:
            # print(f"\nIMPRIMIR PAYLOAD DEPOIS DO IF HTTP_STATUS \n {payload} \n\n")          
            if len(payload["results"]) > 0:
                for results in payload["results"]:
                    if "id" in results:
                        dict_join.update(id = results["id"])
                    if "expiration" in results:  
                        dict_join.update(expiration = results["expiration"])
                    # -----------------------------------------------------------
                    dict_join.update(itera_fortigate = 'IN.FORTIGATE')
            else:
                dict_join.update(id = None)
                dict_join.update(itera_fortigate = 'NOT.FORTIGATE')

            dict_join.update(status = payload['status'])    
            dict_join.update(http_status = payload['http_status'])      
            _code = payload['http_status']
            resp = action_controller.request_response(_code)
            dict_join.update(status_message = resp)
            
            list_dict.append(dict_join)
        else:
            dict_join.update(id = None)
            dict_join.update(itera_fortigate = 'ERROR.FORTIGATE')
            dict_join.update(status = payload['status'])    
            dict_join.update(http_status = payload['http_status'])
            _code = payload['http_status']
            resp = action_controller.request_response(_code)
            dict_join.update(status_message = resp)          
            # -----------------------------------------------------------
            list_dict.append(dict_join)
        # else:
        #     dict_join.update(itera_fortigate = 'ERROR.RESTAPI')
        #     dict_join.update(status = payload['status'])    
        #     dict_join.update(http_status = payload['http_status'])
        #     list_dict.append(dict_join)
        
        return list_dict


    def get_atendime_sql_filter_key_rest_forti(self, guest_dict:dict, filter_key_name="name", filter_operator="==", filter_key_type=None, key_dict=None) -> list: # VOUCHER 2.0  ==> BUSCA LINHA DICIONÁRIO() ORA-MV DENTRO FORTIGATE 
        ''' ### Recebe LINHA DO DICIONÁRIO VINDO DO CARE_MV para selecionar o VALOR da chave informada e buscar no FORTIGATE"
            ### RETORNA O DICIONÁRIO, atualizado com novas chaves e valores de acordo com o retorno do RESTAPI\n
            :guest_dict: Dicionário com chaves:valor
            :filter_key_name: Nome do CAMPO existente no FORTIGATE como parâmetro para consultar na RESTAPI 
            :filter_operator: Operador de comparação ( == , >= , <= , != ) 
            :key_dict: nome da Chave existente no dicionário RECEBIDO, onde iremos buscar o VALOR para a consulta no FORTIGATE\n
        ___________________________________________________________________\n
        VOUCHER 2.0  - USAR PARA ATENDIMENTO / VISITANTES   junho-2024
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        _method = "get-filter"
        _itera_fortigate = "IN.FORTIGATE"
        _child_name="/guest"
        _child_key=""
        _list_dict = []
        
        _group = f"/{guest_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        # passa o valor da chave para a variável DE FILTRO.
        if filter_key_type == "str":
            _value_key = f"'{guest_dict[key_dict]}'"
        else:    
            _value_key = guest_dict[key_dict]

        _filter_str = f"{filter_key_name}{filter_operator}{_value_key}"
        _filter_param = f"filter={_filter_str}" # filtro para consulta  

        # Executa método de GET para procurar o atendimento usando o FILTER_PARAM e retornando o PAYLOAD 
        payload = rest_forti_repository.all_methods_in_forti(_method, _group, _child_name, _child_key, None, _filter_param)
        # print(f"restapi_forti_controller  - > Linha 399 - {payload}")      
        # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
        if "status" in payload:
            if payload['http_status'] == 200:
                # print(f"\nrestapi_forti_controller 284 - HTTP_STATUS = 200 \n {payload} \n")          
                if len(payload["results"]) > 0:
                    for results in payload["results"]:
                        if "id" in results:
                            guest_dict.update(id = results["id"])
                        if "expiration" in results:  
                            guest_dict.update(expiration = results["expiration"])
                        # -----------------------------------------------------------
                        guest_dict.update(itera_fortigate = 'IN.FORTIGATE')
                else:
                    guest_dict.update(itera_fortigate = 'NOT.FORTIGATE')
            else:
                guest_dict.update(itera_fortigate = 'ERROR.FORTIGATE')
            guest_dict.update(status = payload["status"]) 
            guest_dict.update(http_status = payload['http_status'])      
            _code = payload['http_status']
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)
            
            _list_dict.append(guest_dict)
            # print(f"\n\n restapi_forti_controller ==> 305 http_status == 200  ==> RETURN GET \n {_list_dict} \n")
        else:
            guest_dict.update(itera_fortigate = 'ERROR.FORTIGATE')
            guest_dict.update(status = "error")
            _code = 000
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)   
            _list_dict.append(guest_dict)

        return _list_dict

    def post_group_rest_forti(self): # VOUCHER 2.0  - Grupos do fortigate
        ''' Recebe Dicionário com os GRUPOS a sererm enviar AO FORTIGATE
            PRÓXIMA SPRINT - PARA GARANTIR A EXISTÊNCIA DESTES GRUPOS NO FORTIGATE
            __________________________________________________________
            VOUCHER 2.0 (process / )        junho-2024
        '''
        _method ="post"
        _mkey=""
        _child_name=""
        _child_key=""
        _list_dict_groups = table_in_lists_env.FORTI_GROUPS
    
        # INSTANCIAR MODEL GroupRestFortiRepository
        rest_forti_repository = RestFortiRepository()
        action_controller = ActionController() 
        
        for line_dic in _list_dict_groups:
            # print(line_dic)
            answer = rest_forti_repository.all_methods_in_forti(_method, _mkey, _child_name, _child_key, line_dic)
            if answer["status"] == "error":
                line_dic.update(itera_fortigate = 'NOT.FORTIGATE')
                line_dic.update(status = answer["status"])
                line_dic.update(http_status = answer['http_status'])
                _code = answer['http_status']
                resp = action_controller.request_response(_code)
                line_dic.update(status_message = resp)            
            else:
                line_dic.update(itera_fortigate = 'IN.FORTIGATE')
                line_dic.update(status = answer["status"])
                line_dic.update(http_status = answer['http_status'])
                line_dic.update(status_message = None)    
        return _list_dict_groups     

    def post_line_ora_mv_in_group_forti(self, guest_dict:dict) -> list: # VOUCHER 2.0 --> ORA-MV / FORTIGATE!  
        ''' CRIA ATENDIMENTO NO FORTIGATE! Recebe o dicionário com {chaves:valores}.\n
            Substitui ou adiciona CHAVES no dicionário para atender o FORTIGATE.\n
            :guest_dict: = Linha do dict do MV com dados do atendimento:\n
            nr_cpf | cpf_respo | cd_atendimento | TP_ATENDIMENTO | cd_multi_empresa | DT_ATENDIMENTO\n
            RETORNA O DICIONÁRIO RECEBIDO ACRESCIDO DE NOVAS CHAVES: \n
            user-id | itera_fortigate | Status | sponsor: Nome Grupo | expiration: tempo uso. | http_status = 0  
            ___________________________________________________________________
            VOUCHER 2.0   (process)  -   julho-2024
        '''           
        # Instâncias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository()
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        method = "post"
        itera_fortigate = "IN.FORTIGATE"
        self.child_name="/guest"
        self.child_key=""
        answer = {}
        _list_dict = []

        # CRIA DICIONÁRIO COM CHAVES PARA ENVIO AO FORTIGATE
        stamp_dict = action_controller.stamp_from_ora_mv_to_guest_forti(guest_dict, itera_fortigate, "s")
        # print(f"\nCarimba dicionário recebido ==> restapi_forti_controller - linha 375 ==> stamp_dict {stamp_dict}")
        # JUNTA OS DOIS DICIONÁRIOS
        dict_join = action_controller.join_dict(guest_dict, stamp_dict)
        dict_join.pop('comment')
        # print(f"\nDicionário JOIN guest_dict e stamp_dict ==> restapi_forti_controller - linha 379 ==> dict_join {dict_join}")
        if stamp_dict['itera_fortigate'] == "NOT.FORTIGATE":
            dict_join.update(id = None)
            dict_join.update(user_id = None)
            dict_join.update(password = None)
            dict_join.update(status = "error")
            dict_join.update(http_status = 000)
            resp = action_controller.request_response(000) # Desc código erro
            dict_join.update(status_message = resp)
            # ---------------------------------------------------------------            
            _list_dict.append(dict_join)
            # print(f"Lista append == NOT.FORTIGATE ==> restapi_forti_controller - linha 391 ==> _list_dict {_list_dict}")
            return _list_dict
        else:
            self._group = f"/{stamp_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO

        # ENVIAR DICIONÁRIO PARA GRAVAR NO FORTIGATE
        # print(f"\n self._group ==> restapi_forti_controller - linha 391 ==> stamp_dict\n {self._group} \n")
        answer = rest_forti_repository.all_methods_in_forti('post', self._group, self.child_name, self.child_key, stamp_dict)
        # print(f"\nPOST ==> restapi_forti_controller - linha 514 ==> answer -- {answer}\n")
        # --------------------------------------------------------------------------
        if answer["status"] == "error":
            dict_join.update(id = None)
            dict_join.update(user_id = None)
            dict_join.update(itera_fortigate = 'NOT.FORTIGATE')
            dict_join.update(status = answer["status"])
            dict_join.update(http_status = answer['http_status'])
            _code = answer['http_status']
            resp = action_controller.request_response(_code)
            dict_join.update(status_message = resp)   
            # -----------------------------------------------------------
            _list_dict.append(dict_join)
            # print(f"\n if status == error ==> restapi_forti_controller - linha 413 ==> _list_dict.append -- {_list_dict}\n")
            return _list_dict
        else:
            _method = "get-filter"
            filter_param = f"filter=name=={dict_join['name']}" # filtro para consulta após gravação no fortigate
            # print(f"\n filter_param == else ==> restapi_forti_controller - linha 418 ==> filter_param -- {filter_param}\n")            
            # Executa método de GET para procurar o atendimento inserido usando o FILTER_PARAM e retorna o PAYLOAD 
            payload = rest_forti_repository.all_methods_in_forti(_method, self._group, self.child_name, self.child_key, None, filter_param)
            # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo
            # print(f"\n GET-FILTER ==> restapi_forti_controller - linha 422 ==> payload -- {payload}\n")
            if "status" in payload:
                if payload['http_status'] == 200:          
                    # print(f"\nSe http_status 200 ==> GET-FILTER ==> restapi_forti_controller - linha 425 ==> payload -- {payload}\n")
                    # print(f"\nPergunto se result é maior que zero ==> restapi_forti_controller - linha 426 ==> len(payload['results'])>0 {len(payload['results'])>0 }\n")
                    if len(payload['results'])>0:
                        if 'id' in payload['results'][0]:
                            dict_join.update(id = payload['results'][0]['id'])
                        if "expiration" in payload['results'][0]:  
                            dict_join.update(expiration = payload['results'][0]['expiration'])
                            
                        dict_join.update(itera_fortigate = 'IN.FORTIGATE')
                        dict_join.update(status = payload['status'])    
                        dict_join.update(http_status = payload['http_status'])      
                        _code = payload['http_status']
                        resp = action_controller.request_response(_code)
                        dict_join.update(status_message = resp)          
                        # -----------------------------------------------------------
                        _list_dict.append(dict_join)
                        # print(f"\n for em results == atualiza dict_join ==> restapi_forti_controller - linha 439 ==> _list_dict.append -- {_list_dict}\n")
                    else:
                        dict_join.update(itera_fortigate = 'NOT.FORTIGATE')
                        dict_join.update(status = payload['status'])    
                        dict_join.update(http_status = payload['http_status'])      
                        _code = payload['http_status']
                        resp = action_controller.request_response(_code)
                        dict_join.update(status_message = resp)          
                        # -----------------------------------------------------------
                        _list_dict.append(dict_join)
                        # print(f"\n for em results == atualiza dict_join ==> restapi_forti_controller - linha 451 ==> _list_dict.append -- {_list_dict}\n")
                else:
                    # print(f"\nSe http_status IGUAL A 200  - ELSE ==> GET-FILTER ==> restapi_forti_controller - linha 451 ==> payload -- {payload}\n")
                    dict_join.update(id = None)
                    dict_join.update(itera_fortigate = 'ERROR.FORTIGATE')
                    dict_join.update(status = payload['status'])    
                    dict_join.update(http_status = payload['http_status'])
                    _code = payload['http_status']
                    resp = action_controller.request_response(_code)
                    dict_join.update(status_message = resp)          
                    # -----------------------------------------------------------
                    _list_dict.append(dict_join)
            # print(f"\n RETURN POST ==> restapi_forti_controller - linha 452 ==> {_list_dict} \n")                    
            return _list_dict
# =========================  NOVO POST ORA-MV FOR FORTIGATE =======================================
    def post_line_ora_mv_in_forti(self, guest_dict:dict) -> list: # VOUCHER 2.0 --> ORA-MV / FORTIGATE!  
        ''' CRIA ATENDIMENTO NO FORTIGATE! Recebe o dicionário com {chaves:valores}.\n
            :guest_dict: = Linha do dict do MV com dados do atendimento:\n
            RETORNA O DICIONÁRIO RECEBIDO ACRESCIDO DE NOVAS CHAVES: \n
            user-id | itera_fortigate | Status | sponsor: Nome Grupo | expiration: tempo uso. | http_status = 0  
            ___________________________________________________________________
            VOUCHER 2.0   (process)  -   julho-2024
        '''           
        # Instâncias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository()
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        self.child_name="/guest"
        self.child_key=""
        answer = {}
        _list_dict = []

        if guest_dict['itera_fortigate'] == "INVALID":
            guest_dict.update(id = None)
            guest_dict.update(status = "error")
            guest_dict.update(http_status = 000)
            resp = action_controller.request_response(000) # Desc código erro
            guest_dict.update(status_message = resp)
            # ---------------------------------------------------------------            
            _list_dict.append(guest_dict)
            # print(f"Lista append == NOT.FORTIGATE ==> restapi_forti_controller - linha 391 ==> _list_dict {_list_dict}")
            return _list_dict
        else:
            self._group = f"/{guest_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
            _payload = copy.deepcopy(guest_dict)
            if "dt_atendimento" in _payload:
                del _payload["dt_atendimento"]
            elif "DT_ATENDIMENTO" in _payload:
                del _payload["DT_ATENDIMENTO"]

            if "dt_nascimento" in _payload:
                del _payload["dt_nascimento"]
            elif "DT_NASCIMENTO" in _payload:
                del _payload["DT_NASCIMENTO"]

            if "id" in _payload:
                del _payload["id"]
            elif "ID" in _payload:
                del _payload["ID"]
    
        # ENVIAR DICIONÁRIO PARA GRAVAR NO FORTIGATE
        # print(f"\n self._group ==> restapi_forti_controller - linha 617 ==> stamp_dict -- {self._group}")
        # print(f"\n PARA ENVIAR AO FORTIGATE ==> restapi_forti_controller - linha 618 ==> guest_dict -- {guest_dict}")
        answer = rest_forti_repository.all_methods_in_forti('post', self._group, self.child_name, self.child_key, _payload)
        # print(f"\nRESPOSTA DO ENVIO ==> restapi_forti_controller - linha 620 ==> answer -- {answer}\n")
        # --------------------------------------------------------------------------
        if answer["status"] == "error":
            guest_dict.update(id = None)
            guest_dict.update(itera_fortigate = 'NOT.FORTIGATE')
            guest_dict.update(status = answer["status"])
            guest_dict.update(http_status = answer['http_status'])
            _code = answer['http_status']
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)   
            # -----------------------------------------------------------
            _list_dict.append(guest_dict)
            # print(f"\n if status == error ==> restapi_forti_controller - linha 413 ==> _list_dict.append -- {_list_dict}\n")
            return _list_dict
        else:
            guest_dict.update(id = answer['mkey'])
            guest_dict.update(itera_fortigate = 'IN.FORTIGATE')
            guest_dict.update(status = answer['status'])    
            guest_dict.update(http_status = answer['http_status'])      
            _code = answer['http_status']
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)          
            # -----------------------------------------------------------
            _list_dict.append(guest_dict)
            return _list_dict

# =================================================================
# novo 

    def post_line_visitor_in_forti(self, guest_dict:dict) -> list: # VOUCHER 2.0 --> ORA-MV / FORTIGATE!  
        ''' CRIA ATENDIMENTO NO FORTIGATE! Recebe o dicionário com {chaves:valores}.\n
            :guest_dict: = Linha do dict do MV com dados do atendimento:\n
            RETORNA O DICIONÁRIO RECEBIDO ACRESCIDO DE NOVAS CHAVES: \n
            user-id | itera_fortigate | Status | sponsor: Nome Grupo | expiration: tempo uso. | http_status = 0  
            ___________________________________________________________________
            VOUCHER 2.0   (process)  -   julho-2024
        '''           
        # Instâncias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository()
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        self.child_name="/guest"
        self.child_key=""
        answer = {}
        _list_dict = []

        self._group = f"/{guest_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        _payload = copy.deepcopy(guest_dict)
        if "dt_atendimento" in _payload:
            del _payload["dt_atendimento"]
        elif "DT_ATENDIMENTO" in _payload:
            del _payload["DT_ATENDIMENTO"]
        if "dt_nascimento" in _payload:
            del _payload["dt_nascimento"]
        elif "DT_NASCIMENTO" in _payload:
            del _payload["DT_NASCIMENTO"]
        elif 'CD_MULTI_EMPRESA' in _payload:
            del _payload['CD_MULTI_EMPRESA']
        if "id" in _payload:
            del _payload["id"]
        elif "ID" in _payload:
            del _payload["ID"]
        # elif "sponsor" in _payload:
        #     del _payload["sponsor"]
    
        # ENVIAR DICIONÁRIO PARA GRAVAR NO FORTIGATE
        # print(f"\n self._group ==> restapi_forti_controller - linha 617 ==> stamp_dict -- {self._group}")
        # print(f"\n PARA ENVIAR AO FORTIGATE ==> restapi_forti_controller - linha 618 ==> guest_dict -- {guest_dict}")
        answer = rest_forti_repository.all_methods_in_forti('post', self._group, self.child_name, self.child_key, _payload)
        # print(f"\nRESPOSTA DO ENVIO ==> restapi_forti_controller - linha 620 ==> answer -- {answer}\n")
        # --------------------------------------------------------------------------
        if answer["status"] == "error":
            guest_dict.update(id = None)
            guest_dict.update(itera_fortigate = 'NOT.FORTIGATE')
            guest_dict.update(status = answer["status"])
            guest_dict.update(http_status = answer['http_status'])
            _code = answer['http_status']
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)   
            # -----------------------------------------------------------
            _list_dict.append(guest_dict)
            # print(f"\n if status == error ==> restapi_forti_controller - linha 413 ==> _list_dict.append -- {_list_dict}\n")
            return _list_dict
        else:
            guest_dict.update(id = answer['mkey'])
            guest_dict.update(itera_fortigate = 'IN.FORTIGATE')
            guest_dict.update(status = answer['status'])    
            guest_dict.update(http_status = answer['http_status'])      
            _code = answer['http_status']
            resp = action_controller.request_response(_code)
            guest_dict.update(status_message = resp)          
            # -----------------------------------------------------------
            _list_dict.append(guest_dict)
            return _list_dict



# ==============================================================


    def post_line_rollback_in_rest_forti(self, rollback_dict:dict) -> list: # VOUCHER 2.0 - VISITOR!
        ''' CRIA ATENDIMENTO NO FORTIGATE! Recebe o dicionário com {chaves:valores}.\n
            A list_dict = List[ {dict} ] precisa conter também as seguintes chaves:\n
                sponsor=Grupo | user-id=CPF do paciente | cpf_resp=CPF responsável |\n
                itera_fortigate = irá receber Status da Request  
                RETORNA LISTA com CHAVES modificadas e com Informação de status. 
            ___________________________________________________________________
            Applicant: (process) - Julho-2024
        '''           
        # Instancias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() # MODEL - UsersRestFortiRepository
        itera_fortigate = "IN.FORTIGATE"
        # # mkey será atribuído logo abaixo em cada linha do dicionário
        _child_name="/guest"
        _child_key=""
        _list_dict = []
        # INTERA dicionário para enviar PAYLOAD
        _group = f"/{rollback_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        # Executa ENVIA payload para FORTIGATE e retorna resposta  
        answer = rest_forti_repository.all_methods_in_forti("post", _group, _child_name, _child_key, rollback_dict)
        if "status" in answer:
            if answer["status"] == "error":
                rollback_dict.update(itera_fortigate = "NOT.FORTIGATE")
                rollback_dict.update(status = answer['status'])
                rollback_dict.update(http_status = answer['http_status'])
                _list_dict.remove(rollback_dict)
                return _list_dict
            else:
                rollback_dict.update(itera_fortigate = itera_fortigate)
                rollback_dict.update({"dt_update": datetime.now()})
                rollback_dict.update({"itera_fortigate":"REMOVID"})
                rollback_dict.update(status = answer['status'])
                rollback_dict.update(http_status = answer['http_status'])
                _list_dict.remove(rollback_dict)

        return _list_dict
        
    def post_guest_all_groups_rest_forti(self, list_dict: list) -> list: # VOUCHER 2.0 - VISITOR!
        ''' Recebe Lista com os GRUPOS e usuários para enviar linhas(PAYLOAD) para o FORTIGATE.\n
            A list_dict = List[ {dict} ] precisa conter também as seguintes chaves:\n
                sponsor=Grupo | user-id=CPF do paciente | cpf_resp=CPF responsável |\n
                itera_fortigate = irá receber Status da Request  
                RETORNA LISTA com CHAVES modificadas e com Informação de status. 
            ___________________________________________________________________
            Applicant: post_all_care_rest_forti_applicant       
        '''           
        # Instancias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() # MODEL - UsersRestFortiRepository

        # # mkey será atribuído logo abaixo em cada linha do dicionário
        self.child_name="/guest"
        self.child_key=""
        # INTERA dicionário para enviar PAYLOAD
        for dict_line in list_dict: 
            # SUBMIT ------------------------------------------------------------------    
            if dict_line["itera_fortigate"] != 'SUBMIT':
                continue

            self._group = f"/{dict_line['sponsor']}" # ATRIBUIR O NOME DO GRUPO
            filter_param = f"filter=name=={dict_line['name']}" # NÚMERO DO ATENDIMENTO para filtrar            

            # Executa ENVIA payload para FORTIGATE e retorna resposta            
            answer = rest_forti_repository.all_methods_in_forti("post", self._group, self.child_name, self.child_key, dict_line)
            if answer['http_status'] != 200: # and 
                dict_line.update(http_status = answer['http_status'])
                dict_line.update(status = answer["status"])
                if answer['http_status'] != 500:                
                    continue
            # Executa método de GET para procurar o atendimento através do FILTER_PARAM e retorna o PAYLOAD 
            payload = rest_forti_repository.all_methods_in_forti("get-filter", self._group, self.child_name, self.child_key, None, filter_param)
            
            # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
            # print(f"consulta retornou código: {payload['http_status']}")
            if payload['http_status'] == 200:
                for results in payload["results"]:
                        dict_line['id'] = results["id"] # ID do fortigate
                        dict_line['itera_fortigate'] = 'UPDATE'
                        dict_line['expiration'] = results["expiration"]
                        dict_line.update(http_status = payload['http_status'])
                        dict_line.update(status = payload["status"])
            elif payload['http_status'] == 500:
                dict_line['itera_fortigate'] = 'NOT.FORTIGATE'
                dict_line['expiration'] = results["expiration"]
                dict_line.update(http_status = payload['http_status'])
                dict_line.update(status = payload["status"])
            else:
                dict_line['itera_fortigate'] = 'NOT.FORTIGATE'
                dict_line['expiration'] = results["expiration"]
                dict_line.update(http_status = payload['http_status'])
                dict_line.update(status = payload["status"])
                
        return list_dict

    def post_visitor_in_groups_rest_forti(self, list_dict: list) -> list: # VOUCHER 2.0 - VISITOR!
        ''' Recebe Lista com os GRUPOS e usuários para enviar linhas(PAYLOAD) para o FORTIGATE.\n
            A list_dict = List[ {dict} ] precisa conter também as seguintes chaves:\n
                sponsor=Grupo | user-id=CPF do paciente | cpf_resp=CPF responsável |\n
                itera_fortigate = irá receber Status da Request  
                RETORNA LISTA com CHAVES modificadas e com Informação de status. 
            ___________________________________________________________________
            Applicant: post_all_care_rest_forti_applicant       
        '''
        return_list = []           
        # Instancias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() # MODEL - UsersRestFortiRepository

        # # mkey será atribuído logo abaixo em cada linha do dicionário
        self.child_name="/guest"
        self.child_key=""
        # INTERA dicionário para enviar PAYLOAD
        for dict_line in list_dict: 
            # SUBMIT ------------------------------------------------------------------    

            self._group = f"/{dict_line['sponsor']}" # ATRIBUIR O NOME DO GRUPO
            # print(f"\n post_visitor_in_groups_rest_forti ==> 556  sponsor: {self._group}")
            # Executa ENVIA linha do dicionário como payload para FORTIGATE e retorna resposta operação           
            answer = rest_forti_repository.all_methods_in_forti("post", self._group, self.child_name, self.child_key, dict_line)
            # print(f"\n post_visitor_in_groups_rest_forti ==> 559  answer: {answer}")
            if answer['http_status'] != 200: # and 
                dict_line.update(http_status = answer['http_status'])
                dict_line.update(status = answer["status"])
                if answer['http_status'] != 500:                
                    continue
            # Executa método de GET para procurar o atendimento através do FILTER_PARAM e retorna o PAYLOAD 
            filter_param = f"filter=user-id=={dict_line['user-id']}" # NÚMERO DO VOUCHER para filtrar NO FORTIGATE
            payload = rest_forti_repository.all_methods_in_forti("get-filter", self._group, self.child_name, self.child_key, None, filter_param)
            
            # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
            if payload['http_status'] == 200:
                for results in payload["results"]:
                        dict_line['id'] = results["id"] # ID do fortigate
                        dict_line['itera_fortigate'] = 'UPDATE'
                        dict_line['expiration'] = results["expiration"]
                        dict_line.update(http_status = payload['http_status'])
                        dict_line.update(status = payload["status"])
                        
            elif payload['http_status'] == 500:
                dict_line['itera_fortigate'] = 'NOT.FORTIGATE'
                dict_line['expiration'] = results["expiration"]
                dict_line.update(http_status = payload['http_status'])
                dict_line.update(status = payload["status"])
            else:
                dict_line['itera_fortigate'] = 'NOT.FORTIGATE'
                dict_line['expiration'] = results["expiration"]
                dict_line.update(http_status = payload['http_status'])
                dict_line.update(status = payload["status"])
                
            return_list.append(dict_line)
            # print(f"\n restapi_forti_controller Linha 598 -: {dict_line}")
            
        return return_list

    def delete_expiration_in_rest_forti(self, dict_exp:dict) -> list: # VOUCHER 2.0 - DELETA EXPIRADO NO VISITOR!
        ''' Recebe DICIONÁRIO com id, sponsor para remover no FORTIGATE.\n
            :dict_exp: {dict}  precisa conter também as seguintes chaves:\n  
            sponsor=Grupo | user-id=CPF do paciente \n
            itera_fortigate = irá receber Status da Request  
            RETORNA LISTA com O DICIONÁRIO com novas chaves adicionadas e Informação de status.
            CASO não consiga remover algum registro adiciona itera_forti (NOT.REMOVID) registro da LISTA no retorno 
            ________________________________________________________________________________
            VOUCHER 2.0  (process / )           junho-24
        '''           
        # Instancias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() # MODEL - UsersRestFortiRepository
        self.child_name="/guest"
        list_return = []
        if "sponsor" in dict_exp:
            _group = f"/{dict_exp['sponsor']}" # ATRIBUIR O NOME DO GRUPO
            _child_key = f"/{dict_exp['id']}" # NÚMERO DO ATENDIMENTO para filtrar            
        # Executa ENVIA payload para FORTIGATE e retorna resposta  
        answer = rest_forti_repository.all_methods_in_forti("delete", _group, self.child_name, _child_key, dict_exp)
        if "status" in answer:
            if answer["status"] == "error":
                dict_exp.update({"itera_fortigate":"NOT.REMOVED"})
                dict_exp.update(status = answer["status"])
                dict_exp.update(http_status = answer["http_status"])
            else:
                dict_exp.update({"expiration": 0}) # Valor padão é string
                dict_exp.update({"dt_remove": datetime.now()})
                dict_exp.update({"itera_fortigate":"REMOVED"})
                dict_exp.update(status = answer["status"])
                dict_exp.update(http_status = answer["http_status"])
            list_return.append(dict_exp)
        return list_return

    def delete_line_guest_in_group_forti(self, guest_dict:dict) -> list: # VOUCHER 2.0 - DELETA ATENDIMENTOS COM ALTA - TESTADO!
        ''' DELETA USUÁRIO NO FORTIGATE, ! Recebe o dicionário com {chaves:valores}.\n
            Substitui ou adiciona CHAVES no dicionário para atender o FORTIGATE.\n
            :guest_dict: = Linha do dict do MV com dados do atendimento:\n
            :dict_groups: Dicionário com os Grupos do FORTIGATE. [name, tp_atendimento, sn_mv, expire]\n
            nr_cpf | cpf_respo | cd_atendimento | TP_ATENDIMENTO | cd_multi_empresa | DT_ATENDIMENTO\n
            RETORNA LISTA com CHAVES modificadas e novas chaves: \n
            itera_fortigate => = Status | sponsor: Nome Grupo | expiration: tempo uso. | http_status = 0  
            ___________________________________________________________________
            VOUCHER 2.0  (process)    jul-24
        '''           
        # Instâncias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository()
        # ---------------------------------------------------------------------
        status = "REMOVED"
        self.child_name="/guest"
        self.child_key=""
        answer = 0
        list_dict = []

        # SUBSTITUI CHAVES PARA CHAVES DO FORTIGATE e inserir chaves novas
        self._group = f"/{guest_dict['sponsor']}" # ATRIBUIR O NOME DO GRUPO
        
        if "id" in guest_dict:
            if guest_dict["id"] != None:
                self.child_key = f"/{guest_dict['id']}"
        elif "id" in guest_dict:
            if guest_dict['id'] != None:
                self.child_key = f"/{guest_dict['id']}"
                # print(f"\n restapi_forti_controller <==> self.child_key = id : {guest_dict['id']}\n")
        else:
            if "name" in guest_dict:
                filter_param = f"filter=name=={guest_dict['name']}" # filtro para consulta após gravação no fortigate 
                # print(f"\n restapi_forti_controller <==> self.child_key = name : {guest_dict['name']}")
            elif "cd_atendimento" in guest_dict:
                filter_param = f"filter=name=={guest_dict['cd_atendimento']}" # filtro para consulta após gravação no fortigate 
                # print(f"\n restapi_forti_controller <==> self.child_key = name : {guest_dict['cd_atendimento']}")
            
            # Executa método de GET para procurar o atendimento inserido usando o FILTER_PARAM e retorna o PAYLOAD 
            payload = rest_forti_repository.all_methods_in_forti("get-filter", self._group, self.child_name, self.child_key, None, filter_param)
            # VARRE O PAYLOAD na chave RESULTS a procura do ID linha e atribui para as variáveis abaixo                 
            if payload['http_status'] == 200:
                for results in payload["results"]:
                    if len(results[""]) > 0:
                        guest_dict.update(id = results["id"])
                        guest_dict.update(expiration = results["expiration"])
                        guest_dict.update(status = payload['status'])
                        guest_dict.update(http_status = payload['http_status'])
                        break
                    else:
                        guest_dict.update(itera_fortigate = 'NOT.FORTIGATE')
                        guest_dict.update(status = payload['status'])
                        guest_dict.update(http_status = payload['http_status'])
                        list_dict.append(guest_dict)
                        return list_dict
            else:
                guest_dict.update(itera_fortigate = 'ERROR.CODE')
                guest_dict.update(status = payload['status'])
                guest_dict.update(http_status = payload['http_status'])
                list_dict.append(guest_dict)
                return list_dict
            
        payload_delete = rest_forti_repository.all_methods_in_forti("delete", self._group, self.child_name, self.child_key)
        # print(payload_delete)
        if payload_delete['http_status'] == 200:
            guest_dict.update(itera_fortigate = 'REMOVED')
            guest_dict.update(dt_remove = datetime.now())
            guest_dict.update(status = payload_delete['status'])
            guest_dict.update(http_status = payload_delete['http_status'])
        else:
            guest_dict.update(itera_fortigate = 'NOT.FORTIGATE')
            guest_dict.update(status = payload_delete['status'])
            guest_dict.update(http_status = payload_delete['http_status'])


        list_dict.append(guest_dict)
        return list_dict

    def delete_expiration_for_groups_rest_forti(self, list_dict: list) -> list: # VOUCHER 2.0 - VISITOR!
        ''' Recebe Lista com DICIONÁRIO com GRUPOS e usuários para remover no FORTIGATE.\n
            A list_dict = List[ {dict} ] precisa conter também as seguintes chaves:\n
                sponsor=Grupo | user-id=CPF do paciente | cpf_resp=CPF responsável |\n
                itera_fortigate = irá receber Status da Request  
                RETORNA LISTA com CHAVES modificadas e com Informação de status.
                CASO não consiga remover algum registro remove registro da LISTA no retorno 
            ________________________________________________________________________________
            VOUCHER 2.0     01/07/24
        '''           
        # Instancias 
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() # MODEL - UsersRestFortiRepository

        # # mkey será atribuído logo abaixo em cada linha do dicionário
        self.child_name="/guest"
        # INTERA dicionário para enviar PAYLOAD
        for dict_line in list_dict: 
            if dict_line["expiration"] == '0':
                _group = f"/{dict_line['sponsor']}" # ATRIBUIR O NOME DO GRUPO
                _child_key = f"/{dict_line['id']}" # NÚMERO DO ATENDIMENTO para filtrar            
                # Executa ENVIA payload para FORTIGATE e retorna resposta  
                answer = rest_forti_repository.all_methods_in_forti("delete", _group, self.child_name, _child_key, dict_line)
                if "status" in answer:
                    if answer["status"] == "error":
                        dict_line.update(status = answer['status'])
                        dict_line.update(http_status = answer['http_status'])
                        list_dict.remove(dict_line)
                        continue
                    else:
                        dict_line.update({"expiration": 0}) # Valor padão é string
                        dict_line.update({"dt_update": datetime.now()})
                        dict_line.update({"itera_fortigate":"REMOVID"})
                        dict_line.update(status = answer['status'])
                        dict_line.update(http_status = answer['http_status'])
            else:
                list_dict.remove(dict_line)
        return list_dict
