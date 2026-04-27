# Mockoon桌面应用导入配置指南

**安装状态：** ✅ 已安装  
**配置文件：** mockoon-test-api.json  
**服务器端口：** 3000

---

## 📋 导入配置步骤

### 步骤1：启动Mockoon应用

1. **打开Mockoon桌面应用**
   - Windows: 从开始菜单搜索 "Mockoon"
   - 或双击桌面图标

### 步骤2：导入配置文件

#### 方式1：拖拽导入（最简单）

```
1. 打开文件资源管理器
2. 找到文件: D:\QA agent\API_auto_test\mockoon-test-api.json
3. 直接拖拽到Mockoon窗口中
```

#### 方式2：菜单导入

```
1. 点击左上角 "File" 菜单
2. 选择 "Import API"
3. 浏览到文件: D:\QA agent\API_auto_test\
4. 选择 "mockoon-test-api.json"
5. 点击 "打开"
```

### 步骤3：查看导入的API

导入成功后，你应该看到：

```
左侧面板: "HTTP测试API服务器"
├── GET /api/posts
├── GET /api/posts/:id
├── POST /api/posts
├── PUT /api/posts/:id
├── DELETE /api/posts/:id
├── GET /api/protected
├── GET /api/admin/users
├── GET /api/old-url
├── GET /api/temp-redirect
├── GET /api/error
├── GET /api/maintenance
├── GET /api/slow
├── OPTIONS /api/posts
└── GET /api/users
```

### 步骤4：启动服务器

1. **找到启动按钮**
   - 在界面顶部，有一个大的播放按钮 ▶️
   - 或者右上角的 "Start Server" 按钮

2. **点击启动**
   - 按钮会变成红色方形停止按钮 ⏹️
   - 底部状态栏显示 "Running"
   - 端口显示: **localhost:3000**

3. **确认运行**
   - 你应该看到类似这样的提示：
   ```
   ✓ Server listening on http://localhost:3000
   ```

---

## ✅ 验证配置

### 快速验证（浏览器）

打开浏览器，访问以下URL：

```bash
# 1. 基础测试（应该返回JSON数组）
http://localhost:3000/api/posts

# 2. 404测试（应该返回404错误）
http://localhost:3000/api/posts/999999

# 3. 认证测试（应该返回401错误）
http://localhost:3000/api/protected

# 4. 慢速API（应该有200ms延迟）
http://localhost:3000/api/slow
```

### 使用curl验证

打开命令提示符或PowerShell：

```bash
# 测试基础GET请求
curl http://localhost:3000/api/posts

# 应该返回:
[
  {"id": 1, "title": "Test Post 1", "body": "Body 1", "userId": 1},
  {"id": 2, "title": "Test Post 2", "body": "Body 2", "userId": 1}
]

# 测试认证（401）
curl http://localhost:3000/api/protected

# 应该返回:
{"error":{"code":"UNAUTHORIZED","message":"缺少认证token"}}

# 测试认证成功（200）
curl http://localhost:3000/api/protected ^
  -H "Authorization: Bearer valid-token"

# 应该返回:
{"message":"Protected resource accessed","user":{"id":1,"name":"Test User","email":"user@example.com"}}
```

### 运行验证脚本

```bash
cd "D:\QA agent\API_auto_test"
verify-mockoon.bat
```

**预期输出：**
```
========================================
 Mockoon配置验证
========================================

[1/10] 检查服务器状态...
        ✓ 服务器运行中

[1] 测试GET /api/posts (200 OK)
[✓] 测试通过: GET /api/posts 返回200
[2] 测试GET /api/posts/999999 (404 Not Found)
[✓] 测试通过: GET /api/posts/999999 返回404
...

========================================
 验证结果
========================================

通过: 10/10

[✓] 所有测试通过！Mockoon配置正常
```

---

## 🎯 查看API详情

### 查看单个端点配置

1. **点击左侧的端点**（例如：GET /api/posts）
2. **右侧面板会显示：**
   - **Endpoint:** `/api/posts`
   - **Method:** GET
   - **Responses:** 响应列表

3. **点击响应**（例如：200 OK）
   - 可以看到完整的响应配置
   - **Status Code:** 200
   - **Headers:** Content-Type, Cache-Control, ETag
   - **Body:** JSON响应体

### 测试端点

在Mockoon界面中：

1. **选择端点**（例如：GET /api/posts）
2. **点击 "Send" 按钮**（右上角）
3. **查看响应**
   - 状态码
   - 响应头
   - 响应体

---

## 🔧 常见问题

### 问题1：端口3000被占用

**症状：**
```
Error: Port 3000 is already in use
```

**解决方案：**

#### 方式1：更换端口

1. 在Mockoon界面顶部，找到端口输入框（显示3000）
2. 修改为其他端口（例如：3001）
3. 重新启动服务器
4. 更新测试脚本中的端口号

#### 方式2：停止占用端口的程序

```bash
# 查找占用端口3000的进程
netstat -ano | findstr :3000

# 停止进程
taskkill /F /PID <PID号>
```

### 问题2：导入失败

**症状：**
```
Error: Invalid JSON format
```

**解决方案：**

1. 确认文件完整：`mockoon-test-api.json`
2. 用文本编辑器打开，确认是有效JSON
3. 尝试重新下载配置文件

### 问题3：服务器无法启动

**症状：**
点击启动按钮后无反应

**解决方案：**

1. **检查端口是否被占用**
2. **重启Mockoon应用**
3. **查看日志：**
   - 点击 "View" → "Logs"
   - 查看错误信息

---

## 🚀 启动后的下一步

### 选项1：运行自动化测试

```bash
# 确保Mockoon正在运行
# 然后在新的命令行窗口中运行：

cd "D:\QA agent"
python src/pipeline.py swagger_jsonplaceholder.json
```

### 选项2：手动测试API

```bash
# 测试基础CRUD
curl http://localhost:3000/api/posts
curl -X POST http://localhost:3000/api/posts ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Test\",\"body\":\"Content\"}"

# 测试认证
curl http://localhost:3000/api/protected
curl http://localhost:3000/api/protected ^
  -H "Authorization: Bearer valid-token"

# 测试权限
curl http://localhost:3000/api/admin/users ^
  -H "Authorization: Bearer admin-token"

# 测试错误状态码
curl http://localhost:3000/api/posts/999999
curl http://localhost:3000/api/error
curl http://localhost:3000/api/maintenance
```

### 选项3：查看详细文档

打开文件：`Mockoon配置使用指南.md`

---

## 📊 配置验证清单

导入配置后，确认以下内容：

- [ ] ✅ 成功导入 `mockoon-test-api.json`
- [ ] ✅ 左侧显示 "HTTP测试API服务器"
- [ ] ✅ 可以看到22个API端点
- [ ] ✅ 点击 "Start Server" 成功启动
- [ ] ✅ 状态栏显示 "Running"
- [ ] ✅ 端口显示 "localhost:3000"
- [ ] ✅ 浏览器访问 http://localhost:3000/api/posts 成功
- [ ] ✅ 运行 `verify-mockoon.bat` 全部通过

---

## 🎯 成功标志

当一切正常时，你应该看到：

### Mockoon界面
```
┌─────────────────────────────────────┐
│ ▶️ HTTP测试API服务器                │
│ Port: 3000                          │
│ Status: 🟢 Running                  │
│                                     │
│ Endpoints:                          │
│  GET    /api/posts                  │
│  GET    /api/posts/:id              │
│  POST   /api/posts                  │
│  PUT    /api/posts/:id              │
│  DELETE /api/posts/:id              │
│  ... (共22个端点)                   │
└─────────────────────────────────────┘
```

### 命令行验证
```bash
$ curl http://localhost:3000/api/posts
[
  {"id":1,"title":"Test Post 1"...},
  {"id":2,"title":"Test Post 2"...}
]
```

---

## 📝 配置文件信息

**文件名：** mockoon-test-api.json  
**大小：** 约30KB  
**端点数量：** 22个  
**测试场景：** 85%覆盖率

### 主要端点列表

| 端点 | 功能 | 状态码 |
|------|------|--------|
| GET /api/posts | 获取文章列表 | 200 |
| GET /api/posts/:id | 获取文章详情 | 200/404 |
| POST /api/posts | 创建文章 | 201/422 |
| PUT /api/posts/:id | 更新文章 | 200/404 |
| DELETE /api/posts/:id | 删除文章 | 204/404 |
| GET /api/protected | 需要认证 | 401/200 |
| GET /api/admin/users | 需要管理员权限 | 401/403/200 |
| GET /api/old-url | 301重定向 | 301 |
| GET /api/temp-redirect | 302重定向 | 302 |
| GET /api/error | 服务器错误 | 500 |
| GET /api/maintenance | 服务不可用 | 503 |
| GET /api/slow | 慢速API | 200 (200ms延迟) |

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看Mockoon日志：**
   - View → Logs

2. **重新导入配置：**
   - File → Close API
   - File → Import → 选择配置文件

3. **参考官方文档：**
   - https://mockoon.com/docs

4. **检查配置文件：**
   - 用文本编辑器打开 `mockoon-test-api.json`
   - 确认格式正确

---

## ✅ 完成确认

当您成功导入并启动服务器后，请告诉我：

- [ ] ✅ 配置导入成功
- [ ] ✅ 服务器正在运行
- [ ] ✅ 可以访问 http://localhost:3000/api/posts
- [ ] ✅ 验证脚本全部通过

然后我们可以进行下一步：
- 运行完整的测试套件
- 修改测试框架的BASE_URL
- 查看测试报告

---

**更新日期：** 2026-04-26  
**版本：** v1.0
