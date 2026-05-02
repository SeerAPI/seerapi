# SeerAPI 文档

**所有你需要的赛尔号数据，尽在此处。** ~~（如果不在此处，请提交 issue 或 PR😋）~~

**项目源码** https://github.com/SeerAPI/seerapi

## 项目简介

SeerAPI 是一个面向赛尔号游戏数据的开放式 API 平台，为开发者和研究者提供标准化、结构化的游戏数据访问接口。

## 为什么使用 SeerAPI？

### 简化数据获取流程

传统方式获取赛尔号游戏数据需要进行逆向工程、解析游戏文件、处理复杂的数据结构，往往需要数百行代码才能实现基本功能。SeerAPI 将这一过程简化为几行代码的 API 调用，大幅降低开发成本。

### 完整的数据覆盖

SeerAPI 提供全面的游戏数据访问能力：

- **精灵数据**：属性、种族值、技能池、进化链等完整信息
- **技能系统**：技能效果、威力、PP值、命中率等详细数据
- **游戏资源**：道具、装备、刻印、特性等游戏元素
- **数据库访问**：支持 SQL 查询方式直接访问底层数据

### 现代化的使用体验

- **类型安全** 基于 Pydantic 构建的数据模型，提供完整的类型提示、数据验证和序列化支持。
- **开发友好** 简洁直观的 API 设计，完善的 OpenAPI 文档，并提供 Python SDK 支持。
- **持续维护** 游戏更新时，SeerAPI 会自动同步最新数据，无需手动维护数据文件。

## 快速开始

### 安装

```bash
pip install seerapi
```

### 基础使用

```python
from seerapi import SeerAPI
import asyncio


async def main():
    async with SeerAPI() as client:
        # 查询技能数据
        skill = await client.get('skill', 38088)
        print(f"技能名称: {skill.name}")
        print(f"技能威力: {skill.power}")


asyncio.run(main())
```

> 完全看不懂？没关系！访问 [这里](./tutorial/前言.md) 开始零~~点五~~基础 SeerAPI 之旅！👊🤖🔥