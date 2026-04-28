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

### Python 包

```bash
# 安装所有 Python 依赖
uv sync

# 使用 CLI 工具
uv run solaris --help

# 在项目中使用
uv run python -c "from seerapi import SeerAPI; from seerapi_models import Item"
```

### TypeScript 包

```bash
pnpm install
pnpm run build:ts
```

## 许可证

MIT
