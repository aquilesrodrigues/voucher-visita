from src.controllers.action_controller import ActionController
from src.env import creds_admin  # Arquivo com algumas variáveis de Ambiente
from datetime import datetime, date, time, timedelta, timezone
import requests
from requests.exceptions import (HTTPError, ConnectionError, Timeout, InvalidURL, InvalidJSONError, ChunkedEncodingError)
import json

requests.urllib3.disable_warnings() # type: ignore

class RestFortiRepository:
    '''
        Class RestFortiRepository MODEL RESTAPI FORTIGATE
        Todos os MÉTODOS RETORNAM DICIONÁRIOS
    '''
    def __init__(self):
        self._status_healthy = False
        self.action_controller = ActionController()

    def all_methods_in_forti(self, method="get", mkey="", child_name="", child_key="", dictionary=None, filter_param=None) -> dict:

        ''' Busca usuários de um GRUPO caso informado ou TODOS se não informado.\n
            :method: get, get-filter, post, put, delete
            :mkey: Informar o GRUPO que deseja consultar
            :child_key: Chave do registro dentro do grupo informado
            :dictionary: Dicionário para inserção no fortigate
            :filter_param: Parâmetro em conjunto com método <get-filter> para filtro
            POST e PUT precisa que todos os parâmentros sejam passados: \n
            mkey=GRUPO, child_name=guest, child_key=ID ==> (mkey="Internacao"  child_name="/guest", child_key="2")
            Retorna a RESPOSTA em dicionário DICIONÁRIO!
            ___________________________________________________________________
            VOUCHER 2.0 - post_guest_all_groups_rest_forti
        '''
        # Cria URL PADRÃO com parâmetros passados
        _url_origin = f"{creds_admin.FORTI_API_GROUP}{mkey}{child_name}{child_key}/?"
        url_api = f"{creds_admin.FORTI_API_GROUP}{mkey}{child_name}{child_key}/?{creds_admin.FORTI_VDOM_TOKEN}"
        # print(f"\n========== all_methods_in_forti ==============================\n rest_forti_repository, Antes do TRY: \n {url_api}")
        _method = method
        # _response = {}
        try:
          if _method == "get":
              response = requests.get(url_api, verify=False, timeout=30)
              #
          elif _method == "get-filter":
              filter_name = filter_param # Cria a url com parâmetros enviados
              _url_api_filter = f"{url_api}&{filter_name}"
              # print(f"\n restapi_forti_repository - get-filter : {_url_api_filter}")
              response = requests.get(_url_api_filter, verify=False, timeout=30)
              #
          elif _method == "post":
              # Transforma a linha do dicionário em string JSON sem identação para enviar como payload ao FortiGate 
              payload = json.dumps(dictionary)
              response = requests.post(url_api, data=payload, verify=False, timeout=30)
              #
              # print(f"\n restapi_forti_repository - POST : {response}")
          elif _method == "put":
              payload = json.dumps(dictionary)
              response = requests.put(url_api, data=payload, verify=False, timeout=30)
              #
          elif _method == "delete":
              #DELETE o GUEST passando GRUPO e ID  (mkey="Internacao"  child_name="/guest", child_key="2")
              response = requests.delete(url_api, verify=False, timeout=30)
              #
          elif _method == "options":
              response = requests.options(url_api, verify=False, timeout=30)
              # print(f"\n Headers ==> {response.headers['allow']}")
              #
          # CRIA RESPOSTA 
          _response = response.json() # ATRIBUI COMO DICIONÁRIO! Agora posso fechar a REQUISIÇÃO
        except (HTTPError, Timeout, ConnectionError, InvalidURL, InvalidJSONError, ChunkedEncodingError) as error:
          _response = {"http_method": _method.upper(), "status":"error", "http_status": 400, "except": type(error).__name__, "status_message": "url Invalid", "url": _url_origin}
        except (AttributeError, KeyError) as error:
          _response = {"http_method": _method.upper(), "status":"error", "http_status": 400, "except": type(error).__name__, "status_message": "Atribute Error", "url": _url_origin}
        except requests.exceptions.RequestException as error: # VALIDADO
          _response = {"http_method": _method.upper(), "status":"error", "http_status": 400, "except": type(error).__name__, "status_message": "Requests Exceptions", "url": _url_origin}
        else:
          response.close() 
        finally:

          # print(f"\n Restapi_forti_repository 79 <==> RETURN ==> {_response} \n")
          return _response
