from src.view.bash_view import BashView
# from src.view.output_file import OutputFile
from src.controllers.action_controller import ActionController
from src.controllers.set_column_controller import SetColumnController
from src.controllers.care_sql_int_controller import CareSqlIntController
from src.controllers.care_ora_mv_controller import CareOraMVController
from src.controllers.restapi_forti_controller import RestAPIFortiController
from src.controllers.visitor_sql_int_controller import VisitorSqlIntController
from datetime import datetime, timedelta
from pytz import timezone
from itertools import chain
import time
import os
from src.env import table_in_lists_env

def start() -> None:

    # os.system('clear')
    time_difference = timedelta(hours=-3)
    ## instanciando as classes ==============================================
    ## ----------------------------------------------------------------------
    bash_view = BashView()
    # output_file = OutputFile()
    ### Instânciando Controller CARE - ORACLE
    care_ora_mv_controller = CareOraMVController()
    ### Instânciando Controller CARE - MYSQL
    care_sql_int_controller = CareSqlIntController()
    ### Instânciando Controller RESTAPI - FORTIGATE
    restapi_forti_controller = RestAPIFortiController()
    ### Instânciando Controller CONJUNTOS 
    set_column_controller = SetColumnController()
    ### Instânciando Controller AÇÕES auxiliares
    action_controller = ActionController()
    ### Instânciando Controller GROUP - INTEGRADOR
    visitor_sql_int_controller = VisitorSqlIntController()
    # ### Instânciando 
    # _table_in_lists_env = table_in_lists_env # Usada para fins de teste em desenvolvimento
    time_start = datetime.now()
    _time_sleep = 300
    
    while True:
        bash_view.print_header(f"AGUARDANDO {_time_sleep/60} Minutos PARA INÍCIO DA VARREDURA")
        time.sleep(_time_sleep)

        # Início do projeto
        # -----------------------------------------------------------------------------------------------------------
        _mv = False
        _care = False
        _fortigate = False
        # -------------------------------------------------------------------------------------------------------
        ## 1º ==> Abre a view do MV  ===================================================================
        # -------------------------------------------------------------------------------------------------------
        try: # BLOCO DE CONSULTA ORACLE!
            return_care_ora_mv = care_ora_mv_controller.select_query_ora_mv()
            # print(f" Linha 51 ==> {return_mv_groups}")
            if len(return_care_ora_mv) > 0:
                for ora_line in return_care_ora_mv:
                    if "status" in ora_line and "status" == "error":
                        bash_view.print_header("NÃO FOI POSSÍVEL CONSULTAR O  ORACLE - MV")
                        bash_view.print_list_dict_by_pretty_table(return_care_ora_mv)
                        #manda email
                        _mv = False
                        break
                    else:
                        bash_view.print_header(f"ORACLE MV POSSUI ({len(return_care_ora_mv)}) ATENDIMENTOS ATIVOS!")
                        # output_file.file_update("total_records",f"ATENDIMENTOS ATIVOS - VIEW_VOUCHERS - ORACLE - ({len(return_care_ora_mv)})")
                        # output_file.file_json_new("return_care_ora_mv",return_care_ora_mv)
                        _mv = True
                        break
            else:
                bash_view.print_header(f"ORACLE MV POSSUI ({len(return_care_ora_mv)}) ATENDIMENTOS ATIVOS!")
                _mv = True # não retornou registros do MV
            if not _mv:
                continue
        except Exception as e:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO DE CONSULTA ORACLE!" )
            continue
        # -------------------------------------------------------------------------------------------------------
        ## 2º ==> Abre a tabela do care_mv Mysql  =====================================================|
        # -------------------------------------------------------------------------------------------------------
        try: # BLOCO DE CONSULTA SQL - CARE_MV!    
            if _mv:   
                care_sql_mv = care_sql_int_controller.select_all_cd_atendimento_not_dt_remove_int_dic()
                # print(f" Linha 76 ==> {care_sql_mv}")
                if len(care_sql_mv) > 0:
                    for care_line in care_sql_mv:
                        if "status" in care_line and "status" == "error":
                            bash_view.print_header("ERROR: NÃO FOI POSSÍVEL CONSULTAR O MYSQL - CARE_MV")
                            bash_view.print_list_dict_by_pretty_table(care_sql_mv)
                            _care = False
                        else:
                            bash_view.print_header(f"CARE_MV POSSUI ({len(care_sql_mv)}) ATENDIMENTOS ATIVOS ")
                            # output_file.file_update("total_records",f"ATENDIMENTOS ATIVOS - CARE_MV - MYSQL        - ({len(care_sql_mv)})") 
                            # output_file.file_json_new("care_sql_mv",care_sql_mv)
                            _care = True
                        break # sai do loop 
                else:
                    bash_view.print_header("CARE_MV NÃO POSSUI ATENDIMENTOS ATIVOS ")
                    _care = True
            else:
                _care = False
            
            if not _care: 
                continue
        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO DE CONSULTA SQL!", err )
            # output_file.file_update("error_from_process",f"EXCEPT ERROR: ERRO DO BLOCO   DE CONSULTA SQL!", err)
            continue

        # -------------------------------------------------------------------------------------------------------
        ## 3º ==> CONSULTA TODOS OS GRUPOS DO PROJETO NO FORTIGATE  COM SEUS REGISTROS ==========================|
        # -------------------------------------------------------------------------------------------------------                
        try:
            # VARIÁVEIS PARA ATENDER O FLUXO DOS BLOCOS 3, 4 e 5
            # ....................................................................................................
            avaliable_groups_total_free = 0 # Totalizador de grupos com Disponibilidade para receber registros
            avaliable_groups = [] # Nova Lista com dicionários dos grupos e sua Disponibilidade
            vouchers_mv_in_forti = [] # Nova Lista dos atendimentos no Fortigate
            
            # ....................................................................................................
            _vouchers_in_forti = restapi_forti_controller.get_all_groups_from_rest_forti()
            if _vouchers_in_forti["status"]	== "success":
                
                if len(_vouchers_in_forti["results"]) > 0: # Existe Grupos no Fortigate?
                    groups_total_used = 0 
                    _atendime_forti = [] # Lista Receberá dicionário de novos grupos
                    maximum = 500 # Limite máximo de registro no FORTIGATE
                    forti_groups = action_controller.select_forti_groups_type("s") # Lista de todos os GRUPOS do tipo MV
                    if len(forti_groups) > 0: # se Existe grupo do tipo MV
                        for line_forti_group in forti_groups:
                            if line_forti_group["sn_mv"] == "s": # se o grupo pesquisado for do MV
                                for group_guest in _vouchers_in_forti["results"]: # Navegar dentro da consulta Geral a procura da chave results
                                    if line_forti_group["name"] == group_guest["name"]: # Se o valor da chave name do grupo consultado for igual ao name do grupo em result
                                        dict_line_group = {}
                                        dict_line_group.update(name = group_guest["name"]) # Atualizando um novo dicionário com o nome do grupo
                                        ''' Calcular Total de registros em cada GRUPO '''
                                        _length = len(group_guest["guest"]) # Navegar dentro da consulta Geral a procura da chave guest e contar quantos registros tem
                                        ''' Calcular Disponibilidade em cada GRUPO '''
                                        groups_total_used += _length
                                        dict_line_group.update(avaliable = maximum - _length) # Total de disponibilidade para novos registros
                                        avaliable_groups.append(dict_line_group) # Atualiza Lista com dicionário dict_line_group  
                                        if dict_line_group["avaliable"] > 0: # se o grupo tiver disponibilidade?
                                            avaliable_groups_total_free += 1 # Totalizar grupos disponíveis
                                        # Se o Total do grupo for maior que 0 é porque temos registros dentro
                                        if _length > 0:
                                            del _atendime_forti[:]
                                            _atendime_forti = action_controller.stamp_list_dict_for_sponsor(group_guest["guest"], group_guest["name"])
                                            ''' Agrupa os Registros de cada GRUPO em nova Lista '''
                                            vouchers_mv_in_forti.extend(_atendime_forti) # Incrementando novos dicionários a lista
                                            
                        bash_view.print_header(f"TOTAL DE DISPONIBILIDADE DOS GRUPOS EXISTENTES NO FORTIGATE {avaliable_groups_total_free}", avaliable_groups)
                        bash_view.print_header(f"VOUCHERS DE ATENDIMENTOS EXISTENTES NO FORTIGATE (total nos grupos {groups_total_used}) ( total no Dicionário final: {len(vouchers_mv_in_forti)})")
                        # output_file.file_update("total_records",f"ATENDIMENTOS ATIVOS - FORTIGATE              - ({len(vouchers_mv_in_forti)})")
                        # output_file.file_update_insert_table("total_records",f"DISPONIBILIDADE DOS GRUPOS NO FORTIGATE ({avaliable_groups_total_free}) -", avaliable_groups)
                        _fortigate = True

                    else:
                        bash_view.print_header(f"ERROR: NÃO HÁ GRUPOS  DO TIPO INFORMADO NO ARQUIVO JSON {len(forti_groups)}")
                        continue
                else:
                    bash_view.print_header(f"ERROR: NÃO HÁ GRUPOS NO FORTIGATE {len(_vouchers_in_forti)}")
                    continue
            else:
                bash_view.print_header(f"ERROR: AO CONSULTAR O FORTIGATE! AGUARDAR UM TEMPO PARA REINICIAR AS VALIDAÇÕES",  _vouchers_in_forti)
                # output_file.file_update("error_from_process",f"ERROR: AO CONSULTAR O FORTIGATE! AGUARDAR UM TEMPO PARA REINICIAR AS VALIDAÇÕES",  _vouchers_in_forti)
                continue
        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO 3 GRUPOS FORTIGATE", err)
            # output_file.file_update("error_from_process",f"EXCEPT ERROR: BLOCO 3 GRUPOS FORTIGATE", err)
            continue

        # -------------------------------------------------------------------------------------------------------
        ## 4º ==> PROCESSOS DE CONJUNTOS  ======================================================================|
        # -------------------------------------------------------------------------------------------------------  

        try: # BLOCO DOS CONJUNTOS, ORACLE-MV E SQL CARE_MV!
            # -------------------------------------------------------------------------------------------------------------------------------------
            #### Carimbar dicionário ORACLE, com campos que atendam ao fortigate
            # -------------------------------------------------------------------------------------------------------------------------------------
            #### EXTRAÇÃO DOS VALORES DE UMA LISTA COM BASE EM CHAVE PASSADA (CÓDIGO ATENDIMENTO OU USER-ID)
            # -------------------------------------------------------------------------------------------------------------------------------------
            ''' Extrair da consulta MV, lista com Código atendimento '''
            cd_atendimento_ora_value_list_dict = action_controller.value_column_list_dict(return_care_ora_mv, 'CD_ATENDIMENTO')
            bash_view.print_header(f"LISTA COM CÓDIGOS DOS ATENDIMENTOS NA << VIEW-MV - ORACLE >> <== TOTAL ==> {len(cd_atendimento_ora_value_list_dict)}")
            # output_file.file_update("total_records",f"TOTAL DE CD_ATENDIMENTO EXTRAÍDOS DO DICIONÁRIO VIEW-MV - ORACLE ({len(cd_atendimento_ora_value_list_dict)}) -")
            # ------------------------------------------------------------------------------------------------------------------------------------- 
            '''Extrair da consulta SQL, Lista com cd_atendimento'''
            cd_atendimento_in_care_mv_dict = action_controller.value_column_list_dict(care_sql_mv, "cd_atendimento")
            bash_view.print_header(f"LISTA COM CÓDIGOS DOS ATENDIMENTOS NA << CARE_MV - MYSQL  >> <== TOTAL ==> {len(cd_atendimento_in_care_mv_dict)}")
            # output_file.file_update("total_records",f"TOTAL DE CD_ATENDIMENTO EXTRAÍDOS DO DICIONÁRIO CARE_MV - MYSQL ({len(cd_atendimento_in_care_mv_dict)}) -")
            # -------------------------------------------------------------------------------------------------------------------------------------
            ''' Extrair da consulta FORTIGATE, Lista com coluna user-id '''
            user_id_in_fortigate = action_controller.value_column_list_dict(vouchers_mv_in_forti, "user-id")
            # -------------------------------------------------------------------------------------------------------------------------------------
            user_id_in_fortigate_int = action_controller.conv_list_str_for_int(user_id_in_fortigate)
            bash_view.print_header(f"LISTA COM CÓDIGOS DOS ATENDIMENTOS CONVERTIDO PARA INTEIRO NO << FORTIGATE  >> <== TOTAL ==> {len(user_id_in_fortigate_int)}")
            # output_file.file_update("total_records",f"TOTAL DE CD_ATENDIMENTO EXTRAÍDOS DO DICIONÁRIO FORTIGATE ({len(user_id_in_fortigate)}) -")
            # -----------------------------------------------------------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------------------------------------------------------
            #### TRABALHAR COM CONJUNTOS
            # -------------------------------------------------------------------------------------------------------------------------------------

            decreased_care_mv_sql = set_column_controller.sets_difference_a_b(cd_atendimento_in_care_mv_dict, cd_atendimento_ora_value_list_dict)
            ''' Diferença: SÓ EXISTE NO DB - MYSQL '''
            
            bash_view.print_header(f"ANTIGOS ATENDIMENTOS ESTÃO SQL - CARE_MV E NÃO ESTÃO NA VIEW-MV - ORACLE <== TOTAL ==> {len(decreased_care_mv_sql)}") # , decreased_care_mv_sql
            # output_file.file_update("total_records",f"ANTIGOS ATENDIMENTOS ESTÃO SQL - CARE_MV E NÃO ESTÃO NA VIEW-MV - ORACLE <== TOTAL ==> ({len(decreased_care_mv_sql)}) -")
            
            intersection_care_ora_mv = set_column_controller.sets_intersection(cd_atendimento_ora_value_list_dict, cd_atendimento_in_care_mv_dict)
            '''Interseção: EXISTE TANTO NA VIEW, como no DB-MYSQL'''
            
            # output_file.file_update("total_records",f"INTERSEÇÃO: EXISTE TANTO NO ORACLE, COMO NO MYSQL <== TOTAL ==> ({len(intersection_care_ora_mv)}) -")
            bash_view.print_header(f"INTERSEÇÃO: EXISTE TANTO NO ORACLE, COMO NO MYSQL <== TOTAL ==> {len(intersection_care_ora_mv)}")
        
            cod_new_care_ora_mv = set_column_controller.sets_difference_a_b(cd_atendimento_ora_value_list_dict, cd_atendimento_in_care_mv_dict)
            ''' Diferença: SÓ EXISTE NA VIEW- ORACLE '''
            
            bash_view.print_header(f"NOVOS ATENDIMENTOS ESTÃO NA VIEW-MV - ORACLE E NÃO ESTÃO NO CARE_MV - SQL <== TOTAL ==> {len(cod_new_care_ora_mv)}") # , cod_new_care_ora_mv
            # output_file.file_update("total_records",f"NOVOS ATENDIMENTOS ESTÃO NA VIEW-MV - ORACLE E NÃO ESTÃO NO CARE_MV - SQL <== TOTAL ==> ({len(cod_new_care_ora_mv)}) -")

            # -------------------------------------------------------------------------------------------------------
            # ATRIBUINDO GRUPOS  E CARIMBANDO CAMPOS AOS NOVOS ATENDIMENTOS DA VIEW-MV ORACLE  ===============
            # -------------------------------------------------------------------------------------------------------
            new_dict_stamp_new_care_mv = [] # Lista para Receber os novos atendimentos caso  exista disponibilidade de grupos do fortigate
            ''' Lista para receber os novos atendimentos e atribuir grupos. | (Usado no bloco 4 e 5)'''
            
            if len(cod_new_care_ora_mv) > 0 and avaliable_groups_total_free > 0:
                ''' Existe Novos Atendimentos na VIEW e Existe disponibilidades nos grupos? '''
                
                # if avaliable_groups_total_free > 0: # Se existir disponibilidade nos grupos e existir novos atendimentos
                
                filter_new_care_ora_mv = action_controller.search_key_in_dict_insert_key_return_new_dict('CD_ATENDIMENTO', cod_new_care_ora_mv, return_care_ora_mv)
                ''' Agrupar linhas c/novos atendimentos VIEW ORACLE '''

                # bash_view.print_header(f"AGRUPANDO AS LINHAS QUE ESTÃO NA LISTA NOVOS ATENDIMENTOS MV ({len(filter_new_care_ora_mv)})")
                # try: VAMOS atribuir os grupos aos novos atendimento do MV
                _avaliable = False
                for line_new_care_ora_mv in filter_new_care_ora_mv:
                    stamp_line_new_care_ora_mv = action_controller.stamp_dict_ora_mv_to_guest_forti(line_new_care_ora_mv) 
                    ''' Criar novas chaves para atender ao FORTIGATE '''

                    for line_avaliable_groups in avaliable_groups: # Iterar no no grupo criado com as disponibilidades nos grupos
                        if line_avaliable_groups["avaliable"] > 0: # Se o grupo iterada for maior que 0, é por que tem espaço
                            stamp_line_new_care_ora_mv.update(sponsor = line_avaliable_groups["name"]) 
                            ''' Atribuir grupo aos novos atendimento do MV '''
                            line_avaliable_groups.update(avaliable = line_avaliable_groups["avaliable"] -1) 
                            ''' Decrementar a disponibilidade aos grupos do FORTIGATE '''
                            new_dict_stamp_new_care_mv.append(stamp_line_new_care_ora_mv) 
                            '''Atualizar Lista com os novos atendimentos para o FORTIGATE'''
                            _new_care_ora_mv_with_group = True    
                            _avaliable = True
                            break
                        else:
                            bash_view.print_header(f"NÃO HÁ DISPONIBLIDADE PARA O GRUPO {line_avaliable_groups["name"]} RECEBER O ATENDIMENTO", stamp_line_new_care_ora_mv)  

                bash_view.print_header(f"TOTAL DE ATRIBUIÇÃO DE GRUPOS AOS NOVOS ATENDIMENTOS {len(new_dict_stamp_new_care_mv)}") # , filter_new_care_ora_mv
                bash_view.print_header(f"TOTAL DE DISPONIBILIDADE DOS GRUPOS APÓS ATRIBUIÇÃO DOS ATENDIMENTOS", avaliable_groups)       
                # output_file.file_update("new_dict_stamp_new_care_mv",f"ORACLE MV POSSUI ({len(new_dict_stamp_new_care_mv)}) ATENDIMENTOS ATIVOS!",new_dict_stamp_new_care_mv)

            else: # ### try:
                bash_view.print_header(f"NÃO EXISTE NOVOS ATENDIMENTOS VIEW-MV - ORACLE {len(cod_new_care_ora_mv)}") # , cod_new_care_ora_mv

        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO ATRIBUINDO GRUPOS  E CARIMBANDO CAMPOS AOS NOVOS ATENDIMENTOS DA VIEW-MV  ORACLE", err)
            continue
        # -------------------------------------------------------------------------------------------------------
        # 5º ==> INICIANDO PROCESSO DE NOVOS ATENDIMENTOS COM GRUPOS DO FORTIGATE ===========
        #  GRAVAR NO MYSQL / CASO GRAVOU NO FORTIGATE E NÃO GRAVOU NO SQL
        # -------------------------------------------------------------------------------------------------------
        try:
            if len(new_dict_stamp_new_care_mv) > 0:

                # -------------------------------------------------------------------------------------------------------
                # # INICIANDO O PROCESSO SE EXISTIR NO FORTIGATE GRAVAR NA CARE_MV - SQL  ===============================
                # -------------------------------------------------------------------------------------------------------
                linha = 0
                ### for linha :
                #### para cada linha 
                bash_view.print_header(f" 5º - INICIANDO PROCESSO DE NOVOS ATENDIMENTOS COM GRUPOS DO FORTIGATE")
                for line_filter_new_care_ora_mv in new_dict_stamp_new_care_mv: ### FOR LINHA  :  #### para cada linha
                    _continue = False
                    linha += 1
                    ###### Supondo que exista uma situação de erro e que gravou no fortigati e nao conseguiu desfazer:
                    ####### Fazer A PROCURA no dicionário obtido do FORTIGATE para saber se existe e está ativo:
                    # print(f" process - Linha 273 {line_filter_new_care_ora_mv}")
                    do_search_new_care = action_controller.next_dict_in_list(vouchers_mv_in_forti,'user-id', line_filter_new_care_ora_mv)
                    # print(f"\n {do_search_new_care}")
                    # TRY:
                    if "not_found" not in do_search_new_care: 
                            bash_view.print_header("JÁ EXISITE NO FORTIGATE. Vamos inserir apenas no SQL!", do_search_new_care)   
                        # try: # grava na care_mv
                            create_do_search = care_sql_int_controller.insert_line_care_ora_in_sql_int(do_search_new_care)
                            # print(f" Retorno do CREATE no SQL CARE_MV - filter_new_care_ora_mv -- process - Linha 159 ==> \n{do_search_new_care}")
                            for line_create in create_do_search: 
                                # print(f" Retorno do CREATE no SQL CARE_MV - filter_new_care_ora_mv -- process - Linha 151 ==> \n{line_create}")
                                if line_create["status"] != "success": # EXCEPT:    Manda email
                                    bash_view.print_header("ERROR: NãO FOI POSSÍVEL INSERIR NO SQL, MAS, EXISTE NO FORTIGATE!", line_create)
                                else:
                                    bash_view.print_header(f"GRAVANDO NO CARE_MV - SQL, pois já existe NO FORTIGATE ", line_create)
                            _continue = True
                    else: 
                        bash_view.print_header(f"ATENDIMENTO NÃO EXISTE NO FORTIGATE - {line_filter_new_care_ora_mv['CD_ATENDIMENTO']} - sponsor {line_filter_new_care_ora_mv['sponsor']}")
                        _continue = False
                    if _continue: # VAI PARA O PRÓXIMO REGISTRO
                        continue
                    # -------------------------------------------------------------------------------------------------------
                    # # INICIANDO O PROCESSO DE GRAVAR NO FORTIGATE NOVOS ATENDIMENTOS  ===================================
                    # -------------------------------------------------------------------------------------------------------
                    _continue = False # Novo valor
                    ### monta o json
                    #### post da linha para o fortigate
                    return_post_line_ora = restapi_forti_controller.post_line_ora_mv_in_forti(line_filter_new_care_ora_mv)
                    for line_dict in return_post_line_ora: 
                        if line_dict["http_status"]  != 200:
                            #### manda email explicando
                            ##### break
                            if line_dict["http_status"] == 500:
                                bash_view.print_header(f"process 273 - NÃO FOI PERMITIDO GRAVAR NO FORTIGATE (500) : Linha: {linha}  => {line_dict['name']} - status: {line_dict['status_message']}") #, line_filter_new_care_ora_mv
                                _continue = True
                            else:    
                                bash_view.print_header(f"ERROR: process - 300 - NÃO FOI POSSÍVEL INSERIR NO FORTIGATE o Atendimento : {linha}", line_dict)
                            _continue = True
                            # output_file.file_update("err_post_fortigate",f" NÃO FOI POSSÍVEL GRAVAR NO FORTIGATE!",line_dict)
                        else:
                            bash_view.print_header(f"ATENDIMENTO INSERIDO NO FORTIGATE: {line_dict['CD_ATENDIMENTO']}") # , line_dict
                            _continue = False
                    # ----------------------------------------------------------------------
                    if _continue: # VAI PARA O PRÓXIMO REGISTRO
                        continue
                    # -------------------------------------------------------------------------------------------------------
                    # # INICIANDO O PROCESSO DE GRAVAR NA CARE_MV - MYSQL  E REMOVER FORTIGATE CASO ERRO SQL =============
                    # -------------------------------------------------------------------------------------------------------
                    ### grava na care_mv
                    for line_dict in return_post_line_ora:
                        # print(line_dict)
                        create_atendime_from_return_post = care_sql_int_controller.insert_line_care_ora_in_sql_int(line_dict)
                        for line_create in create_atendime_from_return_post:
                            if line_create["status"] != "success":
                                ## try:
                                ### remove do fortigate
                                bash_view.print_header("NÁO FOI POSSÍVEL INSERIR NO - CARE_MV - SQL!", line_create)
                                dict_return_delete = restapi_forti_controller.delete_line_guest_in_group_forti(line_dict)
                                for return_line in dict_return_delete:
                                    if return_line["http_status"] == 200:
                                        bash_view.print_header(f"ATENDIMENTO REMOVIDO DO FORTIGATE: {line_dict['CD_ATENDIMENTO']}")
                                    else:
                                        # except:
                                        ## manda email
                                        bash_view.print_header("ERRO AO TENTAR REMOVER O ATENDIMENTO DO FORTIGATE:", return_line)
                            else:
                                bash_view.print_header(f"ATENDIMENTO INSERIDO NA CARE_MV - SQL: {line_dict['CD_ATENDIMENTO']}") # line_create
                            # finaly:
                            ## close
            else:
                bash_view.print_header(f"ERROR: BLOCO 5 NÃO EXISTE GRUPO COM DISPONIBILIDADE PARA RECEBER OS NOVOS ATENDIMENTOS DO MV", avaliable_groups)    
                    
        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO DE GRAVAR NA CARE_MV - MYSQL  E REMOVER FORTIGATE CASO ERRO SQL", err)
            continue
        # =======================================================================================================
        # 7º ==> INICIANDO O PROCESSO DE ANTIGOS ATENDIMENTOS na CARE_MV =======================================|
        # -------------------------------------------------------------------------------------------------------
        try: # ANTIGOS ATENDIMENTOS (COM ALTA) NO CARE_MV!
            bash_view.print_header(f"INÍCIO DO BLOCO ANTIGOS ATENDIMENTOS (COM ALTA) que existe no CARE_MV")
            if len(decreased_care_mv_sql) > 0: # ### try: 
                # Usar a lista de códigos novos do CARE-MV e selecionar REGISTROS no dicionário passado
                filter_decreased_care_mv_sql = action_controller.search_key_in_dict_insert_key_return_new_dict('cd_atendimento', decreased_care_mv_sql, care_sql_mv)
                # bash_view.print_header(f"QUAIS LINHAS ESTÃO NO CARE_MV-SQL E NÃO ESTÃO NO ORACLE-MV ==> ( COM ALTA ) A SEREM REMOVIDOS DO FORTIGATE >> <== TOTAL ==> {len(filter_decreased_care_mv_sql)}", decreased_care_mv_sql)
                linha = 0
                ### for linha :
                #### para cada linha 
                for Line_filter_decreased_care_mv_sql in filter_decreased_care_mv_sql: ### FOR LINHA  :  #### para cada linha
                    # print(f"\n process - Dentro do for - 326 - linha com atendimentos antigo no sql para remover  \n {Line_filter_decreased_care_mv_sql}\n")
                    _continue = False
                    linha += 1
                    ##### Atendimentos que receberam alta ou não foram removidos por algum erro.
                    ###### faz o get pra saber se existe e está ativo:
                    do_search_decreased = restapi_forti_controller.get_atendime_sql_filter_key_rest_forti(Line_filter_decreased_care_mv_sql, "user-id", "==", None, "user-id")
                    for do_search_line in do_search_decreased: # # Iterar dentro da lista de retorno da pesquisa:
                        if do_search_line["status"] == "success" and do_search_line["itera_fortigate"] == 'IN.FORTIGATE':
                            bash_view.print_header(f"O {Line_filter_decreased_care_mv_sql["user-id"]}  JÁ EXISITE NO FORTIGATE. Vamos 1º remover do FORTIGATE!") # , do_search_line 
                            
                            ## remove do fortigati 
                            dict_return_delete = restapi_forti_controller.delete_line_guest_in_group_forti(do_search_line)
                            for return_line in dict_return_delete: # Se <> 200:  ## manda email explicando
                                if return_line["http_status"] != 200: # EXCEPT:    Manda email
                                    bash_view.print_header(f"ERROR: NãO FOI POSSÍVEL REMOVER DO FORTIGATE: {Line_filter_decreased_care_mv_sql["user-id"]}", return_line)
                                    _continue = True
                                else:
                                    bash_view.print_header(f"ATENDIMENTO REMOVIDO DO FORTIGATE: {Line_filter_decreased_care_mv_sql["user-id"]}") # , return_line  
                                    _continue=False
                        elif do_search_line["status"] == "success" and do_search_line["itera_fortigate"] == "NOT.FORTIGATE":
                            bash_view.print_header(f"O ATENDIMENTO - {Line_filter_decreased_care_mv_sql["user-id"]} - NÃO EXISTE NO FORTIGATE!", do_search_line["status_message"])
                            _continue=False
                        else: # except:	### manda email
                            bash_view.print_header("ERROR: HOUVE UM ERRO AO TENTAR CONSULTAR O FORTIGATE") # , do_search_line
                            _continue = True
                            
                    if _continue: # VAI PARA O PRÓXIMO REGISTRO
                        continue
                    # ------------------------------------------------------------------------------------------
                    ##try:
                    _continue = False # Novo valor
                    delete_care_mv = care_sql_int_controller.delete_return_delete_forti_for_sql_int(Line_filter_decreased_care_mv_sql)
                    for delete_line in delete_care_mv:
                        if delete_line["status"] != "success": # remove da care_mv 
                            bash_view.print_header(f"NÁO FOI POSSÍVEL REMOVER NA CARE_MV - SQL! - {Line_filter_decreased_care_mv_sql["user-id"]}", delete_line)
                        else:
                            bash_view.print_header(f"REMOÇÃO BEM SUCEDIDA - CARE_MV - SQL! - {Line_filter_decreased_care_mv_sql["user-id"]}", delete_line)
        except Exception as err:
            bash_view.print_header(f"ERROR: ERRO DO BLOCO DE ANTIGOS ATENDIMENTOS na CARE_MV", err)
            continue

        try: 
            if _care and _fortigate:
                ### DIFERENCIAÇÃO: EXISTE NO FORTIGATE E NÃO EXISTE NA CARE_MV - SQL - MAS NÃO EXISTE NO FORTIGATE (Faz a diferença entre conjuntos)
                difference_fortigate_care_mv = set_column_controller.sets_difference_a_b(user_id_in_fortigate_int, cd_atendimento_in_care_mv_dict)
                bash_view.print_header(f"ERRO SQL: SÓ EXISTE NO FORTIGATE E NÃO EXISTE NA NA CARE_MV <== TOTAL ==> {len(difference_fortigate_care_mv)}")
                # output_file.file_update("total_records",f"ERRO SQL: SÓ EXISTE NO FORTIGATE E NÃO EXISTE NA NA CARE_MV <== TOTAL ==> ({len(difference_fortigate_care_mv)}) -")

            # -------------------------------------------------------------------------------------------------------
            # ==========================  LIMPANDO A MEMÓRIA DE GRANDES VOLUMES  ===================================|
            # -------------------------------------------------------------------------------------------------------   
            care_sql_mv.clear() # lista todos atendimentos mysql
            return_care_ora_mv.clear() # Lista todos atendimentos oracle
            _vouchers_in_forti.clear()
            vouchers_mv_in_forti.clear() # Todos os vouchers fortigate
            filter_new_care_ora_mv.clear()
            new_dict_stamp_new_care_mv.clear()
            cd_atendimento_ora_value_list_dict.clear()
            cd_atendimento_in_care_mv_dict.clear()
            user_id_in_fortigate.clear()
            user_id_in_fortigate_int.clear()
            cod_new_care_ora_mv.clear()
            decreased_care_mv_sql.clear()
            intersection_care_ora_mv.clear()
            difference_fortigate_care_mv.clear()

        except Exception as err:
            bash_view.print_header(f"ERROR: ERRO DO BLOCO DE ANTIGOS ATENDIMENTOS na CARE_MV", err)
            continue    

        # -------------------------------------------------------------------------------------------------------
        # ==========================  GERENCIAMENTO DE VISITANTES  =============================================|
        # -------------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------
        # 8º ==> LISTAR E REMOVER OS REGISTROS DOS VISITANTES EXPIRADOS NO FORTIGATE: ==========================|
        # -------------------------------------------------------------------------------------------------------        
        try:
            if _fortigate:
                # 
                _visitor_fortigate_expiration = False
                # -----------------------------------------------------------------------------------------------------
                ####### Gerar VARIÁVEIS AUXILADORAS NA FORMAÇÃO DOS GRUPOS VISITANTES
                # -----------------------------------------------------------------------------------------------------
                name_groups_visitor = [] # Lista com nome dos grupos
                _name_key = "expiration" # campo para consultar tempo expiração
                _date_now = datetime.now()
                # _date_now = '1'
                # -----------------------------------------------------------------------------------------------------
                ####### Iniciando processos de formação dos grupos
                # -----------------------------------------------------------------------------------------------------
                bash_view.print_header(f"LISTAR TODOS OS REGISTROS DOS GRUPOS VISITANTES EXPIRADOS NO FORTIGATE")
                _filter_param =f"{_name_key}<={_date_now}" 
                forti_groups = action_controller.select_forti_groups_type("n") # Lista de todos os GRUPOS do tipo MV
                for line_forti_group in forti_groups:
                    if line_forti_group["sn_mv"] == "n": # Grupos do tipo não MV
                        name_groups_visitor.append(line_forti_group["name"]) # CRIA LISTA com nomes dos GRUPOS DO TIPO PASSADO
                # -----------------------------------------------------------------------------------------------------
                ####### Fazer A PROCURA no dicionário obtido do FORTIGATE para saber se existe EXPIRADOS e está ativo:
                all_visitor_expiration_in_groups = restapi_forti_controller.get_all_guest_groups_filter_rest_forti(name_groups_visitor, _filter_param)
                
                if len(all_visitor_expiration_in_groups) > 0:
                    bash_view.print_header(f"REGISTROS EXPIRADOS ENCONTRADOS NO FORTIGATE - ( {len(all_visitor_expiration_in_groups)} )")
                    # bash_view.print_list_dict_by_pretty_table(all_visitor_expiration_in_groups)
                    _visitor_fortigate_expiration = True
                else:
                    bash_view.print_header("NÃO HÁ VISITANTES EXPIRADOS NO FORTIGATE")
                    _visitor_fortigate_expiration = False
                # -----------------------------------------------------------------------------------------------------         
                # REMOVER VISITANTES EXPIRADOS no FORTIGATE e SQL - VISITOR
                # -----------------------------------------------------------------------------------------------------
                if _visitor_fortigate_expiration:
                    for dict_line in all_visitor_expiration_in_groups:
                        # print(dict_line)
                        _continue = False
                        _delete_line_visitor_sql = False
                        exist_line_visitor_sql = visitor_sql_int_controller.select_filter_cd_atendimento_in_visitor_dic(dict_line, "contingency", "`user-id`", "=", "str", "user-id")
                        # print(f"\n process linha 491 - {exist_line_visitor_sql}")
                        if len(exist_line_visitor_sql) > 0:
                            for exist_line_visitor in exist_line_visitor_sql:
                                if "status" in exist_line_visitor:
                                    if exist_line_visitor["status"] == "error":
                                            bash_view.print_header(f"ERRO AO CONSULTAR O VISITANTE EXPIRADO NO VISITOR-SQL!")
                                            bash_view.print_list_dict_by_pretty_table(dict_line)
                                            _delete_line_visitor_sql = False
                                            _continue = True
                                            break
                                    else:
                                        bash_view.print_header(f"VISITANTE EXPIRADO ENCONTRADO NO VISITOR-SQL ==>  user-id: {exist_line_visitor['user-id']}, grupo: {exist_line_visitor['sponsor']}  ")
                                        _delete_line_visitor_sql = True
                                        break
                        else:
                            bash_view.print_header(f"VISITANTE EXPIRADO NÃO ENCONTRADO NO VISITOR-SQL ==> {dict_line["user-id"]}")
                            _delete_line_visitor_sql = False
                        # -----------------------------------------------------------------------------------------------------                            
                        # REMOVENDO LINHA DE VISITANTE NO SQL -----------------------------------------------------------------
                        # -----------------------------------------------------------------------------------------------------
                        if _delete_line_visitor_sql:                    
                            delete_expiration_visitor = visitor_sql_int_controller.delete_expiration_visitor_sql_int(dict_line)
                            for delete_expiration_line in delete_expiration_visitor:
                                if delete_expiration_line["status"] == "error":
                                    bash_view.print_header(f"NÁO FOI POSSÍVEL REMOVER O VISITANTE EXPIRADO NO SQL! {dict_line["user-id"]}")
                                    _continue = True
                                    break
                                else:
                                    bash_view.print_header(f"REMOÇÃO DO VISITANTE EXPIRADO NO SQL - BEM SUCEDIDA! {dict_line["user-id"]}", )
                                    _continue = False
                                    break
                        if _continue:
                            continue
                        # -----------------------------------------------------------------------------------------------------
                        # REMOVENDO LINHA DE VISITANTE NO RESTAPI -------------------------------------------------------------
                        # -----------------------------------------------------------------------------------------------------                        
                        delete_visitor_in_group_rest_forti = restapi_forti_controller.delete_expiration_in_rest_forti(dict_line)
                        for delete_line in delete_visitor_in_group_rest_forti:
                            if delete_line["itera_fortigate"] != "REMOVED":
                                bash_view.print_header("NÃO FOI POSSÍVEL REMOVER NO FORTIGATE", delete_line)
                                delete_line.update(itera_fortigate = 'SUBMIT')
                                _continue = True
                                break
                            else:
                                bash_view.print_header(f"VISITANTE EXPIRADO REMOVIDO DO FORTIGATE {delete_line['user-id']}")
                                _continue = False
                                break
            else:
                bash_view.print_header(f"NÃO HÁ VOUCHERS EXPIRADOS NOS GRUPOS DE VISITANTES NO FORTIGATE",  all_visitor_expiration_in_groups)
                _fortigate = True
        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO REMOVER VISITANTES EXPIRADOS no FORTIGATE!", err )            
            continue

        # ======================================================================================================================
        # NOVAS ROTINAS
        # ======================================================================================================================
        # ----------------------------------------------------------------------------------------------------------------------
        # 9º ==> CONSULTANDO TODOS OS GRUPOS VISITANTES COM SEUS REGISTROS NO FORTIGATE: ======================================|
        # ---------------------------------------------------------------------------------------------------------------------        
        try:
            _vouchers_in_forti = restapi_forti_controller.get_all_groups_from_rest_forti()
            if _vouchers_in_forti["status"]	== "success":
                if len(_vouchers_in_forti["results"]) > 0: # Existe pelo menos 1 grupo criado
                    # 
                    #
                    _range_group = 500 # Tamanho Total de registros por grupo
                    _total_groups_visitors= 0 
                    _len_groups = 0 # Range Total de registros em todos os grupos disponíveis
                    avaliable_groups = [] # Lista com dicionários dos grupos e sua Disponibilidade
                    avaliable_groups_total_free = 0 # Variável com totalizador de grupos com Disponibilidade para receber registros
                    visitors_vouchers_in_forti = [] # Lista dos atendimentos no Fortigate
                    _vouchers_guest = []
                    groups_total_used = 0
                    forti_groups = action_controller.select_forti_groups_type("n") # Lista de todos os GRUPOS do tipo VISITORS
                    if len(forti_groups) > 0: # Consulta Geral no fortigate com todos os grupos
                        for line_forti_group in forti_groups:
                            _total_groups_visitors +=1 # Incremente total de grupos
                            _len_groups = _total_groups_visitors * _range_group # Gera total de registros possíveis para o fortigate
                            #
                            for group_guest in _vouchers_in_forti["results"]: # Navegar dentro da consulta Geral a procura da chave results
                                    if line_forti_group["name"] == group_guest["name"]: # em result tem um grupo com o mesmo nome da tabela de grupos
                                        # Dicionário com nome e disponibilidade ------------------------------------------------------------------
                                        dict_line_group = {}
                                        dict_line_group.update(name = group_guest["name"]) # Atualizando um novo dicionário com o nome do grupo
                                        # Total de vouchers neste grupo
                                        _length = len(group_guest["guest"]) # Chave guest Dentro da consulta Geral, Total de registros
                                        groups_total_used += _length
                                        dict_line_group.update(avaliable = _range_group - _length) # Total de disponibilidade para novos registros
                                        # ---------------------------------------------------------------------------------------------------------
                                        avaliable_groups.append(dict_line_group) # Atualiza Lista com dicionário dict_line_group  
                                        if dict_line_group["avaliable"] > 0: # se o grupo tiver disponibilidade?
                                            avaliable_groups_total_free += 1 # Incrementar variável
                                        # Se total do grupo for maior que 0 é porque temos registros dentro do grupo
                                        if _length > 0:
                                            del _vouchers_guest[:]
                                            _vouchers_guest = action_controller.stamp_list_dict_for_sponsor(group_guest["guest"], group_guest["name"])
                                            visitors_vouchers_in_forti.extend(_vouchers_guest) 
                        bash_view.print_header(f"TOTAL DE GRUPOS COM DISPONIBILIDADE PARA INSERIR VISITANTES NO FORTIGATE {avaliable_groups_total_free}", avaliable_groups)
                        bash_view.print_header(f"TOTAL DE VOUCHERS AVULSOS EXISTENTES NO FORTIGATE (total nos grupos {groups_total_used}) ( total no Dicionário final:  ({len(visitors_vouchers_in_forti)})")
                        # output_file.file_update("total_records",f"TOTAL DE VOUCHERS AVULSOS EXISTENTES NO FORTIGATE   - ({len(visitors_vouchers_in_forti)})")
                        # output_file.file_update_insert_table("total_records",f"DISPONIBILIDADE DOS GRUPOS NO FORTIGATE ({avaliable_groups_total_free}) -", avaliable_groups)
                        if len(visitors_vouchers_in_forti) < _len_groups:
                            _fortigate = True
                            bash_view.print_header(f"HÁ NECESSIDADE DE GERAR NOVOS VOUCHERS! TOTAL NOS GRUPOS: {_len_groups - len(visitors_vouchers_in_forti)}, TOTAL DISPONÍVEL {_len_groups}" )
                        else:
                            _fortigate = False
                            bash_view.print_header(f" TODOS OS GRUPOS DE VOUCHES ESTÃO COMPLETOS! NÃO HÁ NECESSIDADE DE GERAR NOVOS VOUCHERS!")
                    else:
                        bash_view.print_header(f"ERROR: BLOCO 9 - NÃO HÁ GRUPOS COM ESTE TIPO NO ARQUIVO JSON")
                        continue    
                else:
                    bash_view.print_header(f"ERROR: BLOCO 9 - NÃO HÁ GRUPOS NO FORTIGATE - Total 0")
                    _fortigate = False
                    continue
            else:
                bash_view.print_header(f"ERROR: BLOCO 9 - AO CONSULTAR O FORTIGATE! ",  _vouchers_in_forti)
                # output_file.file_update("error_from_process",f"ERROR: AO CONSULTAR O FORTIGATE! - BLOCO 9",  _vouchers_in_forti)
                continue
        except Exception as err:
            # ENVIAR E-MAIL
            bash_view.print_header(f"ERROR: ERRO DO BLOCO 9 GRUPOS FORTIGATE", err)
            # output_file.file_update("error_from_process",f"EXCEPT ERROR: BLOCO 9 - GRUPOS FORTIGATE", err)
            continue


        # ---------------------------------------------------------------------------------------------------------------------
        # 10º ==> GERANDO UM RANGE DE VOUCHES COM SENHAS ALEATÓRIAS PARA SER USADA NO FORTIGATE SEM OS GRUPOS ================|
        # ---------------------------------------------------------------------------------------------------------------------   
        if _fortigate:
            
            total_users = _len_groups
            _status_insert = 'SUBMIT'
            init_interval = 1
            end_interval = total_users
            expiration = 28800
            generator_visitor = action_controller.generate_range_voucher(_status_insert, init_interval, end_interval, expiration)
            # bash_view.print_list_dict_by_pretty_table(generator_visitor)

            # -------------------------------------------------------------------------------------------------------
            ## 11º ==> CONSULTAR  TODOS OS VISITANTES  NO MYSQL  =======================================================|
            # -------------------------------------------------------------------------------------------------------        
            try: # BLOCO DE CONSULTA SQL - VISITANTES ")
                _visitor_sql = False
                select_visitor_sql_user_id = visitor_sql_int_controller.select_user_id_sql_int_dic()
                if len(select_visitor_sql_user_id) > 0:
                    for visitor_line in select_visitor_sql_user_id:
                        if "status" in visitor_line:
                            if visitor_line["status"] == "error":
                                bash_view.print_header("ERROR: NÃO FOI POSSÍVEL CONSULTAR OS VISITANTES - SQL")
                                bash_view.print_list_dict_by_pretty_table(select_visitor_sql_user_id)
                                _visitor_sql = False
                                break
                            else:
                                bash_view.print_header(f"VISITOR - SQL TEM ({len(select_visitor_sql_user_id)}) VOUCHERS CADASTRADOS ")
                                _visitor_sql = True
                                break
                else:
                    bash_view.print_header("NÃO POSSUI VISITANTES")
                    _visitor_sql = True
                    
            except Exception as err:
                bash_view.print_header(f"ERROR: ERRO DO BLOCO DE CONSULTA AO SQL - VISITANTES", err)
                continue

            # _visitor_sql:
                
            # -------------------------------------------------------------------------------------------------------------------------------------
            #### EXTRAÇÃO DOS VALORES DE UMA CHAVE NOS DICIONÁRIOS ABAIXO: (CÓDIGO ATENDIMENTO OU USER-ID)
            # -------------------------------------------------------------------------------------------------------------------------------------
            #### Extrai do DICIONÁRIO GENERATOR_VISITOR, valores DA CHAVE user_id
            user_id_generator_visitor_dict = action_controller.value_column_list_dict(generator_visitor, 'user_id')
            bash_view.print_header(f"LISTA DOS CÓDIGOS GERADOS PARA O FORTIGATE {len(user_id_generator_visitor_dict)}")
            # output_file.file_update("total_records",f"TOTAL DE CD_ATENDIMENTO EXTRAÍDOS DO DICIONÁRIO VIEW-MV - ORACLE ({len(generator_visitor)}) -")

            #### Extrai do DICIONÁRIO SELECT_VISITOR_SQL, registros da coluna user-id
            user_id_visitor_sql_dict = action_controller.value_column_list_dict(select_visitor_sql_user_id, 'user-id')
            bash_view.print_header(f"LISTA DOS CÓDIGOS EXISTENTES NO VISITOR-SQL {len(user_id_visitor_sql_dict)}")
            # output_file.file_update("total_records",f"TOTAL DE CD_ATENDIMENTO EXTRAÍDOS DO DICIONÁRIO VIEW-MV - ORACLE ({len(generator_visitor)}) -")

            # -------------------------------------------------------------------------------------------------------------------------------------
            #### TRABALHAR COM CONJUNTOS
            # -------------------------------------------------------------------------------------------------------------------------------------
            
            ### DIFERENCIAÇÃO:  SÓ EXISTE GENERATOR - VISITANTES  - (Faz a diferença entre conjuntos)
            cod_new_visitors_fortigate = set_column_controller.sets_difference_a_b(user_id_generator_visitor_dict, user_id_visitor_sql_dict)
            bash_view.print_header(f"NOVOS VOUCHERS GERADOS PARA OS VISITANTES <== TOTAL ==> {len(cod_new_visitors_fortigate)}") # , cod_new_care_ora_mv
            # output_file.file_update("total_records",f"NOVOS ATENDIMENTOS ESTÃO NA VIEW-MV - ORACLE E NÃO ESTÃO NO CARE_MV - SQL <== TOTAL ==> ({len(cod_new_care_ora_mv)}) -")

            try: # NOVOS ATENDIMENTOS VISITANTES PARA O FORTIGATE
                if len(cod_new_visitors_fortigate) > 0: # ### try:
                    # Usar a lista de códigos novos do visitors e seleciona as linhas para inserir no fortigate
                    filter_new_visitors_fortigate = action_controller.search_key_in_dict_insert_key_return_new_dict('user-id', cod_new_visitors_fortigate, generator_visitor)
                    bash_view.print_header(f"AGRUPANDO AS LINHAS QUE ESTÃO NA LISTA NOVOS VOUCHERS GERADOS ({len(filter_new_visitors_fortigate)})")
                    # =======================================================
                    # try: VAMOS atribuir os grupos aos novos atendimento do MV
                    new_dict_stamp_new_visitors_fortigate = []
                    _avaliable = False
                    for line_new_visitors_fortigate in filter_new_visitors_fortigate:
                        stamp_line_new_care_ora_mv = line_new_visitors_fortigate # action_controller.stamp_dict_ora_mv_to_guest_forti(line_new_visitors_fortigate) # CARIMBANDO OS ATENDIMENTOS
                        for line_avaliable_groups in avaliable_groups: # Iterar no no grupo criado com disponibilidade dos grupos
                            if line_avaliable_groups["avaliable"] > 0: # Se o grupo iterada for maior que 0, é por que tem espaço
                                stamp_line_new_care_ora_mv.update(sponsor = line_avaliable_groups["name"]) # Atribui a linha a chave sponsor com valor do grupo
                                stamp_line_new_care_ora_mv.update(comment = datetime.now().strftime('%d-%m-%Y %H:%m'))
                                line_avaliable_groups.update(avaliable = line_avaliable_groups["avaliable"] -1) # decrementa a disponibilidade 
                                _avaliable = True
                                break
                            # else:
                            #     _avaliable = False
                            
                        if not _avaliable:
                            bash_view.print_header(f"NÃO HÁ DISPONIBLIDADE DE GRUPO PARA O ATENDIMENTO", line_new_visitors_fortigate)   
                        
                        new_dict_stamp_new_visitors_fortigate.append(stamp_line_new_care_ora_mv) # ATENDIMENTOS CARIMBADOS PARA SEREM INSERIDOS NO FORTIGATE           
                        ############################# line_new_care_ora_mv.update(sponsor = line_avaliable_groups["name"]) # Atribui a linha a chave sponsor com valor do grupo
                    bash_view.print_header(f"TOTAL DE ATRIBUIÇÃO DE GRUPOS AOS NOVOS ATENDIMENTOS {len(new_dict_stamp_new_visitors_fortigate)}") # , filter_new_care_ora_mv
                    bash_view.print_header(f"TOTAL DE DISPONIBILIDADE DOS GRUPOS APÓS ATRIBUIÇÃO DOS ATENDIMENTOS", avaliable_groups)
            
                        # output_file.file_update("new_dict_stamp_new_visitors_fortigate",f"ORACLE MV POSSUI ({len(new_dict_stamp_new_visitors_fortigate)}) ATENDIMENTOS ATIVOS!",new_dict_stamp_new_visitors_fortigate)
            except Exception as err:
                # ENVIAR E-MAIL
                bash_view.print_header(f"ERROR: ERRO DO BLOCO NOVOS ATENDIMENTOS VISITANTES PARA O FORTIGATE", err)
                continue

    ########################## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ########################## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            # -------------------------------------------------------------------------------------------------------
            # 6º ==> INICIANDO PROCESSO DE GRAVAR NO MYSQL / CASO GRAVOU NO FORTIGATE E NÃO GRAVOU NO SQL ===========
            # -------------------------------------------------------------------------------------------------------
            try:
            # -------------------------------------------------------------------------------------------------------
            # # INICIANDO O PROCESSO SE EXISTIR NO FORTIGATE GRAVAR NA CARE_MV - SQL  ===============================
            # -------------------------------------------------------------------------------------------------------
                # print(f"process - Linha 679 {new_dict_stamp_new_visitors_fortigate}")
                if _avaliable and len(cod_new_visitors_fortigate) > 0:  # antiga validação len(cod_new_visitors_fortigate)
                    linha = 0
                    ### for linha :
                    #### para cada linha 
                    bash_view.print_header(f"INICIANDO O PROCESSO DE ITERAÇÃO NA LISTA DE NOVOS ATENDIMENTOS MV")
                    for line_filter_new_visitors_fortigate in new_dict_stamp_new_visitors_fortigate: ### FOR LINHA  :  #### para cada linha
                        _continue = False
                        linha += 1
                        ###### Supondo que exista uma situação de erro e que gravou no fortigati e nao conseguiu desfazer:
                        ####### Fazer A PROCURA no dicionário obtido do FORTIGATE para saber se existe e está ativo:
                        ####### Caso exista remove, porque no sql não tem informação para disponibilizar ao visitante
                        do_search_new_visitors = action_controller.next_dict_in_list(visitors_vouchers_in_forti,'user-id', line_filter_new_visitors_fortigate)
                        # print(f"\n {do_search_new_care}")
                        # TRY:
                        if "not_found" not in do_search_new_visitors: 
                            bash_view.print_header("JÁ EXISITE NO FORTIGATE. Vamos inserir apenas no SQL!", do_search_new_visitors)
                            # -----------------------------------------------------------------------------------------------------
                            # REMOVENDO LINHA DE VISITANTE NO FORTIGATE -----------------------------------------------------------
                            # -----------------------------------------------------------------------------------------------------                        
                            delete_visitor_in_group_rest_forti = restapi_forti_controller.delete_expiration_in_rest_forti(do_search_new_visitors)
                            for delete_line in delete_visitor_in_group_rest_forti:
                                if delete_line["itera_fortigate"] != "REMOVED":
                                    bash_view.print_header("NÃO FOI POSSÍVEL REMOVER NO FORTIGATE", delete_line)
                                    # delete_line.update(itera_fortigate = 'SUBMIT')
                                    _continue = True
                                    break
                                else:
                                    bash_view.print_header(f"VISITANTE EXPIRADO REMOVIDO DO FORTIGATE {delete_line['user-id']}")
                                    _continue = False
                                    break    
                        else: 
                            bash_view.print_header(f"ATENDIMENTO NÃO EXISTE NO FORTIGATE - {line_filter_new_visitors_fortigate['user-id']} - sponsor {line_filter_new_visitors_fortigate['sponsor']}")
                            _continue = False
                            
                        if _continue: # VAI PARA O PRÓXIMO REGISTRO
                            continue
                        # -------------------------------------------------------------------------------------------------------
                        # # INICIANDO O PROCESSO DE GRAVAR NO FORTIGATE NOVOS ATENDIMENTOS  ===================================
                        # -------------------------------------------------------------------------------------------------------
                        _continue = False # Novo valor
                        ### monta o json
                        #### post da linha para o fortigate
                        return_post_line_visitor = restapi_forti_controller.post_line_visitor_in_forti(line_filter_new_visitors_fortigate)
                        for line_dict in return_post_line_visitor: 
                            if line_dict["http_status"]  != 200:
                                #### manda email explicando
                                ##### break
                                if line_dict["http_status"] == 500:
                                    bash_view.print_header(f"process 273 - NÃO FOI PERMITIDO GRAVAR NO FORTIGATE (500) : Linha: {linha}  => {line_dict['name']} - status: {line_dict['status_message']}") #, line_filter_new_visitors_fortigate
                                    _continue = True
                                else:    
                                    bash_view.print_header(f"ERROR: process - 300 - NÃO FOI POSSÍVEL INSERIR NO FORTIGATE o Atendimento : {linha}", line_dict)
                                _continue = True
                                # output_file.file_update("err_post_fortigate",f" NÃO FOI POSSÍVEL GRAVAR NO FORTIGATE!",line_dict)
                            else:
                                bash_view.print_header(f"VOUCHER AVULSO INSERIDO NO FORTIGATE: {line_dict['user-id']}") # , line_dict
                                _continue = False
                        # ----------------------------------------------------------------------
                        if _continue: # VAI PARA O PRÓXIMO REGISTRO
                            continue
                        # -------------------------------------------------------------------------------------------------------
                        # # INICIANDO O PROCESSO DE GRAVAR NO VISITOR - MYSQL  E REMOVER FORTIGATE CASO ERRO SQL =============
                        # -------------------------------------------------------------------------------------------------------
                        ### grava no visitor
                        for line_dict in return_post_line_visitor:
                            # print(line_dict)
                            create_visitor_from_return_post = visitor_sql_int_controller.insert_line_visitor_in_sql_int(line_dict)
                            for line_create in create_visitor_from_return_post:
                                if line_create["status"] != "success":
                                    ## try:
                                    ### remove do fortigate
                                    bash_view.print_header("NÁO FOI POSSÍVEL INSERIR NO - CARE_MV - SQL!", line_create)
                                    dict_return_delete = restapi_forti_controller.delete_line_guest_in_group_forti(line_dict)
                                    for return_line in dict_return_delete:
                                        if return_line["http_status"] == 200:
                                            bash_view.print_header(f"ATENDIMENTO REMOVIDO DO FORTIGATE: {line_dict['user-id']}")
                                        else:
                                            # except:
                                            ## manda email
                                            bash_view.print_header("ERRO AO TENTAR REMOVER O ATENDIMENTO DO FORTIGATE:", dict_return_delete)
                                else:
                                    bash_view.print_header(f"ATENDIMENTO INSERIDO NA CARE_MV - SQL: {line_dict['user-id']}") # line_create
            except Exception as err:
                # ENVIAR E-MAIL
                bash_view.print_header(f"ERROR: ERRO DO BLOCO DE GRAVAR NO VISITOR- MYSQL  E REMOVER FORTIGATE CASO ERRO SQL", err)
                continue


