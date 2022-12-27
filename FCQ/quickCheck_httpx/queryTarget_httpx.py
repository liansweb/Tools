import re
import httpx
import asyncio
import time
import yaml
import sys
import string
import os

class queryTarget():
    def title(self):
        print(f"""

                    quick check

Yaml POC 信息:
    目标dir      :    \033[0;34m {self.poc_targetDir} \033[0m
    目标path     :    \033[0;34m {self.poc_targetPath} \033[0m
    请求method   :    \033[0;34m {self.poc_targetMethod} \033[0m
    超时time     :    \033[0;34m {self.poc_targetTimeout} \033[0m
    输出dir      :    \033[0;34m {self.poc_targetOutputDir} \033[0m
    匹配data     :    \033[0;34m {self.poc_targetReExpression} \033[0m

            """)

    # 请求目录下全部文件
    def removePutDirTarget(self,dirPath):
        self.readOsPath(dirPath)
        for i in self.filesList:
            os.remove(i)

    # 创建输出目录、目录存在、清楚目录下所有文件
    def outPutDirTarget(self,dirPath):
        path = dirPath.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(f"\033[0;32m[+] 输出目录: {path} 创建成功  \033[0m")
        else:
            print(f"\033[0;33m[*] 输出目录: {path} 已存在  \033[0m")
            self.removePutDirTarget(dirPath)

    # 创建输出文件
    def writeFile(self,filePath,successfulTarget:list):
        if successfulTarget :
            filePath = re.search("/(\w+\.\w+)",filePath)[1]
            targetOutputDir = self.poc_targetOutputDir + filePath
            print(f"\033[0;32m[+] 请求成功 : {len(successfulTarget)} 条  \033[0m")
            self.numSuccessTarget = self.numSuccessTarget + len(successfulTarget)
            print(f"\033[0;32m[+] 写入文件 : {targetOutputDir}   \033[0m")
            with open(targetOutputDir,"w") as fp:
                for i in successfulTarget:
                    fp.writelines(i)

    # 读取yaml文件
    def readYaml(self,yamlPath:string):
        with open(yamlPath,"r") as fp:
            return  yaml.safe_load(fp)

    # 获取PocYaml中的配置项
    def readPocYaml(self,pocYaml:string):
        pocYamlDict = self.readYaml(yamlPath=pocYaml)
        self.poc_targetPath = pocYamlDict["targetPath"]
        self.poc_targetMethod = pocYamlDict["targetMethod"]
        self.poc_targetTimeout = pocYamlDict["targetTimeout"]
        self.poc_targetProfixs = pocYamlDict["targetProfixs"]
        self.poc_targetAllowRedirects = pocYamlDict["targetAllowRedirects"]
        self.poc_targetHeaders = pocYamlDict["targetHeaders"]
        self.poc_targetJson = pocYamlDict["targetJson"]
        self.poc_targetData = pocYamlDict["targetData"]
        self.poc_targetReExpression = pocYamlDict["targetReExpression"]
        self.poc_targetDir = pocYamlDict["targetDir"]
        self.poc_targetOutputDir = pocYamlDict["targetOutputDir"]
        self.poc_targetRestText = pocYamlDict["targetRestText"]

    # 初始化程序 获取congfig.yaml中的配置项
    def __init__(self):
        yamlPath = "./config.yaml"
        configYaml = self.readYaml(yamlPath)
        self.config_proxies = configYaml["proxies"]
        self.config_timeout = configYaml["timeout"]
        self.config_follow_redirects = configYaml["follow_redirects"]
        self.config_headers = configYaml["headers"]
        self.config_cookies = configYaml["cookies"]
        self.successfulTarget = None
        self.numAllTarget = 0
        self.numSuccessTarget = 0

    # 获取目录下所有文件
    def readOsPath(self,dirPath):
        targetDir = dirPath
        filesList = []
        for dirpath, dirnames, filenames in os.walk(targetDir):
            for i in filenames:
                filePath = targetDir + i
                filesList.append(filePath)
        print(f"\033[0;32m[+] 读取目标文件路径成功 : {filesList}  \033[0m")
        self.filesList = filesList

    # 发送请求及响应匹配
    async def req(self,url):
        self.successfulTarget = []
        ReExpression = {}
        if self.poc_targetPath:
            url = url.rstrip() + self.poc_targetPath
        try:
            async with httpx.AsyncClient(proxies=self.config_proxies, timeout=self.config_timeout, headers=self.config_headers,follow_redirects=self.config_follow_redirects,cookies=self.config_cookies) as client:
                res = await client.request(method=str.lower(self.poc_targetMethod), url=url,headers=self.poc_targetHeaders,data=self.poc_targetData,json=self.poc_targetJson,timeout=self.poc_targetTimeout,follow_redirects=self.poc_targetAllowRedirects)
                ReExpression["respStatusCode"] = res.status_code
                ReExpression["respHeaders"] = str(res.headers)
                ReExpression["respBody"] = str(res.text)
        except Exception as e:
            print(f"\033[0;31m[!] 目标请求失败 : {url}   \033[0m")

        # 匹配模块
        self.ReExpression = ReExpression
        if self.ReExpression :
            reBoolean = None
            # TODO 只能匹配单个、需要实现多个
            if self.poc_targetReExpression :
                if self.ReExpression["respStatusCode"] == self.poc_targetReExpression["respStatusCode"]:
                    reBoolean = True
                    for i in self.poc_targetReExpression.keys():
                        if i == "respStatusCode":
                            continue
                        if self.poc_targetReExpression[i]:
                            if re.search(self.poc_targetReExpression[i],self.ReExpression[i]):
                                reBoolean = True
                            else:
                                reBoolean = False
                                break
                        else:
                            reBoolean = True
                            break
            else:
                reBoolean = True

            # 获取匹配结果
            if reBoolean:
                print(f"\033[0;32m[+] 目标匹配成功 : {url}   \033[0m")
                self.successfulTarget.append(url)

            else:
                print(f"\033[0;33m[*] 目标匹配失败 : {url}   \033[0m")

            # 打印输出 TODO 输出格式美化
            if self.poc_targetRestText is True:
                print(ReExpression["respStatusCode"])
            elif self.poc_targetRestText == 1:
                print(ReExpression["respStatusCode"])
                print(ReExpression["respHeaders"])
            elif self.poc_targetRestText == 2:
                print(ReExpression["respStatusCode"])
                print(ReExpression["respHeaders"])
                print(ReExpression["respBody"])


    # 并发请求
    async def reqTask(self):

        filesList = self.filesList
        tasks = []
        for i in filesList:
            filePath = i
            print(f"\033[0;32m[+] 正在读取 : {i} 文件中目标  \033[0m")
            # 读取文件目标、发起请求
            with open(filePath, "r") as fp:
                a = fp.readlines()
            print(f"\033[0;32m[+] 包含目标地址 : {len(a)} 条  \033[0m")
            self.numAllTarget = self.numAllTarget + len(a)
            for i in range(len(a)):  # 控制并发量，现在是100
                task = asyncio.create_task(self.req(a[i]))
                tasks.append(task)
            await asyncio.wait(tasks)

            self.writeFile(filePath, self.successfulTarget)

    # 主程序
    def main(self):
        now = time.time()
        self.readPocYaml(sys.argv[1])
        self.title()
        self.outPutDirTarget(self.poc_targetOutputDir)
        self.readOsPath(self.poc_targetDir)
        asyncio.run(self.reqTask())
        end = time.time()
        print(f"\033[0;32m[+] 最终耗时 :", end - now, "\033[0m")
        print(f"\033[0;32m[+] 全部目标 :", self.numAllTarget, "\033[0m")
        print(f"\033[0;32m[+] 成功目标 :", self.numSuccessTarget, "\033[0m")

if "__main__" == __name__:
    start = queryTarget()
    start.main()