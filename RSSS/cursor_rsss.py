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

# 配置日志和SSL
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RssSpider:
    def __init__(self, config_yaml_path):
        self.banner()
        logger.info("程序初始化")
        self.config = self.read_config_yaml(config_yaml_path)
        self.init_attributes()
        self.create_sqlite(self.sql_data_name, self.sql_create_table)

    def init_attributes(self):
        try:
            self.feishu_token = self.config["feishuToken"]
            self.sql_data_name = self.config["sqlDataName"]
            self.sql_table_name = self.config["sqlTableName"]
            self.sql_create_table = self.config["sqlCretaTable"]
            self.filter_search = self.config["filterSearch"]
            self.rss_path = self.config["rssPath"]
        except KeyError as e:
            logger.error(f"config.yaml中缺少必要条件: {e}")
            exit(1)

    @staticmethod
    def banner():
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

    def filter_name_search(self, title):
        if not self.filter_search:
            return True
        return any(re.search(pattern, title, re.MULTILINE | re.IGNORECASE) for pattern in self.filter_search)

    def feishu_requests(self, data, rss_name):
        url = self.feishu_token
        feishu_data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{data[0]}",
                        "content": [
                            [
                                {"tag": "text", "text": f"链接 : {data[1]}\n"},
                                {"tag": "text", "text": f"日期 : {data[2]}\n"},
                                {"tag": "text", "text": f"来源 : {rss_name}\n"}
                            ]
                        ]
                    }
                }
            }
        }
        for _ in range(2):  # 尝试两次
            try:
                resp = requests.post(url=url, json=feishu_data, verify=False, timeout=10)
                logger.info(resp.text)
                break
            except requests.exceptions.Timeout:
                logger.warning("请求超时,重新尝试")
                time.sleep(3)
        else:
            logger.error("请求超时,程序退出")
            exit(1)

    def fs_requests(self, rss_dict, rss_name):
        logger.info("准备发送请求到飞书")
        req_len_check = 0
        for i in rss_dict.keys():
            req_len = len(rss_dict[i])
            if req_len_check == 0:
                req_len_check = req_len
                continue
        for i in range(req_len_check):
            a = []   
            for h in rss_dict.keys():
                a.append(rss_dict[h][i])
            if self.init_select_data_sqlite() is True:
                if self.filter_name_search(a[0]) is True:
                    self.insert_data_sqlite(a[0], a[1], rss_name, a[2])
                    self.feishu_requests(a, rss_name=rss_name)
                else:
                    continue
            else:
                if self.filter_name_search(a[0]) is True:
                    if self.select_data_sqlite(column="link", link=a[1]) is True and self.select_data_sqlite(column="title", link=a[0]) is True:
                        self.insert_data_sqlite(a[0], a[1], rss_name, a[2])
                        self.feishu_requests(a, rss_name=rss_name)
                    else:
                        continue    
                else:
                    continue
    
    def select_data_sqlite(self, column, link):
        with sqlite3.connect(self.sql_data_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.sql_table_name} WHERE {column}='{link}'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False

    def insert_data_sqlite(self, title, link, rss_name, date):
        with sqlite3.connect(self.sql_data_name) as conn:
            cursor = conn.cursor()
            sql = f"insert into rssTable(title, link, rssName, date) VALUES (?,?,?,?);"
            cursor.execute(sql, (title, link, rss_name, date)) 

    def init_select_data_sqlite(self):
        with sqlite3.connect(self.sql_data_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"select link from {self.sql_table_name} ;")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False
    
    def create_sqlite(self, sql_data_name, sql_create_table):
        logger.info("检查数据库是否存在")
        if  os.path.exists(sql_data_name) is False:
            # 创建数据库
            logger.info("创建数据库")
            conn = sqlite3.connect(sql_data_name)
            cur = conn.cursor()
            try:
                sql = sql_create_table
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
            logger.info(f"{sql_data_name} 数据库已存在")

    def rss_requests(self, rss_url, rss_format, rss_name):
        logger.info(f"读取链接: {rss_url}")
        logger.info(f"获取格式: {rss_format}")
        """抓取开源中国RSS"""
        # 网站种子解析
        rss_oschina = feedparser.parse(rss_url)
        check_format = ""
        for i in rss_format.keys():
            if i in rss_oschina.keys():
                check_format=i
                logger.info(f"匹配获取格式: {i}")
        rss_dict = {} 
        for i in rss_format[check_format]:
            rss_list = []
            for h in rss_oschina[check_format]:
                try:
                    rss_list.append(h[i])
                except KeyError:
                    rss_list.append("1")
            rss_dict[i] = rss_list
        logger.info(f"RSS链接解析完成: {rss_url}")
        self.fs_requests(rss_dict, rss_name)
             
    def format_rss_target_dict(self, target_dict):
        try:
            self.rss_requests(rss_url=target_dict['rsslink'], rss_format=target_dict, rss_name=target_dict['rssName'])
        except KeyError as e:
            print(f"请检查rssConfig.yaml中必有字段是否存在,程序退出")
            exit(1)

    def format_rss_target(self, config_format_dict):
        for i in config_format_dict.keys():
            self.format_rss_target_dict(config_format_dict[i])

    def read_config_yaml(self, yaml_url):
        # 获取读取格式
        with open (yaml_url) as fp:
            config_format_dict=yaml.safe_load(fp)
            # 在程序中使用
        logger.info(f"读取配置文件: {yaml_url}")
        return config_format_dict
    
    def main(self, rss_yaml_path):
        # 读取rssConfigYaml配置文件
        config_format_dict = self.read_config_yaml(rss_yaml_path)
        # 解析rss链接
        self.format_rss_target(config_format_dict=config_format_dict)

if __name__ == "__main__":
    try:
        config_yaml_path = f"{os.getcwd()}/config.yaml"
        rs = RssSpider(config_yaml_path)
        rs.main(rs.rss_path)
    except KeyboardInterrupt:
        logger.info("外部关闭,程序退出")
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {e}")
    except Exception as e:
        logger.exception(f"未知异常: {e}")
    finally:
        exit()
