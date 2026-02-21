import os
import time
import oracledb # Conector Oracle
from src.env import creds_admin  # Arquivo com algumas variáveis de Ambiente
from typing import Dict
from datetime import datetime

class CareOraMVRepository:
    ''' Class com métodos de consulta ao banco Oracle
        TODOS OS MÉTODOS RETORNAM LISTA C/ DICIONÁRIOS
        ______________________________________________
        Voucher2.0
    ''' 
    def __init__(self):
        # Instancia a Class OracleConnect que conecta ao banco ORACLE
        
        # Variable TNSNames Oracle ========================================
        self._ora_lib_dir = creds_admin.ORA_LIB_DIR
        self._ora_config_dir = creds_admin.ORA_CONFIG_DIR
        self._ora_error_url = creds_admin.ORA_ERROR_URL 
        self._ora_driver_name = creds_admin.ORA_DRIVER_NAME
        # Variable Connect =====================================================
        self._ora_user = creds_admin.ORA_USER
        self._ora_passwd = creds_admin.ORA_PASSWORD
        self._ora_dsn = creds_admin.ORA_DSN
        self._ora_encoding = creds_admin.ORA_ENCODING
        self.table_name = "view_voucher"
        
        self._select_list_dict = dict
        self._select_list_tupla = list
        self._select_list_cols = list
        self._status_healthy = False
    
    ### CONEXÕES ====================================================================
    ### Method Private ========================================================== 

########################################################################################

    def dict_query_oracle(self) -> list:
        ''' Estabelece conexão com o banco ORACLE
            Todos os métodos desta classe retornam uma LISTA C/ DICIONÁRIOS(com status ou query)
        '''
        result = []
        try:
            oracledb.init_oracle_client(self._ora_lib_dir, self._ora_config_dir, self._ora_error_url, self._ora_driver_name)
            message = "Método TNSNAMES ORACLE - Iniciado Client Oracle!"
        except oracledb.Error as e:
            error, = e.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "oracledb.Error", "message": error.message}]
            print(f"\noracle client error:\n {e} ")
        except Exception as err:
            error, = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "oracledb.Error", "message": error.message}]
            print(f"\noracle client error:\n {err} ")
        else:        
            try:
                connection =  oracledb.connect(
                    user=self._ora_user, 
                    password=self._ora_passwd, 
                    dsn=self._ora_dsn
                )
                with connection.cursor() as cursor:
                    self.key = 0
                    sql = (f"select cd_atendimento, cd_paciente, nm_paciente, nr_cpf, dt_atendimento, "
                        "dt_nascimento, tp_atendimento, cd_multi_empresa, nr_cpf" 
                        f" FROM {self.table_name} where tp_atendimento != 'H'")
                    #  nr_cpf is not null and ROWNUM <= 50
                    # Executa conexão sql
                    cursor.execute(sql)
                    cursor.rowfactory = lambda *arg: dict(
                        zip([desc[0] for desc in cursor.description], arg))
                    
                    ######### CRIA LISTA DO DICIONÁRIO DA QUERY ################   
                    self._select_list_dict = cursor.fetchall()
                    self._status_healthy = connection.is_healthy()
                    result = self._select_list_dict.copy()                 
            except oracledb.Error as e:
                error, = e.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "oracledb.Error", "message": error.message}]
                print(f"\noracle error cursor:\n {e} ")
            else:
                connection.close()
        finally:
            return result
