# pip3 install requests
import requests
import json

method = 'GET'

protocol = 'https://'

host  = 'mp.weixin.qq.com'

port = 443

path = '/cgi-bin/searchbiz'

query = {'action': ['search_biz'], 'begin': ['0'], 'count': ['5'], 'query': ['细枝末节'], 'token': ['682362262'], 'lang': ['zh_CN'], 'f': ['json'], 'ajax': ['1']}

headers = {'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8', 'cookie': 'appmsglist_action_3901431606=card; pgv_pvid=9909122532; RK=ns2ABxPRce; ptcz=586c347e59334d47094d3cc755af2a21596df3948f024cda7c5ffd71ae87917e; ua_id=ujdpfuMoNmwgJwyqAAAAAKFMPwjYkr45EpHXcO4VLYM=; mm_lang=zh_CN; wetest_lang=zh-cn; _hjSessionUser_2765497=eyJpZCI6ImFkNmRmYzQ3LWY3YmYtNWVjZC05MWJmLTAyZDdmN2VhN2U1YSIsImNyZWF0ZWQiOjE2OTIzMjMwOTkzMDIsImV4aXN0aW5nIjpmYWxzZX0=; _ga=GA1.1.957118132.1692323101; _ga_0KGGHBND6H=GS1.1.1692323101.1.1.1692323131.0.0.0; iip=0; _qimei_uuid42=17b090a3210100939ca215948378af8d67521d2b75; _qimei_q36=; _qimei_h38=2ed324c49ca215948378af8d03000001517b09; wxuin=06057938186749; ts_uid=8250774200; __root_domain_v=.weixin.qq.com; _qddaz=QD.410907206023299; personAgree_3901431606=true; pac_uid=0_49701ee7579cf; suid=ek169949821635676031; _qimei_fingerprint=dd874408a1f844844e59c2072110243e; rewardsn=; wxtokenkey=777; _clck=3901431606|1|fl7|0; uuid=fae48fd0ba910348e0583469b9241eeb; rand_info=CAESIKVlSuXM3Wj1cFNv+eZisXf9fzp+NhT3xOpJMXuLn1dy; slave_bizuin=3901431606; data_bizuin=3901431606; bizuin=3901431606; data_ticket=PXIgCXQ2tyh5T07j36p6FnKZwcHcyeglKWNwMS4PDuBqZLwJbvEZNjAgg+NhTgaq; slave_sid=ZzY1ZDJVZUFLSVN0WGFkSWVQOEJXa2k0eE1ITzlfaFpfRDc0RFk2Nk5NVnNxN1R6dmh1elZoeUZfZGpQb1dXS1NGQWpVSVdpbmZhUjZyQUdfQjVySHFhMnVTRDVRNXhMXzRHOUtiT2FpdnlRZVczNmZVS1FNV3BKZ2xXZkFGZUJKM1RVQ0E2TU9idXRFRXd2; slave_user=gh_209be30b7f6e; xid=d53b4e559341ac6427de3700e27a669a; _clsk=1t3q2is|1713929019698|27|1|mp.weixin.qq.com/weheat-agent/payload/record', 'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=682362262&lang=zh_CN&timestamp=1713929017400', 'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0', 'x-requested-with': 'XMLHttpRequest'}

body = None

proxy = None



url = protocol+host+':'+str(port)+path

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