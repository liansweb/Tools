import feedparser
import ssl
import yaml
import requests
import sqlite3
import os
import logging
import urllib3
import time
import re
from sqlite3 import OperationalError
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class rssSpider:

    # acsill 字符背景
    def bannner(self):
        print(f"""

        8888888b.   .d8888b.   .d8888b.   .d8888b.  
        888   Y88b d88P  Y88b d88P  Y88b d88P  Y88b 
        888    888 Y88b.      Y88b.      Y88b.      
        888   d88P  "Y888b.    "Y888b.    "Y888b.   
        8888888P"      "Y88b.     "Y88b.     "Y88b. 
        888 T88b         "888       "888       "888 
        888  T88b  Y88b  d88P Y88b  d88P Y88b  d88P 
        888   T88b  "Y8888P"   "Y8888P"   "Y8888P"


                [*] :   Font: colossal 
                [*] :   RSSS version 1.0 
                [*] :   python3 rsss.py                                 
                [*] :   {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        """)        

    # 程序初始化
    def __init__(self,configYamlPath):
        self.bannner()
        logger.info("程序初始化")
        configDict = self.readConfigYaml(configYamlPath)
        try:
            # 获取飞书token
            self.feishuToken = configDict["feishuToken"]
            # 获取本地数据库文件名
            self.sqlDataName = configDict["sqlDataName"]
            # 获取数据库表名
            self.sqlTableName = configDict["sqlTableName"]
            # 获取数据库建表语句
            self.sqlCretaTable = configDict["sqlCretaTable"]
            # 创建数据库
            self.createSqlite(self.sqlDataName,self.sqlCretaTable)
            # 获取 filterSearch
            self.filterSearch = configDict["filterSearch"]
            self.rssPath = configDict["rssPath"]
        except KeyError as e:
            logger.info(e)
            print(f"config.yaml中缺少必有条件: {e},程序退出")
            exit()

    # 过滤条件匹配
    def filterNameSearch(self,title):
        if self.filterSearch is None:
            return True
        else:
            # 循环过滤条件
            for i in self.filterSearch:
                print("+====+",i,title)
                # 如果标题中存在需匹配的返回True
                if re.search(i,title, re.MULTILINE | re.IGNORECASE):
                    return True     
            return False    

    # 推送飞书请求
    def feishuRequests(self,a,rssName):
        url = self.feishuToken
        feiShuData = {
            "msg_type": "post",
            "content": {
            "post": {
            "zh_cn": {
                "title": f"{a[0]}",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": f"链接 : {a[1]}" + "\n"
                        },
                        {
                            "tag": "text",
                            "text": f"日期 : {a[2]}" + "\n"
                        },
                        {
                            "tag": "text",
                            "text": f"来源 : {rssName}" + "\n"
                        }
                    ]
                ]
                }
            }
            }
        }
        try:
            resp = requests.post(url=url,  json=feiShuData, verify=False)
            logger.info(resp.text)
        except requests.exceptions.Timeout as e:
            try:
                print("重新尝试,发送数据")
                time.sleep(3)
                resp = requests.post(url=url,  json=feiShuData, verify=False)
                logger.info(resp.text)
            except requests.exceptions.Timeout as e:
                print("请求超时,程序退出")
                exit()

    # 判断添加数据库
    def fsRequests(self,rssDict,rssName):
        logger.info("准备发送请求到飞书")
        reqLenCheck = 0
        for i in rssDict.keys():
            reqLen = len(rssDict[i])
            if reqLenCheck == 0:
                reqLenCheck = reqLen
                continue
        for i in range(reqLenCheck):
            a = []   
            for h in rssDict.keys():
                a.append(rssDict[h][i])
            if self.initSelectDataSqlite is True:
                if self.filterNameSearch(a[0]) is True:
                    self.insertDataSqlite(a[0],a[1],rssName,a[2])
                    self.feishuRequests(a,rssName=rssName)
                else:
                    continue
            else:
                if self.filterNameSearch(a[0]) is True:
                    if self.selectDataSqlite(column="link",link=a[1]) is True and self.selectDataSqlite(column="title",link=a[0]) is True:
                        self.insertDataSqlite(a[0],a[1],rssName,a[2])
                        self.feishuRequests(a,rssName=rssName)
                    else:
                        continue    
                else:
                    continue
    
    # 查询数据
    def selectDataSqlite(self,column,link):
        with sqlite3.connect(self.sqlDataName) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.sqlTableName} WHERE {column}='{link}'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False

    # 添加数据
    def insertDataSqlite(self,title,link,rssName,date):
        with sqlite3.connect(self.sqlDataName) as conn:
            cursor = conn.cursor()
            sql = f"insert into rssTable(title, link, rssName,date) VALUES (?,?,?,?);"
            cursor.execute(sql,(title,link,rssName,date)) 

    # 初始化数据
    def initSelectDataSqlite(self):
        with sqlite3.connect(self.sqlDataName) as conn:
            cursor = conn.cursor()
            cursor.execute(f"select link from {self.sqlTableName} ;")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False
    
    # 创建数据库
    def createSqlite(self,sqlDataName,sqlCretaTable):
        logger.info("检查数据库是否存在")
        if  os.path.exists(sqlDataName) is False:
            # 创建数据库
            logger.info("创建数据库")
            conn = sqlite3.connect(sqlDataName)
            cur = conn.cursor()
            try:
                sql = sqlCretaTable
                cur.execute(sql)
                logger.info("创建表成功")
                return True
            except OperationalError as o:
                logger.info(f"{str(o)}")
                pass
                if str(o) == "table gas_price already exists":
                    return True
                return False
            except Exception as e:
                logger.exception(e)
                return False
            finally:
                cur.close()
                conn.close()
        else:
            logger.info(f"{sqlDataName} 数据库已存在")

  # 发送rss请求
    def rssRequests(self,rssUrl,rssFormat,rssName):
        logger.info(f"读取链接: {rssUrl}")
        logger.info(f"获取格式: {rssFormat}")
        """抓取开源中国RSS"""
        # 网站种子解析
        rss_oschina = feedparser.parse(rssUrl)
        checkFormat = ""
        for i in rssFormat.keys():
            if i in rss_oschina.keys():
                checkFormat=i
                logger.info(f"匹配获取格式: {i}")
        rssDict = {} 
        for i in rssFormat[checkFormat]:
            rssList = []
            for h in rss_oschina[checkFormat]:
                try:
                    rssList.append(h[i])
                except KeyError:
                    rssList.append("1")
            rssDict[i] = rssList
        logger.info(f"RSS链接解析完成: {rssUrl}")
        self.fsRequests(rssDict,rssName)
             
    # 获取到rss链接
    def formatRssTargetDict(self,targetDict):
        try:
            self.rssRequests(rssUrl=targetDict['rsslink'],rssFormat=targetDict,rssName=targetDict['rssName'])
        except KeyError as e:
            print(f"请检查rssConfig.yaml中必有字段是否存在,程序退出")
            exit()
    # 解析rss链接
    def formatRssTarget(self,configFormatDict):
        for i in configFormatDict.keys():
            self.formatRssTargetDict(configFormatDict[i])

    # 读取配置文件
    def readConfigYaml(self,yamlUrl):
        # 获取读取格式
        with open (yamlUrl) as fp:
            configFormatDict=yaml.safe_load(fp)
            # 在程序中使用
        logger.info(f"读取配置文件: {yamlUrl}")
        return configFormatDict
    
    # 主程序
    def main(self, rssYamlPath):
        # 读取rssConfigYaml配置文件
        configFormatDict = self.readConfigYaml(rssYamlPath)
        # 解析rss链接
        self.formatRssTarget(configFormatDict=configFormatDict)

if __name__ == "__main__":
    # 捕获异常退出
    try:
        configYamlPath = f"{os.getcwd()}/config.yaml"
        rs = rssSpider(configYamlPath)
        rssYamlPath = rs.rssPath
        rs.main(rssYamlPath)
    except KeyboardInterrupt as e:
        logger.info(e)
        print("外部关闭,程序退出")
        exit()
    except FileNotFoundError as e:
        logger.info(e)
        print("文件不存在,程序退出")
        exit()
    except Exception as e:
        logger.exception(e)
        print("未知异常,程序退出")
        exit()
