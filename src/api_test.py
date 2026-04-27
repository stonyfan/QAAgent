import os
from typing import Dict, Any


def generate_test_code(api_description: str, api_name: str, base_url: str = "http://localhost:8000") -> str:
    """
    根据 API 描述生成增强版 pytest 测试代码

    为每个API生成4个测试函数：
    1. 正常测试
    2. 参数缺失测试
    3. 参数类型错误测试
    4. 边界测试

    Args:
        api_description: API 的自然语言描述
        api_name: API 名称（用于生成文件名）
        base_url: API的基础URL（从swagger文档中提取）

    Returns:
        生成的测试代码字符串
    """
    # 解析API路径和方法
    lines = api_description.split('\n')
    first_line = lines[0]

    # 提取方法和路径
    if 'API:' in first_line:
        api_part = first_line.split('API: ')[1]
        parts = api_part.split()
        method = parts[0]
        path = parts[1] if len(parts) > 1 else '/'
    else:
        method = 'GET'
        path = '/'

    # 处理路径参数
    import re
    def replace_param(match):
        param_name = match.group(1)
        if 'id' in param_name.lower():
            return '1'
        else:
            return '1'

    path_with_params = re.sub(r'\{([^}]+)\}', replace_param, path)
    has_path_param = bool(re.search(r'\{[^}]+\}', path))

    # 生成4个测试函数
    test_functions = []

    # ===== 测试1：正常场景 =====
    if method == "GET":
        success_test = f'''def test_{api_name}_success():
    """测试 {api_name} 正常场景"""
    url = BASE_URL + "{path_with_params}"

    response = requests.get(url)
    log_request_response(f"test_{api_name}_success", url, "GET", response)

    # status code断言
    assert response.status_code == 200, "请求应成功"

    # response.json()校验
    data = response.json()
    assert isinstance(data, (dict, list)), "响应应该是字典或列表"

    # 字段存在性检查
    if isinstance(data, dict):
        assert "id" in data or "code" in data, "响应必须包含标识字段"
    elif isinstance(data, list) and len(data) > 0:
        assert len(data) > 0, "列表不应为空"'''

    elif method == "POST":
        success_test = f'''def test_{api_name}_success():
    """测试 {api_name} 正常场景"""
    url = BASE_URL + "{path_with_params}"
    request_body = {{"title": "Test Title", "content": "Test Content"}}

    response = requests.post(url, json=request_body)
    log_request_response(f"test_{api_name}_success", url, "POST", response, request_body)

    # status code断言
    assert response.status_code in [200, 201], "创建应返回200或201"

    # response.json()校验
    data = response.json()
    assert data is not None, "响应不应为空"

    # 字段存在性检查
    assert "id" in data, "创建成功必须返回id字段"
    if response.status_code == 201:
        assert "Location" in response.headers, "201应包含Location头"'''

    elif method == "PUT":
        success_test = f'''def test_{api_name}_success():
    """测试 {api_name} 正常场景"""
    url = BASE_URL + "{path_with_params}"
    request_body = {{"title": "Updated Title", "content": "Updated Content"}}

    response = requests.put(url, json=request_body)
    log_request_response(f"test_{api_name}_success", url, "PUT", response, request_body)

    # status code断言
    assert response.status_code == 200, "更新应返回200"

    # response.json()校验
    data = response.json()
    assert data is not None, "响应不应为空"

    # 字段存在性检查
    assert "id" in data, "响应必须包含id字段"'''

    elif method == "DELETE":
        success_test = f'''def test_{api_name}_success():
    """测试 {api_name} 正常场景"""
    url = BASE_URL + "{path_with_params}"

    response = requests.delete(url)
    log_request_response(f"test_{api_name}_success", url, "DELETE", response)

    # status code断言
    assert response.status_code in [200, 204], "删除应返回200或204"

    # DELETE成功通常无响应体或为空
    if response.status_code == 200:
        data = response.json()
        assert data is not None, "响应不应为空"'''

    test_functions.append(success_test)

    # ===== 测试2：参数缺失测试 =====
    if method == "GET":
        if has_path_param:
            # 详情API：无法真正测试路径参数缺失（会被路由拒绝）
            # 改为测试缺少必需查询参数
            missing_test = f'''def test_{api_name}_missing_params():
    """测试 {api_name} 缺少必需参数场景"""
    # 测试空字符串参数
    url = BASE_URL + "{path_with_params}" + "?page="

    response = requests.get(url)
    log_request_response(f"test_{api_name}_missing_params", url, "GET", response)

    # status code断言
    assert response.status_code in [200, 400, 422], "应返回有效状态码"

    # response.json()校验
    if response.status_code >= 400:
        error = response.json()
        assert "error" in error or "message" in error, "错误响应应包含错误信息"'''
        else:
            # 列表API：测试缺少分页参数
            missing_test = f'''def test_{api_name}_missing_params():
    """测试 {api_name} 缺少必需参数场景"""
    url = BASE_URL + "{path_with_params}"

    response = requests.get(url)
    log_request_response(f"test_{api_name}_missing_params", url, "GET", response)

    # status code断言（可能使用默认值）
    assert response.status_code in [200, 400, 422], "应返回有效状态码"

    # response.json()校验
    data = response.json()
    assert isinstance(data, (dict, list)), "响应应该是字典或列表"'''

    elif method in ["POST", "PUT"]:
        missing_test = f'''def test_{api_name}_missing_params():
    """测试 {api_name} 缺少必需参数场景"""
    url = BASE_URL + "{path_with_params}"

    # 发送空请求体
    response = requests.{method.lower()}(url, json={{}})
    log_request_response(f"test_{api_name}_missing_params", url, "{method}", response, {{}})

    # status code断言
    assert response.status_code in [400, 422], "缺少参数应返回400或422"

    # response.json()校验
    error = response.json()
    assert isinstance(error, dict), "错误响应应该是字典"

    # 字段存在性检查
    assert "error" in error or "message" in error or "detail" in error, "错误响应应包含错误信息"'''

    else:  # DELETE
        missing_test = f'''def test_{api_name}_missing_params():
    """测试 {api_name} 参数缺失（DELETE无body，跳过）"""
    # DELETE请求通常无body，此测试跳过
    pytest.skip("DELETE请求无需测试参数缺失")'''

    test_functions.append(missing_test)

    # ===== 测试3：参数类型错误测试 =====
    if method == "GET":
        if has_path_param:
            # 详情API：路径参数类型错误
            invalid_type_path = re.sub(r'\{[^}]+\}', 'invalid', path)
            invalid_type_test = f'''def test_{api_name}_invalid_type():
    """测试 {api_name} 参数类型错误场景"""
    url = BASE_URL + "{invalid_type_path}"

    response = requests.get(url)
    log_request_response(f"test_{api_name}_invalid_type", url, "GET", response)

    # status code断言
    assert response.status_code in [400, 404, 422], "类型错误应返回400/404/422"

    # response.json()校验
    if response.status_code >= 400:
        error = response.json()
        assert "error" in error or "message" in error, "错误响应应包含错误信息"'''
        else:
            # 列表API：查询参数类型错误
            invalid_type_test = f'''def test_{api_name}_invalid_type():
    """测试 {api_name} 参数类型错误场景"""
    url = BASE_URL + "{path_with_params}?page=abc"

    response = requests.get(url)
    log_request_response(f"test_{api_name}_invalid_type", url, "GET", response)

    # status code断言
    assert response.status_code in [200, 400, 422], "应返回有效状态码"

    # response.json()校验
    data = response.json()
    assert isinstance(data, (dict, list)), "响应应该是字典或列表"'''

    elif method in ["POST", "PUT"]:
        invalid_type_test = f'''def test_{api_name}_invalid_type():
    """测试 {api_name} 参数类型错误场景"""
    url = BASE_URL + "{path_with_params}"

    # 发送错误类型的参数（数字字段传字符串）
    response = requests.{method.lower()}(url, json={{"id": "not_a_number"}})
    log_request_response(f"test_{api_name}_invalid_type", url, "{method}", response, {{"id": "not_a_number"}})

    # status code断言
    assert response.status_code in [400, 422], "类型错误应返回400或422"

    # response.json()校验
    error = response.json()
    assert isinstance(error, dict), "错误响应应该是字典"

    # 字段存在性检查
    assert "error" in error or "message" in error, "错误响应应包含错误信息"'''

    else:  # DELETE
        invalid_type_test = f'''def test_{api_name}_invalid_type():
    """测试 {api_name} 参数类型错误（DELETE路径参数）"""
    # 使用无效ID类型
    url = BASE_URL + "{re.sub(r'\{[^}]+\}', 'invalid', path_with_params)}"

    response = requests.delete(url)
    log_request_response(f"test_{api_name}_invalid_type", url, "DELETE", response)

    # status code断言
    assert response.status_code in [400, 404], "无效类型应返回400或404"

    # response.json()校验
    if response.status_code >= 400:
        error = response.json()
        assert isinstance(error, dict), "错误响应应该是字典"'''

    test_functions.append(invalid_type_test)

    # ===== 测试4：边界测试 =====
    if method == "GET":
        boundary_test = f'''def test_{api_name}_boundary():
    """测试 {api_name} 边界值场景"""
    # 测试极大的分页值
    url = BASE_URL + "{path_with_params}?page=999999"

    response = requests.get(url)
    log_request_response(f"test_{api_name}_boundary", url, "GET", response)

    # status code断言
    assert response.status_code in [200, 400, 422], "应返回有效状态码"

    # response.json()校验
    data = response.json()
    assert isinstance(data, (dict, list)), "响应应该是字典或列表"'''

    elif method == "POST":
        boundary_test = f'''def test_{api_name}_boundary():
    """测试 {api_name} 边界值场景"""
    url = BASE_URL + "{path_with_params}"

    # 测试空字符串
    response = requests.post(url, json={{"title": "", "content": ""}})
    log_request_response(f"test_{api_name}_boundary", url, "POST", response, {{"title": "", "content": ""}})

    # status code断言（可能接受空值或拒绝）
    assert response.status_code in [200, 201, 400, 422], "应返回有效状态码"

    # response.json()校验
    if response.status_code >= 400:
        error = response.json()
        assert "error" in error or "message" in error, "错误响应应包含错误信息"
    else:
        data = response.json()
        assert "id" in data, "响应应包含id字段"'''

    elif method == "PUT":
        boundary_test = f'''def test_{api_name}_boundary():
    """测试 {api_name} 边界值场景"""
    # 测试更新不存在的资源
    url = BASE_URL + "{re.sub(r'\{[^}]+\}', '999999', path_with_params)}"

    response = requests.put(url, json={{"title": "Updated"}})
    log_request_response(f"test_{api_name}_boundary", url, "PUT", response, {{"title": "Updated"}})

    # status code断言
    assert response.status_code == 404, "更新不存在的资源应返回404"

    # response.json()校验
    error = response.json()
    assert isinstance(error, dict), "错误响应应该是字典"

    # 字段存在性检查
    assert "error" in error or "message" in error, "错误响应应包含错误信息"'''

    else:  # DELETE
        boundary_test = f'''def test_{api_name}_boundary():
    """测试 {api_name} 边界值场景"""
    # 测试删除不存在的资源
    url = BASE_URL + "{re.sub(r'\{[^}]+\}', '999999', path_with_params)}"

    response = requests.delete(url)
    log_request_response(f"test_{api_name}_boundary", url, "DELETE", response)

    # status code断言
    assert response.status_code == 404, "删除不存在的资源应返回404"

    # response.json()校验
    if response.text:
        error = response.json()
        assert isinstance(error, dict), "错误响应应该是字典"
        assert "error" in error or "message" in error, "错误响应应包含错误信息"'''

    test_functions.append(boundary_test)

    # 组装完整的测试代码
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
            "body": response.text[:1000] if response.text else "",
            "response_time_ms": response.elapsed.total_seconds() * 1000
        }}
    }}

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\\n')


{chr(10).join(test_functions)}
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
        api_description = f"API: {api['method']} {api['path']}\n描述: {api['summary']}"
        test_code = generate_test_code(api_description, resource_name, base_url)

        # 保存测试文件
        test_file_path = os.path.join(output_dir, f'{test_name}.py')
        save_test_file(test_code, test_file_path)

        test_files.append(test_file_path)

    return test_files
