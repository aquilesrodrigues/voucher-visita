from prettytable import PrettyTable

class BashView:
    def __init__(self):
        pass

    def print_header(self, title, data = None):
        '''
            Recebe o título e os dados para sererm exibidos no bash
            :title: Texto para a linha de título
            :data: Dados para linha após o título
            _____________________________________________________________
            Módulos:   kick_the_bucket, process
            
        '''

        print(f"\n ------------------------------------------------------------------------"
        "------------------------------------------------------------------------\n"
        f"+++ {title} ++ \n"
        "--------------------------------------------------------------------------"
        "------------------------------------------------------------------------")
        if data != None:
            print(data)


    def print_list_dict_by_pretty_table(self, data):
        
        if len(data) != 0:
            field_names = []        
            for dict_line in data[0]:
                field_names.append(dict_line)

            # Specify the Column Names while initializing the Table 
            ptable = PrettyTable(field_names) 

            for line_dict in data:
                ptable.add_row(line_dict.values())
        else:
            ptable = data
        print(ptable) 

    def print_dict_by_pretty_table(self, data:dict):
        
        field_names = [] 
        for dict_line in data.keys():
            field_names.append(dict_line)

        # Specify the Column Names while initializing the Table 
        ptable = PrettyTable(field_names) 

        for line_dict in data:
            ptable.add_row(line_dict.values())

        print(ptable) 