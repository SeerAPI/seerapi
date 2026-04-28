# Parser 开发指南

本指南介绍如何为 Solaris 项目开发新的 Parser，将游戏二进制配置文件解析为 JSON 数据。

## 目录

- [什么是 Parser](#什么是-parser)
- [快速开始](#快速开始)
- [BytesReader API](#bytesreader-api)
- [开发步骤](#开发步骤)
- [实战示例](#实战示例)
- [常见问题](#常见问题)

## 什么是 Parser

Parser 负责将游戏客户端的二进制配置文件（`.bytes`）解析为结构化的 JSON 数据。

**工作流程：**
```
.bytes 文件 → BytesReader → Parser 解析 → TypedDict → JSON 输出
```

## 快速开始

### 基本结构

```python
from typing import TypedDict
from solaris.parse.base import BaseParser
from solaris.parse.bytes_reader import BytesReader

# 1. 定义数据结构
class YourConfig(TypedDict):
    id: int
    name: str
    value: float

# 2. 创建 Parser 类
class YourParser(BaseParser[YourConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'your_config.bytes'  # 源文件名
    
    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'yourConfig.json'  # 输出文件名
    
    def parse(self, data: bytes) -> YourConfig:
        reader = BytesReader(data)
        return {
            'id': reader.ReadSignedInt(),
            'name': reader.ReadUTFBytesWithLength(),
            'value': reader.ReadFloat()
        }
```

## BytesReader API

BytesReader 提供读取二进制数据的方法，按顺序读取字节流。

### 常用方法

| 方法 | 返回类型 | 说明 | 示例 |
|------|---------|------|------|
| `ReadBoolean()` | `bool` | 读取布尔值（1字节） | `has_data = reader.ReadBoolean()` |
| `ReadSignedInt()` | `int` | 读取有符号32位整数 | `id = reader.ReadSignedInt()` |
| `ReadUnsignedInt()` | `int` | 读取无符号32位整数 | `count = reader.ReadUnsignedInt()` |
| `ReadFloat()` | `float` | 读取32位浮点数 | `rate = reader.ReadFloat()` |
| `ReadDouble()` | `float` | 读取64位浮点数 | `value = reader.ReadDouble()` |
| `ReadUTFBytesWithLength()` | `str` | 读取带长度前缀的UTF-8字符串 | `name = reader.ReadUTFBytesWithLength()` |
| `ReadUTFBytes(length)` | `str` | 读取指定长度的UTF-8字符串 | `text = reader.ReadUTFBytes(10)` |

### 整数类型对照

| Python 方法 | C# 类型 | 字节数 | 范围 |
|------------|---------|--------|------|
| `ReadSignedByte()` | `sbyte` | 1 | -128 ~ 127 |
| `ReadUnsignedByte()` | `byte` | 1 | 0 ~ 255 |
| `ReadSignedShort()` | `short` | 2 | -32,768 ~ 32,767 |
| `ReadUnsignedShort()` | `ushort` | 2 | 0 ~ 65,535 |
| `ReadSignedInt()` | `int` | 4 | -2^31 ~ 2^31-1 |
| `ReadUnsignedInt()` | `uint` | 4 | 0 ~ 2^32-1 |

### 位置控制

```python
# 获取当前位置
pos = reader.Position

# 设置位置
reader.Position = 100

# 跳过字节
reader.Position += 10
```

## 开发步骤

### 1. 找到 C# 源代码

在游戏客户端反编译代码中找到对应的配置类，例如：

```csharp
// C# 代码示例
public class ItemConfig {
    public int ID;
    public string Name;
    public int Type;
    public float Value;
}
```

### 2. 定义 TypedDict

根据 C# 类定义 Python 数据结构：

```python
class ItemConfig(TypedDict):
    id: int          # C# 的 ID
    name: str        # C# 的 Name
    type: int        # C# 的 Type
    value: float     # C# 的 Value
```

**命名规范：**
- 使用 snake_case（Python 风格）
- 保持字段含义一致

### 3. 分析读取顺序

**关键：字段读取顺序必须与 C# 代码完全一致！**

查看 C# 的序列化代码：

```csharp
// C# 序列化顺序
writer.WriteInt(ID);
writer.WriteUTF(Name);
writer.WriteInt(Type);
writer.WriteFloat(Value);
```

对应的 Python 读取顺序：

```python
id = reader.ReadSignedInt()      # 1. ID
name = reader.ReadUTFBytesWithLength()  # 2. Name
type = reader.ReadSignedInt()    # 3. Type
value = reader.ReadFloat()       # 4. Value
```

### 4. 实现 parse() 方法

```python
def parse(self, data: bytes) -> ItemConfig:
    reader = BytesReader(data)
    
    # 按顺序读取字段
    return {
        'id': reader.ReadSignedInt(),
        'name': reader.ReadUTFBytesWithLength(),
        'type': reader.ReadSignedInt(),
        'value': reader.ReadFloat()
    }
```

### 5. 测试

```python
# 测试解析
parser = YourParser()
with open('your_config.bytes', 'rb') as f:
    data = f.read()
result = parser.parse(data)
print(result)
```

## 实战示例

### 示例 1：简单配置

**C# 代码：**
```csharp
public class SimpleConfig {
    public int Count;
    public List<int> IDs;
}
```

**Python 实现：**
```python
class SimpleConfig(TypedDict):
    count: int
    ids: list[int]

class SimpleConfigParser(BaseParser[SimpleConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'simple.bytes'
    
    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'simple.json'
    
    def parse(self, data: bytes) -> SimpleConfig:
        reader = BytesReader(data)
        
        # 读取数量
        count = reader.ReadSignedInt()
        
        # 读取 ID 列表
        ids = []
        for _ in range(count):
            ids.append(reader.ReadSignedInt())
        
        return {'count': count, 'ids': ids}
```

### 示例 2：嵌套结构

**C# 代码：**
```csharp
public class Item {
    public int ID;
    public string Name;
}

public class Container {
    public int ItemCount;
    public List<Item> Items;
}
```

**Python 实现：**
```python
class ItemData(TypedDict):
    id: int
    name: str

class ContainerConfig(TypedDict):
    item_count: int
    items: list[ItemData]

class ContainerParser(BaseParser[ContainerConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'container.bytes'
    
    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'container.json'
    
    def parse(self, data: bytes) -> ContainerConfig:
        reader = BytesReader(data)
        
        # 读取物品数量
        item_count = reader.ReadSignedInt()
        
        # 读取物品列表
        items = []
        for _ in range(item_count):
            item = {
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength()
            }
            items.append(item)
        
        return {
            'item_count': item_count,
            'items': items
        }
```

### 示例 3：条件解析

**C# 代码：**
```csharp
public class Config {
    public bool HasOptional;
    public int Value;
    public string OptionalData;  // 仅当 HasOptional 为 true 时存在
}
```

**Python 实现：**
```python
class ConfigData(TypedDict):
    has_optional: bool
    value: int
    optional_data: str | None

class ConfigParser(BaseParser[ConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'config.bytes'
    
    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'config.json'
    
    def parse(self, data: bytes) -> ConfigData:
        reader = BytesReader(data)
        
        has_optional = reader.ReadBoolean()
        value = reader.ReadSignedInt()
        
        # 条件读取
        optional_data = None
        if has_optional:
            optional_data = reader.ReadUTFBytesWithLength()
        
        return {
            'has_optional': has_optional,
            'value': value,
            'optional_data': optional_data
        }
```

## 常见问题

### 1. 如何确定字段读取顺序？

**答：** 必须查看 C# 源代码的序列化顺序。字段声明顺序不一定是读取顺序！

### 2. 字符串读取用哪个方法？

**答：** 
- 大多数情况用 `ReadUTFBytesWithLength()`（带长度前缀）
- 固定长度字符串用 `ReadUTFBytes(length)`

### 3. 如何处理可选字段？

**答：** 通常有布尔标志指示是否存在：

```python
if reader.ReadBoolean():  # 检查是否有数据
    optional_value = reader.ReadSignedInt()
else:
    optional_value = None
```

### 4. 解析出错怎么办？

**答：** 检查以下几点：
1. 字段读取顺序是否正确
2. 数据类型是否匹配（int/float/string）
3. 是否遗漏了某些字段
4. 条件判断逻辑是否正确

### 5. 如何调试？

**答：** 使用位置追踪：

```python
print(f"当前位置: {reader.Position}")
value = reader.ReadSignedInt()
print(f"读取值: {value}, 新位置: {reader.Position}")
```

## 参考资源

- [BytesReader 源码](../solaris/parse/bytes_reader.py)
- [现有 Parser 示例](../solaris/parse/parsers/)
- [专有名词表](专有名词.md)

## 下一步

学习如何开发 Analyzer：[Analyzer 开发指南](ANALYZER_GUIDE.md)
