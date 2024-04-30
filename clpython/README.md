# 插件 
## clpython
### introduce
将`curl`常用命令转换为`python requests`

### apply arguments
```
    -H 请求头
    -d HTTP POST Data
    -x --proxy 代理参数
```

### test data
```curl
curl -X 'POST' \
  'httsp://10.2.13.173/agentx_origin_websocket?fixed_src_ip=on&src_port=1&dst_port=1&direction=-1&req_method=GET&resp_status_code=200&resp_status_reason=OK&get_kafka_content=off&history_time_switch=off&random_history_time=1&is_container=true&req_started_at=2023-08-08%2008%3A08%3A08&resp_ended_at=2023-08-08%2008%3A08%3A18&frame_started_at=2023-08-08%2008%3A08%3A10&frame_ended_at=2023-08-08%2008%3A08%3A12' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ip_proportion": [],
  "host_proportion": [],
  "handshake_frame_proportion": [
    30,
    70
  ],
  "extra_fields": {
    "type": "handshake",
    "session_id": "dd520b6b-f026-4784-9010-f75d4e20f888"
  },
  "req_headers_dict": {},
  "resp_headers_dict": {}
}'
```

### terminal
```shell


        _______  _        _______          _________          _______  _       
        (  ____ \( \      (  ____ )|\     /|\__   __/|\     /|(  ___  )( (    /|
        | (    \/| (      | (    )|( \   / )   ) (   | )   ( || (   ) ||  \  ( |
        | |      | |      | (____)| \ (_) /    | |   | (___) || |   | ||   \ | |
        | |      | |      |  _____)  \   /     | |   |  ___  || |   | || (\ \) |
        | |      | |      | (         ) (      | |   | (   ) || |   | || | \   |
        | (____/\| (____/\| )         | |      | |   | )   ( || (___) || )  \  |
        (_______/(_______/|/          \_/      )_(   |/     \|(_______)|/    )_)
                                                                                        
                        
                        Author: 李安
                        TIME: 2023
    
2023-11-22 19:01:56,628 - INFO - get_error - 17 - 成功获取到-method-`POST`
2023-11-22 19:01:56,628 - INFO - get_error - 17 - 成功获取到-protocol-`http://`
2023-11-22 19:01:56,631 - INFO - get_error - 17 - 成功获取到-host-`10.2.13.173`
2023-11-22 19:01:56,631 - INFO - get_error - 17 - 成功获取到-port-`9389`
/agentx_origin_dubbo
2023-11-22 19:01:56,631 - INFO - get_error - 17 - 成功获取到-path-`/agentx_origin_dubbo`
2023-11-22 19:01:56,632 - INFO - get_error - 17 - 成功获取到-query-`{'fixed_src_ip': ['on'], 'src_port': ['1'], 'dst_port': ['1'], 'dubbo_version': ['2.0.2'], 'req_var_part_args': ['["java/lang/String", "touch /tmp/success.txt"]'], 'req_var_part_attachment_dict': ['path="com.user.demo"'], 'resp_status': ['20'], 'resp_var_part_value': ['hi, 小李(123456)'], 'resp_var_part_attachment_dict': ['{"interface":"org.apache.dubbo.samples.api.GreetingsService","path":"org.apache.dubbo.samples.api.GreetingsService"'], 'get_kafka_content': ['off'], 'history_time_switch': ['off'], 'random_history_time': ['1'], 'is_container': ['true'], 'req_started_at': ['2023-08-08 08:08:08'], 'resp_ended_at': ['2023-08-08 08:08:18']}`
2023-11-22 19:01:56,632 - INFO - get_error - 17 - 成功获取到-headers-`{'accept': 'application/json', 'Content-Type': 'application/json'}`
2023-11-22 19:01:56,632 - INFO - get_error - 17 - 成功获取到-body-`{
  "ip_proportion": [],
  "host_proportion": []
}`
2023-11-22 19:01:56,632 - WARNING - get_error - 22 - 未获取到-proxy-`代理`
2023-11-22 19:01:56,633 - INFO - write_template - 251 - 写入文件:output/170065091663.py
```

### output truct 
```python
import requests
import json

method = 'POST'

protocol = 'http://'

host  = '10.2.13.173'

port = 9389

path = '/agentx_origin_dubbo/built_in_sensitive_data'

query = {'fixed_src_ip': ['on'], 'src_port': ['1'], 'dst_port': ['1'], 'dubbo_version': ['2.0.2'], 'get_kafka_content': ['off'], 'history_time_switch': ['off'], 'random_history_time': ['1'], 'is_container': ['true'], 'req_started_at': ['2023-08-08 08:08:08'], 'resp_ended_at': ['2023-08-08 08:08:18']}

headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

body = {
  "ip_proportion": [],
  "host_proportion": []
}

proxy = None



url = protocol+host+':'+str(port)+'/'+path

# TODO: timeout Default=10
# TODO: verify Default=False

request = getattr(requests,method.lower())
resp = request(
        url=url,
        headers=headers,
        params=query,
        data=json.dumps(body),
        proxies=proxy,
        verify=False,
        timeout=10
    )

print(resp.status_code)
print(resp.text)
```

### curl help
```bash
用法: curl [选项...] <url>
选项: (H) 表示仅支持 HTTP/HTTPS，(F) 表示仅支持 FTP
     --anyauth       选择“任何”身份验证方法 (H)
 -a, --append        上传时将数据附加到目标文件 (F/SFTP)
     --basic         使用 HTTP 基本身份验证 (H)
     --cacert FILE   对等方验证的 CA 证书 (SSL)
     --capath DIR    对等方验证的 CA 目录 (SSL)
 -E, --cert CERT[:PASSWD] 客户端证书文件和密码 (SSL)
     --cert-type TYPE 证书文件类型 (DER/PEM/ENG) (SSL)
     --ciphers LIST  使用的 SSL 密码 (SSL)
     --compressed    请求压缩响应 (使用 deflate 或 gzip)
 -K, --config FILE   指定要读取的配置文件
     --connect-timeout SECONDS  允许的最长连接时间
 -C, --continue-at OFFSET  恢复传输的偏移量
 -b, --cookie STRING/FILE  从字符串或文件读取 cookie (H)
 -c, --cookie-jar FILE  操作后将 cookie 写入此文件 (H)
     --create-dirs   创建必要的本地目录层次结构
     --crlf          在上传中将 LF 转换为 CRLF
     --crlfile FILE  从给定文件获取 PEM 格式的 CRL 列表
 -d, --data DATA     HTTP POST 数据 (H)
     --data-ascii DATA  HTTP POST ASCII 数据 (H)
     --data-binary DATA  HTTP POST 二进制数据 (H)
     --data-urlencode DATA  HTTP POST 数据 URL 编码 (H)
     --delegation STRING GSS-API 授权权限
     --digest        使用 HTTP Digest 身份验证 (H)
     --disable-eprt  禁止使用 EPRT 或 LPRT (F)
     --disable-epsv  禁止使用 EPSV (F)
 -D, --dump-header FILE  将头写入此文件
     --egd-file FILE  用于随机数据的 EGD 套接字路径 (SSL)
     --engine ENGINGE  加密引擎 (SSL). "--engine list" 以获取列表
 -f, --fail          遇到 HTTP 错误时默默失败（没有任何输出） (H)
 -F, --form CONTENT  指定 HTTP 多部分 POST 数据 (H)
     --form-string STRING  指定 HTTP 多部分 POST 数据 (H)
     --ftp-account DATA  帐户数据字符串 (F)
     --ftp-alternative-to-user COMMAND  替代 "USER [name]" 的字符串 (F)
     --ftp-create-dirs  如果不存在则创建远程目录 (F)
     --ftp-method [MULTICWD/NOCWD/SINGLECWD] 控制 CWD 使用 (F)
     --ftp-pasv      使用 PASV/EPSV 而不是 PORT (F)
 -P, --ftp-port ADR  使用具有给定地址的 PORT 而不是 PASV (F)
     --ftp-skip-pasv-ip 跳过 PASV 的 IP 地址 (F)
     --ftp-pret      在 PASV 之前发送 PRET（对于 drftpd） (F)
     --ftp-ssl-ccc   在身份验证后发送 CCC (F)
     --ftp-ssl-ccc-mode ACTIVE/PASSIVE  设置 CCC 模式 (F)
     --ftp-ssl-control 要求 ftp 登录使用 SSL/TLS，传输时清除 (F)
 -G, --get           使用 HTTP GET 发送 -d 数据 (H)
 -g, --globoff       禁用 URL 中的 {} 和 [] 序列和范围
 -H, --header LINE   传递到服务器的自定义头 (H)
 -I, --head          仅显示文档信息
 -h, --help          此帮助文本
     --hostpubmd5 MD5  主机公钥的十六进制编码 MD5 字符串。 (SSH)
 -0, --http1.0       使用 HTTP 1.0 (H)
     --ignore-content-length  忽略 HTTP Content-Length 头
 -i, --include       在输出中包含协议头 (H/F)
 -k, --insecure      允许连接到没有证书的 SSL 站点 (H)
     --interface INTERFACE  指定要使用的网络接口/地址
 -4, --ipv4          将名称解析为 IPv4 地址
 -6, --ipv6          将名称解析为 IPv6 地址
 -j, --junk-session-cookies 忽略从文件读取的会话 cookie (H)
     --keepalive-time SECONDS  保持活动探测之间的间隔
     --key KEY       私钥文件名 (SSL/SSH)
     --key-type TYPE 私钥文件类型 (DER/PEM/ENG) (SSL)
     --krb LEVEL     启用具有指定安全级别的 Kerberos (F)
     --libcurl FILE  转储此命令行的 libcurl 等效代码
     --limit-rate RATE  限制传输速度到此速率
 -l, --list-only     仅列出 FTP 目录的名称 (F)
     --local-port RANGE  强制使用这些本地端口号
 -L, --location      跟随重定向 (H)
     --location-trusted 像 --location 一样，并将身份验证发送到其他主机 (H)
 -M, --manual        显示完整手册
     --mail-from FROM  邮件来自此地址
     --mail-rcpt TO  发送到此接收器的邮件
     --mail-auth AUTH  原始电子邮件的发件人地址
     --max-filesize BYTES  下载的最大文件大小 (H/F)
     --max-redirs NUM  允许的最大重定向次数 (H)
 -m, --max-time SECONDS  允许的传输时间最长时间
     --metalink      将给定的 URL 处理为 metalink XML 文件
     --negotiate     使用 HTTP Negotiate 身份验证 (H)
 -n, --netrc         必须读取 .netrc 获取用户名和密码
     --netrc-optional 使用 .netrc 或 URL; 覆盖 -n
     --netrc-file FILE  设置要使用的 netrc 文件名
 -N, --no-buffer     禁用输出流的缓冲
     --no-keepalive  在连接上禁用 keepalive 使用
     --no-sessionid  禁用 SSL 会话 ID 重用 (SSL)
     --noproxy       不使用代理的主机列表
     --ntlm          使用 HTTP NTLM 身份验证 (H)
 -o, --output FILE   将输出写入 <file> 而不是 stdout
     --pass PASS     私钥的密码 (SSL/SSH)
     --post301       在跟随 301 重定向后不切换到 GET (H)
     --post302       在跟随 302 重定向后不切换到 GET (H)
     --post303       在跟随 303 重定向后不切换到 GET (H)
 -#, --progress-bar 以进度条形式显示传输进度
     --proto PROTOCOLS  启用/禁用指定的协议
     --proto-redir PROTOCOLS  重定向时启用/禁用指定的协议
 -x, --proxy [PROTOCOL://]HOST[:PORT] 使用指定端口的代理
     --proxy-anyauth 选择“任何”代理身份验证方法 (H)
     --proxy-basic   在代理上使用基本身份验证 (H)
     --proxy-digest  在代理上使用摘要身份验证 (H)
     --proxy-negotiate 在代理上使用 Negotiate 身份验证 (H)
     --proxy-ntlm    在代理上使用 NTLM 身份验证 (H)
 -U, --proxy-user USER[:PASSWORD] 代理用户和密码
     --proxy1.0 HOST[:PORT]  使用具有给定端口的 HTTP/1.0 代理
 -p, --proxytunnel   通过 HTTP 代理隧道运行 (使用 CONNECT)
     --pubkey KEY    公钥文件名 (SSH)
 -Q, --quote CMD     在传输之前将命令发送到服务器 (F/SFTP)
     --random-file FILE  从此文件读取随机数据
 -r, --range RANGE   仅检索范围内的字节
     --raw           进行 HTTP "raw"，无任何传输解码 (H)
 -e, --referer       引用 URL (H)
 -J, --remote-header-name 使用提供的文件名作为头 (H)
 -O, --remote-name   将输出写入与远程文件同名的文件
     --remote-name-all 对所有 URL 使用远程文件名
 -R, --remote-time   设置本地输出上的远程文件时间
 -X, --request COMMAND  指定要使用的请求命令
     --resolve HOST:PORT:ADDRESS  强制解析 HOST:PORT 为 ADDRESS
     --retry NUM   如果发生暂时性问题，重试请求 NUM 次
     --retry-delay SECONDS  重试时，在每次之间等待这么多秒
     --retry-max-time SECONDS  仅在此期间内重试
 -S, --show-error    显示错误。与 -s 一起使用时，使 curl 在发生错误时显示错误
 -s, --silent        静默模式。不输出任何内容
     --socks4 HOST[:PORT]  在给定主机 + 端口上的 SOCKS4 代理
     --socks4a HOST[:PORT]  在给定主机 + 端口上的 SOCKS4a 代理
     --socks5 HOST[:PORT]  在给定主机 + 端口上的 SOCKS5 代理
     --socks5-basic 为 SOCKS5 代理启用用户名/密码身份验证
     --socks5-gssapi 为 SOCKS5 代理启用 GSS-API 身份验证
     --socks5-hostname HOST[:PORT] 使用 SOCKS5 代理，将主机名传递给代理
     --socks5-gssapi-service NAME  用于 gssapi 的 SOCKS5 代理服务名
     --socks5-gssapi-nec 与 NEC SOCKS5 服务器兼容
 -Y, --speed-limit RATE  停止低于速度限制的传输速度 'speed-time' 秒
 -y, --speed-time SECONDS  用于触发速度限制中止的时间。默认为 30
     --ssl           尝试 SSL/TLS（FTP，IMAP，POP3，SMTP）
     --ssl-reqd      要求 SSL/TLS（FTP，IMAP，POP3，SMTP）
 -2, --sslv2         使用 SSLv2 (SSL)
 -3, --sslv3         使用 SSLv3 (SSL)
     --ssl-allow-beast 允许安全漏洞以提高互操作性 (SSL)
     --stderr FILE   将 stderr 重定向到该文件。- 表示 stdout
     --tcp-nodelay   使用 TCP_NODELAY 选项
 -t, --telnet-option OPT=VAL  设置 telnet 选项
     --tftp-blksize VALUE  设置 TFTP BLKSIZE 选项（必须 >512）
 -z, --time-cond TIME  根据时间条件传输
 -1, --tlsv1         使用 => TLSv1 (SSL)
     --tlsv1.0       使用 TLSv1.0 (SSL)
     --tlsv1.1       使用 TLSv1.1 (SSL)
     --tlsv1.2       使用 TLSv1.2 (SSL)
     --tlsv1.3       使用 TLSv1.3 (SSL)
     --tls-max VERSION  使用 TLS 到版本（SSL）
     --trace FILE    将调试跟踪写入给定文件
     --trace-ascii FILE  像 --trace 但没有十六进制输出
     --trace-time    在跟踪/详细输出中添加时间戳
     --trace-time    Add time stamps to trace/verbose output
     --tr-encoding：请求使用压缩传输编码 (H) 
-T,  --upload-file FILE：将文件传输到目标位置
     --url URL：指定要操作的URL 
-B,  --use-ascii：使用ASCII/文本传输 
-u,  --user USER[:PASSWORD]：服务器用户和密码
     --tlsuser USER：TLS用户名 
     --tlspassword STRING：TLS密码 
     --tlsauthtype STRING：TLS身份验证类型（默认为SRP） 
     --unix-socket FILE：通过UNIX域套接字进行连接 
-A,  --user-agent STRING：发送给服务器的用户代理 (H) 
-v,  --verbose：使操作更加冗长 
-V,  --version：显示版本号并退出 
-w,  --write-out FORMAT：完成后输出的内容格式 
     --xattr：将元数据存储在扩展文件属性中
-q： 如果作为第一个参数使用，则禁用 .curlrc 

```