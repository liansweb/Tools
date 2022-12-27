import os
import re
import base64
import json
import requests
import sys
import time
import yaml

requests.packages.urllib3.disable_warnings()


class fofaQuery:

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

    def __init__(self):
        yamlPath = "./control.yaml"
        with open(yamlPath, "r") as fp:
            load = yaml.safe_load(fp)
            self.email = load['email']
            self.key = load['key']
            self.page = load['page']
            self.fields = load['fields'] + ",host"  # 加上host参数、protocol 默认属性是http
            self.fieldsJoin = load['fieldsJoin']
            self.full = load['full']
            self.sleep = load['sleep']
            self.size = load['size']
            self.url = load['url']
            self.query = load['query']
            self.resultSuffix = load['resultSuffix']

    def countryQuery(self):
        path = "countryName/国家名称及简写.yaml"
        with open(path, "r") as fp:
            load = yaml.safe_load(fp)
            return load

    def queryExpression(self, query):
        loadDict = self.countryQuery()
        quertCountryDict = {}
        for i in loadDict.keys():
            if loadDict[i]:
                joinCountry = query + f'&& country ="{loadDict[i]}"'
                bytesString = joinCountry.encode(encoding="utf-8")
                # base64 编码
                encodestr = str(base64.b64encode(bytesString))[2:-1]
                quertCountryDict[i] = encodestr

        return quertCountryDict

    def countryQuery(self):
        path = "countryName/国家名称及简写.yaml"
        with open(path, "r") as fp:
            load = yaml.safe_load(fp)
            return load

    def queryRequests(self, queryEncodestrDict):
        for i in queryEncodestrDict:
            time.sleep(self.sleep)
            jsonRespResultDict = {}
            print(f"\033[0;32m[+] 搜索: {i} 目标  \033[0m")
            queryEncodestr = queryEncodestrDict[i]

            reqQuery = f"{self.email}&key={self.key}&qbase64={queryEncodestr}&fields={self.fields}&full={self.full}&page={self.page}&size={self.size}"
            url = f"{self.url}+{reqQuery}"
            resp = requests.get(url=url, verify=False)
            try:
                jsonRespResultList = json.loads(resp.text)['results']
            except:
                self.queryError(resp.text)
                continue
            lenRespResults = len(jsonRespResultList)
            if lenRespResults == 0:
                print(f"\033[0;31m[!] 目标: {i} 未获取到结果  \033[0m")
                continue
            else:
                jsonRespResultDict[i] = jsonRespResultList
                print(f"\033[0;32m[+] 获取到: {i} 目标结果  \033[0m")
                self.queryResult(jsonRespResultDict)

    def queryResult(self, responseDict):
        for i in responseDict.keys():
            self.queryResultJoinUrl(responseDict[i], i)

    def queryResultJoinUrl(self, responseList, txtName):
        writePath = "countryQueryResult/" + str(txtName) + '.' + self.resultSuffix
        self.isFileBoolean(writePath)
        reduce_joinUrl = {}  # 去重
        for i in range(len(responseList)):
            listI = responseList[i]
            joinUrl = ""
            fieldsJoinDict = {}
            fieldsJoinStr = self.fieldsJoin

            for k in range(len(listI)):
                q = '$' + str(k + 1)
                fieldsJoinDict[q] = listI[k]

            for d in fieldsJoinDict.keys():
                joinUrl = fieldsJoinStr.replace(d, fieldsJoinDict[d])
                fieldsJoinStr = joinUrl

            if reduce_joinUrl.get(joinUrl):
                continue
            else:
                reduce_joinUrl[joinUrl] = True
                self.queryResultWrite(joinUrl, writePath)

        print(f"\033[0;32m[+] 查询结果写入文件: {writePath} \033[0m")

    def queryResultWrite(self, joinUrl, writePath):
        with open(writePath, "a") as fp:
            fp.writelines(joinUrl + "\n")

    def isFileBoolean(self, writePath):
        isFileBoolean = os.path.isfile(writePath)
        if isFileBoolean:
            print(f"\033[0;31m[!] 删除已存在文件: {writePath}  \033[0m")
            os.remove(writePath)

    def queryOne(self, query, controlPath):
        if self.query:
            if query == self.query:
                print(f"\033[0;32m[+] 查询表达式为: {query} \033[0m")
            else:
                uesrQuery = input(f"""

\033[0;32m[+] 检测到查询表达式发生变化: \033[0m
    \033[0;32m[+] 上次查询表达式为 : {self.query} \033[0m
    \033[0;32m[+] 本次查询表达式为 : {query} \033[0m

请确认您的选择：
    1.清除上次查询结果；
    2.撤销当前查询;
    3.不清除上次查询结果。
                """)
                try:
                    uesrQuery = int(uesrQuery)
                except:
                    print(f"\033[0;31m[!] 当前选择为: {uesrQuery} , 请正确选择,程序退出 \033[0m")
                    exit()
                if uesrQuery == 1:
                    print(f"\033[0;31m[!] 当前选择为: 清除上次查询结果 , 查询表达式为: {query} \033[0m")
                    self.delFile("countryQueryResult")
                    self.queryWriteYaml(controlPath, query)
                elif uesrQuery == 2:
                    print(f"\033[0;31m[!] 当前选择为: 撤销当前查询 , 程序退出 \033[0m")
                    exit()
                elif uesrQuery == 3:
                    print(f"\033[0;32m[+] 当前选择为: 不清除上次查询结果 ,查询表达式为: {query} \033[0m")
                    self.queryWriteYaml(controlPath, query)
                else:
                    print(f"\033[0;31m[!] 当前选择为: {uesrQuery} , 请正确选择,程序退出 \033[0m")
                    exit()
        else:
            print(f"\033[0;32m[+] 查询表达式为: {query} \033[0m")
            self.queryWriteYaml(controlPath, query)

    def delFile(self, pathData):
        print(f"\033[0;31m[!] 查询表达式改变,清除 {pathData} 目录下所有文件  \033[0m")
        for i in os.listdir(pathData):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = pathData + "/" + i  # 当前文件夹的下面的所有东西的绝对路径
            if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                os.remove(file_data)

    def queryWriteYaml(self, controlPath, query):
        print(f"\033[0;32m[+] 修改: {controlPath} 配置文件,修改后的查询表达式为: {query} \033[0m")
        with open(controlPath, 'r', encoding='utf-8') as fp:  # print(f.read())
            result = fp.read()
            queryExp = yaml.load(result, Loader=yaml.FullLoader)
            queryExp['query'] = query
            with open(controlPath, 'w', encoding='utf-8') as fpn:  # 覆盖原先的配置文件
                yaml.dump(queryExp, fpn)

    def queryError(self, respError):
        if re.search("Account\s+Invalid", respError):
            print(f"""
\033[0;31m[!] 无效账户 :  \033[0m

    \033[0;31m[!] 邮箱号  :  {self.email} \033[0m
    \033[0;31m[!] key    :  {self.key} \033[0m

\033[0;31m[!] 程序退出 \033[0m
            """)
            exit()
        elif re.search("Coins\s+Insufficient\s+Balance", respError):
            print(f"""
\033[0;31m[!] 账户余额不足 :  \033[0m

    \033[0;31m[!] 邮箱号 :  {self.email} \033[0m
    \033[0;31m[!] key    :  {self.key} \033[0m

\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        elif re.search("Rule\s+do\s+not\s+exist", respError):
            print(f"""
\033[0;31m[!] 规则不存在 :  \033[0m
    \033[0;31m[!] 响应如下 : {respError}  \033[0m
\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        elif re.search("FOFA\s+Query\s+Syntax\s+Incorrect", respError):
            print(f"""
\033[0;31m[!] FOFA语法错误 :  \033[0m
    \033[0;31m[!] 响应如下 : {respError}  \033[0m
\033[0;31m[!] 程序退出 \033[0m
                        """)
            exit()
        else:
            print(f"\033[0;31m[!] 查询出错: {respError}  \033[0m")

    def main(self, query):
        controlPath = "control.yaml"
        self.queryOne(query, controlPath)
        queryEncodestrDict = self.queryExpression(query)
        self.queryRequests(queryEncodestrDict)


if __name__ == '__main__':
    start = fofaQuery()
    start.title()
    query = sys.argv[1]
    start.main(query)