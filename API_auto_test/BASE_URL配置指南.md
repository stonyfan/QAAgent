# BASE_URL 配置说明

## 📋 改进说明

BASE_URL 现在从 Swagger 文档的 `servers` 字段中自动提取，而不是硬编码在测试代码中。

---

## 🎯 优势

| 改进前 | 改进后 |
|--------|--------|
| ❌ 硬编码在测试代码中 | ✅ 在 swagger.json 中统一配置 |
| ❌ 修改需要编辑多个文件 | ✅ 只需修改 swagger.json |
| ❌ 容易出错和混乱 | ✅ 集中管理，清晰明确 |

---

## 🔧 配置方法

### OpenAPI 3.0 格式（推荐）

在 swagger.json 中添加 `servers` 字段：

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "我的API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://api.example.com",
      "description": "生产服务器"
    }
  ],
  "paths": {
    ...
  }
}
```

### Swagger 2.0 格式

使用 `schemes`, `host`, `basePath` 字段：

```json
{
  "swagger": "2.0",
  "info": {
    "title": "我的API",
    "version": "1.0.0"
  },
  "schemes": ["https"],
  "host": "api.example.com",
  "basePath": "/v1",
  "paths": {
    ...
  }
}
```

---

## 📊 提取优先级

系统按以下优先级提取 BASE_URL：

1. **OpenAPI 3.0 的 servers[0].url** （优先级最高）
2. **Swagger 2.0 的 schemes + host + basePath**
3. **默认值**: `http://localhost:8000`

---

## 💡 配置示例

### 示例 1: 本地开发服务器

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "http://localhost:8000",
      "description": "本地开发"
    }
  ]
}
```

**生成的测试代码：**
```python
BASE_URL = "http://localhost:8000"
```

---

### 示例 2: 生产服务器

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "https://api.example.com",
      "description": "生产环境"
    }
  ]
}
```

**生成的测试代码：**
```python
BASE_URL = "https://api.example.com"
```

---

### 示例 3: JSONPlaceholder（已配置）

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "https://jsonplaceholder.typicode.com",
      "description": "生产服务器"
    }
  ]
}
```

**生成的测试代码：**
```python
BASE_URL = "https://jsonplaceholder.typicode.com"
```

---

### 示例 4: 带路径的API

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "https://api.example.com/v2",
      "description": "API v2"
    }
  ]
}
```

**生成的测试代码：**
```python
BASE_URL = "https://api.example.com/v2"
```

---

### 示例 5: 多环境配置

虽然系统只使用第一个服务器，但你可以定义多个：

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "http://localhost:8000",
      "description": "本地开发"
    },
    {
      "url": "https://staging-api.example.com",
      "description": "测试环境"
    },
    {
      "url": "https://api.example.com",
      "description": "生产环境"
    }
  ]
}
```

**系统会自动使用第一个（本地开发）**

要切换环境，只需调整顺序：
```json
{
  "servers": [
    {
      "url": "https://api.example.com",  // 移到第一位
      "description": "生产环境"
    },
    {
      "url": "http://localhost:8000",
      "description": "本地开发"
    }
  ]
}
```

---

## 🔄 迁移指南

### 如果你有旧的测试文件

**旧方式（已弃用）：**
```python
# 手动编辑每个测试文件
BASE_URL = "https://my-api.com"  # ❌ 容易混乱
```

**新方式（推荐）：**
```json
// 在 swagger.json 中配置一次
{
  "servers": [
    {
      "url": "https://my-api.com"  // ✅ 集中管理
    }
  ]
}
```

**重新生成测试：**
```bash
python src/pipeline.py swagger.json
```

---

## 🎯 实际效果

### 配置前
生成的测试代码：
```python
BASE_URL = "https://jsonplaceholder.typicode.com"  # 硬编码
```

### 配置后
生成的测试代码：
```python
# BASE_URL 从 Swagger 文档的 servers 字段自动提取
BASE_URL = "https://jsonplaceholder.typicode.com"  # 从配置读取
```

**区别：**
- 配置前：需要修改源代码或每个测试文件
- 配置后：只需修改 swagger.json 的 servers 字段

---

## 🔍 验证配置

运行测试时会显示提取的 BASE_URL：

```bash
$ python src/pipeline.py swagger_jsonplaceholder.json

============================================================
QA Agent - Swagger 测试流水线
============================================================

[步骤 1/4] 解析 Swagger 文档: swagger_jsonplaceholder.json
✓ 成功解析 11 个 API
✓ BASE_URL: https://jsonplaceholder.typicode.com
  - GET /posts: 获取所有文章
  - POST /posts: 创建新文章
  ...
```

---

## ❓ 常见问题

### Q: 如何修改BASE_URL？

**A:** 编辑 swagger.json 的 servers 字段：
```json
{
  "servers": [
    {
      "url": "你的新URL"
    }
  ]
}
```

然后重新生成测试：
```bash
python src/pipeline.py swagger.json
```

---

### Q: 支持环境变量吗？

**A:** 目前不支持。建议使用不同的 swagger.json 文件：
- `swagger-dev.json` - 开发环境
- `swagger-prod.json` - 生产环境
- `swagger-test.json` - 测试环境

---

### Q: 如果swagger.json没有servers字段会怎样？

**A:** 系统会使用默认值 `http://localhost:8000`。

---

### Q: 可以为不同环境配置不同的BASE_URL吗？

**A:** 可以！创建多个配置文件：
```bash
# 开发环境
python src/pipeline.py swagger-dev.json

# 生产环境
python src/pipeline.py swagger-prod.json

# 测试环境
python src/pipeline.py swagger-test.json
```

---

## 📚 相关文档

- **[使用指南.md](使用指南.md)** - 完整使用教程
- **[快速测试指南.md](快速测试指南.md)** - 5分钟快速上手
- **[公开测试API.md](公开测试API.md)** - 免费测试API列表

---

## 🎉 总结

现在BASE_URL的配置更加：
- ✅ **集中管理** - 在 swagger.json 中统一配置
- ✅ **清晰明确** - 一看就知道测试哪个环境
- ✅ **易于修改** - 只需修改一个字段
- ✅ **标准化** - 遵循OpenAPI/Swagger规范

**不再需要在测试代码中硬编码URL！** 🚀
