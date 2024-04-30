# Support HTTP METHOD
METHOD=['GET', 'POST', 'DELETE','PUT']

# Url Regexp 
URL_REGEXP = r"'(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^']+)'"
URL_REGEXP_GROUP = 1

# Set Log Level
LOG_LEVEL = 'INFO'

# HTTP URL 
HTTP_HOST = [
    'http://',
    'https://'
]

# Field Map
FIEDL_MAP={
    'method':'方法',
    'protocol':'协议',
    'host':'域名',
    'port':"端口",
    'path':'路径',
    'headers':'请求标头',
    'query':'请求参数',
    'body':'请求体',
    'proxy':'代理',
}


# Port Regexp
PORT_REGEXP = r':(\d+)/'
# Port Regexp Group
PORT_REGEXP_GROUP = 1
# Port Host Map
PORT_HOST_MAP={
    'http://':80,
    'https://':443
}

# Header Regexp
HEADER_REGEXP = r"-H '([^']+)'"
# Header Regexp Group
HEADER_REGEXP_GROUP = 1
# Header Regexp Split
HEADER_REGEXP_SPLIT = ':'

# Body Regexp
BODY_REGEXP = r"-d '([^']+)'"
# Body Regexp Group
BODY_REGEXP_GROUP = 1

# Proxy Regexp 
# TODO 支持不带''
PROXY_REGEXP = r"(?:-x|--proxy) '([^']+)'"
# Proxy Regexp Group
PROXY_REGEXP_GROUP = 1