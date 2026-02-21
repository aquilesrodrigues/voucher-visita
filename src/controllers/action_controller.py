from src.view.output_file import OutputFile
from csv import DictReader
from src.env import table_in_lists_env
from datetime import datetime
import json
from typing import List, Dict
import random
import operator

random.seed(version=2)

class ActionController:
    ''' Classe de Métodos de AÇÕES AUXILIARES'''
    def __init__(self) -> None:
        pass
    
    def format_col_args(self, str_col: str): # VOUCHER 2.0  --> cria string %s, %s,
        ''' Recebe string com nome das colunas de um BANCO
            E cria lista com %s baseada no total de colunas do BANCO
            :list_col: Lista com as colunas do BANCO
            ________________________________________________________
            VOUCHER 2.0 (sql_int_repository / ) maio-24
        '''
        values_arg = []
        list_col = str_col.split(sep=",", maxsplit=-1)
        for i in range(len(list_col)):
            values_arg.append(" %s")
        str_col_arg = ','.join(values_arg)
        return str_col_arg
    # -----------------------------------------------------------------------

    def conv_list_str_for_int(self, list_str: list) -> list: # VOUCHER 2.0  --> "1" = 1
        '''
        Recebe uma lista de valores strings e converte todos para inteiro
        :list_str: Lista com valores em strings a ser convertida
        _________________________________________________________________
        VOUCHER 2.0  (process)    junho-2024
        '''
        list_int = [int(numero) for numero in list_str]
        return list_int
        
    def search_key_in_dict_insert_key_return_new_dict(self, key_name, list_value, list_dict) -> list: # VOUCHER 2.0
        ''' 
        #======================================================================================================
        #### Recebe (key_name)-nome da chave e (value_list)-lista com valores relacionados a esta chave.
        #### Será feita a procura no DICIONÁRIO-(list_dict) caso encontre salva em novo DICIONÁRIO(_new_list_dict);
        #### Retorna uma LISTA C/DICIONÁRIOS com as linhas achadas no (list_dict)
        :key_name: Nome da Chave a ser procurada
        :value_list: Lista com os valores para a chave key_name a ser procurado no DICIONÁRIO
        :list_dict: Dicionário recebido para procurar valor da chave
        \n___________________________________________________________________\n
        VOUCHER 2.0 (process / )        junho-2024
        '''
        _new_list_dict = []
        # not_found = {'not_found':'true'}
        # print(f"\n ----------------------------------------------------\n  list_dict : {list_dict}")
        for i in list_value:
            # print(f"\n ---------------------------------------------------\n action_controller line 55 - for i in value_list:  type : {type(i)} linha da lista {i}")
            # procura a chave(key_name) com valor(key_list) no dicionário passada e retorna tupla achada, caso exista
            # print(f"action_controller line 55 - for i in value_list:  key_name {key_name} linha da lista {i}")
            for line_dict in list_dict:
                if key_name in line_dict:
                    if line_dict[key_name] == i:
                        _new_list_dict.append(line_dict)
                        # print(f"\n---------------------------------------------------\n action_controller line 63 - for line_dict |  _new_list_dict:  type : {line_dict} linha da lista {i}")
                else:
                    continue
        return _new_list_dict


    def generate_range_voucher(self, status_insert, init_interval = 1, end_interval = 500, expiration = 28800):
        _abbr_init = 'uni'
        _tp_atendimento = 'V1'
        list_return = []
        dict_line = {}
        # ------------------------------------------------------------
        for i in range(init_interval, end_interval+1):
            # Criando registros baseado em parãmentros passados   
            _password = self.number_random()
            number_pass = str(i) # converte em string
            # print(number_pass)
            _user_id = _abbr_init+number_pass.zfill(5) # preencher com zeros a esquerda
            dict_line = {}
            dict_line["user-id"] = _user_id
            dict_line.update(user_id = _user_id)
            dict_line.update(password = _password)
            dict_line.update(sponsor = "")
            dict_line.update(user_id = _user_id)
            dict_line.update(name = "AVULSO")
            dict_line.update(tp_atendimento = _tp_atendimento)
            dict_line.update(itera_fortigate = status_insert)
            dict_line.update(expiration = expiration)
            list_return.append(dict_line)
            
        return list_return

    
    
    
    


    ####################################################################
    def search_value_in_dict(self, key_name, from_dict, list_dict_source) -> list: # VOUCHER 2.0
        ''' 
        #======================================================================================================
        #### Recebe (key_name)-nome da chave e dicionário com chaves e valores contendo também esta chave.
        #### Será feita a procura no DICIONÁRIO-(list_dict) caso encontre salva em novo DICIONÁRIO(_new_list_dict);
        #### Retorna uma LISTA C/DICIONÁRIOS com as linhas achadas no (list_dict)
        :key_name: Nome da Chave a ser procurada
        :value_list: Lista com os valores para a chave key_name a ser procurado no DICIONÁRIO
        :list_dict: Dicionário recebido para procurar valor da chave
        \n___________________________________________________________________\n
        VOUCHER 2.0 (process / )        junho-2024
        '''
        _new_list_dict = []
        _key_value = from_dict[key_name]
        # procura a chave(key_name) com valor(key_list) no dicionário passada e retorna tupla achada, caso exista
        line_captured = self.next_tuple_list(list_dict_source, key_name, _key_value)
        _new_list_dict.append(line_captured)
        return _new_list_dict


    #####################################################################
    def slice2_join(self, init:str, ini_length:int, fin:str, fin_length:int):
        '''Recebe duas strings e extrai partes das 2 strings e agrupa-as
            :init: String com tamanho >= ao número da ini_length
            :ini_length: Número total a ser extraído do init
            :fin: String com tamanho >= ao número da fin_length
            :fin_length: Número total a ser extraído do fin
            \n___________________________________________________________________\n
            VOUCHER 2.0
        '''
        # slice2_join("98765432109",4,"1234567",4)
        return f"{init[:ini_length]}{fin[-fin_length:]}" 





    def value_column_list_dict(self, list_dict, name_column: str) -> List:  # VOUCHER 2.0
        ''' #
            ### Recebe (list_dict) e nome da Chave a ser consultada (name_column)
            ### Retorna Lista de valores consultados na chave passada 
            :list_dict: **Lista com [{chaves : valores}] a ser iterado**
            :name_column: Nome da coluna que sera usada para extraír os valores
            ___________________________________________________________________\n
            VOUCHER 2.0  (process / )   junho-2024
        '''
        self.list_value = []
        self._name_column = name_column
        #  Itera pelas linhas da lista
        #  Abaixo convertemos a linha em um Dicionário
        for i in list_dict:
            # Cria dicionário com base na linha da LISTA Apontada ->
            dict_new = dict(i)
            # print(f"process linha 122 - dict_new {dict_new}")
            for k in dict_new.keys():
                ''' Este segundo FOR varre as CHAVES da linha do novo dicionário 
                    caso encontre a chave adiciona VALOR em uma LISTA a ser retornada 
                    k = chave, dict_new[k] = valor da chave
                '''
                if k == self._name_column:
                    self.list_value.append(dict_new[k])           
        return list(set(self.list_value))
# ====================== NOVO MÉTODO 14/08/24 ===========================
    def next_dict_in_list(self, list_dict, key_name: str, line_dict: dict, convert_for_str="n") -> dict: # VOUCHER 2.0 PROCURA VALOR EM DICIONÁRIO PASSADO
        ''' 
            #### Recebe Lista com dicionários, chave e valor \n
            #### Retorna Dicionário: com Linha encontrada, caso contrário retorna falso {'not_found' : 'true'}
            :list_dict: dicionário com chave a ser procurada
            :key_name: nome da chave a ser procurada no dicionário
            :convert_for_str: Quer converter em string o valor da chave? (s/n = default = n)
            :line_dict: um valor da chave passada a ser procurado 
            Exemplo: procura( 'cd_atendimento' == 3951488 ), caso contrário retorna {'not_found' : 'true'})
            \n___________________________________________________________________\n
            VOUCHER 2.0     08/2024 - em uso       
        '''
        not_found = {'not_found':'true'}
        if convert_for_str == "s":
            key_value = str(line_dict[key_name])
        else:            
            key_value = line_dict[key_name]
            
        if len(list_dict) > 0:
            _next_dict = next((p for p in list_dict if p[key_name] == key_value), not_found)
            if _next_dict == not_found:
                return not_found
            else:
                line_dict.update(id = _next_dict["id"])
                line_dict.update(sponsor = _next_dict["sponsor"])
                line_dict.update(expiration = _next_dict["expiration"])
                line_dict.update(comment = _next_dict["comment"])
                return line_dict
        else:
            return not_found

# ====================== NOVO MÉTODO 14/08/24 ===========================

    def next_list_dict_in_list(self, list_dict: list, key_name: str, filter_operator: str, key_value, convert_for_str="n") -> dict: # VOUCHER 2.0 PROCURA VALOR EM DICIONÁRIO PASSADO
        ''' 
            #### Recebe Lista com dicionários(chave:valor), nome da chave e valor a ser procurado no dicionário \n
            #### Retorna Dicionário: com Linha ou linhas encontradas, caso contrário retorna um dicionário falso: {'not_found' : 'true'}
            :list_dict: Lista com dicionários que será extraída as linhas que atendam pesquisa
            :key_name: nome da chave a ser procurado o valor passado
            :filter_operator: Operador de comparação
            :key_value: O valor para ser comparado com o valor da chave existente na Lista passada 
            :convert_for_str: Inforar se deseja converter em string o valor da chave? (s/n = default = n)
            Exemplo: procura( 'cd_atendimento' == 3951488 ), caso contrário retorna {'not_found' : 'true'})
            \n___________________________________________________________________\n
            VOUCHER 2.0   - VISITANTES EXPIRADOS         20/08/2024 
        '''
        not_found = {'not_found':'true'}
        _new_list_dict = []
        _err_list_dict = []
        if convert_for_str == "s":
            _key_value = str(key_value)
        else:            
            _key_value = key_value
        filter_operator = "=="    
        if len(list_dict) > 0:
            for line_list_dict in list_dict:
                if key_name in line_list_dict:
                    print(f"\n action_controller - linha 188 key_name {key_name} = key_value {_key_value}")
                    if self.compare(line_list_dict[key_name], filter_operator, _key_value):
                        _new_list_dict.append(line_list_dict)
                        print(f"\n----------------- action_controller line 192 ----------------------------------\n {line_list_dict}")
                else:
                    _err_list_dict.append(line_list_dict)
                    print(f"\n-- action_controller - next_list_dict_in_list -  line 195 ------\n {line_list_dict}")
                    continue
        else:
            _new_list_dict.append(not_found)
        
                        
        return _new_list_dict

                    
    ###############################################################################    
    def next_tuple_list(self, query, key_name: str, key_value) -> dict: # VOUCHER 2.0 PROCURA VALOR EM DICIONÁRIO PASSADO
        ''' 
            #### Recebe Lista com dicionários, chave e valor \n
            #### Retorna Dicionário: com Linha encontrada, caso contrário retorna falso {'not_found' : 'true'}
            :query: dicionário com chave a ser procurada
            :key_name: nome da chave a ser procurada no dicionário
            :key_value: um valor da chave passada a ser procurado 
            Exemplo: procura( 'cd_atendimento' == 3951488 ), caso contrário retorna {'not_found' : 'true'})
            \n___________________________________________________________________\n
            VOUCHER 2.0            
        '''
        not_found = {'not_found':'true'}
        # ---------------------------------------------------------------------------------
        _line_dict = next((p for p in query if p[key_name] == key_value), not_found)
        if _line_dict == not_found:
            return not_found
        else:
            return _line_dict

    ###############################################################################
    def create_range_keys(self, init_interval, end_interval, abbr_init):
        ''' Método retorna Lista de strings no formato [LETRAS00001]\n
            Recebe Número inicial, Número final + String(prefixo)
            \n___________________________________________________________________\n
            VOUCHER 2.0               
        '''
        list_value = []
        for i in range(init_interval, init_interval+end_interval):
            num_seq = str(i)
            id_form = abbr_init+num_seq.zfill(5)
            list_value.append(id_form)
        return list_value
 
    ###############################################################################
    def number_random(self, init_interval = 10, end_interval = 99, size = 4):
        ''' Cria número aleatório com tamanho de acordo com parâmentros passados
            Valores default:
                Número inicial = 10, Número final = 99 e total-Dígitos= 4
            \n___________________________________________________________________\n
            VOUCHER 2.0   
        '''
        pass_random = random.sample(range(init_interval, end_interval), size)
        #'{}{}{}{} = lista
        pass_final=''.join([str(n) for n in pass_random])
        # -------------------------------------------------------------------------
        return pass_final
    ############################################################################
    
# ===============================================================================================
# ------------------------NOVO PADRÃO DE CARIMBO EM UM DICIONÁRIO--------------------------------
    def stamp_dict_ora_mv_to_guest_forti(self, dict_line: dict, itera_fort="SUBMIT", type_group="*") -> dict: # VOUCHER 2.0 #### CARIMBAR CAMPOS
        ''' CARIMBAR chaves no DICIONÁRIO DE ORIGEM MV :\n
            :dict: Dicionário passado que terá suas chaves renomeadas e novas inseridas\n
            :itera_fort: String que informa o status de interação com o fortigate \n
            CHAVES ==> CPF => user-id | cd_atendimento => name | nr_cpf => user-id | 
            cpf_respo => cpf_resp | sponsor=Grupo | password => Será criada a senha|\n
            ------------------------------------------------------------------------
            RETORNA DICIONÁRIO com CHAVES CARIMBADAS:\n
            CASO NÃO TENHA CPF => Retorna itera_fortigate = NOT.FORTIGATE
            ________________________________________________________________________
            VOUCHER 2.0  - USAR PARA ATENDIMENTOS DO MV   14/08/2024 - Agosto-2024
        '''
        # try: 
        mv_groups = self.select_mv_groups_type(type_group)
        companies = self.select_company()
        output_file = OutputFile()
        # ----------------------------------------------
        # Atribuindo variáveis para o comentário
        _group_name = "" # Varible for name
        _company = ""
        _sn_mv = ""
        _type =  ""
        _expiration = 31536000 # Varible for time of expiration
        _dt_atendimento = datetime.now().strftime('%d-%m-%Y %H:%m')  
        _new_dict = {}
        #### Carimbando a CHAVE PRIMÁRIA DO FORTIGATE (id) ==========================================================
        if "id" not in dict_line: # Precisa do resultado da chave acima user-id
                dict_line.update(id = "")
        #### Carimbando o LOGIN FORTIGATE (user-id) ==========================================================
        if "user-id" in dict_line: # LOGIN DE ACESSO AO FORTIGATE
            if dict_line["user-id"] == None or dict_line["user-id"] == "":
                _new_dict["user-id"] = str(dict_line["cd_atendimento"]) # Atualizando chave user-id com cd_atendimento
            else:
                _new_dict["user-id"] = dict_line["user-id"]
        else:
            if "cd_atendimento" in dict_line:
                _new_dict["user-id"] = str(dict_line["cd_atendimento"]) # Criar user-id com cd_atendimento # Criar user-id
                _new_dict.update(user_id = str(dict_line["cd_atendimento"])) # Criar user-id com cd_atendimento # Criar user-id
            elif "CD_ATENDIMENTO" in dict_line:
                _new_dict["user-id"] = str(dict_line["CD_ATENDIMENTO"]) # Criar user-id com cd_atendimento # Criar user-id
                _new_dict.update(user_id = str(dict_line["CD_ATENDIMENTO"])) # Criar user-id com cd_atendimento # Criar user-id
            else:
                _new_dict["user-id"] = "" # Criar user-id sem valor
                _new_dict.update(user_id = "") # Criar user-id sem valor
        
        
        #### Novos valores para estas variáveis
        if "dt_atendimento" in dict_line:
                _dt_atendimento = dict_line["dt_atendimento"]
        elif "DT_ATENDIMENTO" in dict_line:
                _dt_atendimento = dict_line["DT_ATENDIMENTO"]

        # ===============================================================================    
        if "tp_atendimento" in dict_line:
            if dict_line["tp_atendimento"] != None and dict_line["tp_atendimento"] != "":
                for groups_line in mv_groups:
                    if "tp_atendimento" in groups_line:
                        if dict_line["tp_atendimento"] == groups_line["tp_atendimento"]:
                            _group_name = groups_line["name"]
                            _sn_mv = groups_line["sn_mv"]
                            _type =  groups_line["tp_atendimento"]
                            _expiration = groups_line["expire"]
                            _new_dict.update(expiration	= groups_line["expire"])
                            break
        elif "TP_ATENDIMENTO" in dict_line:
            if dict_line["TP_ATENDIMENTO"] != None and dict_line["TP_ATENDIMENTO"] != "":
                for groups_line in mv_groups:
                    if "tp_atendimento" in groups_line:
                        if dict_line["TP_ATENDIMENTO"] == groups_line["tp_atendimento"]:
                            _group_name = groups_line["name"]
                            _sn_mv = groups_line["sn_mv"]
                            _type =  groups_line["tp_atendimento"]
                            _expiration = groups_line["expire"]
                            _new_dict.update(expiration	= groups_line["expire"])
                            break
        else:
            _new_dict.update(TP_ATENDIMENTO = "")
            _new_dict.update(expiration	= _expiration)
            
        # Carimbando cd_multi_empresa e variável _company =============================================
        if "cd_multi_empresa" in dict_line:
            _new_dict.update(cd_multi_empresa = dict_line["cd_multi_empresa"])
            if dict_line['cd_multi_empresa'] != 0:
                for company_line in companies:
                    if "cd_multi_empresa" in company_line:
                        if dict_line["cd_multi_empresa"] == company_line["cd_multi_empresa"]:
                            _company = company_line["description"]
                            _new_dict.update(company= _company)
                            break
        elif "CD_MULTI_EMPRESA" in dict_line:
            _new_dict.update(CD_MULTI_EMPRESA = dict_line["CD_MULTI_EMPRESA"])
            if dict_line["CD_MULTI_EMPRESA"] != 0:
                for company_line in companies:
                    if "cd_multi_empresa" in company_line:
                        if dict_line["CD_MULTI_EMPRESA"] == company_line["cd_multi_empresa"]:
                            _company = company_line["description"]
                            _new_dict.update(company= _company)
                            break
        else:
            _new_dict.update(CD_MULTI_EMPRESA = None)
            _new_dict.update(company= _company)
            
        #### Carimbando name Fortigate (name) ==========================================================
        if "name" in dict_line:
                if dict_line["name"] == None or dict_line["name"] == "":
                    dict_line.update(name = _group_name)
        else:
            _new_dict.update(name = _group_name)

        #### Carimbando Grupo Fortigate Nulo (sponsor) ==========================================================
        if "sponsor" not in dict_line:
            _new_dict.update(sponsor = "")

        #### Carimbando a SENHA (password) ==========================================================
        if "password" in dict_line:
            if dict_line["password"] == None or dict_line["password"] == "":
                if "nr_cpf" in dict_line:
                    if dict_line["nr_cpf"] != None and dict_line["nr_cpf"] != "":
                        _new_dict.update(password = dict_line["nr_cpf"]) # Atualizar user-id com nr_cpf
                    else:
                        if "cpf_respo"  in dict_line:
                            if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != "":
                                _new_dict.update(password = dict_line["cpf_respo"]) # Atualizar user-id com cpf_respo
                elif "NR_CPF" in dict_line:
                    if dict_line["NR_CPF"] != None and dict_line["NR_CPF"] != "":
                        _new_dict.update(password = dict_line["NR_CPF"]) # Atualizar user-id com nr_cpf
                    else:
                        if "CPF_RESPO"  in dict_line:
                            if dict_line["CPF_RESPO"] != None and dict_line["CPF_RESPO"] != "":
                                _new_dict.update(password = dict_line["CPF_RESPO"]) # Atualizar user-id com cpf_respo
                else:
                    if "cpf_respo"  in dict_line:
                        if dict_line["cpf_respo"] != "" and dict_line["cpf_respo"] != None:
                            _new_dict.update(password = dict_line["cpf_respo"]) # Atualizar user-id
                    elif "CPF_RESPO"  in dict_line:
                        if dict_line["CPF_RESPO"] != "" or dict_line["CPF_RESPO"] != None:
                            _new_dict.update(password = dict_line["CPF_RESPO"]) # Atualizar user-id
        else:
            if "nr_cpf" in dict_line:
                if dict_line["nr_cpf"] != None and dict_line["nr_cpf"] != "":
                    _new_dict.update(password = dict_line["nr_cpf"]) # Criar user-id
                else:
                    if "cpf_respo"  in dict_line:
                        if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != "":
                            _new_dict.update(password = dict_line["cpf_respo"]) # Criar user-id
                        else:
                            _new_dict.update(itera_fortigate = "INVALID")
                    else:
                        _new_dict.update(password = None) # Criar user-id sem valor
            elif "NR_CPF" in dict_line:
                if dict_line["NR_CPF"] != None and dict_line["NR_CPF"] != "":
                    _new_dict.update(password = dict_line["NR_CPF"]) # Criar user-id
                else:
                    if "CPF_RESPO"  in dict_line:
                        if dict_line["CPF_RESPO"] != None and dict_line["CPF_RESPO"] != "":
                            _new_dict.update(password = dict_line["CPF_RESPO"]) # Criar user-id
                        else:
                            _new_dict.update(itera_fortigate = "INVALID")
                    else:
                        _new_dict.update(password = "") # Criar user-id sem valor
                        dict_line.update(CPF_RESPO = "")
            else:
                dict_line.update(NR_CPF = "")
                if "cpf_respo"  in dict_line:
                    if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != None:
                        _new_dict.update(password = dict_line["cpf_respo"]) # Criar user-id com cpf_respo 
                    else:
                        _new_dict.update(password = "") # Criar user-id sem valor
                        
                elif "CPF_RESPO"  in dict_line:
                    if dict_line["CPF_RESPO"] != None and dict_line["CPF_RESPO"] != None:
                        _new_dict.update(password = dict_line["CPF_RESPO"]) # Criar user-id com cpf_respo 
                    else:
                        _new_dict.update(password = "") # Criar user-id sem valor

                else:
                    dict_line.update(CPF_RESPO = "")
                    _new_dict.update(password = "") # Criar user-id sem valor
        #### Carimbando o COMENTÁRIO  ========================================================

        if "comment" in dict_line:
            if dict_line["comment"] == None or dict_line["comment"] == "":
                _new_dict.update(comment = f"Tipo: {_type} | {_company} | Data Atend.: {_dt_atendimento}") # strftime('%d-%m-%Y %H:%m')}
        else:
            _new_dict.update(comment = f"Tipo: {_type} | {_company} | Data Atend.: {_dt_atendimento}")

        if _new_dict.get("user-id") == None or _new_dict.get("user-id") == "" or _new_dict.get("password") == None or _new_dict.get("password") == "" :
            _new_dict.update(itera_fortigate = "INVALID")
        else:
            _new_dict.update(itera_fortigate = itera_fort)

        join_dict_line = {**dict_line, **_new_dict}
        output_file.file_update("stamp_dict_ora_mv_to_guest_forti",f"\n action_controller - Line 428 - APÓS CARIMBO(DICT_LINE) ({len(dict_line)})!",dict_line)

        return join_dict_line
        # except Exception as err:
        #     # ENVIAR E-MAIL
        #     dict_line.update(itera_fortigate = "INVALID")
        #     print(f"ERROR: ERRO DO BLOCO ACTION_CONTROLLER - 433 - CARIMBANDO CAMPOS AOS NOVOS ATENDIMENTOS DA VIEW-MV  ORACLE", err)
        #     return dict_line


# -------------------- CRIAR E MODIFICAR CHAVES E VALORES DA LISTA -------------------------------
    def stamp_list_dict_for_sponsor(self, list_dict:list, sponsor:str) -> list: # VOUCHER 2.0  ==> Recebe LISTA COM DICIONÁRIOS contendo chaves e valores da consulta oracle e CARIMBA 
        ''' ### Recebe LISTA COM DICIONÁRIOS contendo chaves e valores e CARIMBA nova chave SPONSOR dentro do LISTA DE DICIONÁRIOS"
            ### RETORNA nova LISTA DE DICIONÁRIOS, com chaves em caixa-baixa com novas chaves e valores para o FORTIGATE\n
            :list_dict: Lista com Dicionários com chaves:valor a serem CARIMBADAS
            :sn_mv: (s)-> pertence ao MV | (n)-> apenas Fortigate | (*) todos os grupos\n
        _________________________________________________________________________________\n
        VOUCHER 2.0  - USAR PARA ATENDIMENTOS DO MV   14/08/2024 - Agosto-2024
        '''           
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        _itera_fortigate = "IN.FORTIGATE"
        return_list_dict = []
        for line_list_dict in list_dict:

            # ATUALIZAR DICIONÁRIO COM CHAVE SPONSOR PARA O FORTIGATE
            line_list_dict.update(sponsor = sponsor)
            return_list_dict.append(line_list_dict)
    
        # print(f"\n\n gest_atendimento_ora_filter_key_rest_forti == DICT_JOIN --> {dict_join} \n")   
        del list_dict
        return return_list_dict




# -------------------- CRIAR E MODIFICAR CHAVES E VALORES DA LISTA -------------------------------
    def stamp_list_dict_for_fortigate(self, list_dict:list, sn_mv='*') -> list: # VOUCHER 2.0  ==> Recebe LISTA COM DICIONÁRIOS contendo chaves e valores da consulta oracle e CARIMBA 
        ''' ### Recebe LISTA COM DICIONÁRIOS contendo chaves e valores da consulta oracle e CARIMBA novas chaves dentro desta LISTA DE DICIONÁRIOS"
            ### RETORNA nova LISTA DE DICIONÁRIOS, com chaves em caixa-baixa com novas chaves e valores para o FORTIGATE\n
            :list_dict: Lista com Dicionários com chaves:valor a serem CARIMBADAS
            :sn_mv: (s)-> pertence ao MV | (n)-> apenas Fortigate | (*) todos os grupos\n
        _________________________________________________________________________________\n
        VOUCHER 2.0  - USAR PARA ATENDIMENTOS DO MV   14/08/2024 - Agosto-2024
        '''           
        action_controller = ActionController()
        # ---------------------------------------------------------------------
        _itera_fortigate = "IN.FORTIGATE"
        _sn_mv = sn_mv
        return_list_dict = []
        for line_list_dict in list_dict:

            # ATUALIZAR DICIONÁRIO COM CHAVES PARA O FORTIGATE
            stamp_dict = self.stamp_dict_ora_mv_to_guest_forti(line_list_dict, _itera_fortigate, _sn_mv)        
            return_list_dict.append(stamp_dict)
    
        # print(f"\n\n gest_atendimento_ora_filter_key_rest_forti == DICT_JOIN --> {dict_join} \n")   
        return return_list_dict


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def stamp_from_ora_mv_to_guest_forti(self, dict: dict, itera_fort="SUBMIT", type_group="*"): # VOUCHER 2.0 #### CARIMBAR CAMPOS
      ''' CARIMBAR novos títulos as CHAVES do DICIONÁRIO DA VIEW-ORACLE - MV :\n
          :dict: Dicionário passado que terá suas chaves renomeadas e novas inseridas\n
          :itera_fort: String que informa o status de interação com o fortigate \n
          CHAVES ==> CPF => user-id | cd_atendimento => name | nr_cpf => user-id | 
          cpf_respo => cpf_resp | sponsor=Grupo | password => Será criada a senha|\n
          ------------------------------------------------------------------------
          RETORNA DICIONÁRIO com CHAVES CARIMBADAS:\n
          CASO NÃO TENHA CPF => Retorna itera_fortigate = NOT.FORTIGATE
          ________________________________________________________________________
          Voucher 2.0      JUL-24 \n
      '''
      # --------------------------------------------------------------------       
      all_stamp = []
      
      # lista os Grupos com tipo informado:
      #   retorna: [name, tp_atendimento, sn_mv, expire] \n
      groups = self.select_mv_groups_type(type_group)
      forti_groups = self.select_forti_groups_type(type_group) 
      companies = self.select_company()
      # --------------------------------------------------
      dict_line = dict
      # print (f"\n Antes STAMP --> {dict_line}")
      stamp_dict = {}
      if "nr_cpf" in dict_line:
        if dict_line["nr_cpf"] != None or dict_line["nr_cpf"] != "":
            stamp_dict = {"user-id" : dict_line["nr_cpf"]}
            stamp_dict.update(itera_fortigate = itera_fort)
        else:
            if "cpf_respo"  in dict_line:
                if dict_line["cpf_respo"] == "" or dict_line["cpf_respo"] != None:
                    stamp_dict = {"user-id" :  dict_line["cpf_respo"]}
                    stamp_dict.update(itera_fortigate = itera_fort)
            else:
                stamp_dict = {"user-id" : ""}
                stamp_dict.update(user_id = "")
                stamp_dict.update(itera_fortigate = "INVALID") # Modifica STATUS quando (NÃO EXISTE CPF e CPF Responsável)            
      else:
        stamp_dict = {"user-id" : ""}
        stamp_dict.update(user_id = "")
        stamp_dict.update(itera_fortigate = "INVALID") # Modifica STATUS quando (NÃO EXISTE CPF e CPF Responsável)            

      if "cd_atendimento" in dict_line:
          stamp_dict.update(name = dict_line["cd_atendimento"])

      if stamp_dict["user-id"] !="" :
          stamp_dict.update(password = self.slice2_join(str(stamp_dict["user-id"]), 4, str(stamp_dict["name"]), 4) )
      else:
          stamp_dict.update(password = "")

      if "tp_atendimento" in dict_line:
        #   stamp_dict.update(tp_atendimento = dict_line["tp_atendimento"]) já existe no mv não precisa criar
          if dict_line["tp_atendimento"] != 0:
              stamp_dict.update(sponsor = "INVALID")
              for groups_line in groups:
                  if "tp_atendimento" in groups_line:
                      if dict_line["tp_atendimento"] == groups_line["tp_atendimento"]:
                          stamp_dict.update(desc_atendimento = groups_line["name"])
                          stamp_dict.update(sn_mv = groups_line["sn_mv"])
                          stamp_dict.update(expiration = groups_line["expire"])
          else:
              stamp_dict.update(sponsor = "INVALID")  
              
      if "cd_multi_empresa" in dict_line:
        #   stamp_dict.update(cd_multi_empresa = dict_line["cd_multi_empresa"]) já existe no mv não precisa criar
          if dict_line["cd_multi_empresa"] != 0:
              stamp_dict.update(company = "INVALID")    
              for company_line in companies:
                  if "cd_multi_empresa" in company_line:
                      if dict_line["cd_multi_empresa"] == company_line["cd_multi_empresa"]:
                          stamp_dict.update(company = company_line["description"])
          else:
              stamp_dict.update(company = "INVALID") 

      if "dt_atendimento" in dict_line:
          _dt_atendimento = dict_line["dt_atendimento"]

      stamp_dict.update(id = 0)
      stamp_dict.update(comment = f"Tipo: {dict_line['tp_atendimento']} | {stamp_dict['company']} | Data Atend.: {_dt_atendimento.strftime('%d-%m-%Y %H:%m')}")
      stamp_dict.update(status = "")
      stamp_dict.update(http_status = 0)
      stamp_dict.update(status_message = "")

      if stamp_dict.get("user-id") == 0 or stamp_dict.get('sponsor') == "INVALID" or stamp_dict.get('company') ==  "INVALID":
          stamp_dict.update(itera_fortigate = "NOT.FORTIGATE")

      # print(f"\n APÓS CARIMBO(STAMP) -----> {stamp_dict}")
      return stamp_dict

    def select_mv_groups_type(self, type_group: str): # VOUCHER 2.0 
        ''' Lista todos os grupos da variável MV_GROUPS\n
            :type_group: Filtrar por TIPO, valor string que pode ser\n
            (s)-> pertence ao MV | (n)-> apenas Fortigate | (*) todos os grupos
            \n___________________________________________________________________\n
            VOUCHER 2.0    (process / )       junho - 2024    
        '''
        # VARIÁVEL COM TODOS OS GRUPOS
        _groups = table_in_lists_env.MV_GROUPS
        _list_new = []
        if type_group == "*":
            for line_dict in _groups:
                _list_new.append(line_dict)
        else:
            for line_dict in _groups:
                if line_dict["sn_mv"] == type_group:
                    _list_new.append(line_dict)
        return(_list_new)      

    def select_forti_groups_type(self, type_group: str): # VOUCHER 2.0 
        ''' Lista todos os grupos FORTIGATE da variável FORTI_GROUPS\n
            :type_group: Filtrar por TIPO, valor string que pode ser\n
            (s)-> pertence ao MV | (n)-> apenas Fortigate | (*) todos os grupos
            \n___________________________________________________________________\n
            VOUCHER 2.0    (process / )       junho - 2024    
        '''
        # VARIÁVEL COM TODOS OS GRUPOS
        _groups = table_in_lists_env.FORTI_GROUPS
        _list_new = []
        if type_group == "*":
            for line_dict in _groups:
                _list_new.append(line_dict)
        else:
            for line_dict in _groups:
                if line_dict["sn_mv"] == type_group:
                    _list_new.append(line_dict)
        return(_list_new)      

    def select_company(self): # VOUCHER 2.0 
        ''' Lista todos os grupos da variável COMPANIES\n
            Retrona dicionário com chave e valores\n
        ___________________________________________________________________\n
            VOUCHER 2.0  (SELF.stamp_from_ora_mv_to_guest_forti / )   JUNHO-2024          
        '''
        # VARIÁVEL COM TODOS OS GRUPOS
        _groups = table_in_lists_env.COMPANIES
        _list_new = []
        for line_dict in _groups:
            _list_new.append(line_dict)

        return(_list_new)   
    
    ####################################################################
    def create_query(self, table, columns: str, where=None, order=None, asc=True):
        '''Cria script sql de CONEXÃO. QUERY SELECT ........'''

        return f"SELECT {columns} FROM {table} {' WHERE ' if where != None else ""}{where if where != None else ""} {' ORDER BY ' if order else ""}{order if order != None else ""}"
        # Retorna QUERY MONTADA    

    ####################################################################
    def join_dict(self, dict1:dict, dict2:dict):
        '''CONCATENA 2 dicionários 
        '''
        join_two = {**dict1, **dict2} 
        return join_two

    ####################################################################    
    def strfromtime(self, time_str) -> str:
        ''' Formata DATA em STRING '''
        str_date = time_str.strftime("%y-%m-%d")
        return str_date

    ####################################################################
    def sets_Key_dic_rest_forti(self, query, name_search) -> set:
        ''' Procurar sub-chave RESULTS / response GUEST in JSON convertido em dicionário
            procura GRUPO if_key_search e COLUMNS key_columns
            RETORNA SETS com VALORES da chave Key_columns
            
        '''
        #name_search = 'cd_atendimento'
        key_columns_set = set()

        for i in query:
            ''' Itera pelas linhas da lista
                Abaixo convertemos a linha em um Dicionário
            '''
            dictionary = dict(i)
            
            for k in dictionary.keys():
                ''' o segundo FOR varre as CHAVES do dicionário criado e retorna VALOR  '''
                if k == name_search:
                    key_columns_set.add(dictionary[k])

        return key_columns_set
        
    #############################################################################    
    def sets_Key_dic_json_rest_forti(self, response, if_key_search, Key_columns) -> set:
        ''' Procurar sub-chave RESULTS / GUEST do JSON convertido em dicionário
            procura GRUPO if_key_search e COLUMNS key_columns
            RETORNA SETS com VALORES da chave Key_columns
        '''
        #### ITERAÇÃO em response - DICIONÁRIO(json) 
        # -------------------------------------------------------------------------------- 
        # chaves de dicionários |FORTIGATE -  ADICIONAR valor da chave(NAME) ->  add em SET()
        for1_key_global = 'results'
        for2_key_dic = 'guest' 
        
        # ------------------------------------
        if_key = 'name'
        #if_key_search = 'Internacao'
        #Key_columns = 'name'
        
        # variable get SET() --------------------- 
        key_columns_set = set()

        for key_global in response[for1_key_global]:
            if key_global[if_key] == if_key_search:
                for key in key_global[for2_key_dic]:
                    key_columns_set.add(int(key[Key_columns])) 

        # print(f"total de registros FORTIGATE: {len(key_columns_set)}")
        # print("========================================================")
        # print(key_columns_set)
        return key_columns_set

    ###########################################################################
    def request_response(self, reason):
        ''' Cria mensagem baseado na resposta do Request
            :reason: Código da resposta
            Retorna string com frase do código
        '''        
        match reason:
            case 000:
                return "not Fortigate"
            case 100:
                return "Continue"
            case 101:
                return  "Switching Protocols"
            case 200:
                return  "OK"
            case 201:
                return  "Created"
            case 202:
                return  "Accepted"
            case 203:
                return  "Non-Authoritative Information"
            case 204:
                return  "No Content"
            case 205:
                return  "Reset Content"
            case 206:
                return  "Partial Content"
            case 300:
                return  "Multiple Choices"
            case 301:
                return  "Moved Permanently"
            case 302:
                return  "Found"
            case 303:
                return  "See Other"
            case 304:
                return  "Not Modified"
            case 305:
                return  "Use Proxy"
            case 307:
                return  "Temporary Redirect"
            case 400:
                return  "Bad Request"
            case 401:
                return  "Unauthorized"
            case 402:
                return  "Payment Required"
            case 403:
                return  "Falta CSRF token"
            case 404:
                return  "Recurso não Encontrado"
            case 405:
                return  "Method Not Allowed"
            case 406:
                return  "Not Acceptable"
            case 407:
                return  "Proxy Authentication Required"
            case 408:
                return  "Request Timeout"
            case 409:
                return  "Conflict"
            case 410:
                return  "Gone"
            case 411:
                return  "Length Required"
            case 412:
                return  "Precondition Failed"
            case 413:
                return  "Payload Muito Grande"
            case 414:
                return  "URI Too Long"
            case 415:
                return  "Unsupported Media Type"
            case 416:
                return  "Range Not Satisfiable"
            case 417:
                return  "Expectation Failed"
            case 426:
                return  "Upgrade Required"
            case 429:
                return  "Bloqueio por Atingir limite de tentativas"
            case 444:
                return  "Nenhuma Resposta"
            case 500:
                return  "Exist: Not Insert"
            case 501:
                return  "Not Implemented"
            case 502:
                return  "Bad Gateway"
            case 503:
                return  "Service Unavailable"
            case 504:
                return  "Gateway Timeout"
            case 505:
                return  "HTTP Version Not Supported"
            case 523:
                return  "Origem É Inatingível"
            case 524:
                return "Um Tempo limite Ocorreu"

    def compare(self, a, _operator:str, b) -> bool:
        '''
            Método compara duas variáveis através do operador de comparação passado
            Retorna booleano (True/False)
        '''

        match _operator:
            case "==":
                return a == b
            case "!=":
                return a != b
            case ">":
                return a > b
            case ">=":
                return a >= b
            case "<":
                return a < b
            case "<=":
                return a <= b
            case _:
                return False
                


    def import_csv_payload(self, csv_file):
        '''Recebe arquivo CSV tabulado por ';' e devolve dicionário '''
        with open(f"{csv_file}", "r", encoding="utf-8") as file:
            reader = DictReader(file, delimiter=';')
            return list(reader) #Retorna uma lista de dicionarários, que correspondem a cada linha do csv

    ####################################################################
    def extract_attrib_table(self, table):
        '''Retorna Lista com os Atributos da Tabela ! DESC column'''
        return ''.join(['DESC', table]) 





    ############################################################################

#     def stamp_from_care_mv_to_guest_forti(self, dict: dict, itera_fort="SUBMIT", type_group="*"): # CARIMBAR CAMPOS
#         ''' CARIMBAR novos títulos as CHAVES do DICIONÁRIO DA CARE_MV - SQL:\n
#             :dict: Dicionário passado que terá suas chaves renomeadas e novas inseridas\n
#             :itera_fort: String que informa o status de interação com o fortigate \n
#             CHAVES ==> CPF => user-id | cd_atendimento => name | nr_cpf => user-id | 
#             cpf_respo => cpf_resp | sponsor=Grupo | password => Será criada a senha|\n
#             ------------------------------------------------------------------------
#             RETORNA DICIONÁRIO com CHAVES CARIMBADAS:\n
#             CASO NÃO TENHA CPF => Retorna itera_fortigate = NOT.FORTIGATE
#             ________________________________________________________________________
#             Voucher 2.0 \n
#         '''
#         # --------------------------------------------------------------------       
#         all_stamp = []

#         # lista os Grupos com tipo informado:
#         #   retorna: [name, tp_atendimento, sn_mv, expire] \n
#         groups = self.select_mv_groups_type(type_group)
#         forti_groups = self.select_forti_groups_type(type_group)  
#         companies = self.select_company()
#         #####################################
#         # print(companies)
#         dict_line = dict
#         # print (f"\n Antes STAMP --> {dict_line}")
#         stamp_dict = {}

#         if "user-id" in dict_line:
#             if dict_line["user-id"] == None or dict_line["user-id"] == "":
#                 if "nr_cpf" in dict_line:
#                     if dict_line["nr_cpf"] != None and dict_line["nr_cpf"] != "":
#                         dict_line["user-id"] = dict_line["nr_cpf"] # Atualizar user-id com nr_cpf
#                         dict_line.update(itera_fortigate = itera_fort)
#                     else:
#                         if "cpf_respo"  in dict_line:
#                             if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != "":
#                                 dict_line["user-id"] = dict_line["cpf_respo"] # Atualizar user-id com cpf_respo
#                                 dict_line.update(itera_fortigate = itera_fort)
#                             else:
#                                 dict_line.update(itera_fortigate = "INVALID")    
#                         else:
#                             dict_line.update(itera_fortigate = "INVALID")
#                 else:
#                     if "cpf_respo"  in dict_line:
#                         if dict_line["cpf_respo"] != "" or dict_line["cpf_respo"] != None:
#                             dict_line["user-id"] = dict_line["cpf_respo"] # Atualizar user-id
#                             dict_line.update(itera_fortigate = itera_fort)
#                         else:
#                             dict_line.update(itera_fortigate = "INVALID")    
#                     else:
#                         dict_line.update(itera_fortigate = "INVALID")
#             else:
                
#                 dict_line.update(itera_fortigate = itera_fort)
#         else:
#             if "nr_cpf" in dict_line:
#                 if dict_line["nr_cpf"] != None and dict_line["nr_cpf"] != "":
#                     dict_line = {"user-id" : dict_line["nr_cpf"]} # Criar user-id
#                     dict_line.update(itera_fortigate = itera_fort)

#                 else:
#                     if "cpf_respo"  in dict_line:
#                         if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != "":
#                             dict_line = {"user-id" : dict_line["cpf_respo"]} # Criar user-id
#                             dict_line.update(itera_fortigate = itera_fort)
#                         else:
#                             dict_line = {"user-id" : None} # Criar user-id sem valor
#                             dict_line.update(itera_fortigate = "INVALID")
#                     else:
#                         dict_line = {"user-id" : None} # Criar user-id sem valor
#                         dict_line.update(itera_fortigate = "INVALID")
#             else:
#                 if "cpf_respo"  in dict_line:
#                     if dict_line["cpf_respo"] != None and dict_line["cpf_respo"] != None:
#                         dict_line = {"user-id" : dict_line["cpf_respo"]} # Criar user-id com cpf_respo 
#                         dict_line.update(itera_fortigate = itera_fort)
#                     else:
#                         dict_line = {"user-id" : None} # Criar user-id sem valor
#                         dict_line.update(itera_fortigate = "INVALID")
#                 else:
#                     dict_line = {"user-id" : None} # Criar user-id sem valor
#                     dict_line.update(itera_fortigate = "INVALID")

#         # == NOVOS CAMPOS  PARA VALIDAR ================================================================================        

#         if "user_id" in dict_line: # Precisa do resultado da chave acima user-id
#             if dict_line["user_id"] == None or dict_line["user_id"] == "":
#                 dict_line.update(user_id =  dict_line["user-id"])
#         else:
#                 dict_line.update(user_id =  dict_line["user-id"])

#         # chave name
#         if "name" in dict_line:
#             if dict_line["name"] == None or dict_line["name"] == "":
#                 if "cd_atendimento" in dict_line:
#                     dict_line.update(name = dict_line["cd_atendimento"])
#         else:
#             if "cd_atendimento" in dict_line:
#                 dict_line.update(name = dict_line["cd_atendimento"])
#             else:
#                 dict_line.update(name = None)

# # ===========================================

#         _dt_atendimento = datetime.now()  
#         stamp_dict.update(password = "")
#         stamp_dict.update(desc_atendimento = "INVALID")
#         stamp_dict.update(sponsor = "INVALID")
#         stamp_dict.update(company = "INVALID")                
#         stamp_dict.update(sn_mv = None)
#         stamp_dict.update(expiration = 0)
#         stamp_dict.update(id = None)
#         stamp_dict.update(comment = f"Tipo: {stamp_dict['tp_atendimento']} | {stamp_dict['company']} | Data Atend.: {_dt_atendimento.strftime('%d-%m-%Y %H:%m')}")
#         stamp_dict.update(status = "")
#         stamp_dict.update(http_status = 0)
#         stamp_dict.update(status_message = "")
        
#         if "cd_atendimento" in dict_line:
#             stamp_dict.update(name = dict_line["cd_atendimento"])

#         if stamp_dict["user-id"] !="" and stamp_dict["name"] !='':
#             stamp_dict.update(password = "" )

#         if "tp_atendimento" in dict_line:
#             if stamp_dict['tp_atendimento'] != 0:
#                 for groups_line in groups:
#                     if "tp_atendimento" in groups_line:
#                         if stamp_dict["tp_atendimento"] == groups_line["tp_atendimento"]:
#                             stamp_dict.update(name = groups_line["name"])
#                             stamp_dict.update(sn_mv = groups_line["sn_mv"])
#                             stamp_dict.update(expiration = groups_line["expire"])
#                             break

#         if "cd_multi_empresa" in dict_line:
#             stamp_dict.update(cd_multi_empresa = dict_line["cd_multi_empresa"])
#             if stamp_dict['cd_multi_empresa'] != 0:
#                 stamp_dict.update(company =  "INVALID")     
#                 for company_line in companies:
#                     if "cd_multi_empresa" in company_line:
#                         if stamp_dict["cd_multi_empresa"] == company_line["cd_multi_empresa"]:
#                             stamp_dict.update(company = company_line["description"])
#                             break

#         if "dt_atendimento" in dict_line:
#             _dt_atendimento = dict_line["dt_atendimento"]


#         stamp_dict.update(comment = f"Tipo: {stamp_dict['tp_atendimento']} | {stamp_dict['company']} | Data Atend.: {_dt_atendimento.strftime('%d-%m-%Y %H:%m')}")

#         if stamp_dict.get("user-id") == None or stamp_dict.get('sponsor') == "INVALID" or stamp_dict.get('company') ==  "INVALID":
#             stamp_dict.update(itera_fortigate = "NOT.FORTIGATE")

#         return stamp_dict
