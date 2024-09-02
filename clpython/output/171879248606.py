# pip3 install requests
import requests
import json

method = 'POST'

protocol = 'http://'

host  = '10.2.14.127'

port = 9998

path = '/agentx_origin_http'

query = {'src_ip': ['164.53.174.23'], 'fixed_src_ip': ['off'], 'src_port': ['80'], 'dst_ip': ['11.22.33.99'], 'dst_port': ['80'], 'host_in_req_headers': ['true'], 'host': ['admin.'], 'resp_status_code': ['200'], 'resp_status_reason': ['OK'], 'get_kafka_content': ['off'], 'history_time_switch': ['off'], 'random_history_time': ['1'], 'set_size': ['1'], 'is_container': ['False'], 'req_started_at': ['2023-08-08 08:08:08'], 'resp_ended_at': ['2023-08-08 08:08:18']}

headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

body = -d

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