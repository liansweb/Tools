## QUERY TARGET
## 快速开始
```
    pip3 install -r requirements.txt
    python3 queryTarget_httpx.py ../1yamlPoc/cAdvisor.yaml
```

## 注意
- 使用前修改 config.yaml 中 proxies
- 配置代理必须在 config.yaml 中设置
### config.yaml 简介
```
    proxies:               # 设置代理 ===在此处设置后 yamlPOC          
        http://: http://127.0.0.1:7890
        https://: https://127.0.0.1:7890
    timeout: 2              # 超时时间
    follow_redirects: Fasle # 是否允许重定向
    headers:                # 请求头、全局设置
    cookies:                # 请求cookie设置
```
