# QA Agent 全链路开发说明（Swagger → API测试 → 报告）

---

## 🎯 目标

构建一个完整的 QA 自动化链路，实现：

Swagger 文档 → 自动生成 API 测试 → 自动执行 → 自动生成测试报告

---

## 🧭 总体流程（核心链路）

```text
Swagger JSON
   ↓
解析（swagger_parser）
   ↓
API描述（list[str]）
   ↓
生成测试代码（api_test）
   ↓
执行 pytest（test_runner）
   ↓
收集结果
   ↓
生成测试报告（report）
```

---

## 🧠 核心原则（必须遵守）

1. 模块独立（不可耦合）
2. 每个模块单一职责
3. 主控只做调度
4. 不做全自动流水线（支持逐步执行）
5. 每一步必须可测试

---

## 🏗️ 项目结构（推荐）

```bash
qa_agent/
├── agent.py
├── tools/
│   ├── swagger_parser.py
│   ├── api_test.py
│   ├── test_runner.py
│   ├── report.py
│   └── file_manager.py
├── prompts/
│   ├── api_test.txt
│   └── report.txt
├── tests/
│   └── (自动生成测试文件)
├── swagger.json
├── agent.md
├── USAGE.md
├── PIPELINE.md
```

---

## 🧩 模块职责说明

### 1️⃣ swagger_parser.py

功能：

* 读取 Swagger JSON
* 提取 API 信息
* 转换为标准化描述

核心函数：

```python
load_swagger(path) -> dict
extract_apis(swagger) -> list
format_api_description(api) -> str
generate_all_descriptions(swagger) -> list[str]
```

---

### 2️⃣ api_test.py

功能：

* 调用 LLM（Prompt）
* 生成 pytest 测试代码
* 保存到 tests/ 目录

核心函数：

```python
generate_api_test(api_desc: str, filename: str)
```

---

### 3️⃣ test_runner.py

功能：

* 执行 pytest
* 返回执行结果

核心函数：

```python
run_tests() -> str
```

---

### 4️⃣ report.py

功能：

* 根据 pytest 输出生成测试报告

核心函数：

```python
generate_report(test_output: str) -> str
```

---

## 🔗 全链路核心函数（主控）

```python
def run_swagger_pipeline(swagger_path: str):
    # 1. 加载 Swagger
    swagger = load_swagger(swagger_path)

    # 2. 提取 API 描述
    apis = generate_all_descriptions(swagger)

    # 3. 生成测试代码
    for i, api_desc in enumerate(apis):
        filename = f"test_api_{i}.py"
        generate_api_test(api_desc, filename)

    # 4. 执行测试
    result = run_tests()

    # 5. 生成报告
    report = generate_report(result)

    return report
```

---

## 🧪 开发步骤（Claude执行流程）

---

### 🟢 Step 1：设计全链路

```text
请基于以下项目背景执行任务：

（粘贴 agent.md）

当前任务：
设计 Swagger → API测试 → 报告 的全链路流程

要求：
- 使用已有模块
- 模块解耦
- 明确输入输出

不要写代码
```

---

### 🟡 Step 2：实现 pipeline

```text
当前任务：
实现 run_swagger_pipeline(swagger_path)

要求：
- 串联 swagger_parser / api_test / test_runner / report
- 可运行
```

---

### 🟠 Step 3：优化测试文件生成

```text
当前任务：
优化测试文件命名

要求：
- 每个API一个文件
- 文件名语义清晰（test_login.py）
```

---

### 🔵 Step 4：实现测试执行

```text
当前任务：
实现 run_tests()

要求：
- 使用 subprocess 调用 pytest
- 返回完整输出
```

---

### 🟣 Step 5：报告优化

```text
当前任务：
优化测试报告

要求：
- 统计通过/失败数量
- 输出失败详情
- 提供风险提示
```

---

## 🚀 使用方式（最终效果）

输入：

```text
解析这个 swagger 并生成测试
```

系统执行：

1. 自动解析所有 API
2. 生成多个 pytest 文件
3. 执行测试
4. 输出测试报告

---

## 📈 实际价值（非常重要）

---

### 🟢 对个人

* 新项目接入速度 ↑↑
* QA体系搭建效率 ↑↑
* 重复劳动 ↓↓↓

---

### 🟡 对自由职业（freelance）

工作方式变为：

```text
获取 Swagger → 自动生成测试 → 人工优化
```

---

👉 你从“写测试的人”升级为：

**测试体系构建者**

---

## ⚠️ 常见问题

---

### ❗1. API需要认证

解决：

* 支持 headers
* 增加 token 管理

---

### ❗2. Swagger不完整

解决：

* fallback 到自然语言输入

---

### ❗3. 测试不稳定

解决：

* 优化 api_test.txt Prompt

---

## 🔥 后续升级路线

---

### 🥇 必做

* 支持 base_url
* 支持 headers
* token 管理

---

### 🥈 推荐

* 按模块拆分测试目录

```bash
tests/login/test_login.py
```

---

### 🥉 进阶

* Swagger URL自动拉取
* 自动生成测试数据
* 覆盖率分析

---

## 🎯 总结

这个系统的本质不是：

❌ 写测试代码

而是：

✅ **从 API 文档自动构建测试体系**

---

## 🧠 最重要的一句话

你不是在做一个工具，而是在构建：

👉 **QA 自动化生产力系统**

---
