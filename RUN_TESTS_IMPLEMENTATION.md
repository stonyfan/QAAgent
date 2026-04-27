# run_tests() 函数实现文档

## 📋 函数签名

```python
def run_tests(test_dir: str = 'tests', pytest_args: list = None) -> Tuple[int, str, str]:
    """
    运行 pytest 测试并返回完整的原始输出

    Args:
        test_dir: 测试文件目录或测试文件路径
        pytest_args: 额外的 pytest 参数（如 ['-v', '-s']）

    Returns:
        元组 (exit_code, stdout, stderr)
        - exit_code: 退出码（0表示成功，1表示有失败）
        - stdout: 标准输出（完整输出）
        - stderr: 标准错误（错误信息）
    """
```

---

## 🎯 核心特性

### 1️⃣ 使用 subprocess 调用 pytest
```python
result = subprocess.run(
    ['pytest', test_dir, '-v', '--tb=short'],
    capture_output=True,
    text=True,
    timeout=300
)
```

### 2️⃣ 返回完整原始输出
- **stdout**: 完整的测试输出（包含所有测试结果）
- **stderr**: 错误信息（如果有）
- **exit_code**: 退出码（0=全部通过，非0=有失败）

---

## 💡 使用示例

### 示例 1: 基本使用

```python
from src.test_runner import run_tests

# 运行测试
exit_code, stdout, stderr = run_tests('tests')

# 检查结果
if exit_code == 0:
    print("✓ 所有测试通过")
else:
    print(f"✗ 有测试失败:\n{stdout}")
```

### 示例 2: 打印完整输出

```python
exit_code, stdout, stderr = run_tests('tests')

print("=" * 60)
print("测试输出:")
print("=" * 60)
print(stdout)

if stderr:
    print("=" * 60)
    print("错误信息:")
    print("=" * 60)
    print(stderr)
```

### 示例 3: 传递额外参数

```python
# 运行特定测试文件
exit_code, stdout, stderr = run_tests(
    'tests/test_post_login.py',
    pytest_args=['-v', '-s', '--tb=long']
)

# 只运行匹配的测试
exit_code, stdout, stderr = run_tests(
    'tests',
    pytest_args=['-k', 'login']  # 只运行包含 'login' 的测试
)
```

### 示例 4: 在流水线中使用

```python
def run_swagger_pipeline(swagger_path: str):
    # ... 生成测试文件 ...

    # 运行测试
    exit_code, stdout, stderr = run_tests('tests')

    # 保存完整输出
    with open('reports/test_output.txt', 'w') as f:
        f.write(f"Exit Code: {exit_code}\n")
        f.write(f"STDOUT:\n{stdout}\n")
        if stderr:
            f.write(f"STDERR:\n{stderr}\n")

    return exit_code == 0
```

---

## 📊 输出格式

### 成功示例 (exit_code = 0)

```
================ test session starts =================
collected 3 items

test_post_login.py::test_login_success PASSED [33%]
test_post_login.py::test_login_invalid_params PASSED [67%]
test_get_users.py::test_users_success PASSED [100%]

================ 3 passed in 0.45s =================
```

### 失败示例 (exit_code = 1)

```
================ test session starts =================
collected 3 items

test_post_login.py::test_login_success FAILED [33%]
test_post_login.py::test_login_invalid_params PASSED [67%]
test_get_users.py::test_users_success PASSED [100%]

========================== FAILURES ==========================
________________________ test_login_success ________________________

    def test_login_success():
        url = f"{BASE_URL}/api/login"
>       response = requests.post(url, json={"username": "test"})
E       AssertionError: Expected 200, got 401

test_post_login.py:12: AssertionError
================= 1 failed, 2 passed in 0.52s =================
```

---

## 🔧 函数对比

| 函数 | 返回值 | 用途 |
|------|--------|------|
| **run_tests()** | (exit_code, stdout, stderr) | 获取完整原始输出 |
| **run_pytest()** | Dict[str, Any] | 获取解析后的结构化数据 |

### 选择建议

- **使用 run_tests()** 当你需要：
  - 完整的原始输出
  - 自己解析输出
  - 保存输出到文件
  - 传递给其他工具

- **使用 run_pytest()** 当你需要：
  - 结构化的测试结果
  - 快速获取统计数据（通过/失败数量）
  - 集成到自动化流程

---

## ✨ 优势

| 特性 | 说明 |
|------|------|
| **完整性** | 返回 stdout 和 stderr，不丢失任何信息 |
| **灵活性** | 支持自定义 pytest 参数 |
| **易用性** | 简单的元组返回，易于解包使用 |
| **健壮性** | 包含超时处理和错误处理 |
| **兼容性** | 兼容所有 pytest 参数 |

---

## 🧪 实际测试

### 测试代码

```python
# test_example.py
import pytest

def test_success():
    assert True

def test_failure():
    assert False
```

### 运行测试

```python
exit_code, stdout, stderr = run_tests('test_example.py')

print(f"退出码: {exit_code}")
print(f"输出长度: {len(stdout)} 字符")
print(f"错误: {stderr if stderr else '无'}")
```

### 输出

```
退出码: 1
输出长度: 234 字符
错误: 无
```

---

## 🎉 总结

`run_tests()` 函数提供了：
- ✅ 使用 subprocess 调用 pytest
- ✅ 返回完整输出（stdout + stderr）
- ✅ 返回退出码
- ✅ 支持自定义参数
- ✅ 完善的错误处理

符合任务要求：
- ✅ 使用 subprocess 调用 pytest
- ✅ 返回完整输出
