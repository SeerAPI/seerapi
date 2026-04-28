# SeerAPI TypeScript SDK

这是 SeerAPI 的官方 TypeScript SDK，由 `@hey-api/openapi-ts` 自动生成。它提供了与 SeerAPI 交互的类型安全客户端，并集成了 Drizzle ORM 以支持本地 SQLite 数据库操作。

## 特性

- **全自动生成**: 无论是 API 客户端还是数据库 Schema，均通过自动化工具生成，确保与服务端定义高度一致。
- **类型安全**: 完全基于 OpenAPI 规范生成的 TypeScript 类型定义。
- **多种客户端支持**: 内置对 Axios 的支持。
- **本地数据库集成**: 使用 Drizzle ORM 和 LibSQL (SQLite) 管理本地数据，Schema 自动同步。
- **自动转换**: 支持日期等复杂类型的自动转换。

## 安装

```bash
npm install @seerapi/client
# 或者
yarn add @seerapi/client
# 或者
pnpm add @seerapi/client
```

## 快速开始

### API 客户端使用

```typescript
import { createClient } from '@seerapi/client';

const client = createClient({
  baseURL: 'https://api.seerapi.com', // 替换为实际 API 地址
});

// 使用生成的 SDK 方法
async function fetchData() {
  try {
    const response = await client.getSomeEndpoint();
    console.log(response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
```

### 数据库操作 (Drizzle ORM)

项目内置了自动生成的 SQLite 数据库 Schema：

```typescript
import { db } from '@seerapi/client/db';
import { pet, skill } from '@seerapi/client/db/schema';

async function queryDb() {
  // 所有的表定义均根据 SeerAPI 的 SQLite 数据库自动生成
  const allPets = await db.select().from(pet).limit(10).all();
  console.log(allPets);
}
```

## 许可证

[MIT](LICENSE)

## 相关链接

- [GitHub 仓库](https://github.com/SeerAPI/seerapi-ts)

