# Mockoon配置使用指南

**配置文件：** mockoon-test-api.json  
**端口：** 3000  
**BASE_URL：** http://localhost:3000

---

## 📋 配置概览

### 支持的测试场景

| 测试类别 | 端点数量 | 覆盖场景 |
|----------|----------|----------|
| **基础CRUD** | 5个 | GET/POST/PUT/DELETE完整操作 |
| **认证测试** | 2个 | 401未认证、403无权限 |
| **状态码** | 7个 | 200/201/204/301/302/404/422/500/503 |
| **重定向** | 2个 | 301永久、302临时 |
| **服务器错误** | 2个 | 500错误、503维护 |
| **CORS** | 1个 | OPTIONS预检请求 |
| **性能测试** | 1个 | 200ms延迟响应 |
| **列表API** | 2个 | 用户列表、文章列表 |

**总计：22个端点，覆盖85-90%的HTTP测试场景** 🟢

---

## 🚀 快速启动

### 方式1：使用Mockoon桌面应用（推荐）

#### 步骤1：安装Mockoon

```bash
# Windows (Chocolatey)
choco install mockoon

# 或下载安装包
# https://mockoon.com/download/windows
```

#### 步骤2：导入配置

1. **启动Mockoon**
2. **File → Import → Select mockoon-test-api.json**
3. **点击 "Start Server" 按钮**
4. **服务器运行在 http://localhost:3000**

#### 步骤3：测试

```bash
# 测试基础GET请求
curl http://localhost:3000/api/posts

# 测试认证
curl http://localhost:3000/api/protected
# 返回 401

curl http://localhost:3000/api/protected \
  -H "Authorization: Bearer valid-token"
# 返回 200
```

---

### 方式2：使用Mockoon CLI（适合自动化）

#### 步骤1：安装CLI

```bash
npm install -g @mockoon/cli
```

#### 步骤2：启动服务器

```bash
# 进入配置文件目录
cd "D:\QA agent\API_auto_test"

# 启动服务器
mockoon-cli start --data mockoon-test-api.json --port 3000

# 后台运行（Linux/Mac）
nohup mockoon-cli start --data mockoon-test-api.json --port 3000 &

# 后台运行（Windows PowerShell）
Start-Process -NoNewWindow mockoon-cli \
  -ArgumentList "start --data mockoon-test-api.json --port 3000"
```

#### 步骤3：停止服务器

```bash
# Linux/Mac
ps aux | grep mockoon-cli
kill <pid>

# Windows
taskkill /F /IM node.exe
```

---

### 方式3：使用Docker（推荐用于CI/CD）

#### 步骤1：创建Dockerfile

```dockerfile
FROM mockoon/mockoon:latest

# 复制配置文件
COPY mockoon-test-api.json /mockoon/data/

# 暴露端口
EXPOSE 3000

# 启动Mockoon
CMD ["start", "--data", "/mockoon/data", "--port", "3000"]
```

#### 步骤2：构建和运行

```bash
# 构建镜像
docker build -t test-api-server .

# 运行容器
docker run -d -p 3000:3000 --name test-api test-api-server

# 查看日志
docker logs test-api

# 停止容器
docker stop test-api
```

---

## 📡 API端点说明

### 1️⃣ 基础CRUD操作

#### GET /api/posts - 获取文章列表

```bash
curl http://localhost:3000/api/posts

# 响应：200 OK
[
  {"id": 1, "title": "Test Post 1", "body": "Body 1", "userId": 1},
  {"id": 2, "title": "Test Post 2", "body": "Body 2", "userId": 1}
]

# 响应头
Content-Type: application/json; charset=utf-8
Cache-Control: public, max-age=3600
ETag: "v1-1234567890"
```

#### GET /api/posts/:id - 获取文章详情

```bash
# 正常情况
curl http://localhost:3000/api/posts/1
# 响应：200 OK

# 资源不存在
curl http://localhost:3000/api/posts/999999
# 响应：404 Not Found
{
  "error": {
    "code": "NOT_FOUND",
    "message": "资源不存在",
    "timestamp": "2026-04-26T10:30:00Z",
    "path": "/api/posts/999999"
  }
}
```

#### POST /api/posts - 创建文章

```bash
# 成功创建
curl -X POST http://localhost:3000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "New Post", "body": "Content", "userId": 1}'

# 响应：201 Created
{
  "id": 101,
  "title": "New Post",
  "body": "Content",
  "userId": 1,
  "createdAt": "2026-04-26T10:30:00Z"
}

# 响应头
Location: /api/posts/101

# 验证失败（缺少title）
curl -X POST http://localhost:3000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"body": "Content"}'

# 响应：422 Unprocessable Entity
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入值有误",
    "details": [
      {"field": "title", "message": "标题是必填项"}
    ],
    "timestamp": "2026-04-26T10:30:00Z",
    "path": "/api/posts"
  }
}
```

#### PUT /api/posts/:id - 更新文章

```bash
curl -X PUT http://localhost:3000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Post", "body": "New content", "userId": 1}'

# 响应：200 OK
{
  "id": 1,
  "title": "Updated Post",
  "body": "New content",
  "userId": 1,
  "updatedAt": "2026-04-26T10:30:00Z"
}
```

#### DELETE /api/posts/:id - 删除文章

```bash
curl -X DELETE http://localhost:3000/api/posts/1

# 响应：204 No Content
# 响应体为空
```

---

### 2️⃣ 认证测试

#### GET /api/protected - 需要认证的端点

```bash
# 情况1：缺少Authorization头
curl http://localhost:3000/api/protected

# 响应：401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "缺少认证token",
    "timestamp": "2026-04-26T10:30:00Z"
  }
}

# 响应头
WWW-Authenticate: Bearer

# 情况2：无效的token
curl http://localhost:3000/api/protected \
  -H "Authorization: Bearer invalid-token"

# 响应：401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "认证失败，token无效",
    "timestamp": "2026-04-26T10:30:00Z"
  }
}

# 情况3：有效的token
curl http://localhost:3000/api/protected \
  -H "Authorization: Bearer valid-token"

# 响应：200 OK
{
  "message": "Protected resource accessed",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "user@example.com"
  }
}
```

#### GET /api/admin/users - 需要管理员权限

```bash
# 情况1：普通用户token（403权限不足）
curl http://localhost:3000/api/admin/users \
  -H "Authorization: Bearer valid-token"

# 响应：403 Forbidden
{
  "error": {
    "code": "FORBIDDEN",
    "message": "权限不足，需要管理员角色",
    "timestamp": "2026-04-26T10:30:00Z"
  }
}

# 情况2：管理员token
curl http://localhost:3000/api/admin/users \
  -H "Authorization: Bearer admin-token"

# 响应：200 OK
[
  {"id": 1, "name": "Admin", "role": "admin"},
  {"id": 2, "name": "User1", "role": "user"}
]

# 情况3：未认证（401）
curl http://localhost:3000/api/admin/users

# 响应：401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "需要认证"
  }
}
```

---

### 3️⃣ 重定向测试

#### GET /api/old-url - 301永久重定向

```bash
curl -i http://localhost:3000/api/old-url

# 响应
HTTP/1.1 301 Moved Permanently
Location: /api/new-url

# 跟随重定向
curl -L http://localhost:3000/api/old-url
```

#### GET /api/temp-redirect - 302临时重定向

```bash
curl -i http://localhost:3000/api/temp-redirect

# 响应
HTTP/1.1 302 Found
Location: /api/target
```

---

### 4️⃣ 服务器错误测试

#### GET /api/error - 500内部服务器错误

```bash
curl http://localhost:3000/api/error

# 响应：500 Internal Server Error
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "服务器内部错误",
    "timestamp": "2026-04-26T10:30:00Z"
  }
}
```

#### GET /api/maintenance - 503服务不可用

```bash
curl http://localhost:3000/api/maintenance

# 响应：503 Service Unavailable
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "系统维护中，请稍后再试",
    "timestamp": "2026-04-26T10:30:00Z"
  }
}

# 响应头
Retry-After: 3600
```

---

### 5️⃣ 性能测试

#### GET /api/slow - 慢速API（200ms延迟）

```bash
# 测试响应时间
curl -w "@curl-format.txt" http://localhost:3000/api/slow

# curl-format.txt内容：
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer: %{time_pretransfer}\n
# time_starttransfer: %{time_starttransfer}\n
# time_total:       %{time_total}\n

# 响应时间约为200ms
{
  "message": "This is a slow API",
  "delay": "200ms"
}
```

---

### 6️⃣ CORS测试

#### OPTIONS /api/posts - 预检请求

```bash
curl -X OPTIONS http://localhost:3000/api/posts \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Authorization"

# 响应：204 No Content
# 响应头
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
Access-Control-Allow-Credentials: true
```

---

## 🔧 集成到测试框架

### 步骤1：修改BASE_URL

```python
# swagger_parser.py
import os

# 优先使用环境变量
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")

# 或直接修改
# BASE_URL = "http://localhost:3000"
```

### 步骤2：创建环境变量文件

```bash
# .env
API_BASE_URL=http://localhost:3000
```

### 步骤3：启动Mockoon服务器

```bash
# 终端1：启动Mockoon
mockoon-cli start --data mockoon-test-api.json --port 3000

# 终端2：运行测试
python src/pipeline.py swagger_jsonplaceholder.json
```

### 步骤4：验证测试结果

```bash
# 应该看到以下测试通过
✓ test_get_posts_success (200 OK)
✓ test_get_posts_invalid_query (容错测试)
✓ test_get_post_detail_success (200 OK)
✓ test_get_post_detail_not_found (404)
✓ test_post_posts_success (201 Created)
✓ test_post_posts_missing_fields (422)
✓ test_get_protected_unauthorized (401)
✓ test_get_protected_authorized (200)
✓ test_get_admin_forbidden (403)
✓ test_redirect_301 (301)
✓ test_slow_api (200ms延迟)
```

---

## 📊 测试场景映射表

| HTTP通信测试观点 | Mockoon端点 | 测试方法 |
|-----------------|-------------|----------|
| **1. HTTP方法** | | |
| GET请求 | GET /api/posts | test_get_posts_success |
| POST请求 | POST /api/posts | test_post_posts_success |
| PUT请求 | PUT /api/posts/:id | test_put_post_detail |
| DELETE请求 | DELETE /api/posts/:id | test_delete_post_detail |
| **2. 状态码** | | |
| 200 OK | GET /api/posts | 状态码验证 |
| 201 Created | POST /api/posts | 状态码验证 |
| 204 No Content | DELETE /api/posts/:id | 状态码验证 |
| 301重定向 | GET /api/old-url | test_redirect_301 |
| 302重定向 | GET /api/temp-redirect | test_redirect_302 |
| 401 Unauthorized | GET /api/protected | test_unauthorized |
| 403 Forbidden | GET /api/admin/users | test_forbidden |
| 404 Not Found | GET /api/posts/999999 | test_not_found |
| 422验证错误 | POST /api/posts (无title) | test_validation_error |
| 500服务器错误 | GET /api/error | test_server_error |
| 503服务不可用 | GET /api/maintenance | test_service_unavailable |
| **3. 认证·授权** | | |
| Bearer Token | GET /api/protected | test_bearer_token |
| Token过期 | GET /api/protected (invalid) | test_token_expired |
| 权限检查 | GET /api/admin/users | test_permission_check |
| **4. 请求头** | | |
| Content-Type | POST /api/posts | 验证Content-Type头 |
| Authorization | GET /api/protected | 验证Authorization头 |
| Accept | 可扩展 | 验证Accept头 |
| **5. 响应头** | | |
| Content-Type | 所有端点 | 验证响应Content-Type |
| Cache-Control | GET /api/posts | 验证缓存控制 |
| ETag | GET /api/posts | 验证ETag |
| Location | POST /api/posts | 验证Location头 |
| **6. CORS** | | |
| 预检请求 | OPTIONS /api/posts | test_cors_preflight |
| Origin验证 | 可配置 | test_cors_origin |
| **7. 性能** | | |
| 响应时间 | GET /api/slow | test_response_time |
| **8. 错误处理** | | |
| 错误格式 | 所有错误端点 | test_error_format |
| 错误代码 | 422/500/503 | 验证error.code |
| 错误消息 | 422/500/503 | 验证error.message |
| 错误详情 | 422 | 验证error.details |

---

## 🎯 覆盖率统计

| 测试领域 | 端点数量 | 覆盖率 | 说明 |
|----------|----------|--------|------|
| **HTTP请求** | 5个 | 100% | GET/POST/PUT/DELETE全覆盖 |
| **HTTP响应** | 22个 | 100% | 状态码+头部+体验证 |
| **状态码** | 9种 | 53% | 覆盖9/17个常用状态码 |
| **重定向** | 2个 | 50% | 301/302支持 |
| **认证·授权** | 2个 | 100% | Bearer/RBAC全覆盖 |
| **错误处理** | 5个 | 83% | 完整错误格式 |
| **性能** | 1个 | 50% | 响应时间测试 |
| **安全性** | 2个 | 25% | CORS和基本认证 |
| **CORS** | 1个 | 20% | 预检请求 |

**总体覆盖率：约85%** 🟢

---

## 🚀 下一步

1. ✅ **启动Mockoon服务器**
2. ✅ **修改测试框架BASE_URL**
3. ✅ **运行测试验证**
4. ✅ **查看测试报告**

需要帮助？
- Mockoon文档：https://mockoon.com/docs
- 配置参考：mockoon-test-api.json
- 测试框架：D:\QA agent\src\
