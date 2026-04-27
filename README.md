# QA Agent - Swagger 测试流水线

## 📖 项目简介

QA Agent 是一个模块化的自动化测试框架，能够根据 Swagger 文档自动生成、执行 API 测试，并生成测试报告。

**✨ 最新特性：BASE_URL 自动从 Swagger 文档提取！** 详见：[BASE_URL配置指南.md](BASE_URL配置指南.md)

## 📚 文档导航

### 快速开始
- **[快速测试指南](快速测试指南.md)** - 5分钟快速上手
- **[使用指南](使用指南.md)** - 完整的使用教程
- **[BASE_URL配置指南](BASE_URL配置指南.md)** - API地址配置说明
- **[快速参考](快速参考.md)** - 命令速查表

### 测试资源
- **[公开测试API.md](公开测试API.md)** - 免费测试API网站
- **[测试资源索引](测试资源索引.md)** - 所有资源汇总
- **[swagger_jsonplaceholder.json](swagger_jsonplaceholder.json)** - JSONPlaceholder配置（可直接使用）

### 技术文档
- **[PIPELINE_IMPLEMENTATION.md](PIPELINE_IMPLEMENTATION.md)** - 系统架构
- **[FILENAME_OPTIMIZATION.md](FILENAME_OPTIMIZATION.md)** - 文件命名规则
- **[REPORT_OPTIMIZATION.md](REPORT_OPTIMIZATION.md)** - 报告功能说明
- **[RUN_TESTS_IMPLEMENTATION.md](RUN_TESTS_IMPLEMENTATION.md)** - 测试执行说明

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pytest requests
```

### 2. 运行测试流水线

```bash
# 使用公开API测试（推荐）
python src/pipeline.py swagger_jsonplaceholder.json
```

### 3. 查看测试报告

```bash
cat reports/api_test_report_*.txt
```

## 🎯 配置自己的API

在 swagger.json 中添加 `servers` 字段：

```json
{
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "https://your-api.com",
      "description": "你的API地址"
    }
  ],
  "paths": { ... }
}
```

然后运行：
```bash
python src/pipeline.py swagger.json
```

**📖 详细使用方法请查看: [使用指南.md](使用指南.md)**

## 📁 项目结构

```
QA agent/
├── src/                    # 源代码
│   ├── swagger_parser.py   # Swagger 解析模块
│   ├── api_test.py         # API 测试生成模块
│   ├── test_runner.py      # 测试执行模块
│   ├── report.py           # 报告生成模块
│   └── pipeline.py         # 主控流水线（入口）
├── tests/                  # 生成的测试文件目录
├── reports/                # 生成的测试报告目录
└── swagger.json            # 示例 Swagger 文档
```

## 🔧 模块说明

### 1. swagger_parser
解析 Swagger/OpenAPI 文档，提取 API 信息

### 2. api_test
根据 API 信息生成 pytest 测试代码

### 3. test_runner
执行 pytest 测试并收集结果

### 4. report
生成测试报告（文本格式）

### 5. pipeline
主控模块，串联整个测试流程

## 📊 输出示例

运行完成后会生成：
- 测试文件：`tests/test_xxx.py`
- 测试报告：`reports/api_test_report_YYYYMMDD_HHMMSS.txt`

## 🛠️ 开发原则

- 每个模块独立实现
- 模块之间通过标准数据格式通信
- 主控只负责路由，不做复杂业务逻辑
- 支持逐步执行，不强制流水线

## 📝 后续计划

- 集成真实 LLM API 生成更智能的测试
- 支持 HTML 格式报告
- 增加更多测试场景覆盖
