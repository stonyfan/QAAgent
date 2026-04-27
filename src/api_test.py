import os
from typing import Dict, Any


def generate_test_code(api_description: str, api_name: str, base_url: str = "http://localhost:8000") -> str:
    """
    根据 API 描述生成 pytest 测试代码

    Args:
        api_description: API 的自然语言描述
        api_name: API 名称（用于生成文件名）
        base_url: API的基础URL（从swagger文档中提取）

    Returns:
        生成的测试代码字符串
    """
    # 解析API路径和方法
    lines = api_description.split('\\n')
    first_line = lines[0]

    # 提取方法和路径
    # 格式: "API: GET /posts/{postId}"
    if 'API:' in first_line:
        api_part = first_line.split('API: ')[1]
        parts = api_part.split()
        method = parts[0]
        path = parts[1] if len(parts) > 1 else '/'
    else:
        method = 'GET'
        path = '/'

    # 处理路径参数：将 {param} 转换为示例值
    import re
    def replace_param(match):
        param_name = match.group(1)
        # 根据参数名生成示例值
        if 'id' in param_name.lower():
            return '1'
        elif param_name in ['username', 'userId']:
            return '1'
        else:
            return '1'

    # 替换路径参数
    path_with_params = re.sub(r'\{([^}]+)\}', replace_param, path)

    # 根据HTTP方法生成不同的断言
    if method == "GET":
        success_assertion = '''
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list)), "响应应该是字典或列表"'''

    elif method in ["POST", "PUT"]:
        success_assertion = '''
    # 验证响应
    assert response.status_code in [200, 201]
    data = response.json()
    assert data is not None, "响应不应为空"'''

    elif method == "DELETE":
        success_assertion = '''
    # 验证响应
    assert response.status_code in [200, 204]'''

    else:
        success_assertion = '''
    assert response.status_code == 200'''

    # 生成异常测试代码
    if method == "GET":
        # GET异常测试：使用不存在的资源ID
        has_path_param = bool(re.search(r'\{[^}]+\}', path))
        if has_path_param:
            # 详情API异常测试：不存在的ID
            invalid_path = re.sub(r'\{([^}]+)\}', '999999', path)
            invalid_test = f'''
def test_{api_name}_not_found():
    """测试 {api_name} 资源不存在场景"""
    url = BASE_URL + "{invalid_path}"

    response = requests.get(url)

    # 记录请求和响应
    log_request_response(f"test_{api_name}_not_found", url, "GET", response)

    # 验证返回404
    assert response.status_code == 404, "不存在的资源应返回404"'''
        else:
            # 列表API异常测试：使用无效查询参数
            invalid_test = f'''
def test_{api_name}_invalid_query():
    """测试 {api_name} 无效查询参数场景"""
    url = BASE_URL + "{path_with_params}?invalid_param=test"

    response = requests.get(url)

    # 记录请求和响应
    log_request_response(f"test_{api_name}_invalid_query", url, "GET", response)

    # 验证API能处理（可能忽略无效参数或返回错误）
    assert response.status_code in [200, 400, 422], "应返回有效状态码"'''

    elif method == "POST":
        # POST异常测试：发送空请求体
        invalid_test = f'''
def test_{api_name}_missing_fields():
    """测试 {api_name} 缺少必需字段场景"""
    url = BASE_URL + "{path_with_params}"

    # 发送空请求体
    response = requests.post(url, json={{}})

    # 记录请求和响应
    log_request_response(f"test_{api_name}_missing_fields", url, "POST", response, {{}})

    # 验证返回错误（400或422）
    assert response.status_code in [400, 422], "缺少必需字段应返回400或422"'''

    elif method == "PUT":
        # PUT异常测试：更新不存在的资源
        invalid_path = re.sub(r'\{([^}]+)\}', '999999', path)
        invalid_test = f'''
def test_{api_name}_not_found():
    """测试 {api_name} 更新不存在的资源"""
    url = BASE_URL + "{invalid_path}"

    response = requests.put(url, json={{"title": "updated"}})

    # 记录请求和响应
    log_request_response(f"test_{api_name}_not_found", url, "PUT", response, {{"title": "updated"}})

    # 验证返回404
    assert response.status_code == 404, "更新不存在的资源应返回404"'''

    elif method == "DELETE":
        # DELETE异常测试：删除不存在的资源
        invalid_path = re.sub(r'\{([^}]+)\}', '999999', path)
        invalid_test = f'''
def test_{api_name}_not_found():
    """测试 {api_name} 删除不存在的资源"""
    url = BASE_URL + "{invalid_path}"

    response = requests.delete(url)

    # 记录请求和响应
    log_request_response(f"test_{api_name}_not_found", url, "DELETE", response)

    # 验证返回404
    assert response.status_code == 404, "删除不存在的资源应返回404"'''

    else:
        invalid_test = ''

    test_code = f'''import requests
import pytest
import json
import os
from datetime import datetime

# BASE_URL 从 Swagger 文档的 servers 字段自动提取
BASE_URL = "{base_url}"

# 日志文件路径
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'reports', 'api_detailed_log.jsonl')


def log_request_response(test_name, url, method, response, request_body=None):
    """记录API请求和响应的详细信息"""
    log_entry = {{
        "timestamp": datetime.now().isoformat(),
        "test_name": test_name,
        "request": {{
            "url": url,
            "method": method,
            "body": request_body
        }},
        "response": {{
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text[:1000] if response.text else "",  # 限制响应体大小
            "response_time_ms": response.elapsed.total_seconds() * 1000
        }}
    }}

    # 追加到日志文件
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\\n')


def test_{api_name}_success():
    """测试 {api_name} 正常场景"""
    url = BASE_URL + "{path_with_params}"
    method = "{method}"

    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json={{"key": "value"}})
    elif method == "PUT":
        response = requests.put(url, json={{"key": "value"}})
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        pytest.skip(f"Unsupported method: {{method}}")

    # 记录请求和响应
    log_request_response(f"test_{api_name}_success", url, method, response)

{success_assertion}

{invalid_test}
'''

    return test_code


def save_test_file(test_code: str, output_path: str) -> None:
    """
    保存测试代码到文件

    Args:
        test_code: 生成的测试代码
        output_path: 输出文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(test_code)


def generate_test_filename(api: dict) -> str:
    """
    生成语义化的测试文件名

    规则：
    - 提取路径最后一个有意义的部分
    - 结合HTTP方法（get/post/put/delete）
    - 区分列表API和详情API
    - 转换为小写，用下划线连接

    示例：
    - GET /api/posts → test_get_posts.py (列表API，保持复数)
    - GET /api/posts/{postId} → test_get_post_detail.py (详情API，单数+detail)
    - POST /api/users → test_post_users.py (创建API，复数)
    - DELETE /api/posts/{postId} → test_delete_post_detail.py (删除API)

    Args:
        api: API 信息字典

    Returns:
        测试文件名（不含扩展名）
    """
    path = api['path']
    method = api['method'].lower()

    # 移除开头的斜杠
    path = path.lstrip('/')

    # 检查是否包含路径参数（详情API）
    import re
    has_path_params = bool(re.search(r'\{[^}]+\}', path))

    # 分割路径
    path_parts = path.split('/')

    # 提取最后一个有意义的部分（非路径参数）
    resource_name = None
    for part in reversed(path_parts):
        # 跳过路径参数（花括号包裹的）
        if part and not (part.startswith('{') and part.endswith('}')):
            resource_name = part
            break

    # 如果没有找到有意义的部分，使用 summary
    if not resource_name:
        summary = api.get('summary', 'api')
        # 从摘要中提取关键词（取第一个词）
        resource_name = summary.split()[0].lower()

    # 清理资源名称：移除特殊字符，转为小写
    resource_name = resource_name.lower().replace('-', '_').replace(' ', '_')

    # 根据是否有路径参数决定命名
    if has_path_params:
        # 详情API：单数化 + _detail
        if resource_name.endswith('s') and len(resource_name) > 3:
            resource_name = resource_name[:-1]  # posts → post
        filename = f"test_{method}_{resource_name}_detail"
    else:
        # 列表API：保持复数形式
        filename = f"test_{method}_{resource_name}"

    return filename


def generate_tests_for_apis(apis: list, base_url: str = "http://localhost:8000", output_dir: str = 'tests') -> list:
    """
    为多个 API 生成测试文件

    Args:
        apis: API 信息列表
        base_url: API的基础URL（从swagger文档中提取）
        output_dir: 测试文件输出目录

    Returns:
        生成的测试文件路径列表
    """
    test_files = []

    for api in apis:
        # 生成语义化的文件名
        test_name = generate_test_filename(api)

        # 生成API名称（用于测试函数命名）
        resource_name = test_name.replace('test_', '').replace(f"_{api['method'].lower()}_", '')

        # 生成测试代码
        api_description = f"API: {api['method']} {api['path']}\\n描述: {api['summary']}"
        test_code = generate_test_code(api_description, resource_name, base_url)

        # 保存测试文件
        test_file_path = os.path.join(output_dir, f'{test_name}.py')
        save_test_file(test_code, test_file_path)

        test_files.append(test_file_path)

    return test_files
