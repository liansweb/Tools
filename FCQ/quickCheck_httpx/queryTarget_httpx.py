import re
import httpx
import asyncio
import time
import yaml
import sys
import os


class QueryTarget:
    def __init__(self):
        yaml_path = "./config.yaml"
        config_yaml = self.read_yaml(yaml_path)
        self.config_proxies = config_yaml["proxies"]
        self.config_timeout = config_yaml["timeout"]
        self.config_follow_redirects = config_yaml["follow_redirects"]
        self.config_headers = config_yaml["headers"]
        self.config_cookies = config_yaml["cookies"]
        self.successful_target = None
        self.num_all_target = 0
        self.num_success_target = 0

    def title(self):
        print(f"""
            quick check
        Yaml POC 信息:
            目标dir      :    \033[0;34m {self.poc_target_dir} \033[0m
            目标path     :    \033[0;34m {self.poc_target_path} \033[0m
            请求method   :    \033[0;34m {self.poc_target_method} \033[0m
            超时time     :    \033[0;34m {self.poc_target_timeout} \033[0m
            输出dir      :    \033[0;34m {self.poc_target_output_dir} \033[0m
            匹配data     :    \033[0;34m {self.poc_target_re_expression} \033[0m
        """)

    def remove_put_dir_target(self, dir_path):
        self.read_os_path(dir_path)
        for i in self.files_list:
            os.remove(i)

    def output_dir_target(self, dir_path):
        path = dir_path.strip().rstrip("\\")
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
            print(f"\033[0;32m[+] 输出目录: {path} 创建成功  \033[0m")
        else:
            print(f"\033[0;33m[*] 输出目录: {path} 已存在  \033[0m")
            self.remove_put_dir_target(dir_path)

    def write_file(self, file_path, successful_target):
        if successful_target:
            file_path = re.search("/(\w+\.\w+)", file_path)[1]
            target_output_dir = self.poc_target_output_dir + file_path
            print(f"\033[0;32m[+] 请求成功 : {len(successful_target)} 条  \033[0m")
            self.num_success_target += len(successful_target)
            print(f"\033[0;32m[+] 写入文件 : {target_output_dir}   \033[0m")
            with open(target_output_dir, "w") as fp:
                for item in successful_target:
                    fp.write(item+"\n")

    def read_yaml(self, yaml_path: str):
        with open(yaml_path, "r") as fp:
            return yaml.safe_load(fp)

    def read_poc_yaml(self, poc_yaml: str):
        poc_yaml_dict = self.read_yaml(poc_yaml)
        self.poc_target_path = poc_yaml_dict["targetPath"]
        self.poc_target_method = poc_yaml_dict["targetMethod"]
        self.poc_target_timeout = poc_yaml_dict["targetTimeout"]
        self.poc_target_profixs = poc_yaml_dict["targetProfixs"]
        self.poc_target_allow_redirects = poc_yaml_dict["targetAllowRedirects"]
        self.poc_target_headers = poc_yaml_dict["targetHeaders"]
        self.poc_target_json = poc_yaml_dict["targetJson"]
        self.poc_target_data = poc_yaml_dict["targetData"]
        self.poc_target_re_expression = poc_yaml_dict["targetReExpression"]
        self.poc_target_dir = poc_yaml_dict["targetDir"]
        self.poc_target_output_dir = poc_yaml_dict["targetOutputDir"]
        self.poc_target_rest_text = poc_yaml_dict["targetRestText"]

    def read_os_path(self, dir_path):
        target_dir = dir_path
        files_list = []
        for dirpath, dirnames, filenames in os.walk(target_dir):
            for i in filenames:
                file_path = target_dir + i
                files_list.append(file_path)
        print(f"\033[0;32m[+] 读取目标文件路径成功 : {files_list}  \033[0m")
        self.files_list = files_list

    async def req(self, url):
        self.successful_target = []
        re_expression = {}
        if self.poc_target_path:
            url = url.rstrip() + self.poc_target_path
        try:
            async with httpx.AsyncClient(
                proxies=self.config_proxies,
                timeout=self.config_timeout,
                headers=self.config_headers,
                follow_redirects=self.config_follow_redirects,
                cookies=self.config_cookies,
            ) as client:
                res = await client.request(
                    method=str.lower(self.poc_target_method),
                    url=url,
                    headers=self.poc_target_headers,
                    data=self.poc_target_data,
                    json=self.poc_target_json,
                    timeout=self.poc_target_timeout,
                    follow_redirects=self.poc_target_allow_redirects,
                )
                re_expression["respStatusCode"] = res.status_code
                re_expression["respHeaders"] = str(res.headers)
                re_expression["respBody"] = str(res.text)
        except Exception:
            print(f"\033[0;31m[!] 目标请求失败 : {url} \033[0m")

        self.re_expression = re_expression
        if self.re_expression:
            re_boolean = None
            if self.poc_target_re_expression:
                try:
                    if self.re_expression["respStatusCode"] == self.poc_target_re_expression[
                        "respStatusCode"
                    ]:
                        re_boolean = True
                        for i in self.poc_target_re_expression.keys():
                            if i == "respStatusCode":
                                continue
                            if self.poc_target_re_expression[i]:
                                if re.search(
                                    self.poc_target_re_expression[i],
                                    self.re_expression[i],
                                ):
                                    re_boolean = True
                                else:
                                    re_boolean = False
                                    break
                            else:
                                re_boolean = True
                                break
                except KeyError as e:
                    print(e)
            else:
                re_boolean = True

            if re_boolean:
                print(f"\033[0;32m[+] 目标匹配成功 : {url}   \033[0m")
                self.successful_target.append(url)
            else:
                print(f"\033[0;33m[*] 目标匹配失败 : {url}   \033[0m")

            if self.poc_target_rest_text is True:
                print(self.re_expression["respStatusCode"])
            elif self.poc_target_rest_text == 1:
                print(self.re_expression["respStatusCode"])
                print(self.re_expression["respHeaders"])
            elif self.poc_target_rest_text == 2:
                print(self.re_expression["respStatusCode"])
                print(self.re_expression["respHeaders"])
                print(self.re_expression["respBody"])

    async def req_task(self):
        files_list = self.files_list
        tasks = []
        for i in files_list:
            file_path = i
            print(f"\033[0;32m[+] 正在读取 : {i} 文件中目标  \033[0m")
            with open(file_path, "r") as fp:
                a = fp.readlines()
            print(f"\033[0;32m[+] 包含目标地址 : {len(a)} 条  \033[0m")
            self.num_all_target += len(a)
            for i in range(len(a)):
                task = asyncio.create_task(self.req(a[i]))
                tasks.append(task)
            await asyncio.wait(tasks)

            self.write_file(file_path, self.successful_target)

    def main(self):
        now = time.time()
        self.read_poc_yaml(sys.argv[1])
        self.title()
        self.output_dir_target(self.poc_target_output_dir)
        self.read_os_path(self.poc_target_dir)
        asyncio.run(self.req_task())
        end = time.time()
        print(f"\033[0;32m[+] 最终耗时 :", end - now, "\033[0m")
        print(f"\033[0;32m[+] 全部目标 :", self.num_all_target, "\033[0m")
        print(f"\033[0;32m[+] 成功目标 :", self.num_success_target, "\033[0m")


if __name__ == "__main__":
    start = QueryTarget()
    start.main()
