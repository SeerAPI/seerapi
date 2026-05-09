"""创建仅包含表结构的轻量级 SQLite 数据库

用于 CI/CD 中的 drizzle-kit pull，无需运行完整的 Solaris 数据分析流程。
通过导入 seerapi_models 注册所有 SQLModel 表定义，
然后调用 SQLModel.metadata.create_all 创建空表。
"""

import sys
from pathlib import Path

from sqlmodel import SQLModel, create_engine

import seerapi_models  # noqa: F401


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else 'schema-only.db'
    output_path = Path(output)
    if output_path.exists():
        output_path.unlink()

    engine = create_engine(f'sqlite:///{output_path.resolve()}')
    SQLModel.metadata.create_all(engine)
    print(f'已创建 schema-only DB: {output}')


if __name__ == '__main__':
    main()
