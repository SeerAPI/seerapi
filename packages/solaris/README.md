<div align="center">

# Solaris
~~[序外执行者（不吃香菜版）](https://www.bilibili.com/video/BV17g411b75m)~~</br>
赛尔号客户端数据解析/整理工具

[![Python](https://img.shields.io/badge/python->=3.10-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](./pyproject.toml)

</div>

## 简介

Solaris 是 SeerAPI 的核心部分，用于解析和整理赛尔号三平台（Flash、HTML5、Unity）客户端数据。通过标准化的数据处理流程，将原始客户端数据转换为 [seerapi-models](https://github.com/SeerAPI/seerapi-models) 定义的标准结构，并输出为 JSON 文件、数据库记录和相关资源文件。

## 功能特性

- 🎮 **多平台支持**: 支持 Flash、HTML5、Unity 三个平台的数据解析
- 📊 **数据标准化**: 将客户端原始数据转换为标准化格式
- 🗃️ **多格式输出**: 支持带 Schema 的 JSON 表格、SQLite 数据库输出
- 🔧 **模块化架构**: 基于插件式的解析器和分析器架构，易于扩展
- ⚡ **命令行接口**: 提供简洁易用的 CLI 工具

## 安装

确保你的 Python 版本 >= 3.10，然后安装 Solaris，这里使用 [uv](https://docs.astral.sh/uv/getting-started/installation/) 进行安装：

```bash
# 从源码安装
git clone https://github.com/SeerAPI/solaris.git
cd solaris
uv sync
```

## 使用方法

Solaris 提供了两个主要命令：`parse` 和 `analyze`。

### 基本用法

```bash
# 激活虚拟环境 (Linux/MacOS)
source .venv/bin/activate

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 查看帮助
solaris --help

# 查看版本
solaris --version
```

### 数据解析 (parse)

将Unity客户端二进制数据文件解析为中间格式：

```bash
# 基本解析
solaris parse --source-dir /path/to/client/data --output-dir /path/to/output

# 查看可用的解析器
solaris parse --list-parsers

# 使用自定义解析器包
solaris parse --package-name my.custom.parsers
```

### 数据分析 (analyze)

将解析后的数据进行分析并输出为最终格式：

```bash
# 输出为 JSON 格式（默认）
solaris analyze --source-dir ./source --json-output-dir ./data --schema-output-dir ./schema

# 输出为数据库格式
solaris analyze --output-mode db --db-url solaris.db

# 同时输出 JSON 和数据库
solaris analyze --output-mode all

# 指定 API 信息
solaris analyze --api-url https://api.example.com --api-version v1beta

# 查看可用的分析器
solaris analyze --list-analyzers
```

## 命令参数详解

### parse 命令

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--source-dir` | `source` | 客户端数据源目录 |
| `--output-dir` | `output` | 解析结果输出目录 |
| `--package-name` | `solaris.parse.parsers` | 解析器包名（可多个） |
| `-l, --list-parsers` | - | 显示所有可用解析器 |

### analyze 命令

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-w, --source-dir` | 环境变量或 `./source` | 数据源目录 |
| `-m, --output-mode` | `json` | 输出模式：json/db/all |
| `--json-output-dir` | `data` | JSON 文件输出目录 |
| `--schema-output-dir` | `schema` | JSON Schema 输出目录 |
| `-d, --db-url` | `solaris.db` | 数据库文件路径 |
| `--api-url` | 环境变量 | API 基础 URL |
| `--api-version` | 环境变量 | API 版本号 |
| `--package-name` | `solaris.analyze.analyzers` | 分析器包名（可多个） |
| `-l, --list-analyzers` | - | 显示所有可用分析器 |

## 环境变量

Solaris 支持通过环境变量进行配置：

```bash
# 数据源基础目录
export SOLARIS_DATA_BASE_DIR="/path/to/data"

# API 配置
export SOLARIS_API_URL="https://api.example.com"
export SOLARIS_API_VERSION="v1beta"

# 下列环境变量无法通过命令行指定

# 在仅设置SOLARIS_DATA_BASE_DIR的情况下，各分类数据源目录为  SOLARIS_DATA_BASE_DIR/[patch|html5|unity|flash]
# 设置下列变量以指定单个分类的目录
export SOLARIS_DATA_PATCH_DIR="/path/to/patch"
export SOLARIS_DATA_HTML5_DIR="/path/to/html5"
export SOLARIS_DATA_UNITY_DIR="/path/to/unity"
export SOLARIS_DATA_FLASH_DIR="/path/to/flash"

# 在输出中添加源信息
export SOLARIS_API_DATA_SOURCE="https://github.com/example/data.git"
export SOLARIS_API_DATA_VERSION="v1beta"
export SOLARIS_API_PATCH_SOURCE="https://example.com/patch"
export SOLARIS_API_PATCH_VERSION="v1beta"
```

## 项目结构

```
solaris/
├── analyze/          # 数据分析模块
├── cli/             # 命令行接口
│   ├── analyze.py   # analyze 命令实现
│   └── parse.py     # parse 命令实现
├── parse/           # 数据解析模块
├── settings.py      # 配置管理
├── typing.py        # 类型定义
└── utils.py         # 工具函数
```

## 输出格式

### JSON 输出
- **数据文件**: 结构化的 JSON 表格，包含解析后的游戏数据
- **Schema 文件**: 对应的 JSON Schema 定义，用于数据验证
- **元数据**: API 版本、URL 等元信息

### 数据库输出
- **SQLite 数据库**: 包含所有解析数据的单一数据库文件

## 开发

### 环境要求

- Python >= 3.10
- 依赖管理：使用 `uv` 或 `pip`

### 代码风格

项目使用 Ruff 进行代码格式化和检查：

```bash
# 安装开发依赖
uv sync --dev

# 代码检查
uv run ruff check .

# 代码格式化
uv run ruff format .
```

### 扩展开发

#### 添加新的解析器

1. 在 `solaris/parse/parsers/` 下创建新模块
2. 继承 `BaseParser` 类
3. 实现 `parse()` 方法

#### 添加新的分析器

1. 在 `solaris/analyze/analyzers/` 下创建新模块
2. 继承 `BaseAnalyzer` 类
3. 实现数据分析逻辑

## 贡献

目前该项目的parser只有寥寥几个，欢迎提交更多的parser！

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
