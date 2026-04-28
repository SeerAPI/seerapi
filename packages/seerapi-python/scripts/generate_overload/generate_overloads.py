"""代码生成工具：使用 AST 生成 overload 类型注释

使用方法：
    from generate_overloads import OverloadGenerator

    generator = OverloadGenerator(
        function_name="get_resource",
        mapping=MODEL_MAP,
        key_param="resource_name",
        additional_params=[("id", "int")],
        is_async=True,
        has_self=True,
    )

    code = generator.generate()
"""

import ast
from typing import Any


class OverloadGenerator:
    """基于 AST 的 overload 代码生成器"""

    def __init__(
        self,
        function_name: str,
        mapping: dict[Any, Any],
        key_param: str = 'resource_name',
        additional_params: list[tuple[str, str]] | None = None,
        is_async: bool = False,
        has_self: bool = True,
        return_type_from_mapping: bool = True,
        return_type_fallback: str = 'Any',
    ):
        """初始化生成器

        Args:
            function_name: 函数名称
            mapping: 映射字典，key 为 Literal 值，value 为返回类型（类或字符串）
            key_param: 需要使用 Literal 约束的参数名
            additional_params: 额外的参数列表，格式为 [(参数名, 类型注解), ...]
            is_async: 是否为异步函数
            has_self: 是否有 self 参数（类方法）
            return_type_from_mapping: 是否从 mapping 的值中提取返回类型
            return_type_fallback: 当无法从 mapping 提取类型时的后备类型
        """
        self.function_name = function_name
        self.mapping = mapping
        self.key_param = key_param
        self.additional_params = additional_params or []
        self.is_async = is_async
        self.has_self = has_self
        self.return_type_from_mapping = return_type_from_mapping
        self.return_type_fallback = return_type_fallback

    def _create_type_annotation(self, type_str: str) -> ast.expr:
        """创建类型注解的 AST 节点

        支持简单类型和泛型类型，例如：
        - int, str, Any
        - list[str]
        - dict[str, Any]
        """
        # 处理泛型类型
        if '[' in type_str:
            # 简单解析泛型
            base, args = type_str.split('[', 1)
            args = args.rstrip(']')

            # 解析泛型参数
            arg_list = []
            depth = 0
            current = []
            for char in args:
                if char == '[':
                    depth += 1
                    current.append(char)
                elif char == ']':
                    depth -= 1
                    current.append(char)
                elif char == ',' and depth == 0:
                    arg_list.append(''.join(current).strip())
                    current = []
                else:
                    current.append(char)
            if current:
                arg_list.append(''.join(current).strip())

            # 创建泛型类型的 AST
            return ast.Subscript(
                value=ast.Name(id=base.strip()),
                slice=ast.Tuple(
                    elts=[self._create_type_annotation(arg) for arg in arg_list]
                )
                if len(arg_list) > 1
                else self._create_type_annotation(arg_list[0]),
            )
        else:
            return ast.Name(id=type_str.strip())

    def _create_literal_annotation(self, value: str) -> ast.Subscript:
        """创建 Literal 类型注解"""
        return ast.Subscript(
            value=ast.Name(id='Literal'), slice=ast.Constant(value=value)
        )

    def _create_arguments(self, literal_value: str | None = None) -> ast.arguments:
        """创建函数参数列表

        Args:
            literal_value: 如果提供，key_param 使用 Literal[literal_value]，否则使用 str
        """
        args = []

        # 添加 self 参数
        if self.has_self:
            args.append(ast.arg(arg='self', annotation=None))

        # 添加 key_param
        if literal_value is not None:
            key_annotation = self._create_literal_annotation(literal_value)
        else:
            key_annotation = ast.Name(id='str')

        args.append(ast.arg(arg=self.key_param, annotation=key_annotation))

        # 添加额外参数
        for param_name, param_type in self.additional_params:
            args.append(
                ast.arg(
                    arg=param_name, annotation=self._create_type_annotation(param_type)
                )
            )

        return ast.arguments(
            posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[]
        )

    def _get_return_type_name(self, value: Any) -> str:
        """从 mapping 的值获取返回类型名称"""
        if not self.return_type_from_mapping:
            return str(value)

        if isinstance(value, type):
            return value.__name__
        elif isinstance(value, str):
            return value
        else:
            return self.return_type_fallback

    def _create_overload_function(
        self, key: str, return_type_name: str
    ) -> ast.AsyncFunctionDef | ast.FunctionDef:
        """创建一个 overload 函数定义"""
        func_class = ast.AsyncFunctionDef if self.is_async else ast.FunctionDef

        return func_class(
            name=self.function_name,
            args=self._create_arguments(literal_value=key),
            body=[ast.Expr(value=ast.Constant(value=...))],
            decorator_list=[ast.Name(id='overload')],
            returns=self._create_type_annotation(return_type_name),
        )

    def _create_implementation_function(
        self, body_code: str | None = None
    ) -> ast.AsyncFunctionDef | ast.FunctionDef:
        """创建实际实现的函数定义"""
        func_class = ast.AsyncFunctionDef if self.is_async else ast.FunctionDef

        # 解析函数体
        body: list[ast.stmt]
        if body_code:
            # 使用 ast.parse 解析函数体代码
            body_module = ast.parse(body_code)
            body = body_module.body
        else:
            body = [ast.Expr(value=ast.Constant(value=...))]

        return func_class(
            name=self.function_name,
            args=self._create_arguments(literal_value=None),
            body=body,
            decorator_list=[],
            returns=self._create_type_annotation(self.return_type_fallback),
        )

    def generate(
        self,
        include_implementation: bool = False,
        implementation_body: str | None = None,
    ) -> str:
        """生成 overload 代码

        Args:
            include_implementation: 是否包含实际实现的函数定义
            implementation_body: 实际实现的函数体代码

        Returns:
            生成的 Python 代码字符串
        """
        functions = []

        # 为每个映射项创建 overload
        for key, value in self.mapping.items():
            return_type_name = self._get_return_type_name(value)
            func_def = self._create_overload_function(str(key), return_type_name)
            functions.append(func_def)

        # 如果需要，添加实际实现
        if include_implementation:
            impl_func = self._create_implementation_function(implementation_body)
            functions.append(impl_func)

        # 创建模块并转换为代码
        module = ast.Module(body=functions, type_ignores=[])

        # 修复缺失的位置信息
        ast.fix_missing_locations(module)

        # 转换为代码
        code = ast.unparse(module)

        return code

    def generate_with_imports(
        self,
        include_implementation: bool = False,
        implementation_body: str | None = None,
        extra_imports: list[str] | None = None,
    ) -> str:
        """生成包含必要导入的完整代码

        Args:
            include_implementation: 是否包含实际实现
            implementation_body: 实际实现的函数体
            extra_imports: 额外的导入语句列表

        Returns:
            包含导入的完整代码
        """
        imports = ['from typing import overload, Literal']

        if extra_imports:
            imports.extend(extra_imports)

        code = self.generate(include_implementation, implementation_body)

        return '\n'.join(imports) + '\n\n\n' + code


class ClassMethodOverloadGenerator(OverloadGenerator):
    """用于生成类方法 overload 的生成器"""

    def __init__(self, class_name: str, *args: Any, **kwargs: Any):
        """初始化类方法生成器

        Args:
            class_name: 类名
            *args, **kwargs: 传递给父类的参数
        """
        super().__init__(*args, **kwargs)
        self.class_name = class_name
        # 类方法必须有 self
        self.has_self = True

    def generate_class(
        self,
        include_implementation: bool = False,
        implementation_body: str | None = None,
        include_docstring: bool = True,
    ) -> str:
        """生成包含 overload 方法的完整类定义

        Args:
            include_implementation: 是否包含实际实现
            implementation_body: 实际实现的函数体
            include_docstring: 是否包含类文档字符串

        Returns:
            完整的类定义代码
        """
        # 生成方法
        methods = []

        for key, value in self.mapping.items():
            return_type_name = self._get_return_type_name(value)
            func_def = self._create_overload_function(str(key), return_type_name)
            methods.append(func_def)

        if include_implementation:
            impl_func = self._create_implementation_function(implementation_body)
            methods.append(impl_func)

        # 创建类定义
        class_body = []

        if include_docstring:
            class_body.append(
                ast.Expr(value=ast.Constant(value=f'{self.class_name} 类'))
            )

        class_body.extend(methods)

        class_def = ast.ClassDef(
            name=self.class_name,
            bases=[],
            keywords=[],
            body=class_body,
            decorator_list=[],
        )

        module = ast.Module(body=[class_def], type_ignores=[])
        ast.fix_missing_locations(module)

        return ast.unparse(module)


# ============ 便捷函数 ============


def generate_overloads(
    function_name: str, mapping: dict[Any, Any], **kwargs: Any
) -> str:
    """便捷函数：生成 overload 代码

    参数同 OverloadGenerator
    """
    generator = OverloadGenerator(function_name, mapping, **kwargs)
    return generator.generate()


def generate_overloads_with_imports(
    function_name: str, mapping: dict[Any, Any], **kwargs: Any
) -> str:
    """便捷函数：生成包含导入的 overload 代码

    参数同 OverloadGenerator
    """
    generator = OverloadGenerator(function_name, mapping, **kwargs)
    return generator.generate_with_imports()


# ============ 示例使用 ============

if __name__ == '__main__':
    from seerapi._model_map import MODEL_MAP

    print('=' * 70)
    print('示例 1: 基础用法 - 为 SeerAPI.get_resource 生成 overload')
    print('=' * 70)

    generator = OverloadGenerator(
        function_name='get_resource',
        mapping=MODEL_MAP,
        key_param='resource_name',
        additional_params=[('id', 'int')],
        is_async=True,
        has_self=True,
    )

    code = generator.generate()
    print(code[:1000])  # 只打印前 1000 个字符
    print('...')
    print(f'\n[总共生成了 {len(code)} 个字符]\n')

    print('=' * 70)
    print('示例 2: 包含实际实现')
    print('=' * 70)

    implementation = """
response = await self._client.get(f'/{resource_name}/{id}')
return response.json()
"""

    code = generator.generate(
        include_implementation=True, implementation_body=implementation
    )

    # 只显示最后几行（实际实现部分）
    lines = code.split('\n')
    print('\n'.join(lines[-10:]))

    print('\n' + '=' * 70)
    print('示例 3: 包含导入和实现的完整代码')
    print('=' * 70)

    full_code = generator.generate_with_imports(
        include_implementation=True,
        implementation_body=implementation,
        extra_imports=[
            'from seerapi._model_map import ModelName, ModelType',
            'from httpx import Response',
        ],
    )

    # 显示开头部分
    print('\n'.join(full_code.split('\n')[:20]))
    print('...')

    print('\n' + '=' * 70)
    print('示例 4: 自定义映射示例')
    print('=' * 70)

    custom_map = {
        'json': 'dict[str, Any]',
        'xml': 'str',
        'csv': 'list[list[str]]',
        'binary': 'bytes',
    }

    custom_gen = OverloadGenerator(
        function_name='parse_data',
        mapping=custom_map,
        key_param='format',
        additional_params=[('data', 'bytes'), ('encoding', 'str')],
        is_async=False,
        has_self=False,
        return_type_from_mapping=False,
    )

    print(custom_gen.generate(include_implementation=True))

    print('\n' + '=' * 70)
    print('示例 5: 生成完整的类定义')
    print('=' * 70)

    class_gen = ClassMethodOverloadGenerator(
        class_name='SeerAPI',
        function_name='get_resource',
        mapping={k: v for k, v in list(MODEL_MAP.items())[:5]},  # 只用前 5 个示例
        key_param='resource_name',
        additional_params=[('id', 'int')],
        is_async=True,
    )

    print(
        class_gen.generate_class(
            include_implementation=True,
            implementation_body=implementation,
            include_docstring=True,
        )
    )
