# SeerAPI Monorepo

SeerAPI 项目 monorepo — 赛尔号游戏数据开放 API 平台。

## 包结构

| 包 | 说明 | 技术栈 |
|---|---|---|
| `packages/seerapi-models` | 数据模型 / ORM 定义 | Python, uv |
| `packages/seerapi-python` | Python 异步 API 客户端 | Python, uv |
| `packages/solaris` | 客户端数据解析 / 整理工具 CLI | Python, uv |
| `packages/seerapi-ts` | TypeScript SDK | TypeScript, pnpm |

## 快速开始

### 环境要求

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) >= 0.9.0
- [pnpm](https://pnpm.io/)（仅 TypeScript 包需要）

### 安装

```bash
git clone https://github.com/SeerAPI/seerapi.git
cd seerapi
```

### Python 包

Python 包由 [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/) 统一管理：

```bash
# 安装所有 Python 依赖
uv sync

# 使用 CLI 工具
uv run solaris --help

# 运行单个包的测试
uv run --package seerapi-models pytest
uv run --package seerapi-python pytest
uv run --package seerapi-solaris pytest

# 代码检查
uv run ruff check .
uv run ruff format .
```

### TypeScript 包

```bash
pnpm install
pnpm run build:ts
```

### 使用已发布的包

```bash
# Python
pip install seerapi
pip install seerapi-models

# TypeScript
pnpm add @seerapi/client
```

## 相关链接

- [在线文档](https://docs.seerapi.com)
- [API 参考](https://api.seerapi.com/docs/v1/api_reference.html)
- [GitHub 仓库](https://github.com/SeerAPI/seerapi)

## 许可证

MIT
