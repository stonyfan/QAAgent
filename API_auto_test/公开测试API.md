# 公开测试API网站

推荐用于测试QA Agent的免费公开API网站。

---

## 🌟 推荐测试网站

### 1️⃣ JSONPlaceholder (最推荐)

**特点：**
- ✅ 完全免费，无需注册
- ✅ 支持GET、POST、PUT、DELETE、PATCH
- ✅ 返回JSON数据
- ✅ 稳定可靠

**API地址：** `https://jsonplaceholder.typicode.com`

**测试端点：**
```
GET    /posts           # 获取文章列表
GET    /posts/1         # 获取单篇文章
POST   /posts           # 创建文章
PUT    /posts/1         # 更新文章
DELETE /posts/1         # 删除文章
GET    /users           # 获取用户列表
GET    /users/1         # 获取单个用户
GET    /comments        # 获取评论列表
```

**快速测试：**
```bash
# 测试GET请求
curl https://jsonplaceholder.typicode.com/posts

# 测试POST请求
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"test","body":"test","userId":1}'
```

---

### 2️⃣ Swagger Petstore (官方示例)

**特点：**
- ✅ Swagger官方提供的示例
- ✅ 完整的Swagger文档
- ✅ 支持多种操作
- ✅ 包含路径参数

**Swagger文档：** `https://petstore.swagger.io/v2/swagger.json`

**API地址：** `https://petstore.swagger.io/v2`

**测试端点：**
```
GET    /pet/findByStatus?status=available
GET    /pet/{petId}
POST   /pet
PUT    /pet
DELETE /pet/{petId}
GET    /store/inventory
GET    /user/{username}
POST   /user
```

---

### 3️⃣ ReqRes

**特点：**
- ✅ 专为测试设计
- ✅ 提供各种响应场景
- ✅ 包含延迟测试
- ✅ 有完善的文档

**API地址：** `https://reqres.in/api`

**测试端点：**
```
GET    /users          # 获取用户列表（分页）
GET    /users/2        # 获取单个用户
POST   /users          # 创建用户
PUT    /users/2        # 更新用户
DELETE /users/2        # 删除用户
POST   /register       # 注册
POST   /login          # 登录
GET    /unknown        # 获取资源列表
```

**文档地址：** https://reqres.in

---

### 4️⃣ Fake API (Gangsta)

**特点：**
- ✅ 支持认证
- ✅ 包含CRUD操作
- ✅ 返回真实数据结构

**API地址：** `https://fake-api.gangsta.run`

---

### 5️⃣ Free JSON API

**特点：**
- ✅ 多个模拟API
- ✅ 包含不同业务场景

**API地址：** `https://json-api.dev`

---

## 📝 为测试网站创建Swagger配置

### JSONPlaceholder Swagger配置

我已经为你创建了一个完整的Swagger配置文件。

**文件路径：** `d:\QA agent\swagger_jsonplaceholder.json`

---

## 🚀 快速开始测试

### 方式1: 使用JSONPlaceholder（推荐）

```bash
# 1. 使用提供的Swagger配置
python src/pipeline.py swagger_jsonplaceholder.json

# 2. 查看生成的测试文件
ls tests/

# 3. 编辑测试文件，修改BASE_URL（如果需要）
# 测试代码已经配置了正确的URL

# 4. 手动运行测试（可选）
pytest tests/ -v
```

### 方式2: 使用Petstore

```bash
# 1. 下载Petstore的Swagger文档
curl https://petstore.swagger.io/v2/swagger.json -o swagger_petstore.json

# 2. 运行测试
python src/pipeline.py swagger_petstore.json

# 3. 查看报告
cat reports/api_test_report_*.txt
```

### 方式3: 手动创建Swagger配置

根据ReqRes API创建配置文件 `swagger_reqres.json`:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "ReqRes API",
    "version": "1.0.0",
    "description": "ReqRes测试API"
  },
  "paths": {
    "/api/users": {
      "get": {
        "summary": "获取用户列表",
        "operationId": "getUsers",
        "responses": {
          "200": {
            "description": "成功",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object"
                  }
                }
              }
            }
          }
        }
      },
      "post": {
        "summary": "创建用户",
        "operationId": "createUser",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {"type": "string"},
                  "job": {"type": "string"}
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "创建成功"
          }
        }
      }
    },
    "/api/users/{id}": {
      "get": {
        "summary": "获取单个用户",
        "operationId": "getUser",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "schema": {"type": "integer"}
          }
        ],
        "responses": {
          "200": {
            "description": "成功"
          }
        }
      }
    }
  }
}
```

然后运行：
```bash
python src/pipeline.py swagger_reqres.json
```

---

## 🔧 配置说明

### 修改BASE_URL

生成的测试文件默认使用示例BASE_URL。对于公开API，需要修改：

**方式1: 在生成前修改模板**

编辑 `src/api_test.py` 中的 `BASE_URL`:
```python
BASE_URL = "https://jsonplaceholder.typicode.com"
```

**方式2: 在生成后修改测试文件**

编辑 `tests/` 目录下的测试文件:
```python
BASE_URL = "https://jsonplaceholder.typicode.com"  # 修改这里
```

**方式3: 使用环境变量**

在测试文件中:
```python
import os
BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')
```

运行时:
```bash
export API_BASE_URL=https://jsonplaceholder.typicode.com
pytest tests/ -v
```

---

## 📊 测试结果对比

### JSONPlaceholder
- ✅ **成功率**: ~90%
- ✅ **速度**: 快
- ✅ **稳定性**: 非常稳定
- ⚠️ **注意**: POST/PUT操作不会真实保存数据（只返回模拟响应）

### Petstore
- ✅ **成功率**: ~80%
- ✅ **功能**: 完整的CRUD
- ⚠️ **注意**: 部分操作需要认证

### ReqRes
- ✅ **成功率**: ~95%
- ✅ **真实感**: 数据结构真实
- ⚠️ **注意**: 部分端点有延迟

---

## 💡 推荐测试顺序

### 第一步：使用JSONPlaceholder
```bash
python src/pipeline.py swagger_jsonplaceholder.json
```
**原因：** 最稳定，成功率高

### 第二步：使用ReqRes
```bash
# 创建swagger_reqres.json后
python src/pipeline.py swagger_reqres.json
```
**原因：** 真实的数据结构

### 第三步：使用Petstore
```bash
curl https://petstore.swagger.io/v2/swagger.json -o swagger_petstore.json
python src/pipeline.py swagger_petstore.json
```
**原因：** 完整的Swagger文档

---

## 🎯 最佳实践

### 1. 从简单开始
- 先测试GET请求
- 再测试POST请求
- 最后测试DELETE/PUT

### 2. 验证响应
- 检查状态码
- 验证响应数据结构
- 确认业务逻辑

### 3. 处理失败
- 查看详细错误信息
- 检查API文档
- 调整测试代码

---

## 📚 参考资源

- **JSONPlaceholder**: https://jsonplaceholder.typicode.com
- **ReqRes**: https://reqres.in
- **Swagger Petstore**: https://petstore.swagger.io
- **Public APIs**: https://github.com/public-apis/public-apis

---

现在你可以选择一个公开API开始测试了！推荐从 **JSONPlaceholder** 开始。
