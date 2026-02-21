from prettytable import PrettyTable
from datetime import datetime, date, time, timedelta
from pytz import timezone
import json
from src.controllers.datetime_encoder_controller import DatetimeEncoder

class OutputFile:
    def __init__(self) -> None:
        
        self.date_time_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    
    def file_json_new(self, name_file:str, list_dict:dict):
        '''
        #### Salva DICIONÁRIO passado em arquivo no formato JSON
        :name_file: Nome para o arquivo que será salvo no disco
        :list_dict: Lista de dicionário que será convertida para formato JSON
        _____________________________________________________________________
        Versão 2.0 - Agosto/2024
        '''
        json_list_dict = json.dumps(list_dict, cls=DatetimeEncoder, indent=4)
        _name_file = f'src/logs/{name_file}_{self.date_time_now}.json'
        with open(_name_file, 'w') as file:
            file.write(json_list_dict)

    def file_update(self, name_file:str, title:str, record=None):
        '''
        #### Cria ou atualiza arquivo no formato txt com dados passados como parâmentros
        :name_file: Nome para o arquivo que será salvo no disco
        :title: Título da primeira linha 
        :record: Valores a serem exibidos após o a linha de título
        _____________________________________________________________________
        Versão 2.0 - Agosto/2024
        '''
        _name_file = f'src/logs/{name_file}.txt'
        if record == None:
            _data_file = (f"\n--------------------------------------------------------------------------------\n"
                        f"{title} || {self.date_time_now} \n"
                        "--------------------------------------------------------------------------------")
        else:
            _data_file = (f"\n--------------------------------------------------------------------------------\n"
                        f"{title} || {self.date_time_now} \n"
                        "--------------------------------------------------------------------------------\n"
                        f"{record}\n"
                        "--------------------------------------------------------------------------------")

        with open(_name_file, 'a') as file:
            file.write(_data_file)
        

    def file_update_insert_table(self, name_file:str, title:str, list_dict:dict):
        '''
        #### Cria ou atualiza arquivo no formato txt com dados passados como parâmentros
        ##### Converte dicionário em TABEla e insere no arquivo
        :name_file: Nome para o arquivo que será salvo no disco
        :title: Título da primeira linha 
        :list_dict: Lista com dicionário 
        _____________________________________________________________________
        Versão 2.0 - Agosto/2024
        '''
        _name_file = f'src/logs/{name_file}.txt'
        
        if len(list_dict) > 0:
            field_names = []        
            for dict_line in list_dict[0]:
                field_names.append(dict_line)

            # Specify the Column Names while initializing the Table 
            ptable = PrettyTable(field_names) 

            for line_dict in list_dict:
                ptable.add_row(line_dict.values())
        else:
            ptable = list_dict

        _data_file = (f"\n--------------------------------------------------------------------------------\n"
                    f"{title} || {self.date_time_now} \n"
                    "--------------------------------------------------------------------------------\n"
                    f"{ptable}\n"
                    "--------------------------------------------------------------------------------")
        with open(_name_file, 'a') as file:
            file.write(_data_file)
