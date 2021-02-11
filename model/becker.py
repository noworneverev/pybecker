import requests
import json
import html2text
from type.subject import SubjectType
from util.constant import URL_FAR, URL_AUD, URL_REG, URL_BEC, SUCCESS_CODE, SEPERATOR_UNIT, SEPERATOR_MODULE, URL_CHECK
from util.cookie import Cookie
from src.extract import Extractor


class Becker:
    def __init__(self, cookie, subject_type):
        self.url = self.__get_request_url(subject_type)
        self.cookie = cookie
        self.subject_type = subject_type

    def __get_request_url(self, subject_type:SubjectType) -> str:
        '''
        Wrapper to get acutal parsing url
        '''
        url = ""
        if subject_type == SubjectType.Financial:
            url = URL_FAR
        elif subject_type == SubjectType.Auditing:
            url = URL_AUD
        elif subject_type == SubjectType.Regulation:
            url = URL_REG
        else:
            url = URL_BEC
        return url

    # def __get_response(self):
    #     return requests.get(self.url, cookies=self.cookie)
        
    # def __get_table_of_contents(self):
    #     table_of_contents = {}
    #     response = self.__get_response()
        
    #     if response.status_code == 200:
    #         table_of_contents = json.loads(response.text)

    #     return table_of_contents

    def check_connection(self) -> bool:
        return Extractor.is_api_available(URL_CHECK, self.cookie)


    def get_units_from_toc(self):
        table_of_contents = Extractor.get_table_of_contents(self.url, self.cookie)
        dic = Extractor.get_units_from_toc(table_of_contents, self.cookie)
        return dic

    def get_units_info_from_toc(self):
        unit_title_list = []
        unit_dic = self.get_units_from_toc()      
        for key, value in unit_dic.items():
            # unit_title_list.append(f"{value['content']['displayName']} {value['content']['title']}")
            element = (key, f"{value['content']['displayName']} {value['content']['title']}")
            unit_title_list.append(element)
        return unit_title_list, unit_dic
    
    def get_modules_info_from_unit(self, unit_data):
        module_title_list = []
        element = None
        module_dic = self.get_modules_from_unit(unit_data)
        for key, value in module_dic.items():
            # module_title_list.append(value['title'])
            element = (key, value['title'])
            module_title_list.append(element)

        return module_title_list, module_dic

    def get_modules_from_unit(self, unit_data):
        return Extractor.get_modules_from_unit(unit_data, self.cookie)        
    
    def get_mcqs_from_module(self, unit_data, start, end) ->str:
        return Extractor.get_mcqs_from_modules(unit_data, self.cookie, start, end)        
    
    def get_simulations_from_modules(self, unit_data, start, end) ->str:
        return Extractor.get_simulations_from_modules(unit_data, self.cookie, start, end)

    def get_mcsqs(self) -> str:
        parse_result = ""            
        # table_of_contents = self.__get_table_of_contents()
        table_of_contents = Extractor.get_table_of_contents(self.url, self.cookie)
        
        # check toc is existing to make sure that parsing is successful 
        if not table_of_contents:
            return parse_result
        

        parse_result = Extractor.get_mcqs_from_units(table_of_contents, self.cookie)

        # #top level like F1-F10
        # for d in table_of_contents['status']['units']:
        #     #title of unit
        #     unit_url = f"https://cpa.becker.com/rest/unit/{d['id']}"
        #     unit_response = requests.get(unit_url,cookies=self.cookie)    
        #     unit_data = json.loads(unit_response.text)    
        #     unit_title = f"{unit_data['content']['displayName']} {unit_data['content']['title']} ({unit_data['content']['variantName']})"
            
        #     parse_result += f"{SEPERATOR_UNIT}{unit_title}\n{SEPERATOR_UNIT}"

        #     parse_result += Extractor.get_modules_from_unit(unit_data, self.cookie)

        #     # i = 0
        #     # #modules of unit
        #     # for module_content in unit_data['content']['modulesContent']:
        #     #     module_title = f"{module_content['displayName']} {module_content['title']}"
        #     #     module_id = module_content['id']
        #     #     module_mcqs_url = f"https://cpa.becker.com/rest/question/search?moduleId={module_id}&filter=0&context=homework"
        #     #     module_mcqs_response = requests.get(module_mcqs_url,cookies=self.cookie)
                
        #     #     parse_result += f"{SEPERATOR_MODULE}{module_title}\n{SEPERATOR_MODULE}"
  
        #     #     mcqs_data = json.loads(module_mcqs_response.text)
                
        #     #     parse_result += Extractor.get_mcqs_from_module(mcqs_data,self.cookie)

        #     #     # #mcsq of module
        #     #     # for question_id in mcqs_data['questionIds']:
        #     #     #     question_url = f"https://cpa.becker.com/rest/question/{question_id}"
        #     #     #     question_response = requests.get(question_url,cookies=self.cookie)
                    
        #     #     #     question_data = json.loads(question_response.text)
        #     #     #     question_content = html2text.html2text(question_data['content']['body'])
                    
        #     #     #     question_options_header = html2text.html2text(question_data['content']['optionsHeader'])

        #     #     #     question_options_list = question_data['content']['optionTexts']
        
        #     #     #     question_options_list = [html2text.html2text(x).replace('\n\n','\n') for x in question_options_list]
        #     #     #     question_options_list[0] = f"A. {question_options_list[0]}"
        #     #     #     question_options_list[1] = f"B. {question_options_list[1]}"
        #     #     #     question_options_list[2] = f"C. {question_options_list[2]}"
        #     #     #     question_options_list[3] = f"D. {question_options_list[3]}"
                    
        #     #     #     question_options = ''.join(question_options_list)
        #     #     #     if question_options_header.strip():
        #     #     #         question_options = question_options_header + question_options
                        
        #     #     #     question_explanations = html2text.html2text(' '.join(question_data['content']['explanations'])).replace('|','').replace('\n\n\n','\n').replace('#1#','A').replace('#2#','B').replace('#3#','C').replace('#4#','D')
        #     #     #     i += 1
        #     #     #     question_final = f"{i}. (MCQ-{question_id})\n{question_content}{question_options}"
        #     #     #     print(f"{question_final}\n▲ Explanation \n\n{question_explanations}")
        #     #     #     parse_result += f"{question_final}\n▲ Explanation \n\n{question_explanations}"
        #     #     i = 0
        
        return parse_result