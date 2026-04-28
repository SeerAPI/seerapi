# Analyzer 开发指南

本指南介绍如何为 Solaris 项目开发新的 Analyzer，将解析后的数据转换为标准化的 API 模型。

## 目录

- [什么是 Analyzer](#什么是-analyzer)
- [Analyzer 类型](#analyzer-类型)
- [快速开始](#快速开始)
- [开发步骤](#开发步骤)
- [实战示例](#实战示例)
- [数据加载](#数据加载)
- [常见问题](#常见问题)

## 什么是 Analyzer

Analyzer 负责将 Parser 输出的 JSON 数据转换为符合 [seerapi-models](https://github.com/SeerAPI/seerapi-models) 规范的标准化模型。

**工作流程：**
```
JSON 数据 → Analyzer 分析 → Pydantic 模型 → API 输出
```

**主要作用：**
1. 数据转换和映射
2. 建立数据关联（如 ID 引用）
3. 数据清洗和标准化
4. 生成符合 API 规范的输出

## Analyzer 类型

Solaris 提供三种 Analyzer 基类：

| 类型 | 基类 | 用途 | 输入 | 输出 |
|------|------|------|------|------|
| 数据源 | `BaseDataSourceAnalyzer` | 转换单个数据源 | JSON 文件 | 模型列表 |
| 后处理 | `BasePostAnalyzer` | 处理已有模型 | 其他 Analyzer 结果 | 模型列表 |
| 混合 | `BaseDataSourcePostAnalyzer` | 结合两者 | JSON + 其他结果 | 模型列表 |

### 如何选择？

```
只需要读取 JSON 文件？
    → 使用 BaseDataSourceAnalyzer

需要使用其他 Analyzer 的结果？
    → 使用 BasePostAnalyzer

两者都需要？
    → 使用 BaseDataSourcePostAnalyzer
```

## 快速开始

### 示例：数据源 Analyzer

```python
from solaris.analyze.base import BaseDataSourceAnalyzer
from solaris.analyze.typing_ import DataImportConfig
from seerapi_models import YourModel

class YourAnalyzer(BaseDataSourceAnalyzer[YourModel]):
    """你的分析器"""
    
    @classmethod
    def data_import_config(cls) -> DataImportConfig:
        """配置数据源"""
        return {
            'your_data': 'yourData.json'  # 键名: JSON文件名
        }
    
    def analyze(self, your_data: dict) -> list[YourModel]:
        """分析逻辑"""
        results = []
        for item in your_data['items']:
            model = YourModel(
                id=item['id'],
                name=item['name']
            )
            results.append(model)
        return results
```

## 开发步骤

### 1. 确定 Analyzer 类型

根据数据来源选择合适的基类：

```python
# 只读取 JSON
from solaris.analyze.base import BaseDataSourceAnalyzer

# 只使用其他 Analyzer 结果
from solaris.analyze.base import BasePostAnalyzer

# 两者都需要
from solaris.analyze.base import BaseDataSourcePostAnalyzer
```

### 2. 配置数据源

#### 数据源 Analyzer

```python
@classmethod
def data_import_config(cls) -> DataImportConfig:
    return {
        'items': 'items.json',      # 必需的数据
        'config': 'config.json'     # 可以配置多个
    }
```

#### 后处理 Analyzer

```python
@classmethod
def dependencies(cls) -> list[type[BaseAnalyzer]]:
    return [ItemAnalyzer, ConfigAnalyzer]  # 依赖的 Analyzer
```

### 3. 实现 analyze() 方法

方法签名根据 Analyzer 类型不同：

```python
# BaseDataSourceAnalyzer
def analyze(self, items: dict, config: dict) -> list[YourModel]:
    # items 和 config 对应 data_import_config 中的键名
    pass

# BasePostAnalyzer
def analyze(self, items: list[ItemModel], config: list[ConfigModel]) -> list[YourModel]:
    # 参数对应 dependencies 中的 Analyzer 输出
    pass

# BaseDataSourcePostAnalyzer
def analyze(
    self,
    data: dict,  # 来自 data_import_config
    items: list[ItemModel],  # 来自 dependencies
    config: list[ConfigModel]
) -> list[YourModel]:
    pass
```

### 4. 转换数据

```python
def analyze(self, items: dict) -> list[ItemModel]:
    results = []
    
    for item_data in items['items']:
        # 创建模型实例
        model = ItemModel(
            id=item_data['id'],
            name=item_data['name'],
            value=item_data['value']
        )
        results.append(model)
    
    return results
```

### 5. 测试

```python
# 运行 Analyzer
analyzer = YourAnalyzer()
results = analyzer.run()
print(f"生成了 {len(results)} 个模型")
```

## 实战示例

### 示例 1：简单数据转换

将道具数据转换为标准模型：

```python
from solaris.analyze.base import BaseDataSourceAnalyzer
from solaris.analyze.typing_ import DataImportConfig
from seerapi_models import Item

class ItemAnalyzer(BaseDataSourceAnalyzer[Item]):
    """道具分析器"""
    
    @classmethod
    def data_import_config(cls) -> DataImportConfig:
        return {'items': 'items.json'}
    
    def analyze(self, items: dict) -> list[Item]:
        results = []
        
        for item_data in items['items']:
            item = Item(
                id=item_data['id'],
                name=item_data['name'],
                category=item_data['cat_id'],
                price=item_data['bean'],
                rarity=item_data.get('rarity', 1)
            )
            results.append(item)
        
        return results
```

### 示例 2：建立数据关联

使用其他 Analyzer 的结果建立关联：

```python
from solaris.analyze.base import BasePostAnalyzer
from seerapi_models import Skill, Effect

class SkillAnalyzer(BasePostAnalyzer[Skill]):
    """技能分析器（依赖效果数据）"""
    
    @classmethod
    def dependencies(cls) -> list[type[BaseAnalyzer]]:
        return [EffectAnalyzer]  # 依赖效果分析器
    
    def analyze(self, effects: list[Effect]) -> list[Skill]:
        # 创建效果 ID 到效果对象的映射
        effect_map = {e.id: e for e in effects}
        
        results = []
        for skill_data in self._load_skill_data():
            # 查找关联的效果
            effect_ids = skill_data['effect_ids']
            skill_effects = [
                effect_map[eid] 
                for eid in effect_ids 
                if eid in effect_map
            ]
            
            skill = Skill(
                id=skill_data['id'],
                name=skill_data['name'],
                effects=skill_effects  # 关联效果对象
            )
            results.append(skill)
        
        return results
    
    def _load_skill_data(self) -> list[dict]:
        """辅助方法：加载技能数据"""
        # 实现数据加载逻辑
        pass
```

### 示例 3：混合数据源

同时使用 JSON 数据和其他 Analyzer 结果：

```python
from solaris.analyze.base import BaseDataSourcePostAnalyzer
from solaris.analyze.typing_ import DataImportConfig
from seerapi_models import Pet, Skill

class PetAnalyzer(BaseDataSourcePostAnalyzer[Pet]):
    """精灵分析器（使用 JSON 和技能数据）"""
    
    @classmethod
    def data_import_config(cls) -> DataImportConfig:
        return {'pets': 'monsters.json'}
    
    @classmethod
    def dependencies(cls) -> list[type[BaseAnalyzer]]:
        return [SkillAnalyzer]
    
    def analyze(
        self,
        pets: dict,
        skills: list[Skill]
    ) -> list[Pet]:
        # 创建技能映射
        skill_map = {s.id: s for s in skills}
        
        results = []
        for pet_data in pets['monsters']['monster']:
            # 查找精灵的技能
            skill_ids = pet_data['skill_array']
            pet_skills = [
                skill_map[sid]
                for sid in skill_ids
                if sid in skill_map
            ]
            
            pet = Pet(
                id=pet_data['id'],
                name=pet_data['def_name'],
                type=pet_data['type'],
                skills=pet_skills
            )
            results.append(pet)
        
        return results
```

## 数据加载

### 使用 DataImportConfig

`data_import_config` 定义需要加载的 JSON 文件：

```python
@classmethod
def data_import_config(cls) -> DataImportConfig:
    return {
        'items': 'items.json',          # 键名可以自定义
        'config': 'config.json',
        'effects': 'effects.json'
    }
```

**规则：**
- 键名会成为 `analyze()` 方法的参数名
- 值是 JSON 文件名（相对于数据目录）
- 文件必须存在，否则会报错

### 使用 ResourceRef

在 `analyze()` 方法中可以使用 `ResourceRef` 引用其他数据：

```python
from solaris.analyze.utils import ResourceRef

def analyze(self, items: dict) -> list[ItemModel]:
    # 加载额外的数据文件
    extra_data = ResourceRef('extra.json').load()
    
    # 使用数据
    for item in items['items']:
        extra_info = extra_data.get(item['id'])
        # ...
```

### 补丁系统

使用补丁数据覆盖或补充原始数据：

```python
from solaris.analyze.utils import ResourceRef

def analyze(self, items: dict) -> list[ItemModel]:
    # 加载补丁数据
    patches = ResourceRef('items_patch.json', is_patch=True).load()
    
    # 应用补丁
    for item in items['items']:
        if item['id'] in patches:
            item.update(patches[item['id']])
    
    # 继续处理...
```

## 常见问题

### 1. 如何选择 Analyzer 类型？

**答：** 
- 只需要 JSON 数据 → `BaseDataSourceAnalyzer`
- 需要其他 Analyzer 结果 → `BasePostAnalyzer`
- 两者都需要 → `BaseDataSourcePostAnalyzer`

### 2. analyze() 方法的参数从哪来？

**答：**
- `BaseDataSourceAnalyzer`: 参数名对应 `data_import_config` 的键
- `BasePostAnalyzer`: 参数名对应 `dependencies` 中 Analyzer 的类名（小写）
- `BaseDataSourcePostAnalyzer`: 第一个参数是 `data_import_config`，后续参数是 `dependencies`

### 3. 如何处理缺失数据？

**答：** 使用 Python 的安全访问：

```python
# 使用 get() 提供默认值
value = item_data.get('optional_field', default_value)

# 使用条件判断
if 'optional_field' in item_data:
    value = item_data['optional_field']
```

### 4. 如何建立双向引用？

**答：** 分两步处理：

```python
def analyze(self, data: dict) -> list[Model]:
    # 第一步：创建所有对象
    items = [Model(id=d['id'], name=d['name']) for d in data['items']]
    item_map = {item.id: item for item in items}
    
    # 第二步：建立引用关系
    for item_data in data['items']:
        item = item_map[item_data['id']]
        # 设置引用
        if 'related_id' in item_data:
            item.related = item_map.get(item_data['related_id'])
    
    return items
```

### 5. 如何调试 Analyzer？

**答：** 使用日志和断点：

```python
def analyze(self, items: dict) -> list[ItemModel]:
    print(f"处理 {len(items['items'])} 个道具")
    
    results = []
    for item in items['items']:
        print(f"处理道具 ID: {item['id']}")
        # 处理逻辑...
    
    print(f"生成了 {len(results)} 个模型")
    return results
```

## 参考资源

- [现有 Analyzer 示例](../solaris/analyze/analyzers/)
- [seerapi-models 文档](https://github.com/SeerAPI/seerapi-models)
- [专有名词表](专有名词.md)

## 下一步

- 查看 [Parser 开发指南](PARSER_GUIDE.md) 了解数据来源
- 参考现有 Analyzer 代码学习最佳实践
