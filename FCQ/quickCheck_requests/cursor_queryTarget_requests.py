import requests
import yaml
import os
import re
import sys
import time

requests.packages.urllib3.disable_warnings()

class CheckTarget:
    def __init__(self, config):
        self.targetDir = config['targetDir']
        self.targetPath = config['targetPath']
        self.targetReExpression = config['targetReExpression']
        self.targetMethod = config['targetMethod'].lower()
        self.targetHeaders = config['targetHeaders']
        self.targetJson = config['targetJson']
        self.targetData = config['targetData']
        self.targetTimeout = config['targetTimeout']
        self.targetProxies = config['targetProfixs']
        self.targetAllowRedirects = config['targetAllowRedirects']
        self.verify = False
        self.targetOutputDir = config['targetOutputDir']
        self.targetRestText = config['targetRestText']

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

    @staticmethod
    def read_yaml(yaml_path):
        with open(yaml_path, "r") as fp:
            return yaml.safe_load(fp)

    @staticmethod
    def ensure_dir(path):
        os.makedirs(path, exist_ok=True)
        print(f"\033[0;32m[+] 输出目录: {path} 创建成功 \033[0m" if not os.path.exists(path) else f"\033[0;33m[+] 输出目录: {path} 已存在 \033[0m")

    @staticmethod
    def write_to_file(dir_path, file_name, content):
        file_path = os.path.join(dir_path, re.search(r"[^/]+\.txt", file_name)[0])
        print(f"\033[0;32m[+] 写入文件 : {file_path} \033[0m")
        with open(file_path, "w") as fp:
            for line in content.values():
                fp.write(f"{line}\n")

    def match_expression(self, response):
        if not self.targetReExpression:
            return {"code": "未配置自定义表达式"}

        for key, pattern in self.targetReExpression.items():
            if not re.search(str(pattern), str(response.get(key, '')), re.I):
                return {"code": "自定义表达式匹配失败"}

        return {"code": "自定义表达式匹配成功"}

    def send_request(self, url):
        method = getattr(requests, self.targetMethod, None)
        if not method:
            print(f"\033[0;36m[!] 请求方法无效: {self.targetMethod} \033[0m")
            return None

        try:
            response = method(
                url=url, headers=self.targetHeaders, json=self.targetJson, data=self.targetData,
                proxies=self.targetProxies, verify=self.verify, allow_redirects=self.targetAllowRedirects,
                timeout=self.targetTimeout
            )
            return {
                "status_code": response.status_code,
                "headers": response.headers,
                "body": response.text
            }
        except Exception as e:
            print(f"\033[0;31m[!] 请求失败: {url} \033[0m\n{e}")
            return None

    def process_response(self, response, url):
        result = self.match_expression(response)
        if result['code'] == "自定义表达式匹配失败":
            print(f"\033[0;33m[!] 目标匹配失败: {url} \033[0m")
            return None

        print(f"\033[0;32m[+] 目标匹配成功: {url} \033[0m")
        if self.targetRestText:
            print(response['status_code'])
            if self.targetRestText > 1:
                print(response['headers'])
            if self.targetRestText > 2:
                print(response['body'])
        return url

    def process_target(self, target):
        url = target + self.targetPath if self.targetPath else target
        response = self.send_request(url)
        if response:
            matched_url = self.process_response(response, url)
            if matched_url:
                return {target: matched_url}
        return {}

    def read_and_process_files(self, file_paths):
        all_matches = {}
        for file_path in file_paths:
            print(f"\033[0;32m[+] 正在读取文件: {file_path} \033[0m")
            with open(file_path, "r") as file:
                targets = file.readlines()
            for target in targets:
                target = target.strip()
                matches = self.process_target(target)
                all_matches.update(matches)
        return all_matches

    def collect_files(self, directory):
        return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]

    def run(self, yaml_path):
        config = self.read_yaml(yaml_path)
        self.__init__(config)
        self.title()
        self.ensure_dir(self.targetOutputDir)
        files = self.collect_files(self.targetDir)
        matches = self.read_and_process_files(files)
        if matches:
            print(f"\033[0;32m[+] 匹配成功目标: {len(matches)} 条 \033[0m")
            self.write_to_file(self.targetOutputDir, "result.txt", matches)

if __name__ == '__main__':
    start_time = time.time()
    yaml_path = sys.argv[1]
    checker = CheckTarget(CheckTarget.read_yaml(yaml_path))
    checker.run(yaml_path)
    end_time = time.time()
    print(f"\033[0;32m[+] 最终耗时: {end_time - start_time:.2f} 秒 \033[0m")
