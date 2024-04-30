
from log import logger
from typing import TypeVar
T = TypeVar('T')

def get_error(field_name,check: T) -> T:
    """检查Field是否获取成功

    Args:
        check (T): 待检查的条件

    Returns:
        T: 如果检查条件为真，则返回 T 类型的值
    """  
    from config import FIEDL_MAP
    if check:
        logger.info(f"成功获取到-{field_name}-`{check}`")
        return check
    else:
        # 如果不满足条件，可以选择返回 None 或者其他默认值
        field_map = next(FIEDL_MAP[i] for i in FIEDL_MAP if i == field_name)
        logger.warning(f"未获取到-{field_name}-`{field_map}`")
        return None

def get_method(command: str) -> T:
  """获取请求方法

  Args:
      command (str): curl命令字符串

  TODO:
      支持 GET POST PUT DELETE

  Returns:
      T: 请求方法或None
  """  
  
  from config import METHOD
  
  method = next((i for i in METHOD if i in command), None)
  if method is None:
      method = 'GET'
  return get_error('method',method)

def get_url(command: str) -> T:
    """获取完整的URL

    Args:
        command (str): curl命令字符串

    Returns:
        T: 完整的URL字符串或错误信息
    """
    from config import URL_REGEXP,URL_REGEXP_GROUP
    import re 
    
    try:
        url = re.search(URL_REGEXP, command)[URL_REGEXP_GROUP]
    except (TypeError, UnboundLocalError, KeyError):
        url = None

    return url

def get_protocol(url: str) -> T:
  """获取请求protocol

  Args:
      command (str): 输入Url字符串

  Returns:
      T: 完整的protocol信息或None
  """  
  from config import HTTP_HOST
  protocol = next((i for i in HTTP_HOST if i in url),None)
  return get_error('protocol',protocol)

def get_host(url: str) -> T:
  """获取请求host

  Args:
      command (str): 输入Url字符串

  Returns:
      T: 完整的Host信息或None
  """  
  from urllib.parse import urlparse
  try:
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    return get_error('host',host)
  except Exception:
    return get_error('host',None)

def get_port(url: str) -> T:
    """获取端口号

    Args:
        command (str): 输入Url字符串

    Returns:
        T: 端口号或错误信息
    """
    import re
    from config import PORT_REGEXP, PORT_REGEXP_GROUP, PORT_HOST_MAP
    
    try:
        port = re.search(PORT_REGEXP, url)[PORT_REGEXP_GROUP]
    except (TypeError, UnboundLocalError, KeyError):
        port = None

    if port is None:
        try:
            port = PORT_HOST_MAP[get_protocol(url)]
        except KeyError:
            port = None

    return get_error('port', port)

def get_path(url: str) -> T:
    """获取路径

    Args:
        command (str): 输入Url字符串

    Returns:
        T: 路径字符串或错误信息
    """
    from urllib.parse import urlparse

    try:

        parsed_url = urlparse(url)
        path = parsed_url.path
        print(path)
        return get_error('path', path)
    except Exception as e:
        return get_error('path', None)


def get_query(url: str) -> T:
    """获取查询参数

    Args:
        command (str): 输入Url字符串

    Returns:
        T: 查询参数字符串或错误信息
    """
    from urllib.parse import urlparse, parse_qs

    try:
        parsed_url = urlparse(url)
        query_params = parsed_url.query
        parsed_query = parse_qs(query_params)
        return get_error('query', parsed_query)
    except Exception as e:
        return get_error('query', None)

import re
from config import HEADER_REGEXP, HEADER_REGEXP_SPLIT

def get_headers(command: str) -> dict:
    """Extract headers from a curl command string.

    Args:
        command (str): curl command string.

    Returns:
        dict: Dictionary of headers.
    """
    try:
        header_matches = re.findall(HEADER_REGEXP, command)
        headers = {}
        for header in header_matches:
            # 使用 re.split 并限制最大分割次数为1，确保只分割第一个冒号
            header_parts = re.split(HEADER_REGEXP_SPLIT, header, maxsplit=1)
            if len(header_parts) == 2:
                header_name, header_value = header_parts
                headers[header_name] = header_value.lstrip()  # 确保移除值两端的空格
            else:
                # 如果找不到冒号分隔符，可以记录错误、跳过该头部或按需处理
                print(f"Invalid header format: {header}")
        return headers
    except Exception as e:
        raise ValueError(f"Failed to parse headers: {e}")



def get_body(command: str) -> T:
    """获取 HTTP 请求体

    Args:
        command (str): curl命令字符串

    Returns:
        T: 请求体字符串或错误信息
    """
    import re
    from config import BODY_REGEXP, HEADER_REGEXP_GROUP
    
    try:
        # 使用正则表达式匹配 -d 参数后的数据
        body_match = re.search(BODY_REGEXP, command)
        body_data = body_match.group(HEADER_REGEXP_GROUP) if body_match else None
        return get_error('body', body_data)
    except Exception as e:
        return get_error('body', None)


def get_proxy(command: str) -> T:
    import re
    from config import PROXY_REGEXP, PROXY_REGEXP_GROUP
    
    try:
        # 使用正则表达式匹配 -d 参数后的数据
        proxy_match = re.search(PROXY_REGEXP, command)
        proxy_data = proxy_match.group(PROXY_REGEXP_GROUP) if proxy_match else None
        if proxy_data is None:
          return get_error('proxy', None)
        proxy_dict = {
          "http":proxy_data,
          "https":proxy_data
        }
        return get_error('proxy', proxy_dict)
    except Exception as e:
        return get_error('proxy', None)




def write_template(method, protocol, port, url, path, query, headers, body, proxy, host):
    """将参数写入文件
    """    
    
    import time
    
    with open('template/requests.template', 'r') as fp:
        template_content = fp.read()

        # Replace placeholders in the template
        placeholders = {
            '${method}': "'"+str(method)+"'",
            '${protocol}': "'"+str(protocol)+"'",
            '${path}': "'"+str(path)+"'",
            '${query}': str(query),
            '${body}': str(body),
            '${headers}': str(headers),
            '${port}': str(port),
            '${url}': "'"+str(url)+"'",
            '${proxy}': str(proxy),
            '${host}': "'"+str(host)+"'",
        }

        for placeholder, value in placeholders.items():
            template_content = template_content.replace(placeholder, value)

        file = f"output/{int(time.time()*100)}.py"

        logger.info(f'写入文件:{file}')
        
        # Write the updated content to a new file
        with open(file, 'w') as output_fp:
            output_fp.write(template_content)
