# SeerAPI Python 客户端

[SeerAPI](https://github.com/SeerAPI) 是一个提供赛尔号游戏数据的开放 API 平台。本项目是 SeerAPI 的官方 Python 客户端库，提供了简洁易用的异步接口，支持获取精灵、技能、装备、刻印等 50+ 种游戏资源数据。

## 特性

- 🚀 **异步优先**：基于 `httpx` 和 `hishel` 构建，提供高性能的异步 HTTP 请求
- 💾 **自动缓存**：集成 HTTP 缓存机制，减少重复请求
- 🎯 **类型安全**：完整的类型提示支持，提供良好的 IDE 智能提示
- 📦 **分页支持**：内置分页处理，方便获取大量数据
- 🔄 **同步兼容**：提供 `async_to_sync` 装饰器，在同步代码中也能使用
## 安装

使用 pip 安装：

```bash
pip install seerapi
```

或使用 uv：

```bash
uv add seerapi
```

## 快速开始

### 异步使用方式

```python
import asyncio
from seerapi import SeerAPI, PageInfo

async def main():
    # 使用异步上下文管理器，自动管理连接
    async with SeerAPI() as client:
        # 获取单个精灵信息
        pet = await client.get('pet', id=1)
        print(f"精灵名称: {pet.name}")
        
        # 获取所有精灵（自动分页）
        count = 0
        async for pet in client.list('pet'):
            print(f"ID: {pet.id}, 名称: {pet.name}")
            count += 1
            if count >= 10:  # 只显示前 10 个
                break

if __name__ == '__main__':
    asyncio.run(main())
```

### 同步使用方式

如果你需要在同步代码中使用，可以使用 `async_to_sync` 装饰器：

```python
from seerapi import SeerAPI, PageInfo, async_to_sync

@async_to_sync
async def get_pet_info(pet_id: int):
    async with SeerAPI() as client:
        pet = await client.get('pet', id=pet_id)
        return pet

# 像普通同步函数一样调用
pet = get_pet_info(1)
print(pet.name)
```

## API 文档

### SeerAPI 客户端

#### 初始化

```python
from seerapi import SeerAPI

# 使用默认配置（指向官方 API）
client = SeerAPI()

# 自定义配置
client = SeerAPI(
    scheme='https',
    hostname='api.seerapi.com',
    version_path='v1'
)
```

#### 方法

##### `get(resource_name, id)`

获取单个资源的详细信息。

**参数：**
- `resource_name` (str): 资源类型名称
- `id` (int): 资源 ID

**返回：**
- 对应的模型实例

**示例：**

```python
# 获取精灵信息
pet = await client.get('pet', id=1)

# 获取技能信息
skill = await client.get('skill', id=100)

# 获取装备信息
equip = await client.get('equip', id=50)
```

##### `list(resource_name)`

获取所有资源的异步生成器，自动处理分页。

**参数：**
- `resource_name` (str): 资源类型名称

**返回：**
- `AsyncGenerator`: 异步生成器，用于遍历所有资源

**示例：**

```python
# 遍历所有精灵
async for pet in client.list('pet'):
    print(pet.name)

# 只获取前 100 个
count = 0
async for pet in client.list('pet'):
    print(pet.name)
    count += 1
    if count >= 100:
        break
```

##### `paginated_list(resource_name, page_info)`

获取资源列表（手动分页控制）。

**参数：**
- `resource_name` (str): 资源类型名称
- `page_info` (PageInfo): 分页信息对象

**返回：**
- `PagedResponse` 对象，包含：
  - `count` (int): 总记录数
  - `results` (AsyncGenerator): 异步生成器，用于遍历当前页结果
  - `next` (PageInfo | None): 下一页信息
  - `previous` (PageInfo | None): 上一页信息
  - `first` (PageInfo | None): 首页信息
  - `last` (PageInfo | None): 末页信息

**示例：**

```python
from seerapi import PageInfo

# 获取前 20 条记录
page_info = PageInfo(offset=0, limit=20)
response = await client.paginated_list('pet', page_info)

# 查看总数
print(f"总数: {response.count}")

# 遍历当前页的结果
async for pet in response.results:
    print(pet.name)

# 获取下一页
if response.next:
    next_response = await client.paginated_list('pet', response.next)
```

##### `get_by_name(resource_name, name)`

通过名称获取资源。该方法仅支持具有名称属性的资源类型。

**参数：**
- `resource_name` (str): 资源类型名称（必须是支持按名称查询的资源类型）
- `name` (str): 资源名称

**返回：**
- `NamedData` 对象，包含：
  - `data[int, named_model_instance]`: 同名的模型实例字典，key 为 ID，value 为模型实例

**示例：**

```python
# 通过名称获取技能
    async with SeerAPI() as client:
        skills = await client.get_by_name('skill', '虚妄幻境') # 有三个技能都叫虚妄幻境
        for id, skill in skills.data.items():
            print(id)
            print(skill.skill_effect)

```
### PageInfo 类

用于指定分页参数。

**属性：**
- `offset` (int): 偏移量，默认为 0
- `limit` (int): 每页记录数，默认为 100

**示例：**

```python
from seerapi import PageInfo

# 获取第 1-10 条记录
page1 = PageInfo(offset=0, limit=10)

# 获取第 11-20 条记录
page2 = PageInfo(offset=10, limit=10)

# 获取第 21-30 条记录
page3 = PageInfo(offset=20, limit=10)
```

### async_to_sync 装饰器

将异步函数转换为同步函数的装饰器。

**示例：**

```python
from seerapi import async_to_sync, SeerAPI

@async_to_sync
async def fetch_pet_list(limit: int = 10):
    async with SeerAPI() as client:
        pets = []
        count = 0
        async for pet in client.list('pet'):
            pets.append(pet)
            count += 1
            if count >= limit:
                break
        return pets

# 同步调用
pets = fetch_pet_list(limit=5)
for pet in pets:
    print(pet.name)
```

## 错误处理

```python
import asyncio
from httpx import HTTPStatusError
from seerapi import SeerAPI

async def safe_get_pet(pet_id: int):
    async with SeerAPI() as client:
        try:
            pet = await client.get('pet', id=pet_id)
            return pet
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"精灵 ID {pet_id} 不存在")
            else:
                print(f"HTTP 错误: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            return None

asyncio.run(safe_get_pet(999999))
```

## 开发环境设置

### 环境要求

- Python >= 3.10
- uv（推荐）或 pip

### 安装开发依赖

```bash
# 克隆仓库
git clone https://github.com/your-org/seerapi-python.git
cd seerapi-python

# 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 代码风格

项目使用 Ruff 进行代码格式化和检查：

```bash
# 格式化代码
ruff format .

# 检查代码
ruff check .

# 自动修复问题
ruff check --fix .
```

### 类型检查

项目使用 Pyright 进行类型检查：

## 依赖项

- [httpx](https://www.python-httpx.org/) - 现代化的 HTTP 客户端
- [hishel](https://hishel.com/) - HTTP 缓存库
- [seerapi-models](https://github.com/SeerAPI/seerapi-models) - SeerAPI 数据模型

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
