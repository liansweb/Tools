import os
import re
import base64
import json
import requests
import sys
import time
import yaml

requests.packages.urllib3.disable_warnings()

class FofaQuery:
    def __init__(self):
        with open("./control.yaml", "r") as fp:
            config = yaml.safe_load(fp)
            self.__dict__.update(config)
            self.fields += ",host"
    
    def title(self):
        print("""
__ __  __      __ __         ___ __       __      __ __     
|_ /  \|_ /\   /  /  \/  \|\ | | |__)\_/  /  \/  \|_ |__)\_/ 
|  \__/| /--\  \__\__/\__/| \| | | \  |   \_\/\__/|__| \  |  


Author:李安
            	""")
        print(f"""
配置文件信息如下：
    fofa email    :   \033[0;34m {self.email} \033[0m
    fofa key      :   \033[0;34m {self.key} \033[0m
    page          :   \033[0;34m {self.page} \033[0m
    fields        :   \033[0;34m {self.fields} \033[0m
    fieldsJoin    :   \033[0;34m {self.fieldsJoin} \033[0m
    sleep         :   \033[0;34m {self.sleep} \033[0m
    size          :   \033[0;34m {self.size} \033[0m
    resultSuffix  :   \033[0;34m {self.resultSuffix} \033[0m
            """)

    def country_query(self):
        with open("countryName/国家名称及简写.yaml", "r") as fp:
            return yaml.safe_load(fp)

    def query_expression(self, query):
        country_dict = self.country_query()
        return {
            i: base64.b64encode(f"{query} && country=\"{country}\"".encode()).decode()
            for i, country in country_dict.items() if country
        }

    def query_requests(self, query_encodestr_dict):
        for country, encoded_query in query_encodestr_dict.items():
            time.sleep(self.sleep)
            print(f"\033[0;32m[+] 搜索: {country} 目标  \033[0m")
            
            url = f"{self.url}+{self.email}&key={self.key}&qbase64={encoded_query}&fields={self.fields}&full={self.full}&page={self.page}&size={self.size}"
            resp = requests.get(url=url, verify=False)
            
            try:
                results = json.loads(resp.text)['results']
            except:
                self.query_error(resp.text)
                continue
            
            if not results:
                print(f"\033[0;31m[!] 目标: {country} 未获取到结果  \033[0m")
                continue
            
            print(f"\033[0;32m[+] 获取到: {country} 目标结果  \033[0m")
            self.query_result({country: results})

    def query_result(self, response_dict):
        for country, results in response_dict.items():
            self.query_result_join_url(results, country)

    def query_result_join_url(self, results, txt_name):
        write_path = f"countryQueryResult/{txt_name}.{self.resultSuffix}"
        self.is_file_boolean(write_path)
        unique_urls = set()
        for result in results:
            fields_dict = dict(enumerate(result, start=1))
            join_url = self.fieldsJoin.format(**fields_dict)
            if join_url not in unique_urls:
                unique_urls.add(join_url)
                self.query_result_write(join_url, write_path)

        print(f"\033[0;32m[+] 查询结果写入文件: {write_path} \033[0m")

    def query_result_write(self, join_url, write_path):
        with open(write_path, "a") as fp:
            fp.writelines(join_url + "\n")

    def is_file_boolean(self, write_path):
        if os.path.isfile(write_path):
            print(f"\033[0;31m[!] 删除已存在文件: {write_path}  \033[0m")
            os.remove(write_path)

    def query_one(self, query, control_path):
        if self.query:
            if query == self.query:
                print(f"\033[0;32m[+] 查询表达式为: {query} \033[0m")
            else:
                user_query = input(f"""

\033[0;32m[+] 检测到查询表达式发生变化: \033[0m
    \033[0;32m[+] 上次查询表达式为 : {self.query} \033[0m
    \033[0;32m[+] 本次查询表达式为 : {query} \033[0m

请确认您的选择：
    1.清除上次查询结果；
    2.撤销当前查询;
    3.不清除上次查询结果。
                """)
                try:
                    user_query = int(user_query)
                except:
                    print(f"\033[0;31m[!] 当前选择为: {user_query} , 请正确选择,程序退出 \033[0m")
                    exit()
                if user_query == 1:
                    print(f"\033[0;31m[!] 当前选择为: 清除上次查询结果 , 查询表达式为: {query} \033[0m")
                    self.del_file("countryQueryResult")
                    self.query_write_yaml(control_path, query)
                elif user_query == 2:
                    print(f"\033[0;31m[!] 当前选择为: 撤销当前查询 , 程序退出 \033[0m")
                    exit()
                elif user_query == 3:
                    print(f"\033[0;32m[+] 当前选择为: 不清除上次查询结果 ,查询表达式为: {query} \033[0m")
                    self.query_write_yaml(control_path, query)
                else:
                    print(f"\033[0;31m[!] 当前选择为: {user_query} , 请正确选择,程序退出 \033[0m")
                    exit()
        else:
            print(f"\033[0;32m[+] 查询表达式为: {query} \033[0m")
            self.query_write_yaml(control_path, query)

    def del_file(self, path_data):
        print(f"\033[0;31m[!] 查询表达式改变,清除 {path_data} 目录下所有文件  \033[0m")
        for file_name in os.listdir(path_data):
            file_path = os.path.join(path_data, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def query_write_yaml(self, control_path, query):
        print(f"\033[0;32m[+] 修改: {control_path} 配置文件,修改后的查询表达式为: {query} \033[0m")
        with open(control_path, 'r', encoding='utf-8') as fp:
            config = yaml.safe_load(fp)
            config['query'] = query
            with open(control_path, 'w', encoding='utf-8') as fpn:
                yaml.dump(config, fpn)

    def query_error(self, resp_error):
        if re.search("Account\s+Invalid", resp_error):
            print(f"""
\033[0;31m[!] 无效账户 :  \033[0m

    \033[0;31m[!] 邮箱号  :  {self.email} \033[0m
    \033[0;31m[!] key    :  {self.key} \033[0m

\033[0;31m[!] 程序退出 \033[0m
            """)
            exit()
        elif re.search("Coins\s+Insufficient\s+Balance", resp_error):
            print(f"""
\033[0;31m[!] 账户余额不足 :  \033[0m

    \033[0;31m[!] 邮箱号 :  {self.email} \033[0m
    \033[0;31m[!] key    :  {self.key} \033[0m

\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        elif re.search("Rule\s+do\s+not\s+exist", resp_error):
            print(f"""
\033[0;31m[!] 规则不存在 :  \033[0m
    \033[0;31m[!] 响应如下 : {resp_error}  \033[0m
\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        elif re.search("FOFA\s+Query\s+Syntax\s+Incorrect", resp_error):
            print(f"""
\033[0;31m[!] FOFA语法错误 :  \033[0m
    \033[0;31m[!] 响应如下 : {resp_error}  \033[0m
\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        else:
            print(f"\033[0;31m[!] 查询出错: {resp_error}  \033[0m")

    def main(self, query):
        control_path = "control.yaml"
        self.query_one(query, control_path)
        query_encodestr_dict = self.query_expression(query)
        self.query_requests(query_encodestr_dict)

if __name__ == '__main__':
    start = FofaQuery()
    start.title()
    query = sys.argv[1]
    start.main(query)