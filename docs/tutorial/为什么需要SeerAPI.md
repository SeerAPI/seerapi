# 为什么需要 SeerAPI？

在前言中，我们简单提到了 SeerAPI 的作用。但你可能会想：**"我真的需要它吗？"** 🤔

这是个好问题！让我们通过一个真实的例子来回答。

## 一个真实的挑战 💪

假设你想做一个简单的功能：**获取某个技能的效果描述**。

听起来很简单对吧？让我们看看如果 **不使用** SeerAPI，你需要做什么。

> 💡 **提示**：准备好了吗？接下来的代码可能会让你感到惊讶... 💩

## 不使用 SeerAPI 的做法 😰

*Talk is cheap, show me the code! 👇*
```python
from dataclasses import KW_ONLY, dataclass
from typing import Literal


def _slice_args(args_nums: list[int], args: list[int]) -> list[list[int]]:
    """
    将args按args_nums以切片。
    最后一个切片会包含所有剩余的参数。
    """
    if not args_nums:
        return []

    result = []
    start_index = 0

    # 处理到倒数第二个切片
    for num in args_nums[:-1]:
        end_index = start_index + num
        result.append(args[start_index:end_index])
        start_index = end_index

    # 最后一个切片包含所有剩余的参数
    result.append(args[start_index:])
    return result


@dataclass
class StatChange:
    atk: int
    def_: int
    sp_atk: int
    sp_def: int
    spd: int
    acc: int
    _: KW_ONLY
    # 字符串格式化模式：正符号、负符号、无符号、根据值、无数字
    format_mode: Literal['+', '-', 'unsigned', 'value', 'none'] = 'value'
    split_char: str = '、'

    def __post_init__(self):
        self.stat_info = [
            '攻击',
            '防御',
            '特攻',
            '特防',
            '速度',
            '命中',
        ]
        self._format_func = {
            '+': lambda x: f'+{abs(x):d}',
            '-': lambda x: f'-{abs(x):d}',
            'unsigned': lambda x: f'{abs(x):d}',
            'value': lambda x: f'{x:+d}',
            'none': lambda x: '',
        }[self.format_mode]

    def __str__(self) -> str:
        return self.split_char.join(
            [
                f'{stat}{self._format_func(num)}'
                for stat, num in zip(self.stat_info, self.__dict__.values())
                if num != 0 and stat
            ]
        )


@dataclass
class SkillEffectType:
    args_num: int
    param: list['SkillEffectParamInType'] | None
    info: str


@dataclass
class SkillEffectParam:
    id: int
    infos: list[str] | None


@dataclass
class SkillEffectParamInType:
    position: int
    param: SkillEffectParam


@dataclass
class Skill:
    id: int
    power: int
    max_pp: int
    infos: list[str] | None


class SkillInfoAnalyzer:
    def __init__(self):
        self.effect_param_map = self.create_effect_param_map()
        self.effect_type_map = self.create_effect_type_map()
        self.skill_map = self.create_skill_map()

    def load_json(self, path: str) -> dict:
        import json
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_effect_param_map(self) -> dict[int, SkillEffectParam]:
        effect_param_data: list = self.load_json('effectInfo.json')['root']['param_type']

        effect_param_map: dict[int, SkillEffectParam] = {}
        for effect_param in effect_param_data:
            id_ = effect_param['id']
            infos = None
            if param_str := effect_param.get('params'):
                infos = param_str.split('|')
            effect_param_map[id_] = SkillEffectParam(id=id_, infos=infos)

        return effect_param_map

    def create_effect_type_map(self) -> dict[int, SkillEffectType]:
        effect_type_data: list = self.load_json('effectInfo.json')['root']['effect']

        effect_type_map: dict[int, SkillEffectType] = {}
        for effect_type in effect_type_data:
            if not (info := effect_type.get('info')):
                continue
            id_ = effect_type['id']
            params: list[SkillEffectParamInType] | None = None
            if param_list := effect_type.get('param'):
                params = [
                    SkillEffectParamInType(
                        position=start_index,
                        param=self.effect_param_map[id_],
                    )
                    for id_, start_index, _ in [
                        param_list[i : i + 3] for i in range(0, len(param_list), 3)
                    ]
                ]
            skill_effect_type = SkillEffectType(
                args_num=effect_type['args_num'],
                param=params,
                info=info,
            )
            effect_type_map[id_] = skill_effect_type

        return effect_type_map


    def create_skill_info(self, type_ids: list[int], args: list[int]) -> list[str]:
        """根据效果类型ID和参数列表，创建技能效果对象列表。

        Args:
            type_ids: 技能效果的类型ID列表。
            args: 所有技能效果的参数列表。

        Returns:
            一个包含效果字符串的列表。如果出现未知效果类型或参数错误，则返回空列表。
        """
        args_nums = []
        # 遍历每个效果类型ID，从effect_type_map中获取所需参数数量
        for i in type_ids:
            if i not in self.effect_type_map:
                return []

            args_nums.append(self.effect_type_map[i].args_num)

        # 使用_slice_args辅助函数，根据每个效果所需的参数数量，将扁平的args列表
        # 切分为嵌套列表
        sliced_args: list[list[int]] = _slice_args(args_nums, list(args))
        results = []
        format_mode_map = {16: 'none', 24: '-'}
        # 遍历切分后的参数和对应的效果类型ID
        for type_id, effect_args in zip(type_ids, sliced_args):
            type_ = self.effect_type_map[type_id]
            # info_args用于格式化效果描述字符串，初始值为效果参数的副本
            info_args: list[int | StatChange | str | None] = list(effect_args)
            # 处理需要特殊格式化的参数
            for p in type_.param or []:
                param_index = p.position
                param = p.param
                # param_id为16, 24表示这是一个StatChange（状态变化）参数
                if (param_id := param.id) in (0, 16, 24) and len(info_args) > 6:
                    # 将6个参数合并为一个StatChange对象
                    slice_ = slice(param_index, param_index + 6)
                    kwargs = {}
                    if mode := format_mode_map.get(param_id):
                        kwargs['format_mode'] = mode
                    info_args[slice_] = [StatChange(*effect_args[slice_], **kwargs)] + [
                        None
                    ] * 5
                    # 由于状态变化占用6个参数位置，所以填充5个None
                    continue
                # 特别处理id为14的参数
                if param_id == 14:
                    info_args[param_index] = f'{effect_args[param_index]:+d}'
                    continue
                # 如果参数有预定义的描述信息(param.infos)
                if isinstance(param_infos := param.infos, list):
                    pos = effect_args[param_index]
                    try:
                        # 使用参数值作为索引，在infos中查找对应的描述文本并使用
                        info_args[param_index] = param_infos[pos]
                    except IndexError:
                        return []
            try:
                results.append(type_.info.format(*info_args))
            except IndexError:
                continue # 部分游戏内数据是错误的！

        return results

    def create_skill_map(self) -> dict[int, Skill]:
        unity_data: list = self.load_json('moves.json')['root']['moves']['move']
        result = {}
        for data in unity_data:
            id_ = data['id']
            power = data['power']
            max_pp = data['max_pp']
            infos = self.create_skill_info(
                data['side_effect'],
                data['side_effect_arg'],
            )
            result[id_] = Skill(id=id_, power=power, max_pp=max_pp, infos=infos)

        return result
    
    def get_skill(self, id_: int):
        return self.skill_map[id_]


if __name__ == '__main__':
    analyzer = SkillInfoAnalyzer()
    print(analyzer.get_skill(38088))
```

### 看到了什么？😨

如果你仔细看了上面的代码，你会发现：

* 📏 **230+ 行代码** - 仅仅为了获取技能的效果描述！
* 🧩 **复杂的数据结构** - 需要定义多个 dataclass 来处理嵌套的游戏数据
* 🔄 **繁琐的数据解析** - 需要手动处理参数切片、类型映射、格式化等
* 🤯 **维护噩梦** - 游戏更新后，你可能需要手动更新解析逻辑

**而且这还只是技能数据！** 如果你还想获取精灵、装备、刻印等其他类型的数据，你需要人肉分析数据，编写完全不同的代码... 😱

> 🚨 **重要**：我们甚至还没有讨论这些 JSON 数据文件从哪里来（这涉及游戏资源提取，是另一个复杂的话题🤫）。

这就是为什么我们创建了 **SeerAPI**！

实际上，上面的代码是 SeerAPI 内部技能分析器的**简化版本**。我们已经把这些复杂的工作搞定了，所以你不需要吃这些Sh*t了。 ✨

## 使用 SeerAPI 的做法 😍

现在，让我们看看使用 SeerAPI 完成同样的任务需要多少代码：
```python
import asyncio
from seerapi import SeerAPI


async def main():
    async with SeerAPI() as client:
        skill = await client.get('skill', 38088)
        print(skill)
        print('\n\n')
        print('技能效果:\n' + '\n'.join([effect.info for effect in skill.skill_effect]))


if __name__ == '__main__':
    asyncio.run(main())
```

### 让我们直观地对比一下：

| 对比项 | 不使用 SeerAPI | 使用 SeerAPI |
|--------|---------------|-------------|
| **代码行数** | 230+ 行 | 10 行 |
| **复杂度** | 需要理解游戏数据结构 | 调用简单的 API |
| **数据文件** | 需要自己获取和管理 | 无需关心 |
| **类型安全** | 需要自己定义类型 | 自带 Pydantic 模型 |
| **维护成本** | 游戏更新需要手动修改 | 自动同步 |
| **学习曲线** | 陡峭 😰 | 平缓 😊 |

**代码量减少了 95% 以上！** 🎉

## SeerAPI 的魔力 ✨

使用 SeerAPI，你只需要：

1. ✅ **导入客户端** - `from seerapi import SeerAPI`
2. ✅ **创建实例** - `async with SeerAPI() as client:`
3. ✅ **发起请求** - `await client.get('skill', 38088)`
4. ✅ **使用数据** - 数据已经被解析成清晰的 Python 对象

你不需要关心：

* ❌ 数据从哪里来
* ❌ 如何解析复杂的游戏格式
* ❌ 如何处理各种边界情况
* ❌ 游戏更新时如何维护代码

**这就是 SeerAPI 存在的意义**：让你专注于创造有价值的应用，而不是浪费时间在数据提取和解析上。 🚀

顺带一提，SeerAPI 还帮你解决了数据更新问题，你不需要手动实现更新逻辑，只需要等待SeerAPI自动更新即可。😎🔁

## 下一步 ➡️

现在你已经了解了为什么需要 SeerAPI，以及它能为你节省多少时间和精力。

接下来，我们将开始实际使用 SeerAPI，看看如何用几行代码就能构建出强大的功能！

让我们继续！🔥🤖👊
