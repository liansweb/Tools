import  requests
import  yaml
import  os
import  re
import  sys
import  time


requests.packages.urllib3.disable_warnings()

class checkTarget:

    def title(self):
        print(f"""
        
                quick check

配置文件信息如下:
    目标dir      :    \033[0;34m {self.targetDir} \033[0m
    目标path     :    \033[0;34m {self.targetPath} \033[0m
    请求method   :    \033[0;34m {self.targetMethod} \033[0m
    超时time     :    \033[0;34m {self.targetTimeout} \033[0m
    输出dir      :    \033[0;34m {self.targetOutputDir} \033[0m
    匹配data     :    \033[0;34m {self.targetReExpression} \033[0m
                
        """)

    def readYaml(self,yamlPath):
        print(yamlPath)
        with open(yamlPath, "r") as fp:
            load = yaml.safe_load(fp)
            self.targetDir = load['targetDir']
            self.targetPath = load['targetPath']
            self.targetReExpression = load['targetReExpression']
            self.targetMethod = load['targetMethod']
            self.targetHeaders = load['targetHeaders']
            self.targetJson = load['targetJson']
            self.targetData = load['targetData']
            self.targetTimeout = load['targetTimeout']
            self.targetProfixs = load['targetProfixs']
            self.targetAllowRedirects = load['targetAllowRedirects']
            self.verify = False
            self.targetOutputDir = load['targetOutputDir']
            self.targetRestText = load['targetRestText']

    def outPutDirTarget(self,dirPath):
        path = dirPath.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(f"\033[0;32m[+] 输出目录: {path} 创建成功  \033[0m")
        else:
            print(f"\033[0;33m[+] 输出目录: {path} 已存在  \033[0m")

    def outPutFileTarget(self,dirPath,targetFilePath,requestsTargetDict):
        targetFilePath = re.search("[^/]+\.txt",targetFilePath)[0]
        if re.match(".*/",dirPath):
            targetFilePath = dirPath + targetFilePath
        else:
            targetFilePath = dirPath +"/"+ targetFilePath
        print(f"\033[0;32m[+] 写入文件 : {targetFilePath}   \033[0m")
        with open(targetFilePath,"w") as fp:
            print(requestsTargetDict)
            for i in requestsTargetDict.keys():
                fp.writelines(requestsTargetDict[i]+"\n")

    def respTarget(self,respText):
        respTargetDict = {}
        targetReExpression = self.targetReExpression
        if targetReExpression:
            respTargetCheck = None
            for i in targetReExpression.keys():
                if re.search(str(targetReExpression[i]),str(respText[i]),re.I):
                    respTargetCheck = True
                else:
                    respTargetCheck = False
            if respTargetCheck and respTargetCheck == True:
                respTargetDict['code'] = "自定义表达式匹配成功"

            else:
                respTargetDict['code'] = "自定义表达式匹配失败"
        else:
            respTargetDict['code'] = "未配置自定义表达式"

        return respTargetDict

    def requestsTarget(self,i,targetPath):
        requestsTargetDict = {}
        respDict = {}
        # 获得请求方法
        respStop = False
        requestsMethod = self.targetMethod

        # 判断是否有请求方法
        if hasattr(requests, requestsMethod):
            # 反射获取请求方法
            sendRequestsMethod = getattr(requests, requestsMethod)

            # TODO 异常处理
            try:
                resp = sendRequestsMethod(url=targetPath, headers=self.targetHeaders,
                                          json=self.targetJson, data=self.targetData,
                                          proxies=self.targetProfixs, verify=self.verify,
                                          allow_redirects=self.targetAllowRedirects,
                                          timeout=self.targetTimeout)
            except Exception:
                respStop  = True

            if respStop == False:

                respDict["respStatusCode"] = resp.status_code
                respDict["respHeaders"] = resp.headers
                respDict["respBody"] = resp.text
                respTargetDict = self.respTarget(respDict)
                if respTargetDict['code'] != "自定义表达式匹配失败":
                    requestsTargetDict[i] = targetPath
                    print(f"\033[0;32m[+] 目标匹配成功 : {targetPath}   \033[0m")
                    if self.targetRestText == 1 or self.targetRestText == True:
                        print(resp.text)
                    elif self.targetRestText == 2:
                        print(resp.headers)
                        print(resp.text)
                    elif self.targetRestText == 3:
                        print(resp.headers)
                else:
                    print(f"\033[0;33m[!] 目标匹配失败 : {targetPath}   \033[0m")
                    if self.targetRestText == True:
                        print(resp.text)
            else:
                print(f"\033[0;31m[!] 目标请求失败 : {targetPath}   \033[0m")
        else:
            print(f"\033[0;36m[!] 请求方法为小写 : {targetPath}   \033[0m")

        return requestsTargetDict

    def requestsFileTargetJoin(self,readFileList:list,targetFile):
        targetInitPath = self.targetPath
        requestsFileTargetJoinDict = {}
        print(f"\033[0;32m[+] 包含目标地址 : {len(readFileList)} 条  \033[0m")
        for i  in readFileList :
            i = i.rstrip('\n')
            if targetInitPath :
                targetPath = i+ targetInitPath
            else:
                targetPath = i
            requestsTargetDict = self.requestsTarget(i,targetPath)
            requestsFileTargetJoinDict.update(requestsTargetDict)

        if len(requestsFileTargetJoinDict) != 0:
            print(f"\033[0;32m[+] 匹配成功目标 : {len(requestsFileTargetJoinDict)} 条  \033[0m")
            self.outPutFileTarget(self.targetOutputDir,targetFile,requestsFileTargetJoinDict)


    def readTargetFile(self,filesList:list):
        for i in filesList:
            readFileList = []
            print(f"\033[0;32m[+] 正在读取 : {i} 文件中目标  \033[0m")
            with open(i,"r") as fp:
                readFileList = fp.readlines()
            self.requestsFileTargetJoin(readFileList,i)


    def dirTarget(self):
        targetDir  = self.targetDir
        filesList = []
        for dirpath, dirnames, filenames in os.walk(targetDir):
            for i in filenames:
                filePath = targetDir + i
                filesList.append(filePath)
        print(f"\033[0;32m[+] 读取目标文件路径成功 : {filesList}  \033[0m")
        return filesList


    def main(self):
        yamlPath = sys.argv[1]
        self.readYaml(yamlPath)
        self.title()
        self.outPutDirTarget(self.targetOutputDir)
        fileList  = self.dirTarget()
        readFileList = self.readTargetFile(fileList)


if __name__ == '__main__':
    now = time.time()
    target = checkTarget()
    target.main()
    end = time.time()
    print(f"\033[0;32m[+] 最终耗时:", end - now, "\033[0m")