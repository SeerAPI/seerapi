# Overload 生成器使用指南

基于 AST 的代码生成工具，用于自动生成 Python `@overload` 类型注释。

为 SeerAPI 类编写类型注释时很好用。

## 核心优势

✅ **基于 AST**: 结构化生成代码，可读性好，易于维护  
✅ **类型安全**: 正确处理各种 Python 类型注解  
✅ **灵活扩展**: 支持同步/异步、函数/方法、带/不带实现  
✅ **自动导入**: 可选生成完整的导入语句  

## 快速开始

### 基础使用

```python
from generate_overloads import OverloadGenerator
from seerapi._model_map import MODEL_MAP

# 创建生成器
generator = OverloadGenerator(
    function_name="get_resource",
    mapping=MODEL_MAP,
    key_param="resource_name",
    additional_params=[("id", "int")],
    is_async=True,
    has_self=True,
)

# 生成代码
code = generator.generate()
print(code)
```

### 生成结果示例

```python
@overload
async def get_resource(self, resource_name: Literal['battle_effect'], id: int) -> BattleEffect:
    ...

@overload
async def get_resource(self, resource_name: Literal['pet_effect'], id: int) -> PetEffect:
    ...

# ... 更多 overload ...
```

## 常用场景

### 场景 1: 只生成 overload 签名

用于手动编写实现时：

```python
generator = OverloadGenerator(
    function_name="get_resource",
    mapping=MODEL_MAP,
    key_param="resource_name",
    additional_params=[("id", "int")],
    is_async=True,
    has_self=True,
)

code = generator.generate()

# 复制粘贴到你的类中，然后手动添加实现
```

### 场景 2: 生成包含实现的完整代码

```python
implementation = """
response = await self._client.get(f'/{resource_name}/{id}')
return response.json()
"""

code = generator.generate(
    include_implementation=True,
    implementation_body=implementation
)
```

### 场景 3: 生成包含导入的完整文件

```python
code = generator.generate_with_imports(
    include_implementation=True,
    implementation_body=implementation,
    extra_imports=[
        "from seerapi._model_map import ModelName",
        "from httpx import Response"
    ]
)

# 直接写入文件
with open("generated_api.py", "w") as f:
    f.write(code)
```

### 场景 4: 生成类定义

```python
from generate_overloads import ClassMethodOverloadGenerator

class_gen = ClassMethodOverloadGenerator(
    class_name="SeerAPI",
    function_name="get_resource",
    mapping=MODEL_MAP,
    key_param="resource_name",
    additional_params=[("id", "int")],
    is_async=True,
)

code = class_gen.generate_class(
    include_implementation=True,
    implementation_body=implementation,
    include_docstring=True
)
```

### 场景 5: 自定义映射

不仅限于 `MODEL_MAP`，可以用于任何映射：

```python
# 文件格式解析器
format_map = {
    "json": "dict[str, Any]",
    "xml": "str",
    "csv": "list[list[str]]",
    "binary": "bytes",
}

generator = OverloadGenerator(
    function_name="parse_file",
    mapping=format_map,
    key_param="format",
    additional_params=[("path", "str")],
    is_async=False,
    has_self=False,
    return_type_from_mapping=False,  # 直接使用映射中的字符串
)

code = generator.generate()
```

## 参数说明

### OverloadGenerator 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `function_name` | `str` | 必需 | 函数名称 |
| `mapping` | `dict[Any, Any]` | 必需 | 映射字典 (key → 返回类型) |
| `key_param` | `str` | `"resource_name"` | 使用 Literal 约束的参数名 |
| `additional_params` | `list[tuple[str, str]]` | `None` | 额外参数，格式 `[("参数名", "类型")]` |
| `is_async` | `bool` | `False` | 是否为异步函数 |
| `has_self` | `bool` | `True` | 是否有 self 参数（类方法） |
| `return_type_from_mapping` | `bool` | `True` | 是否从 mapping 值提取返回类型 |
| `return_type_fallback` | `str` | `"Any"` | 无法提取类型时的后备类型 |

### generate() 方法参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `include_implementation` | `bool` | `False` | 是否包含实际实现 |
| `implementation_body` | `str` | `None` | 实际实现的函数体代码 |

### generate_with_imports() 方法参数

继承 `generate()` 的所有参数，额外增加：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `extra_imports` | `list[str]` | `None` | 额外的导入语句 |

## 工作流程建议

### 推荐工作流程

1. **生成 overload 签名**：
   ```python
   generator = OverloadGenerator(...)
   code = generator.generate()
   print(code)
   ```

2. **复制到目标文件**：将生成的代码复制到 `_client.py`

3. **手动添加实现**：编写实际的函数实现

4. **验证类型**：使用 IDE 检查类型提示是否正确

### 快速迭代

如果需要频繁更新：

```python
# 创建一个专用脚本 update_client.py
from generate_overloads import OverloadGenerator
from seerapi._model_map import MODEL_MAP

generator = OverloadGenerator(...)
code = generator.generate_with_imports(...)

# 直接写入文件（开发环境）
with open("seerapi/_client_generated.py", "w") as f:
    f.write(code)

print("✅ 生成完成！")
```

## 类型支持

生成器支持常见的 Python 类型注解：

- ✅ 简单类型：`int`, `str`, `bool`, `bytes`, `Any`
- ✅ 泛型类型：`list[str]`, `dict[str, Any]`
- ✅ 嵌套泛型：`dict[str, list[int]]`
- ✅ 可选类型：`Optional[int]` (需要字符串形式)
- ✅ 联合类型：`int | str` (需要字符串形式)

## 最佳实践

### 1. 分离生成和实现

```python
# 生成 overload 部分
overloads = generator.generate()

# 手动编写实现
implementation = """
def my_function(...):
    # 实际逻辑
    pass
"""

# 合并
final_code = overloads + "\n\n" + implementation
```

### 2. 使用版本控制

```python
# 在文件顶部添加注释
header = '''"""
此文件由 generate_overloads.py 自动生成
生成时间: {datetime.now()}
请勿手动编辑 overload 部分
"""
'''

code = header + generator.generate_with_imports(...)
```

### 3. 增量更新

只在映射变化时重新生成：

```bash
# 监控 _model_map.py 变化
# 自动触发重新生成
```

## 常见问题

### Q: 如何处理复杂的返回类型？

A: 在 mapping 中使用字符串表示：

```python
mapping = {
    "complex": "tuple[int, str, dict[str, Any]]",
}
```

### Q: 如何生成多个函数？

A: 创建多个生成器：

```python
gen1 = OverloadGenerator("func1", map1, ...)
gen2 = OverloadGenerator("func2", map2, ...)

code = gen1.generate() + "\n\n" + gen2.generate()
```

### Q: 能否自定义代码格式？

A: AST 生成的代码使用 `ast.unparse()`，格式固定。建议使用 `ruff format` 后处理：

```bash
python generate_overloads.py > output.py
uv run ruff format output.py
```

## 运行示例

```bash
# 查看所有示例
cd /workspaces/SeerAPI/seerapi/packages/seerapi-python
uv run python scripts/generate_overload/generate_overloads.py

# 生成并格式化
uv run python scripts/generate_overload/generate_overloads.py | uv run ruff format -
```

## 进阶用法

### 自定义 AST 节点

如果需要更复杂的类型注解，可以继承并扩展 `_create_type_annotation` 方法：

```python
class CustomGenerator(OverloadGenerator):
    def _create_type_annotation(self, type_str: str) -> ast.expr:
        # 自定义逻辑
        if type_str.startswith("Optional"):
            # 特殊处理
            ...
        return super()._create_type_annotation(type_str)
```

## 总结

这个工具通过 AST 提供了：

- 🎯 清晰的面向对象 API
- 🔧 灵活的配置选项
- 📦 开箱即用的常见场景支持
- 🚀 类型安全的代码生成

享受类型安全的开发体验！ 🎉

