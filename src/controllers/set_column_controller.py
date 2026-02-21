from src.controllers.action_controller import ActionController 

class SetColumnController:
    def __init__(self): 
        self.action_controller = ActionController()


    def sets_difference_a_b(self, set_base:list, set_referent:list) -> list: # VOUCHER 2.0
        ''' Recebe 2 listas(1 Coluna cada), converte-as em conjunto. \n
            Retorna os valores que existem no set_base, q não estão no set_referente
            :set_base: Lista-a (1 coluna)
            :set_referent: Lista-b (1 coluna) \n
            ___________________________________________________________________
            VOUCHER 2.0   (process / )      junho-2024         
        '''
        _set_base_a =set() 
        _set_referent_b = set()
        _set_base_a.update(set_base)
        _set_referent_b.update(set_referent)
        _list_order = sorted(_set_base_a.difference(_set_referent_b), reverse=True)
        return _list_order


    #############################################################################
    def sets_intersection(self, set_base:list, set_referent:list):
        ''' Recebe 2 listas (apenas 1 coluna cada)
            retorna um novo conjunto contendo apenas os itens presentes em ambos
            ___________________________________________________________________
            Applicant: care_sql_int_applicant  
        '''
        _set_base_intersection= set(set_base)
        _set_referent_intersection = set(set_referent)
        _list_order = sorted(_set_base_intersection.intersection(_set_referent_intersection), reverse=True)
        return _list_order
    
    ##############################################################################
