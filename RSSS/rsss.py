import feedparser
import ssl
import yaml
import requests
import sqlite3
import os
import logging
import urllib3
from sqlite3 import OperationalError
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class rssSpider:

    def bannner(self):
        print("""

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

        """)        

    def __init__(self,configYamlPath):
        self.bannner()
        logger.info("程序初始化")
        configDict = self.readConfigYaml(configYamlPath)
        # 获取飞书token
        self.feishuToken = configDict["feishuToken"]
        # 获取本地数据库文件名
        self.sqlDataName = configDict["sqlDataName"]
        # 获取数据库表名
        self.sqlTableName = configDict["sqlTableName"]
        # 获取数据库建表语句
        self.sqlCretaTable = configDict["sqlCretaTable"]
        self.createSqlite(self.sqlDataName,self.sqlCretaTable)

    # 发送飞书
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
                self.insertDataSqlite(a[0],a[1],rssName,a[2])
                self.feishuRequests(a,rssName=rssName)
            else:
                if self.selectDataSqlite(a[1]) is True :
                    self.insertDataSqlite(a[0],a[1],rssName,a[2])
                    self.feishuRequests(a,rssName=rssName)
                else:
                    continue    

    # 发送到飞书
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
        resp = requests.post(url=url,  json=feiShuData, verify=False)
        logger.info(resp.text)

    # 发送请求
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
             
    # 读取配置文件
    def readConfigYaml(self,yamlUrl):
        # 获取读取格式
        with open (yamlUrl) as fp:
            configFormatDict=yaml.safe_load(fp)
            # 在程序中使用
        logger.info(f"读取配置文件: {yamlUrl}")
        return configFormatDict

    # 读取最外层结构
    def formatRssTarget(self,configFormatDict):
        for i in configFormatDict.keys():
            self.formatRssTargetDict(configFormatDict[i])
    # 获取到rss链接
    def formatRssTargetDict(self,targetDict):
        self.rssRequests(rssUrl=targetDict['rsslink'],rssFormat=targetDict,rssName=targetDict['rssName'])
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
    # 添加数据
    def insertDataSqlite(self,title,link,rssName,date):
        with sqlite3.connect(self.sqlDataName) as conn:
            cursor = conn.cursor()
            cursor.execute(f"insert into rssTable(title, link, rssName,date) VALUES ('{title}','{link}','{rssName}','{date}');")  
    # 查询数据
    def selectDataSqlite(self,link):
        with sqlite3.connect(self.sqlDataName) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.sqlTableName} WHERE link='{link}'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False
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
    # 主程序
    def main(self, yamlPath):
        configFormatDict = self.readConfigYaml(yamlPath)
        self.formatRssTarget(configFormatDict=configFormatDict)
if __name__ == "__main__":
    try:
        configYamlPath = f"{os.getcwd()}/config.yaml"
        rs = rssSpider(configYamlPath)
        rssYamlPath = f"{os.getcwd()}/rssConfig.yaml"
        rs.main(rssYamlPath)
    except KeyboardInterrupt as e:
        logger.warning("Program exit")
        exit()