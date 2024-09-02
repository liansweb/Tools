import requests

headers = {
    'accept': 'application/json',
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
}

params = {
    'src_ip': '164.53.174.23',
    'fixed_src_ip': 'off',
    'src_port': '80',
    'dst_ip': '11.22.33.99',
    'dst_port': '80',
    'host_in_req_headers': 'true',
    'host': 'admin.',
    'resp_status_code': '200',
    'resp_status_reason': 'OK',
    'get_kafka_content': 'off',
    'history_time_switch': 'off',
    'random_history_time': '1',
    'set_size': '1',
    'is_container': 'False',
    'req_started_at': '2023-08-08 08:08:08',
    'resp_ended_at': '2023-08-08 08:08:18',
}

json_data = {
    'ip_proportion': [],
    'host_proportion': [],
    'req_headers_dict': {},
    'resp_headers_dict': {},
}

response = requests.post('http://10.2.14.127:9998/agentx_origin_http', params=params, headers=headers, json=json_data)

print(response.status_code)
print(response.text)
print(response.url)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "ip_proportion": [],\n  "host_proportion": [],\n  "req_headers_dict": {},\n  "resp_headers_dict": {}\n}'
#response = requests.post('http://10.2.14.127:9998/agentx_origin_http', params=params, headers=headers, data=data)
