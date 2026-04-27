import json
from typing import List, Dict, Any


def parse_swagger(swagger_path: str) -> tuple:
    """
    解析 Swagger 文档，提取 API 信息和 BASE_URL

    Args:
        swagger_path: Swagger 文档路径（本地文件路径）

    Returns:
        (base_url, apis) 元组
        - base_url: str, 从swagger文档的servers字段提取
        - apis: API信息列表
        [
            {
                "path": "/api/login",
                "method": "post",
                "summary": "用户登录",
                "parameters": {...},
                "responses": {...}
            }
        ]
    """
    with open(swagger_path, 'r', encoding='utf-8') as f:
        swagger_data = json.load(f)

    # 提取 base_url
    base_url = extract_base_url(swagger_data)

    apis = []

    # 兼容 OpenAPI 2.0 和 3.0
    paths = swagger_data.get('paths', {})

    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                continue

            api_info = {
                'path': path,
                'method': method.upper(),
                'summary': details.get('summary', details.get('description', '')),
                'parameters': details.get('parameters', []),
                'request_body': details.get('requestBody', {}),
                'responses': details.get('responses', {})
            }

            apis.append(api_info)

    return base_url, apis


def extract_base_url(swagger_data: dict) -> str:
    """
    从 Swagger 数据中提取 BASE_URL

    优先级：
    1. OpenAPI 3.0 的 servers 字段
    2. Swagger 2.0 的 schemes + host + basePath
    3. 默认值: http://localhost:8000

    Args:
        swagger_data: Swagger 文档的字典数据

    Returns:
        base_url 字符串
    """
    # OpenAPI 3.0
    if 'servers' in swagger_data and swagger_data['servers']:
        server = swagger_data['servers'][0]
        url = server.get('url', '')
        # 替换变量（如 {port}）
        url = url.replace('{port}', '8000').replace('{protocol}', 'http')
        return url.rstrip('/')

    # Swagger 2.0
    schemes = swagger_data.get('schemes', ['http'])
    host = swagger_data.get('host', 'localhost')
    base_path = swagger_data.get('basePath', '')

    if schemes:
        scheme = schemes[0]
        base_url = f"{scheme}://{host}{base_path}"
        return base_url.rstrip('/')

    # 默认值
    return "http://localhost:8000"


def api_to_description(api_info: Dict[str, Any]) -> str:
    """
    将 API 信息转换为自然语言描述（用于 LLM 生成测试）

    Args:
        api_info: 单个 API 的信息字典

    Returns:
        API 的自然语言描述
    """
    desc = f"API: {api_info['method']} {api_info['path']}\n"
    desc += f"描述: {api_info['summary']}\n"

    if api_info.get('request_body'):
        desc += f"请求体: {json.dumps(api_info['request_body'], ensure_ascii=False)}\n"

    if api_info.get('parameters'):
        desc += f"参数: {json.dumps(api_info['parameters'], ensure_ascii=False)}\n"

    if api_info.get('responses'):
        desc += f"响应: {json.dumps(api_info['responses'], ensure_ascii=False)}\n"

    return desc
