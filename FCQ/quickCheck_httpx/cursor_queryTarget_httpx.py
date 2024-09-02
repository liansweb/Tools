import re
import httpx
import asyncio
import time
import yaml
import sys
import os
from typing import Dict, List

class QueryTarget:
    def __init__(self, config_path: str):
        config_yaml = self.read_yaml(config_path)
        self.config_proxies = config_yaml["proxies"]
        self.config_timeout = config_yaml["timeout"]
        self.config_follow_redirects = config_yaml["follow_redirects"]
        self.config_headers = config_yaml["headers"]
        self.config_cookies = config_yaml["cookies"]
        self.successful_target = []
        self.num_all_target = 0
        self.num_success_target = 0
        self.poc_config = {}

    def title(self):
        print(f"""
            quick check
        Yaml POC 信息:
            目标dir      :    \033[0;34m {self.poc_config['targetDir']} \033[0m
            目标path     :    \033[0;34m {self.poc_config['targetPath']} \033[0m
            请求method   :    \033[0;34m {self.poc_config['targetMethod']} \033[0m
            超时time     :    \033[0;34m {self.poc_config['targetTimeout']} \033[0m
            输出dir      :    \033[0;34m {self.poc_config['targetOutputDir']} \033[0m
            匹配data     :    \033[0;34m {self.poc_config['targetReExpression']} \033[0m
        """)

    def read_yaml(self, yaml_path: str):
        with open(yaml_path, "r") as fp:
            return yaml.safe_load(fp)

    def read_poc_yaml(self, poc_yaml: str):
        self.poc_config = self.read_yaml(poc_yaml)

    def ensure_output_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"\033[0;32m[+] 输出目录: {dir_path} 创建成功  \033[0m")
        else:
            print(f"\033[0;33m[*] 输出目录: {dir_path} 已存在  \033[0m")

    def write_file(self, file_path, successful_target):
        if successful_target:
            target_output_dir = os.path.join(self.poc_config['targetOutputDir'], os.path.basename(file_path))
            print(f"\033[0;32m[+] 请求成功 : {len(successful_target)} 条  \033[0m")
            self.num_success_target += len(successful_target)
            print(f"\033[0;32m[+] 写入文件 : {target_output_dir}   \033[0m")
            with open(target_output_dir, "w") as fp:
                for item in successful_target:
                    fp.write(item + "\n")

    def read_os_path(self, dir_path):
        self.files_list = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) for f in filenames]
        print(f"\033[0;32m[+] 读取目标文件路径成功 : {self.files_list}  \033[0m")

    async def req(self, url: str) -> Dict:
        re_expression = {}
        if self.poc_config['targetPath']:
            url = f"{url.rstrip()}{self.poc_config['targetPath']}"
        try:
            async with httpx.AsyncClient(
                proxies=self.config_proxies,
                timeout=self.config_timeout,
                headers=self.config_headers,
                follow_redirects=self.config_follow_redirects,
                cookies=self.config_cookies,
            ) as client:
                res = await client.request(
                    method=self.poc_config['targetMethod'].lower(),
                    url=url,
                    headers=self.poc_config['targetHeaders'],
                    data=self.poc_config['targetData'],
                    json=self.poc_config['targetJson'],
                    timeout=self.poc_config['targetTimeout'],
                    follow_redirects=self.poc_config['targetAllowRedirects'],
                )
                re_expression = {
                    "respStatusCode": res.status_code,
                    "respHeaders": str(res.headers),
                    "respBody": res.text
                }
        except Exception as e:
            print(f"\033[0;31m[!] 目标请求失败 : {url} \033[0m\n{e}")

        return re_expression

    async def process_target(self, url: str):
        re_expression = await self.req(url)
        if re_expression:
            self.evaluate_expression(url, re_expression)

    async def req_task(self):
        for file_path in self.files_list:
            print(f"\033[0;32m[+] 正在读取 : {file_path} 文件中目标  \033[0m")
            with open(file_path, "r") as fp:
                targets = fp.read().splitlines()
            print(f"\033[0;32m[+] 包含目标地址 : {len(targets)} 条  \033[0m")
            self.num_all_target += len(targets)
            
            tasks = [self.process_target(target) for target in targets]
            await asyncio.gather(*tasks)
            
            self.write_file(file_path, self.successful_target)
            self.successful_target.clear()  # 清空列表,为下一个文件做准备

    def evaluate_expression(self, url, re_expression):
        if self.poc_config['targetReExpression']:
            match = all(
                re.search(str(self.poc_config['targetReExpression'].get(key, '')), str(re_expression.get(key, '')))
                for key in self.poc_config['targetReExpression']
            )
            if match:
                print(f"\033[0;32m[+] 目标匹配成功 : {url}   \033[0m")
                self.successful_target.append(url)
            else:
                print(f"\033[0;33m[*] 目标匹配失败 : {url}   \033[0m")
        else:
            self.successful_target.append(url)
            print(f"\033[0;32m[+] 目标匹配成功 : {url}   \033[0m")

        self.print_response_details(re_expression)

    def print_response_details(self, re_expression):
        if self.poc_config['targetRestText'] == 1 or self.poc_config['targetRestText'] is True:
            print(re_expression["respStatusCode"])
        elif self.poc_config['targetRestText'] == 2:
            print(re_expression["respStatusCode"])
            print(re_expression["respHeaders"])
        elif self.poc_config['targetRestText'] == 3:
            print(re_expression["respStatusCode"])
            print(re_expression["respHeaders"])
            print(re_expression["respBody"])

    def main(self, poc_yaml_path):
        start_time = time.time()
        self.read_poc_yaml(poc_yaml_path)
        self.title()
        self.ensure_output_dir(self.poc_config['targetOutputDir'])
        self.read_os_path(self.poc_config['targetDir'])
        asyncio.run(self.req_task())
        end_time = time.time()
        print(f"\033[0;32m[+] 最终耗时: {end_time - start_time:.2f} 秒 \033[0m")
        print(f"\033[0;32m[+] 全部目标: {self.num_all_target} \033[0m")
        print(f"\033[0;32m[+] 成功目标: {self.num_success_target} \033[0m")

if __name__ == "__main__":
    poc_yaml_path = sys.argv[1]
    query = QueryTarget(config_path="./config.yaml")
    query.main(poc_yaml_path)


