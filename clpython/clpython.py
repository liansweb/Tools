

def main():
    
    from lib import get_url,write_template,get_method,get_protocol,get_host,get_port,get_path,get_query,get_headers,get_body,get_proxy
    
    curl_command = """
    curl 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query=%E7%BB%86%E6%9E%9D%E6%9C%AB%E8%8A%82&token=682362262&lang=zh_CN&f=json&ajax=1' \
      -H 'accept: */*' \
      -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
      -H 'cookie: appmsglist_action_3901431606=card; pgv_pvid=9909122532; RK=ns2ABxPRce; ptcz=586c347e59334d47094d3cc755af2a21596df3948f024cda7c5ffd71ae87917e; ua_id=ujdpfuMoNmwgJwyqAAAAAKFMPwjYkr45EpHXcO4VLYM=; mm_lang=zh_CN; wetest_lang=zh-cn; _hjSessionUser_2765497=eyJpZCI6ImFkNmRmYzQ3LWY3YmYtNWVjZC05MWJmLTAyZDdmN2VhN2U1YSIsImNyZWF0ZWQiOjE2OTIzMjMwOTkzMDIsImV4aXN0aW5nIjpmYWxzZX0=; _ga=GA1.1.957118132.1692323101; _ga_0KGGHBND6H=GS1.1.1692323101.1.1.1692323131.0.0.0; iip=0; _qimei_uuid42=17b090a3210100939ca215948378af8d67521d2b75; _qimei_q36=; _qimei_h38=2ed324c49ca215948378af8d03000001517b09; wxuin=06057938186749; ts_uid=8250774200; __root_domain_v=.weixin.qq.com; _qddaz=QD.410907206023299; personAgree_3901431606=true; pac_uid=0_49701ee7579cf; suid=ek169949821635676031; _qimei_fingerprint=dd874408a1f844844e59c2072110243e; rewardsn=; wxtokenkey=777; _clck=3901431606|1|fl7|0; uuid=fae48fd0ba910348e0583469b9241eeb; rand_info=CAESIKVlSuXM3Wj1cFNv+eZisXf9fzp+NhT3xOpJMXuLn1dy; slave_bizuin=3901431606; data_bizuin=3901431606; bizuin=3901431606; data_ticket=PXIgCXQ2tyh5T07j36p6FnKZwcHcyeglKWNwMS4PDuBqZLwJbvEZNjAgg+NhTgaq; slave_sid=ZzY1ZDJVZUFLSVN0WGFkSWVQOEJXa2k0eE1ITzlfaFpfRDc0RFk2Nk5NVnNxN1R6dmh1elZoeUZfZGpQb1dXS1NGQWpVSVdpbmZhUjZyQUdfQjVySHFhMnVTRDVRNXhMXzRHOUtiT2FpdnlRZVczNmZVS1FNV3BKZ2xXZkFGZUJKM1RVQ0E2TU9idXRFRXd2; slave_user=gh_209be30b7f6e; xid=d53b4e559341ac6427de3700e27a669a; _clsk=1t3q2is|1713929019698|27|1|mp.weixin.qq.com/weheat-agent/payload/record' \
      -H 'referer: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=682362262&lang=zh_CN&timestamp=1713929017400' \
      -H 'sec-ch-ua: "Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "macOS"' \
      -H 'sec-fetch-dest: empty' \
      -H 'sec-fetch-mode: cors' \
      -H 'sec-fetch-site: same-origin' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0' \
      -H 'x-requested-with: XMLHttpRequest'
    """
    
    curl_command = """
    curl -i -s -k -X $'POST' \
    -H $'Host: apis.starcross.cn:8888' -H $'Content-Length: 51' -H $'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' -H $'Content-Type: application/json' -H $'Accept: */*' -H $'Origin: http://apis.starcross.cn:8888' -H $'Referer: http://apis.starcross.cn:8888/login' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: zh-CN,zh;q=0.9' -H $'Connection: close' \
    --data-binary $'{\"email\":\"liteanso@test.com\",\"password\":\"6tfc&YGV\"}' \
    $'http://apis.starcross.cn:8888/identity/api/auth/login'
    """
    
    curl_command = """
    curl -X 'POST' \
    'http://10.2.14.127:9998/agentx_origin_http?src_ip=164.53.174.23&fixed_src_ip=off&src_port=80&dst_ip=11.22.33.99&dst_port=80&host_in_req_headers=true&host=admin.&resp_status_code=200&resp_status_reason=OK&get_kafka_content=off&history_time_switch=off&random_history_time=1&set_size=1&is_container=False&req_started_at=2023-08-08%2008%3A08%3A08&resp_ended_at=2023-08-08%2008%3A08%3A18' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "ip_proportion": [],
    "host_proportion": [],
    "req_headers_dict": {},
    "resp_headers_dict": {}
    }'
    """
    
    # Example usage
    write_template(
        method=get_method(command=curl_command),
        protocol=get_protocol(url=get_url(command=curl_command)),
        host=get_host(url=get_url(command=curl_command)),
        port=get_port(url=get_url(command=curl_command)),
        url=get_url(command=curl_command),
        path=get_path(url=get_url(command=curl_command)),
        query=get_query(url=get_url(command=curl_command)),
        headers=get_headers(command=curl_command),
        body=get_body(command=curl_command),
        proxy=get_proxy(command=curl_command),
    )


if __name__ == '__main__':
    from banner import banner
    banner()
    main()