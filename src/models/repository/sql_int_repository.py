# from mysql.connector.errors import Error
import mysql.connector  # Conector MYSql
from mysql.connector import (Error, errorcode)
# import mysql.opentelemetry
from src.env import creds_admin  # Arquivo com algumas variáveis de Ambiente
from src.controllers.action_controller import ActionController
from datetime import timedelta
import pytz
import datetime

import os

class SqlIntRepository:
    def __init__(self):
        ''' Class Modelagem de banco AUX. MySQL
            Todos os métodos desta classe retornam uma LISTA C/ DICIONÁRIOS(com status ou query)
            else roda se não houver erros no try. O finally sempre roda, independente de erros,
            TODOS OS MÉTODOS RETORNA uma LISTA:\n
            [{}{}] = RESULTADO DA CONSULTA (SELECT) ou [{status : "success"}] STATUS DA OPERAÇÃO (INSERT, UPDATE, DELETE)
        ''' 
        self._my_host = creds_admin.MY_HOST
        self._my_username = creds_admin.MY_USERNAME
        self._my_password = creds_admin.MY_PASSWORD
        self._my_database = creds_admin.MY_DATABASE
        self.creds = {                
            'host' : self._my_host,
            'user' : self._my_username,
            'password' : self._my_password,
            'database' : self._my_database
            }
        self.time_difference = timedelta(hours=-3)
        tz_Brasilia = pytz.timezone('Brazil/West')
        datetime_Brasilia = datetime.datetime.now(tz_Brasilia)
        
        # Configurar conexão como false
        self._status_healthy = False # Status da conexão
        self.connected = False
        # INSTÃNCIANDO CLASSE ACTION -------------------
        self.action = ActionController()


    def read_query_mysql_dic(self, table, columns, where=None, order=None, asc=True) -> list: # VOUCHER 2.0 - ATENDIMENTO E VISITOR
        ''' Recebe os parâmetros para conexão e retorna dicionário da consulta no banco \n
            :table: nome da tabela em strings
            :columns: passar * ou uma lista com colunas a serem consultadas
            :where: condicional para campos
            :order: string nome da coluna para ordenar
            :desc: booleano se os dados devem ser asc ou desc
            ___________________________________________________________________
            Voucher 2.0         jul-24
            Utlizado por: (care_sql_int_controller e visitor_sql_int_controller)
        '''
        try:
            # print(f"\n 1º ==> try # TRATA CONEXÃO COM O BANCO MYSQL\n===========================================================")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        except Exception as err:
            message = "Exception All"
            result = [{"status":"error", "healthy": self._status_healthy, "except": "Exception", "message": message}]
        else:
            try: 
                # print(f"\n1º else: 2º ==> Try # TRATA Cursor")
                sql = self.action.create_query(table, columns, where, order, asc)
                # print(f"\n {sql}")
                with _conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql)
                    result_cursor = cursor.fetchall()
                    result = result_cursor.copy()
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except mysql.connector.InterfaceError as err:
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.InterfaceError", "message": error}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:            
                _conn.close()
        finally:
            return result

    def read_fetchall_mysql_dic(self, table, columns, where=None, order=None, asc=True) -> list: # VOUCHER 2.0 - ATENDIMENTO E VISITOR
        ''' Recebe os parâmetros para conexão e retorna dicionário da consulta no banco \n
            :table: nome da tabela em strings
            :columns: passar * ou uma lista com colunas a serem consultadas
            :where: condicional para campos
            :order: string nome da coluna para ordenar
            :desc: booleano se os dados devem ser asc ou desc
            ___________________________________________________________________
            Voucher 2.0         jul-24
            Utlizado por: (care_sql_int_controller e visitor_sql_int_controller)
        '''
        try:
            # print(f"\n 1º ==> try # TRATA CONEXÃO COM O BANCO MYSQL\n===========================================================")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        except Exception as err:
            message = "Exception All"
            result = [{"status":"error", "healthy": self._status_healthy, "except": "Exception", "message": message}]
        else:
            try: 
                # print(f"\n1º else: 2º ==> Try # TRATA Cursor")
                sql = self.action.create_query(table, columns, where, order, asc)
                # print(f"sql_int_repository line 136 - \n {sql}")
                with _conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except mysql.connector.InterfaceError as err:
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.InterfaceError", "message": error}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:            
                _conn.close()
        finally:
            return result

    def create_line_in_mysql(self, columns, tuple, table_name: str): # VERSION 2.0
        ''' Recebe valores e insere na tabela informada inserir no ATENDIMENTO -> MYSQL
            :tupla: Tuplas 14 colunas
            ________________________________________________
            Version: 2.0
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except (mysql.connector.Error, IOError) as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                # print("1º - else | 2º Try # TRATA Cursor")
                col_args = self.action.format_col_args(columns)
                data = tuple
                sql = (f"INSERT INTO {table_name} ("
                    f"{columns})"
                    f" VALUES ({col_args})")
                with _conn.cursor() as cursor:
                    cursor.execute(sql, data)
                    _conn.commit()  
                result = [{"status" : "success", "healthy": self._status_healthy, "message": cursor.lastrowid}]    
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:

            return result

    def create_care_mysql(self, tupla): # VERSION 2.0
        ''' Recebe tupla / inserir no ATENDIMENTO -> MYSQL
            :tupla: Tuplas 14 colunas
            ________________________________________________
            Version: 2.0
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                table_name = 'care_mv'
                columns =("cd_atendimento, cd_paciente, nm_paciente, nr_cpf, dt_atendimento, "
                            "dt_nascimento, tp_atendimento, cd_multi_empresa, dt_alta, hr_alta, "
                            " password, dt_remove, itera_fortigate")
                col_args = self.action.format_col_args(columns)
                data = tupla
                sql = (f"INSERT INTO {table_name} ("
                    f"{columns})"
                    f" VALUES ({col_args})")
                with _conn.cursor() as cursor:
                    cursor.execute(sql, data)
                    _conn.commit()
                result = [{"status" : "success", "healthy": self._status_healthy, "message": cursor.lastrowid}]   
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                userid = cursor.lastrowid
                _conn.close() 
        finally:
            return result

    def create_all_users_contingency_mysql(self, query, columns, table_name: str): # VOUCHER 2.0 Insert_care_ora_filter_in_sql_int
        ''' Método - recebe parâmetros e insere REGISTROS no BANCO MYSQL
            :query: Lista de tuplas com valores das colunas
            :columns: Títulos das colunas(chaves)
            :table_name: nome da tabela em strings
            TABELA = CONTINGENCY
        '''
        try:
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                _cursor_sql = _conn.cursor()
                col_args = self.action.format_col_args(columns)
                for t in query:
                    sql = (f"INSERT INTO {table_name} ("
                            f"{columns})"
                            f" VALUES ({col_args})"
                            f" ON DUPLICATE KEY UPDATE user_id='{t[0]}'")
                    tuple_value = t  
                    _cursor_sql.execute(sql, tuple_value)
                    _conn.commit()
                result = [{"status" : "success", "healthy": self._status_healthy, "message": _cursor_sql.lastrowid}]     
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def create_all_duplicate_key_mysql(self, query, columns, table_name: str, primary_key): # VOUCHER 2.0 Insere vários registro passados no MYSQL
        ''' Método - recebe parâmetros e insere VÁRIOS REGISTROS no BANCO MYSQL
            :query: Lista de tuplas com valores das colunas
            :columns: Títulos das colunas(chaves)
            :table_name: nome da tabela em strings
            TABELA = CONTINGENCY
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                _cursor_sql = _conn.cursor()
                col_args = self.action.format_col_args(columns)
                for t in query:
                    sql = (f"INSERT INTO {table_name} ("
                            f"{columns})"
                            f" VALUES ({col_args})"
                            f" ON DUPLICATE KEY UPDATE {primary_key}='{t[0]}'")
                    tuple_value = t  
                    _cursor_sql.execute(sql, tuple_value)
                    _conn.commit()
                result = [{"status" : "success", "healthy": self._status_healthy, "message": _cursor_sql.lastrowid}] 
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def update_return_fortigate_care_mv(self, data, table_name: str) -> list:  # VOUCHER 2.0  = ATENDIMENTO
        ''' Método - recebe lista com 7+1 coluna com valores para atualiar Banco de dados
            :data: Lista com dados para as colunas Obs.: adicionar mais 1 coluna no final
            para condição da consulta WHERE
            :table_name: nome da tabela em strings
            Coluna para verificar se já existe registro!
            RETORNA lista de status
            _____________________________________________________________________________
            VOUCHER 2.0             02/07/24
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
                
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        except Exception as err:
            message = "Exception All"
            result = [{"status":"error", "healthy": self._status_healthy, "except": "Exception", "message": message}]
        else:
            try: 
                _data = (data)
                sql = (f"UPDATE {table_name} SET `user-id` ="
                        " %s, id_forti = %s, itera_fortigate = %s, expiration = %s, dt_remove = %s" 
                        " WHERE cd_atendimento = %s") 
                with _conn.cursor() as _cursor:
                    _cursor.execute(sql, _data)
                    _conn.commit()
                result = [{"status" : "success", "record_inserted" : _cursor.rowcount}]
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro de código"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def update_return_insert_fortigate_care_mv(self, data, table_name: str) -> list:  # VOUCHER 2.0  = ATENDIMENTO
        ''' Método - recebe lista com 7+1 coluna com valores para atualiar Banco de dados
            :data: Lista com dados para as colunas Obs.: adicionar mais 1 coluna no final
            para condição da consulta WHERE
            :table_name: nome da tabela em strings
            Coluna para verificar se já existe registro!
            RETORNA lista de status
            _____________________________________________________________________________
            VOUCHER 2.0             02/07/24
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
                
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        except Exception as err:
            message = "Exception All"
            result = [{"status":"error", "healthy": self._status_healthy, "except": "Exception", "message": message}]
        else:
            try: 
                _data = (data)
                sql = (f"UPDATE {table_name} SET `user-id` ="
                        " %s, id_forti = %s, itera_fortigate = %s, expiration = %s, dt_remove = %s" 
                        " WHERE cd_atendimento = %s") 
                with _conn.cursor() as _cursor:
                    _cursor.execute(sql, _data)
                    _conn.commit()
                result = [{"status" : "success", "record_inserted" : _cursor.rowcount}]
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro de código"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def update_visitor_return_fortigate_mysql(self, data, table_name: str) -> list:  # VOUCHER 2.0  = VISITANTES
        ''' Método - recebe lista com 7+1 coluna com valores para atualiar Banco de dados
            :data: Lista com dados para as colunas Obs.: adicionar mais 1 coluna no final
            para condição da consulta WHERE
            :table_name: nome da tabela em strings
            Coluna para verificar se já existe registro!
            RETORNA lista de status
            _____________________________________________________________________________
            VOUCHER 2.0             02/07/24
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                _data = (data)
                sql = (f"UPDATE {table_name} SET `user-id` ="
                    " %s, user_id = %s, id_forti = %s, itera_fortigate = %s, expiration = %s, dt_remove = %s, nr_cpf = %s" 
                    " WHERE `user-id` = %s") 
                # print(sql)
                # print(f"\n{_data}")
                with _conn.cursor() as _cursor:
                    _cursor.execute(sql, _data)
                    _conn.commit()
                result = [{"status" : "success", "record_inserted" : _cursor.rowcount}]
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def create_duplicate_key_mysql(self, tuple_value, columns, table_name: str, primary_key, key_value): # VOUCHER 2.0 Insere VISITANTES no MYSQL
        ''' Método - recebe parâmetros e insere VÁRIOS REGISTROS no BANCO MYSQL
            :query: Lista de tuplas com valores das colunas
            :columns: Títulos das colunas(chaves)
            :table_name: nome da tabela em strings
            TABELA = CONTINGENCY
        '''
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try: 
                _cursor_sql = _conn.cursor()
                col_args = self.action.format_col_args(columns)
                sql = (f"INSERT INTO {table_name} ("
                        f"{columns})"
                        f" VALUES ({col_args})"
                        f" ON DUPLICATE KEY UPDATE {primary_key}={key_value}")
                _cursor_sql.execute(sql, tuple_value)
                _conn.commit()
                result = [{"status" : "success", "healthy": self._status_healthy, "message": _cursor_sql.lastrowid}] 
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result

    def delete_care_mysql(self, column_name, value, table_name): #  VOUCHER 2.0
        """
            Recebe nome da tabela, coluna e id referência para exclusão
            :column_name: Nome da coluna para pesquisa
            :value: Valor a ser comparado
            :table_name: Nome da Tabela
        """
        try:
            # print("try # TRATA CONEXÃO COM O BANCO MYSQL")
            _conn = mysql.connector.connect(**self.creds)
            self._status_healthy = True
        except mysql.connector.errors.ProgrammingError as err: # VALIDADO
            error = err.args
            result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
        except mysql.connector.Error as err: # VALIDADO
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = "Algo está errado com seu nome de usuário ou senha"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                message = "Database não existe"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error.errorcode.ER_ACCESS_DENIED_ERROR", "message": message}]
            else:
                message = err
                self._status_healthy = False
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error", "message": message}]
        else:
            try:
                # cria o ponteiro nesta conexão
                # _cursor_sql = _conn.cursor()
                id = (value,)
                sql = (f"DELETE FROM {table_name} WHERE {column_name}" " = %s")    
                with _conn.cursor() as cursor:
                    cursor.execute(sql, id)
                    _conn.commit() 
                result = [{"status" : "success", "healthy": self._status_healthy, "message": cursor.lastrowid}]  
            except mysql.connector.errors.ProgrammingError as err: # VALIDADO
                error = err.args
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.errors.ProgrammingError", "message": error}]
            except (mysql.connector.Error, IOError) as err: # VALIDADO
                if err.errno == 1146:
                    message = "Database não existe"   
                elif err.errno == 1292:
                    message = "Incorreto valor de Data"
                elif err.errno == 2002:
                    message = "Não consigo conectar ao Servidor Mysql"
                elif err.errno == 2006:
                    message = "O servidor TIMED OUT e FECHOU CONEXÃO"    
                elif err.errno == 2013:
                    message = "Conexão foi Perdida" 
                else:
                    message = err.args 
                result = [{"status":"error", "healthy": self._status_healthy, "except": "mysql.connector.Error, IOError", "message": message}]
            except TypeError as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            except  errorcode as err:
                message = "Erro ao executar o cursor"
                result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
            else:
                _conn.close()
        finally:
            return result













#     def update_care_return_forti(self, data: list):
#         """ Recebe Lista com um conjunto prédefinido de campos a serem atualizados
#             :data: id, password, itera_fortigate, cd_atendimento
#         """
#         _conn = self._connecting_sql()
#         if self._status_healthy:
#             print(f"\n!!!! CONECTADO COM successOOOO!!!!")
#         cursor = _conn.cursor()
#         sql = "UPDATE care_mv SET id = %s, password = %s, itera_fortigate = %s WHERE cd_atendimento = %s"
#         data = (data)
#         cursor.execute(sql, data)
#         _conn.commit()
#         # cursor.close()
#         # print(f"\n END => Method -> update_care_return_forti  - IN Class SqlIntRepository =================\n\n")        
#     def get_database_name(self):
#         ''' Método Retorna nome Banco Conectado'''
#         return self._my_database 
    
#     def get_database_user(self):
#         ''' Método para Retorna nome Banco Conectado'''
#         return self._my_username





#########################


# #############################################################################
# #  CONEXÕES ANTES DO 2.0
# #
# #############################################################################

#     def create_tuple_mysql(self, query, columns, table_name: str):
#         ''' Método - recebe parâmetros e insere REGISTROS no BANCO MYSQL
#             :query: Lista de tuplas com valores das colunas
#             :columns: Títulos das colunas(chaves)
#             :table_name: nome da tabela em strings
#         '''
#         _conn = self._connecting_sql()
#         if self._status_healthy:
#             print(f"\n!!!! CONECTADO COM successOOOO!!!!")
#         # cria o ponteiro nesta conexão
#         _cursor_sql = _conn.cursor()
#         col_args = self.action.format_col_args(columns)
#         for t in query:
#             sql = (f"INSERT INTO {table_name} ("
#                     f"{columns})"
#                     f"VALUES ({col_args})")
#             tuple_value = t  
#             _cursor_sql.execute(sql, tuple_value)
#             _conn.commit()
#             _cursor_sql.close()
#         # print(f"\n END => Table: {table_name} Method -> create_tuple_mysql  - IN Class SqlIntRepository =================\n\n")

# #############################################################################
#         # #### Cria string para CONSULTA '''
#         # sql = self.action.create_query(table, columns, where, order, asc)
#         # # print(query)
#         # _conn = self._connecting_sql()
#         # if self._status_healthy:
#         #     #### cria o ponteiro nesta conexão
#         #     try:
#         #         with _conn.cursor(dictionary=True) as cursor:
#         #             cursor.execute(sql)
#         #             result = cursor.fetchall()
#         #     except TypeError as err:
#         #         message = "Database não existe"
#         #         result = [{"healthy": self._status_healthy, "except": "oracledb.Error", "message": message}]
#                 except  errorcode as err:
#                     message = "Erro ao executar o cursor"
#                     result = [{"status":"error", "healthy": self._status_healthy, "except": "TypeError", "message": message}]
#         #     finally:
#         #         return result
#         # else:
#         #     return [{"healthy": self._status_healthy, "except": "oracledb.Error", "message": "xiiiiiiiiiiiii"}]

# ##############################################################################


#     def update_care_intera_fortigate(self, data: list):
#         """
#             Recebe Lista com 2 campos prédefinido para atualizar STATUS
#             :data: Composta de 2 campos: itera_fortigate e cd_atendimento
#         """
#         _conn = self._connecting_sql()
#         if self._status_healthy:
#             print(f"\n!!!! CONECTADO COM successOOOO!!!!")
#         cursor = _conn.cursor()
#         sql = "UPDATE care_mv SET itera_fortigate = %s WHERE cd_atendimento = %s"
#         data = (data)
#         print(data)
#         cursor.execute(sql, data)
#         _conn.commit()
#         # cursor.close()
#         # print(f"\n END => Method -> update_care_intera_fortigate  - IN Class SqlIntRepository =================\n\n")        

