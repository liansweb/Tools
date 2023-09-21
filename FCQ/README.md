## FOFA COUNTRY QUERY
## 快速开始
```
    pip3 install -r requirements.txt
    python3 fofaQuery.py 'app="Elasticsearch" && status_code=200'
    ================快速验证脚本==================
    httpx模块
        cd quickCheck_httpx
        pip3 install -r requirements.txt
        python3 queryTarget_httpx.py ../1yamlPoc/Elasticsearch.yaml
    requests模块    
        cd quickCheck_requests
        pip3 install -r requirements.txt
        python3 queryTarget_requests.py ../1yamlPoc/Elasticsearch.yaml
```
## 文件介绍
### 目录结构
```
    countryName/  
           国家名称及简写.txt       # 各国家名称及简写
           国家名称及简写.yaml      # fofaQuery.py 会提取 yaml文件中的 国家简写、名称 (默认全部查询、可使用注释忽略)
           生产国家名称及简写.py     # 生成名称及简写会默认忽略 CN
    countryQuertResult/           # 查询结果保存到该目录 以自定义后缀结尾 默认 txt 
    country.yaml                  # fofa 用户配置、及自定义配置
    fofaQuery.py                  # 查询fofa结果
        python3 fofaQuery.py 'app="Elasticsearch" && status_code=200'
    quickCheck_requests           # requests 请求发包慢
    quickCheck_httpx              # httpx    请求发包快
```
### control.yaml 配置
```
    email:                              /fofa邮箱账户
    fields: protocol,ip,port            /查询字段（默认：协议、IP、port） 
    fieldsJoin: $1://$2:$3              /查询字段的拼接格式，（http://12.33.44.11:2222 / https://23.33.22.11:8888）可自定义
    full: false                         /默认搜索一年内的数据，指定为true即可搜索全部数据
    key:                                /fofa API KEY
    page: 1                             /查询的页数、默认一页（页数变动、影响未知）
    query: app=ATLASSIAN-JIRA           /查询语法 第一次可为空
    size: 100                           /每页查询数量，默认为100条，最大支持10,000条/页
    sleep: 1                            /每次请求fofaAPI的间隔
    resultSuffix : txt                  /查询结果后缀 可自定义
    
    url: https://fofa.info/api/v1/search/all?email=     /fofa API 无需修改
    
```

#### control.yaml 细节
```
    请添加:
        email        ：     fofa个人中心邮箱账号
        key          ：     fofa个人中心API KEY
        fields       ：     查询字段       （默认为：protocol,ip,port） protocol默认属性是http,会自动添加host识别protocol
        fieldsJoin   ：     查询结果表达式  （$1://$2:$3）与查询字段的位置对应（字段的连接字符可自定义）
        resultSuffix ：     查询结果后缀 可自定义 默认 .txt
    注意：
        fofaQuery.py 会记录上一次的查询表达式。
        初始化会直接写入 country.yaml 配置文件中。
```

### fofaQuery.py 
```
    启动：
        python3 fofaQuery.py 'app="Elasticsearch" && status_code=200'
    参数：
        参数为fofa的查询表达式
    注意：
        1、每次查询都会清除上次查询结果
        2、会记录当前查询表达式
        3、两次(上次、本次)不同，会提示是否清除上次查询结果
```

### 快速使用
![图片文字](./jpeg/1.jpeg)
![图片文字](./jpeg/2.jpeg)
![图片文字](./jpeg/3.jpeg)
![图片文字](./jpeg/4.jpeg)
![图片文字](./jpeg/5.jpeg)

### quickChecl_requests
![图片文字](./jpeg/6.jpeg)

### quickCheck_httpx
![图片文字](./jpeg/7.jpeg)

