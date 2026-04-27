# 开源Mock API服务器推荐

**更新日期：** 2026-04-26  
**用途：** 本地API测试环境

---

## 🏆 Top推荐（按场景分类）

### 🥇 第1名：Mockoon（最易用）

**⭐ 强烈推荐！**

| 项目 | 信息 |
|------|------|
| **项目地址** | https://github.com/mockoon/mockoon |
| **官网** | https://mockoon.com |
| **类型** | 桌面应用 + CLI + Docker |
| **语言** | Electron + Node.js |
| **许可证** | MIT |
| **Stars** | 6.5k+ |

#### ✅ 核心功能

- ✅ **可视化界面** - 拖拽式API配置
- ✅ **支持所有HTTP方法** - GET/POST/PUT/PATCH/DELETE
- ✅ **完整的状态码** - 200/201/204/400/401/403/404/422/500等
- ✅ **认证支持** - Bearer Token、API Key、Basic Auth
- ✅ **CORS配置** - 可视化配置CORS
- ✅ **随机数据生成** - 支持Faker.js
- ✅ **响应延迟** - 模拟慢速API
- ✅ **Docker支持** - 一键部署
- ✅ **导入OpenAPI/Swagger** - 直接导入API文档

#### 🚀 快速启动

**方式1：桌面应用（最简单）**

```bash
# 下载安装
# Windows: https://mockoon.com/download/windows
# 或使用 Chocolatey
choco install mockoon

# 启动后：
# 1. 点击 "New API"
# 2. 添加端点：GET /api/posts
# 3. 配置响应：状态码、JSON body
# 4. 点击 "Start Server"（默认端口: 3000）
```

**方式2：Docker（推荐）**

```bash
# 拉取镜像
docker pull mockoon/mockoon:latest

# 启动服务器
docker run -d \
  -p 3000:3000 \
  -v $(pwd)/mockoon-data:/mockoon/data \
  mockoon/mockoon:latest \
  --data /mockoon/data

# 访问
curl http://localhost:3000/posts
```

**方式3：CLI**

```bash
# 安装CLI
npm install -g @mockoon/cli

# 启动服务器
mockoon-cli start --data mockoon-data.json --port 3000
```

#### 📝 配置示例

```json
{
  "uuid": "mock-api",
  "name": "Test API Server",
  "port": 3000,
  "endpoints": [
    {
      "method": "get",
      "path": "/api/posts",
      "responses": [
        {
          "statusCode": 200,
          "body": "[{\"id\": 1, \"title\": \"Test Post\"}]",
          "headers": [
            {
              "key": "Content-Type",
              "value": "application/json"
            }
          ]
        }
      ]
    },
    {
      "method": "post",
      "path": "/api/posts",
      "responses": [
        {
          "statusCode": 201,
          "body": "{\"id\": 101, \"title\": \"{{title}}\"}",
          "rules": [
            {
              "target": "body",
              "modifier": "title",
              "operator": "exists"
            }
          ],
          "fallbackResponse": {
            "statusCode": 422,
            "body": "{\"error\": {\"code\": \"VALIDATION_ERROR\", \"message\": \"Title required\"}}"
          }
        }
      ]
    },
    {
      "method": "get",
      "path": "/api/protected",
      "responses": [
        {
          "statusCode": 401,
          "body": "{\"error\": \"Unauthorized\"}",
          "rules": [
            {
              "target": "header",
              "modifier": "authorization",
              "operator": "not_exists"
            }
          ]
        }
      ]
    }
  ]
}
```

#### 🎯 覆盖的测试场景

| 测试场景 | 覆盖情况 | 说明 |
|----------|----------|------|
| **HTTP方法** | ✅ 100% | GET/POST/PUT/PATCH/DELETE |
| **状态码** | ✅ 100% | 所有标准状态码 |
| **认证** | ✅ 90% | Bearer/API Key/Basic |
| **CORS** | ✅ 100% | 完整CORS配置 |
| **请求头** | ✅ 95% | 可验证任意请求头 |
| **响应头** | ✅ 100% | 可自定义任意响应头 |
| **重定向** | ✅ 100% | 301/302/307/308 |
| **响应延迟** | ✅ 100% | 可配置延迟时间 |
| **随机数据** | ✅ 100% | 支持Faker.js |

**覆盖率预估：85-90%** 🟢

---

### 🥈 第2名：JSON Server（最轻量）

**⭐ 简单好用，适合快速测试**

| 项目 | 信息 |
|------|------|
| **项目地址** | https://github.com/typicode/json-server |
| **官网** | https://jsonplaceholder.typicode.com（同作者） |
| **类型** | Node.js CLI |
| **语言** | Node.js |
| **许可证** | MIT |
| **Stars** | 70k+ |

#### ✅ 核心功能

- ✅ **零配置启动** - 一条命令启动
- ✅ **完整CRUD** - 自动生成CRUD端点
- ✅ **RESTful** - 标准REST API
- ✅ **支持关系** - 一对多、多对多
- ✅ **查询参数** - ?_limit=10, ?_page=1
- ✅ **中间件支持** - 可添加认证、日志等
- ✅ **自定义路由** - 可添加自定义端点

#### 🚀 快速启动

```bash
# 安装
npm install -g json-server

# 创建db.json
echo '{
  "posts": [
    { "id": 1, "title": "Test Post", "author": "User1" }
  ],
  "users": [
    { "id": 1, "name": "User1" }
  ]
}' > db.json

# 启动服务器
json-server --watch db.json --port 3000

# 访问
curl http://localhost:3000/posts
curl http://localhost:3000/posts/1
curl -X POST http://localhost:3000/posts -H "Content-Type: application/json" -d '{"title":"New Post"}'
```

#### ⚙️ 添加认证中间件

```javascript
// auth-middleware.js
module.exports = (req, res, next) => {
  if (req.path === '/protected') {
    const auth = req.headers.authorization;
    if (!auth || auth !== 'Bearer valid-token') {
      return res.status(401).json({ error: 'Unauthorized' });
    }
  }
  next();
};

// 启动时使用
json-server --watch db.json --port 3000 --middlewares auth-middleware.js
```

#### 🎯 覆盖的测试场景

| 测试场景 | 覆盖情况 | 说明 |
|----------|----------|------|
| **HTTP方法** | ✅ 100% | GET/POST/PUT/PATCH/DELETE |
| **状态码** | ⚠️ 40% | 需要手动配置中间件 |
| **认证** | ⚠️ 30% | 需要自定义中间件 |
| **CORS** | ⚠️ 20% | 需要自定义中间件 |
| **响应延迟** | ❌ 0% | 不支持 |

**覆盖率预估：40-50%** 🟡

---

### 🥉 第3名：Mock Server（可编程）

**⭐ 高度可定制，适合复杂场景**

| 项目 | 信息 |
|------|------|
| **项目地址** | https://github.com/mock-server/mockserver |
| **官网** | https://www.mock-server.com |
| **类型** | Java/Node.js/Docker |
| **语言** | Java + Node.js |
| **许可证** | Apache 2.0 |
| **Stars** | 4.5k+ |

#### ✅ 核心功能

- ✅ **完整的HTTP/S代理** - 可记录和回放请求
- ✅ **Expectations** - 强大的请求匹配规则
- ✅ **动态响应** - 支持JavaScript模板
- ✅ **WebSocket支持** - 可测试WebSocket
- ✅ **API接口** - 可编程控制
- ✅ **Docker支持** - 容器化部署

#### 🚀 快速启动

```bash
# Docker方式
docker run -d \
  -p 1080:1080 \
  mockserver/mockserver:latest

# 配置expectation
curl -X PUT http://localhost:1080/mockserver/expectation \
  -d '{
    "httpRequest": {
      "method": "GET",
      "path": "/api/posts"
    },
    "httpResponse": {
      "statusCode": 200,
      "body": "[{\"id\": 1, \"title\": \"Test\"}]"
    }
  }'

# 测试
curl http://localhost:1080/api/posts
```

#### 🎯 覆盖的测试场景

| 测试场景 | 覆盖情况 | 说明 |
|----------|----------|------|
| **HTTP方法** | ✅ 100% | 所有方法 |
| **状态码** | ✅ 100% | 所有状态码 |
| **认证** | ✅ 95% | 支持各种认证 |
| **WebSocket** | ✅ 100% | 支持WebSocket测试 |
| **代理** | ✅ 100% | 可录制真实API |

**覆盖率预估：80-85%** 🟢

---

### 🌟 第4名：WireMock（Java生态）

**⭐ Java项目首选**

| 项目 | 信息 |
|------|------|
| **项目地址** | https://github.com/wiremock/wiremock |
| **官网** | https://wiremock.org |
| **类型** | Java独立应用 |
| **语言** | Java |
| **许可证** | Apache 2.0 |
| **Stars** | 6k+ |

#### ✅ 核心功能

- ✅ **Standalone运行** - 独立jar包
- ✅ **录制回放** - 可录制真实API
- ✅ **优先级匹配** - 支持复杂匹配规则
- ✅ **故障注入** - 模拟延迟、错误
- ✅ **状态管理** - 有状态的API模拟

#### 🚀 快速启动

```bash
# 下载
wget https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/3.0.1/wiremock-standalone-3.0.1.jar

# 启动
java -jar wiremock-standalone-3.0.1.jar --port 3000

# 配置stub
curl -X POST http://localhost:3000/__admin/mappings \
  -d '{
    "request": {
      "method": "GET",
      "urlPathPattern": "/api/posts/.*"
    },
    "response": {
      "status": 200,
      "jsonBody": {"id": 1, "title": "Test"}
    }
  }'
```

**覆盖率预估：75-80%** 🟢

---

### 🎭 第5名：MSW（前端测试神器）

**⭐ 前端项目首选**

| 项目 | 信息 |
|------|------|
| **项目地址** | https://github.com/mswjs/msw |
| **官网** | https://mswjs.io |
| **类型** | NPM包 |
| **语言** | TypeScript |
| **许可证** | MIT |
| **Stars** | 15k+ |

#### ✅ 核心功能

- ✅ **Service Worker** - 拦截浏览器请求
- ✅ **Node.js支持** - 可用于服务端测试
- ✅ **REST + GraphQL** - 支持两种API类型
- ✅ **TypeScript** - 完整类型支持

#### 🚀 快速启动

```bash
# 安装
npm install msw --save-dev

# 初始化
npx msw init public/

// handlers.ts
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/posts', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([{ id: 1, title: 'Test' }])
    )
  }),
  rest.post('/api/posts', async (req, res, ctx) => {
    const data = await req.json()
    if (!data.title) {
      return res(
        ctx.status(422),
        ctx.json({ error: 'Title required' })
      )
    }
    return res(
      ctx.status(201),
      ctx.json({ id: 101, ...data })
    )
  })
]
```

**覆盖率预估：60-70%** 🟡（仅浏览器环境）

---

## 📊 对比总结

| 工具 | 易用性 | 功能完整性 | 覆盖率 | 推荐场景 |
|------|--------|-----------|--------|----------|
| **Mockoon** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 85-90% | 🔥 **最推荐** |
| **JSON Server** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 40-50% | 快速原型 |
| **Mock Server** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 80-85% | 复杂场景 |
| **WireMock** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 75-80% | Java项目 |
| **MSW** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 60-70% | 前端测试 |

---

## 🎯 针对你的需求的推荐

### 最佳方案：Mockoon

**原因：**
1. ✅ **可视化界面** - 不需要写代码
2. ✅ **完整功能** - 支持所有HTTP测试场景
3. ✅ **导入Swagger** - 可以直接导入你的OpenAPI文档
4. ✅ **Docker部署** - 可以集成到CI/CD
5. ✅ **免费开源** - MIT许可证

**实施步骤：**

```bash
# 步骤1：安装Mockoon
choco install mockoon

# 步骤2：启动应用
mockoon

# 步骤3：导入Swagger
# File -> Import -> Select swagger_jsonplaceholder.json

# 步骤4：配置认证端点
# 添加 GET /api/protected
# Rules: Authorization header must exist
# Response: 401 if missing

# 步骤5：导出配置
# File -> Export -> Export as JSON
# 保存为 mockoon-config.json

# 步骤6：使用CLI部署
npm install -g @mockoon/cli
mockoon-cli start --data mockoon-config.json --port 3000
```

### 备选方案：JSON Server + 自定义中间件

```bash
# 适合快速开始的轻量方案
npm install -g json-server

# 创建增强版配置
# 使用中间件添加认证、CORS等功能
```

---

## 🚀 立即开始

### 推荐路线：Mockoon

#### 今天（30分钟）

1. ✅ 下载安装Mockoon
2. ✅ 创建第一个API端点
3. ✅ 配置认证规则
4. ✅ 测试401/403状态码

#### 本周（2-3小时）

1. ✅ 导入你的Swagger文档
2. ✅ 配置完整的测试场景
3. ✅ 导出配置文件
4. ✅ 集成到测试框架

#### 配置修改

```python
# 修改BASE_URL指向本地Mockoon服务器
BASE_URL = "http://localhost:3000"

# 或使用环境变量
import os
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
```

---

## 📚 参考资源

- **Mockoon文档：** https://mockoon.com/docs
- **JSON Server文档：** https://github.comtypicode/json-server
- **Mock Server文档：** https://www.mock-server.com
- **WireMock文档：** https://wiremock.org/docs

---

**推荐总结：**  
**🔥 首选：Mockoon** - 功能最完整，易用性最好  
**🚀 快速：JSON Server** - 适合快速原型  
**💪 强大：Mock Server** - 适合复杂场景

需要我帮你配置Mockoon吗？我可以：
1. 创建Mockoon配置文件
2. 生成Docker启动脚本
3. 编写集成代码
