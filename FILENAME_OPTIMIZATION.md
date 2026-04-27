# 测试文件命名优化文档

## 📋 优化目标

- ✅ 每个API一个独立文件
- ✅ 文件名语义清晰
- ✅ 包含HTTP方法
- ✅ 自动处理复数形式

---

## 🔄 优化前后对比

### 示例 1: POST /api/login

| 优化前 | 优化后 |
|--------|--------|
| `test_api_login.py` | `test_post_login.py` |

**改进：**
- ✅ 明确显示HTTP方法（POST）
- ✅ 简化路径，去除冗余的 `api_` 前缀

---

### 示例 2: GET /api/users

| 优化前 | 优化后 |
|--------|--------|
| `test_api_users.py` | `test_get_users.py` |

**改进：**
- ✅ 明确显示HTTP方法（GET）
- ✅ 简化路径

---

### 示例 3: GET /api/users/{userId}

| 优化前 | 优化后 |
|--------|--------|
| `test_api_users__userId_` | `test_get_user.py` |

**改进：**
- ✅ 自动移除路径参数 `{userId}`
- ✅ 自动将复数 `users` 转为单数 `user`
- ✅ 文件名更简洁清晰

---

### 示例 4: PUT /api/products/{productId}

| 优化前 | 优化后 |
|--------|--------|
| `test_api_products__productId_` | `test_put_product.py` |

**改进：**
- ✅ 明确显示HTTP方法（PUT）
- ✅ 移除路径参数
- ✅ 复数转单数

---

## 🎯 命名规则

### 1️⃣ 基础格式
```
test_{http_method}_{resource_name}.py
```

### 2️⃣ HTTP方法映射
- `GET` → `get_`
- `POST` → `post_`
- `PUT` → `put_`
- `DELETE` → `delete_`
- `PATCH` → `patch_`

### 3️⃣ 资源名称提取
- 提取路径最后一个有意义的部分
- 移除路径参数（如 `{userId}`）
- 自动复数转单数（`users` → `user`）
- 转换为小写，特殊字符转下划线

### 4️⃣ 命名示例

| API路径 | HTTP方法 | 文件名 |
|---------|---------|--------|
| `/api/login` | POST | `test_post_login.py` |
| `/api/users` | GET | `test_get_users.py` |
| `/api/users/{userId}` | GET | `test_get_user.py` |
| `/api/products` | POST | `test_post_product.py` |
| `/api/products/{id}` | PUT | `test_put_product.py` |
| `/api/orders/{orderId}` | DELETE | `test_delete_order.py` |

---

## 🔧 实现细节

### 核心函数：`generate_test_filename(api)`

```python
def generate_test_filename(api: dict) -> str:
    """
    生成语义化的测试文件名

    步骤：
    1. 提取路径最后一个有意义的部分
    2. 移除路径参数
    3. 复数转单数
    4. 组合：test_{method}_{resource}
    """
    # ... 实现代码
```

### 处理逻辑

1. **路径解析**
   - `/api/users/{userId}` → `['api', 'users', '{userId}']`

2. **提取资源名**
   - 从后向前找第一个非路径参数的部分 → `users`

3. **单数化**
   - `users` → `user`

4. **组合文件名**
   - `GET` + `user` → `test_get_user.py`

---

## ✨ 优势

| 特性 | 说明 |
|------|------|
| **可读性** | 文件名即文档，一眼看出测试内容 |
| **组织性** | 按HTTP方法和资源分组，易于管理 |
| **一致性** | 统一的命名规则，降低认知负担 |
| **可扩展** | 规则清晰，易于扩展新场景 |

---

## 📊 实际效果

### 输入：swagger.json

```json
{
  "paths": {
    "/api/login": { "post": {...} },
    "/api/users": { "get": {...} },
    "/api/users/{userId}": { "get": {...} }
  }
}
```

### 输出：测试文件

```
tests/
├── test_post_login.py      # POST /api/login
├── test_get_users.py       # GET /api/users
└── test_get_user.py        # GET /api/users/{userId}
```

---

## 🎉 总结

优化后的文件命名：
- ✅ 语义清晰，易于理解
- ✅ 包含HTTP方法，便于区分
- ✅ 自动处理边界情况（路径参数、复数）
- ✅ 统一规范，便于维护

符合项目要求：每个API一个文件，文件名语义清晰（test_login.py）
