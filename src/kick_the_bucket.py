from src.view.bash_view import BashView
from src.env import table_in_lists_env # Arquivo de grupos do fortigate
from src.controllers.action_controller import ActionController
from src.controllers.restapi_forti_controller import RestAPIFortiController
from datetime import datetime, timedelta
from pytz import timezone
import time
import os
# time_difference = timedelta(hours=-3)

def start() -> None:
    os.system("cls")
    os.system('clear')
    ## instanciando as classes ==============================================
    ## ----------------------------------------------------------------------
    ### Instânciando View bash_view
    bash_view = BashView()

    ### Instânciando Controller AÇÕES auxiliares
    action_controller = ActionController()
    restapi_forti_controller = RestAPIFortiController()

    time_start = datetime.now()
    _time_sleep = 10


    # -------------------------------------------------------------------------------------------------------
    ## 1º ==> CRIA TODOS OS GRUPOS que pertençam AO PROJETO NO FORTIGATE  ==================================|
    # -------------------------------------------------------------------------------------------------------                
    # try:

        # groups_exist = restapi_forti_controller.post_group_rest_forti()   # AÇÃO ÚNICA AO INICIAR O PROJETO
    #     bash_view.print_list_dict_by_pretty_table(groups_exist)

    # except Exception as err:
    #     # ENVIAR E-MAIL
    #     bash_view.print_header(f"ERROR: AO TENTAR GRAVAR GRUPOS NO FORTIGATE!", err)

    # # -------------------------------------------------------------------------------------------------------
    # ## 2º ==> CONSULTA todos os GRUPOS DO PROJETO NO FORTIGATE  ============================================|
    # # -------------------------------------------------------------------------------------------------------                
    try:
        _list_forti_groups = table_in_lists_env.FORTI_GROUPS
        # _vouchers_in_forti = table_in_lists_env.vouchers
        _vouchers_in_forti = restapi_forti_controller.get_all_groups_from_rest_forti()
        if _vouchers_in_forti["status"]	== "success":
            if len(_vouchers_in_forti["results"]) > 0:
                avaliable_groups = [] # Lista com dicionários dos grupos e sua Disponibilidade
                avaliable_groups_total = 0 # Variável com totalizador de grupos com Disponibilidade para receber registros
                mv_vouchers_in_forti = [] # Lista dos atendimentos no Fortigate
                maximum = 500
                forti_groups = action_controller.select_forti_groups_type("s") # Lista de todos os GRUPOS do tipo MV
                if len(_vouchers_in_forti["results"]) > 0: # Consulta Geral no fortigate com todos os grupos
                    for forti_group in forti_groups:
                        if forti_group["sn_mv"] == "s": # se o grupo pesquisado for do MV
                            for group_guest in _vouchers_in_forti["results"]: # Navegar dentro da consulta Geral a procura da chave results
                                    if forti_group["name"] == group_guest["name"]: # Se o valor da chave name do grupo consultado for igual ao name do grupo em result
                                        line_group = {}
                                        line_group.update(name = group_guest["name"]) # Atualizando um novo dicionário com o nome do grupo
                                        # Total de vouchers neste grupo
                                        _length = len(group_guest["guest"]) # Navegar dentro da consulta Geral a procura da chave guest e contar quantos registros tem
                                        line_group.update(avaliable = maximum - _length) # Total de disponibilidade para novos registros
                                        avaliable_groups.append(line_group) # Atualiza Lista com dicionário line_group  
                                        if line_group["avaliable"] > 0: # se o grupo tiver disponibilidade?
                                            avaliable_groups_total += 1 # Incrementar variável
                                        # Se total do grupo for maior que 0 é porque temos registros dentro do grupo
                                        if _length > 0:
                                            for line_group_guest in group_guest["guest"]: # Captura todos os dicionários dentro do guest para atualizar
                                                mv_vouchers_in_forti.append(line_group_guest) # Lista sendo atualizada com os dicionários encontrados  
                    bash_view.print_header(f"TOTAL DE DISPONIBILIDADE DOS GRUPOS EXISTENTES NO FORTIGATE {avaliable_groups_total}", avaliable_groups)
                    bash_view.print_header(f"VOUCHERS DE ATENDIMENTOS EXISTENTES NO FORTIGATE ({len(mv_vouchers_in_forti)})")
                    _fortigate = True
            else:
                bash_view.print_header(f"ERROR: NÃO HÁ GRUPOS COM DISPONIBILIDADE NO FORTIGATE",  _vouchers_in_forti)
                _fortigate = False
        else:
            bash_view.print_header(f"ERROR: AO CONSULTAR O FORTIGATE! \n AGUARDAR UM TEMPO PARA REINICIAR AS VALIDAÇÕES",  _vouchers_in_forti)

    except Exception as err:
        # ENVIAR E-MAIL
        bash_view.print_header(f"ERROR: ERRO DO BLOCO GRUPOS FORTIGATE", err)

    print(f"\n =========FIM DO BLOCO CONSULTAR =============================================================\n")

    # -----------------------------------------------------------------------------------------------------         
    # 3º ==> REMOVER TODOS OS REGISTROS no FORTIGATE
    # -----------------------------------------------------------------------------------------------------
    # try:
    #     if _fortigate:
    #         for dict_line in mv_vouchers_in_forti:
    #             delete_visitor_in_group_rest_forti = restapi_forti_controller.delete_expiration_in_rest_forti(dict_line)
    #             for delete_line in delete_visitor_in_group_rest_forti:
    #                 if delete_line["itera_fortigate"] != "REMOVED":
    #                     bash_view.print_header("NÃO FOI POSSÍVEL REMOVER NO FORTIGATE", delete_line)
    #                 else:
    #                     print(f"{delete_line['name']}:{delete_line['sponsor']}, ")
    #                 dict_line.update(itera_fortigate = delete_line['itera_fortigate'])
    #                 dict_line.update(status = delete_line['status'])
    #                 dict_line.update(http_status = delete_line["http_status"])
    #         # ---------------------------------------------------------------------------------------------
    #         bash_view.print_header("HISTÓRICO DA AÇÃO DE REMOÇÃO:")
    #         bash_view.print_list_dict_by_pretty_table(mv_vouchers_in_forti)
    # except Exception as err:
    #     # ENVIAR E-MAIL
    #     bash_view.print_header(f"ERROR: ERRO DO BLOCO REMOVER VISITANTES EXPIRADOS no FORTIGATE!", err )            
    #     # continue






    # for line_avaliable_groups in avaliable_groups:
    #     if line_avaliable_groups["avaliable"] >0:
    #         print(line_avaliable_groups)
    #         # for i in range(line_avaliable_groups["avaliable"]):
    #         #     print(f"group = {line_avaliable_groups["name"]} - {i}, ")

    #     else:
    #         continue
# =============================================================================        
#     _value_list = {'user-id':'user4037x', } # 'user7158', 
#     # print(f"\n=========================\n{mv_vouchers_in_forti}\n")  (key_name, from_dict, list_dict_source)
#     filter_care_from_fortigate = action_controller.search_value_in_dict('user-id', _value_list, mv_vouchers_in_forti)
#     print(f"\nRETORNO do procura no dicionário: \n{filter_care_from_fortigate}")
#     if len(filter_care_from_fortigate) >0:
#         bash_view.print_header("JÁ EXISITE NO FORTIGATE. Vamos inserir no SQL!", filter_care_from_fortigate)
        
#     else: 
#         bash_view.print_header(f"ATENDIMENTO NÃO EXISTE NO FORTIGATE")

    #     ### Seleciona TODOS os NOMES dos GRUPOS do PROJETO:
    #     select_groups_in_visitor  = action_controller.select_mv_groups_type('*')
    #     bash_view.print_header("GRUPOS PERTENCENTES AO PROJETO")
    #     bash_view.print_list_dict_by_pretty_table(select_groups_in_visitor)
    #     ## Extrai TODOS os NOMES dos GRUPOS do DICIONÁRIO:
    #     name_groups_list_dict = action_controller.value_column_list_dict(select_groups_in_visitor, 'name')
    #     bash_view.print_header("NOME DOS GRUPOS PARA O FORTIGATE", name_groups_list_dict)

    #     ## Exibe TODOS os NOMES dos GRUPOS do DICIONÁRIO:

    #     # Consulta ao fortigate
    #     all_guest_rest_forti = restapi_forti_controller.get_all_guest_by_groups_in_rest_forti(name_groups_list_dict)
    #     bash_view.print_header("REGISTROS ENCONTRADOS NO FORTIGATE QUE PERTENÇAM AOS GRUPOS DO PROJETO")
    #     if len(all_guest_rest_forti) > 0:
    #         for guest_line in all_guest_rest_forti:
    #             if "status" in guest_line:
    #                 if guest_line["status"] == "error":
    #                     bash_view.print_header("ERROR: NÃO FOI POSSÍVEL REALIZAR CONSULTA DOS REGISTROS DOS GRUPOS DO FORTIGATE")
    #                     bash_view.print_list_dict_by_pretty_table(all_guest_rest_forti)
    #                     _fortigate = False
    #                     break
    #             else:  # ENVIAR E-MAIL
    #                 bash_view.print_header(f"FORAM ENCONTRADOS {len(all_guest_rest_forti)} REGISTROS DOS GRUPOS DO FORTIGATE")
    #                 bash_view.print_list_dict_by_pretty_table(all_guest_rest_forti)
    #                 _fortigate = True
    #                 break
    #     else:
    #         bash_view.print_header(f"NÃO FORAM ENCONTRADOS REGISTROS DOS GRUPOS DO PROJETO NO FORTIGATE")
    #         _fortigate = False
    # except Exception as err:
    #     # ENVIAR E-MAIL
    #     bash_view.print_header(f"ERROR: NO BLOCO CONSULTA A GRUPOS DO PROJETO NO FORTIGATE!", err)
