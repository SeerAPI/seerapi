# seerapi-models

SeerAPI 数据模型/ORM 定义，用于前后端开发。

## 安装
使用 uv：

```bash
uv add seerapi-models
```
或者使用 pip：

```bash
pip install seerapi-models
```
也可以使用其他包管理器，如 poetry 等。

## 使用

```python
from seerapi_models import Item, ItemORM, ItemCategory, ResourceRef

category_ref = ResourceRef.from_model(ItemCategory, id=1) # 定义物品分类字段引用
item = Item(
    id=1,
    name="Item 1",
    max=100,
    category=catgeory_ref
)

print(item.name)

assert isinstance(item.to_orm(), ItemORM) # 转换为 ORM 模型
```

## 开发环境部署

### 使用 uv 部署

1. **安装 uv**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **克隆项目**
   ```bash
   git clone https://github.com/SeerAPI/seerapi-models.git
   cd seerapi-models
   ```

3. **安装依赖**
   ```bash
   # 同步项目依赖
   uv sync
   ```

4. **运行开发环境**
   ```bash
   # 在项目虚拟环境中运行 Python
   uv run python
   
   # 运行测试
   uv run pytest
   
   # 运行代码检查
   uv run ruff check
   uv run ruff format
   ```

### 开发容器 (推荐)

项目提供了 Dev Container 配置，支持一键部署开发环境：

1. 使用 VS Code 打开项目
2. 安装 Dev Containers 扩展
3. 按 `Ctrl+Shift+P` 打开命令面板
4. 选择 "Dev Containers: Reopen in Container"

容器会自动安装：
- Python 3.10
- uv 包管理器
- Ruff 代码检查工具
- 相关 VS Code 扩展

### 环境要求

- Python >= 3.10
- uv >= 0.9.0 (推荐使用最新版)

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
