import { drizzle } from 'drizzle-orm/libsql';
import { type Client } from '@libsql/client';
import * as schema from "./schema.js";
import { relations } from "./relations.js";

/**
 * 创建一个新的数据库实例。
 * @param client - 用于数据库的客户端。
 * @returns 数据库实例。
 */
export function createDb(client: Client) {
    return drizzle({ client, schema, relations });
}

export type DBType = ReturnType<typeof createDb>;
