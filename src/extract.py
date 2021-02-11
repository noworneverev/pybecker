import requests
from bs4 import BeautifulSoup
import os
import json
import html2text
import browser_cookie3
import pandas as pd
import re
from type.subject import SubjectType
from util.constant import URL_FAR, URL_AUD, URL_REG, URL_BEC, SUCCESS_CODE, SEPERATOR_UNIT, SEPERATOR_MODULE, SEPERATOR_HEADER_QUESTION, SEPERATOR_FOOTER_QUESTION, SEPERATOR_HEADER_EXPLANATION, SEPERATOR_FOOTER_EXPLANATION

PATTERN = re.compile(r'<table(.*?)</table>')

class Extractor:
    @staticmethod
    def get_response(url, cookie):
        return requests.get(url, cookies=cookie)
        
    @staticmethod
    def get_table_of_contents(url, cookie):
        table_of_contents = {}
        response = Extractor.get_response(url, cookie)
        
        if response.status_code == 200:
            table_of_contents = json.loads(response.text)

        return table_of_contents
    
    @staticmethod
    def is_api_available(url, cookie) -> bool:
        result = False        
        response = Extractor.get_response(url, cookie)        
        return response.status_code == 200

    ###############################################################################################pure data
    @staticmethod
    def get_units_from_toc(table_of_contents,cookie) -> dict:
        result_dic = {}
        for d in table_of_contents['status']['units']:
            unit_url = f"https://cpa.becker.com/rest/unit/{d['id']}" # dropdownsource
            unit_response = requests.get(unit_url,cookies=cookie)    
            unit_data = json.loads(unit_response.text)   
            result_dic[d['id']] = unit_data
        return result_dic
    
    @staticmethod
    def get_modules_from_unit(unit_data: dict, cookie) -> dict:
        result_dic = {}
        for module_content in unit_data['content']['modulesContent']:
            module_title = f"{module_content['displayName']} {module_content['title']}"
            module_id = module_content['id']
            module_mcqs_url = f"https://cpa.becker.com/rest/question/search?moduleId={module_id}&filter=0&context=homework"
            module_mcqs_response = requests.get(module_mcqs_url,cookies=cookie)                        
            mcqs_data = json.loads(module_mcqs_response.text)
            mcqs_data['title'] = module_title
            result_dic[module_id] = mcqs_data
   
        return result_dic

    ###############################################################################################

    @staticmethod
    def get_mcqs_from_units(table_of_contents,cookie):
    #def get_units_from_toc(table_of_contents,cookie):
        """
        units of a subject
        """
        result_units = ''
        for d in table_of_contents['status']['units'][0:1]:
            #title of unit
            unit_url = f"https://cpa.becker.com/rest/unit/{d['id']}" # dropdownsource
            unit_response = requests.get(unit_url,cookies=cookie)    
            unit_data = json.loads(unit_response.text)    
            unit_title = f"{unit_data['content']['displayName']} {unit_data['content']['title']} ({unit_data['content']['variantName']})"            
            result_units += f"{SEPERATOR_UNIT}{unit_title}\n{SEPERATOR_UNIT}"

            result_units += Extractor.get_mcqs_from_modules(unit_data, cookie)
        
        return result_units

    @staticmethod
    def get_mcqs_from_modules(unit_data: dict, cookie, start, end) -> str:
        """
        modules of a unit
        """
        result_modules = ''
        for module_content in unit_data['content']['modulesContent'][start:end]:
            module_title = f"{module_content['displayName']} {module_content['title']}"
            module_id = module_content['id']
            module_mcqs_url = f"https://cpa.becker.com/rest/question/search?moduleId={module_id}&filter=0&context=homework"
            module_mcqs_response = requests.get(module_mcqs_url,cookies=cookie)            
            result_modules += f"{SEPERATOR_MODULE}{module_title}\n{SEPERATOR_MODULE}"
            mcqs_data = json.loads(module_mcqs_response.text)
            
            result_modules += Extractor.get_mcqs_from_module(mcqs_data,cookie)
            
        return result_modules

    @staticmethod
    def get_mcqs_from_module(mcqs_data: dict, cookie) -> str:
        """
        mcqs of a module
        """        
        result_mcqs = ''
        question_url = ''
        question_response = None
        question_data = {}
        question_content = ''
        question_options = ''
        question_explanations = ''
        question_final = ''
        question_answer = ''

        i = 0 # index of mcq

        for question_id in mcqs_data['questionIds']:
            question_url = f"https://cpa.becker.com/rest/question/{question_id}"
            question_response = requests.get(question_url,cookies=cookie)                      
            question_data = json.loads(question_response.text)

            # Clean up the content of a question
            question_content = Extractor.get_clean_question_content(question_data)

            # Clean up the options of a question
            question_options = Extractor.get_clean_options(question_data)

            # Clean up the explanations of a question
            question_explanations = Extractor.get_clean_explanations(question_data)
            
            # Get answer
            question_answer = Extractor.get_answer(question_data)

            from type.color import Color
                
            # question_explanations = html2text.html2text(' '.join(question_data['content']['explanations'])).replace('|','').replace('\n\n\n','\n').replace('#1#','A').replace('#2#','B').replace('#3#','C').replace('#4#','D')
            i += 1
            question_final = f"{i}. (MCQ-{question_id})\n{question_content}{question_options}"
            # print(f"{question_final}\n▲ Explanation \n\n{question_explanations}")
            # result_mcqs += f"{question_final}\n{Color.BOLD}▲ Choice {question_answer} is correct. Explanation: {Color.END}\n\n{question_explanations}"
            result_mcqs += f"{question_final}\n▲ Choice {question_answer} is correct. Explanation:\n\n{question_explanations}"

        return result_mcqs
    
    @staticmethod
    def get_simulations_from_modules(unit_data: dict, cookie, start, end) -> str:        
        result_modules = ''
        for module_content in unit_data['content']['modulesContent'][start:end]:
            if module_content['homeworkSimTasks']:
                module_title = f"{module_content['displayName']} {module_content['title']}"
                module_id = module_content['id']
                module_simulation_url = f"https://cpa.becker.com/rest/module/{module_id}/simulationTasks"
                module_simulations_response = requests.get(module_simulation_url,cookies=cookie)       
                # module_mcqs_url = f"https://cpa.becker.com/rest/question/search?moduleId={module_id}&filter=0&context=homework"
                # module_mcqs_response = requests.get(module_mcqs_url,cookies=cookie)            
                
                result_modules += f"\n{SEPERATOR_MODULE}{module_title}\n{SEPERATOR_MODULE}"
                # mcqs_data = json.loads(module_mcqs_response.text)
                # simulations_data = json.loads(module_simulations_response.text)
                simulations_data = module_simulations_response.text
                
                # result_modules += Extractor.get_mcqs_from_module(mcqs_data,cookie)
                # result_modules += simulations_data
                result_modules += simulations_data
                result_modules += '\n'
            
        return result_modules

    
    @staticmethod
    def get_clean_question_content(question_data: dict) -> str:
        question_content = ''                
        raw_html_question_content = question_data['content']['body']
        question_table_list = []

        pd.set_option('display.float_format', lambda x: f'{x:,.0f}')
        is_table_existed = '</table>'.upper() in str(raw_html_question_content).upper() and '<table'.upper() in str(raw_html_question_content).upper()
        if is_table_existed:
            question_table_list = Extractor.convert_html_table_to_readable_table(raw_html_question_content, SEPERATOR_HEADER_QUESTION, SEPERATOR_FOOTER_QUESTION)
            raw_question_content = PATTERN.sub("", raw_html_question_content.replace('\n',''))                
            question_content = html2text.html2text(raw_question_content).replace('\n','')

            for tb in question_table_list:
                question_content += tb

        else:
            question_content = html2text.html2text(question_data['content']['body'])

        return question_content

    @staticmethod
    def convert_html_table_to_readable_table(html_table: str, separator_header: str, separator_footer: str) -> list:
        table_element = ""
        tmp_table = ""            
        table_list = []
        try:
            dfs = pd.read_html(html_table)
            for df in dfs:
                df.rename(columns={"Unnamed: 0": ""},inplace=True)
                df.fillna('', inplace=True)
                tmp_table = df.to_string(index=False)            
                table_element += separator_header
                table_element += f"{tmp_table}\n"
                table_element += separator_footer
                table_list.append(table_element)
        except:
            pass
           
        return table_list

    @staticmethod
    def get_clean_options(question_data: dict) -> str:
        question_options = ''        
        question_options_header = question_data['content']['optionsHeader']
        question_options_list = question_data['content']['optionTexts']
        modified_question_options_list = []

        if question_options_header:
            soup = BeautifulSoup(question_options_header,'lxml')
            header_th = soup.find_all('th')
            header_td = soup.find_all('td')
            all_header = header_th + header_td
            question_options = '| '.join([x.text.replace('\n\n',' ') for x in all_header]) + '\n'
        
            for option in question_options_list:
                soup_option = BeautifulSoup(option,'lxml')
                tmp_option = soup_option.find_all('td')                    
                modified_question_options_list.append(' '.join([x.text.replace('\n','') for x in tmp_option]))

            modified_question_options_list[0] = f"A. {modified_question_options_list[0]}\n"
            modified_question_options_list[1] = f"B. {modified_question_options_list[1]}\n"
            modified_question_options_list[2] = f"C. {modified_question_options_list[2]}\n"
            modified_question_options_list[3] = f"D. {modified_question_options_list[3]}\n"
            question_options += ''.join(modified_question_options_list)

        else:            
            question_options_list = [html2text.html2text(x).replace('\n\n','\n') for x in question_options_list]
            question_options_list[0] = f"A. {question_options_list[0]}"
            question_options_list[1] = f"B. {question_options_list[1]}"
            question_options_list[2] = f"C. {question_options_list[2]}"
            question_options_list[3] = f"D. {question_options_list[3]}"
        
            question_options = ''.join(question_options_list)
        
        return question_options

    @staticmethod
    def get_clean_explanations(question_data: dict) -> str:    
        raw_html_list = [x.replace('\n','').replace('#1#','A').replace('#2#','B').replace('#3#','C').replace('#4#','D') for x in question_data['content']['explanations'] if x]
        html_explanations = ''.join(raw_html_list)

        html_explanations_without_table = ''
        question_explanations = ''
        explanation_table_list = []        
        if '</table>' in html_explanations:
            explanation_table_list = Extractor.convert_html_table_to_readable_table(html_explanations, SEPERATOR_HEADER_EXPLANATION, SEPERATOR_FOOTER_EXPLANATION)
            html_explanations_without_table = PATTERN.sub("", html_explanations)
            question_explanations = html2text.html2text(html_explanations_without_table)
            for tb in explanation_table_list:
                question_explanations += tb     
                        
        else:
            question_explanations_list = [html2text.html2text(x) for x in raw_html_list if x]            
            question_explanations = '\n'.join(question_explanations_list).replace('\n\n','\n')
            question_explanations += '\n'
        return question_explanations

    @staticmethod
    def get_answer(question_data: dict) -> str:
        answer_index = question_data['content']['correctOptionIndex']
        answer = ''
        if answer_index == 1:
            answer = 'A'
        elif answer_index == 2:
            answer = 'B'
        elif answer_index == 3:
            answer = 'C'
        elif answer_index == 4:
            answer = 'D'
        return answer