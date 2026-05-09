/**
 * 修复 drizzle-kit 生成的 .ts 文件中缺少 .js 后缀的相对导入路径，
 * 使其兼容 TypeScript 的 NodeNext 模块解析。
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const dir = 'src/db';
for (const file of readdirSync(dir).filter(f => f.endsWith('.ts'))) {
    const filePath = join(dir, file);
    const content = readFileSync(filePath, 'utf8');
    const fixed = content.replace(/from "(\.\/[^"]+?)(?<!\.js)"/g, 'from "$1.js"');
    if (fixed !== content) {
        writeFileSync(filePath, fixed);
    }
}
