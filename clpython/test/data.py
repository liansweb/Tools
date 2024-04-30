http_command = """curl -X 'POST' \
  'http://10.2.13.173:9389/agentx_origin_dubbo/built_in_sensitive_data?fixed_src_ip=on&src_port=1&dst_port=1&dubbo_version=2.0.2&get_kafka_content=off&history_time_switch=off&random_history_time=1&is_container=true&req_started_at=2023-08-08%2008%3A08%3A08&resp_ended_at=2023-08-08%2008%3A08%3A18' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ip_proportion": [],
  "host_proportion": []
}'"""

websocket_command= """curl -X 'POST' \
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
"""

dubbo_command = """curl -X 'POST' \
  'http://10.2.13.173:9389/agentx_origin_dubbo?fixed_src_ip=on&src_port=1&dst_port=1&dubbo_version=2.0.2&req_var_part_args=%5B%22java%2Flang%2FString%22%2C%20%22touch%20%2Ftmp%2Fsuccess.txt%22%5D&req_var_part_attachment_dict=path%3D%22com.user.demo%22&resp_status=20&resp_var_part_value=hi%2C%20%E5%B0%8F%E6%9D%8E%28123456%29&resp_var_part_attachment_dict=%7B%22interface%22%3A%22org.apache.dubbo.samples.api.GreetingsService%22%2C%22path%22%3A%22org.apache.dubbo.samples.api.GreetingsService%22&get_kafka_content=off&history_time_switch=off&random_history_time=1&is_container=true&req_started_at=2023-08-08%2008%3A08%3A08&resp_ended_at=2023-08-08%2008%3A08%3A18' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ip_proportion": [],
  "host_proportion": []
}'
"""