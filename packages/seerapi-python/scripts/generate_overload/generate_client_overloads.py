#!/usr/bin/env python3
"""为 SeerAPI 客户端生成 overload 类型注释的专用脚本

运行此脚本将生成 get_resource 方法的所有 overload 签名。
"""

from pathlib import Path
import sys

# 添加项目根目录到 sys.path，以便导入 seerapi 包
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from generate_overloads import OverloadGenerator

from seerapi._model_map import MODEL_MAP


def main():
    """生成 overload 签名"""

    # 创建生成器
    generator = OverloadGenerator(
        function_name='list',
        mapping={k: f'M.{v.__name__}' for k, v in MODEL_MAP.items()},
        key_param='resource_name',
        additional_params=[('page_info', 'PageInfo')],
        is_async=True,
        has_self=True,
        return_type_fallback='ModelType',
    )
    # 生成完整代码（包含导入）
    code = generator.generate_with_imports(
        include_implementation=False,
        extra_imports=[
            'from seerapi._model_map import ModelName, ModelType',
            'import seerapi_models as M',
        ],
    )

    output_file = 'seerapi/_client_generated.py'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)


if __name__ == '__main__':
    main()
