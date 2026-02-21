from src.models.repository.ora_mv_repository import CareOraMVRepository

class CareOraMVController:
    def __init__(self):
        self.sql = str
        self.query_ora = None
        self.query_description_ora = None
        # self.table_name = "view_voucher"
        # self.key = 0
        
    def select_query_ora_mv(self):
        ''' SELECT ALL Atendimentos - ORACLE MV - Retorna DICIONÁRIO da consulta
            ___________________________________________________________________
            Applicant: care_sql_int_applicant  
        '''
        care_oracle_mv_repository = CareOraMVRepository()
        self.query_ora = care_oracle_mv_repository.dict_query_oracle()
        return self.query_ora
