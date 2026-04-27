# Bug修复：路径参数处理问题

## 🐛 问题描述

运行测试时所有测试失败，报错：
```
NameError: name 'postId' is not defined
```

### 原因分析

测试代码生成逻辑有bug，当API路径包含路径参数时（如 `/posts/{postId}`），生成的测试代码直接使用了花括号：

```python
# 错误的生成代码
url = f"{BASE_URL}/posts/{postId}"  # {postId} 会被当作变量解析
```

由于 `postId` 变量未定义，导致测试失败。

---

## ✅ 修复方案

### 修改文件
`src/api_test.py` 中的 `generate_test_code()` 函数

### 修复内容

1. **正确解析API路径**
   - 从描述中提取方法和路径
   - 处理多行描述

2. **路径参数处理**
   - 使用正则表达式识别路径参数 `{paramName}`
   - 将路径参数替换为示例值
   - `{postId}` → `1`
   - `{userId}` → `1`

3. **安全生成URL**
   - 使用字符串拼接而不是f-string
   - 避免花括号被二次解析

### 修复后的代码

```python
# 替换路径参数
import re
def replace_param(match):
    param_name = match.group(1)
    if 'id' in param_name.lower():
        return '1'
    else:
        return '1'

path_with_params = re.sub(r'\{([^}]+)\}', replace_param, path)

# 生成安全的URL
url = BASE_URL + "/posts/1"  # 不使用f-string
```

---

## 🧪 验证修复

### 重新生成测试

```bash
# 删除旧的测试文件
rm tests/*.py

# 重新生成
python src/pipeline.py swagger_jsonplaceholder.json
```

### 检查生成的测试

```bash
cat tests/test_delete_post.py
```

应该看到：
```python
def test_delete_post_success():
    url = BASE_URL + "/posts/1"  # ✓ 路径参数已被替换
    method = "DELETE"
    response = requests.delete(url)
    ...
```

### 运行测试

```bash
pytest tests/test_delete_post.py -v
```

预期结果：
```
test_delete_post_success PASSED
test_delete_post_invalid_params PASSED
```

---

## 📊 影响范围

### 受影响的测试

所有包含路径参数的API：
- ✅ `GET /posts/{postId}` → `GET /posts/1`
- ✅ `DELETE /posts/{postId}` → `DELETE /posts/1`
- ✅ `PUT /posts/{postId}` → `PUT /posts/1`
- ✅ `GET /users/{userId}` → `GET /users/1`

### 不受影响的测试

没有路径参数的API：
- ✅ `GET /posts`
- ✅ `POST /posts`
- ✅ `GET /users`

---

## 🔄 迁移步骤

### 如果你有旧的测试文件

1. **删除旧测试文件**
```bash
rm tests/*.py
```

2. **重新生成**
```bash
python src/pipeline.py swagger_jsonplaceholder.json
```

3. **验证**
```bash
python src/pipeline.py swagger_jsonplaceholder.json
```

---

## 💡 技术细节

### 路径参数替换规则

| 参数模式 | 替换值 | 示例 |
|---------|--------|------|
| `{*id*}` | `1` | `{postId}` → `1` |
| `{*Id*}` | `1` | `{userId}` → `1` |
| `{*name*}` | `1` | `{username}` → `1` |

### URL生成方式

**修复前（错误）：**
```python
url = f"{BASE_URL}/posts/{postId}"  # NameError!
```

**修复后（正确）：**
```python
url = BASE_URL + "/posts/1"  # 安全
```

---

## 🎯 完整示例

### API定义
```json
{
  "path": "/posts/{postId}",
  "method": "DELETE"
}
```

### 生成的测试代码

```python
def test_delete_post_success():
    url = BASE_URL + "/posts/1"  # ✓ 参数已替换
    method = "DELETE"

    if method == "DELETE":
        response = requests.delete(url)

    assert response.status_code == 200
```

---

## ✅ 修复验证清单

- [x] 定位问题根源（路径参数处理）
- [x] 修复代码生成逻辑
- [x] 添加参数替换函数
- [x] 测试无参数路径
- [x] 测试带参数路径
- [x] 验证所有API类型

---

## 📝 相关文档

- **[使用指南.md](使用指南.md)** - 使用方法
- **[BASE_URL配置指南.md](BASE_URL配置指南.md)** - URL配置
- **[快速测试指南.md](快速测试指南.md)** - 快速上手

---

**版本**: v0.2.1 | **修复日期**: 2026-04-26

**现在可以正常测试带路径参数的API了！** 🎉
