from src.view.bash_view import BashView
from src.env.table_in_lists_env import TableInListsEnv
from src.controllers.action_controller import ActionController
from src.models.repository.restapi_forti_repository import RestFortiRepository
from datetime import datetime

class KickTheBucketController:
    ''' _summary_
        Classe tipo Controler responsável por limpar os registros no fortigate para fins de teste
        TODOS OS MÉTODOS AQUI RETORNAM LISTAS
    '''
    def __init__(self):

        pass

    def remove_all_guest_by_groups_in_rest_forti(self, list_groups:list) -> list: # VOUCHER 2.0 ==> todos registros
        ''' 
        #### Remove Todos os registros do fortigate baseado na lista dos GRUPOS passados
        #### RETORNA LISTA Dicionário AGRUPANDO todos registros com status da operação. 
        :list_groups: lista dos grupos para consulta
        :list_group: Lista com nome dos grupos para procura no fortigate
        ___________________________________________________________________
        Voucher 01-08-24
        '''           
        # Instancia MODEL - UsersRestFortiRepository
        # --------------------------------------------------------------------
        rest_forti_repository = RestFortiRepository() 
        action_controller = ActionController()
        self._method = "delete"
        self.child_name="/guest"
        self.child_key=""
        _list_dict = []
        for i in list_groups:
            self._mkey= f"/{i}" # nome do grupo Iterado
            payload_delete = rest_forti_repository.all_methods_in_forti("delete", self._group, self.child_name, self.child_key)

            if payload_delete["http_status"] == 200:
                if "results" in payload_delete:
                    if len(payload_delete["results"]) != 0:
                        for line_dic in payload_delete["results"]:
                            _list_dict.append(line_dic)
            else:
                _list_dict.append(payload_delete)
                return _list_dict

        if payload_delete['http_status'] == 200:
            list_groups.update(itera_fortigate = 'REMOVED')
            list_groups.update(dt_remove = datetime.now())
            list_groups.update(status = payload_delete['status'])
            list_groups.update(http_status = payload_delete['http_status'])
            _code =  list_groups['http_status']
            resp = action_controller.request_response(_code)
            list_groups.update(status_message = resp)             
        else:
            list_groups.update(itera_fortigate = 'NOT.FORTIGATE')
            list_groups.update(status = payload_delete['status'])
            list_groups.update(http_status = payload_delete['http_status'])
            _code =  list_groups['http_status']
            resp = action_controller.request_response(_code)
            list_groups.update(status_message = resp) 

        return _list_dict




