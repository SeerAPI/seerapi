"""
itemsOptimizeCat 相关解析器模块

此模块包含赛尔号道具配置的解析器，包括：
- 道具类别解析器 (itemsOptimizeCat)
- 各个道具类别项解析器 (itemsOptimizeCatItems0-26)

每个解析器都遵循标准的 BaseParser 接口，支持从 .bytes 文件解析数据到 JSON 格式。
"""

from .items_optimize_cat import ItemsOptimizeCatParser
from .parsers_0_to_9 import (
	Item0,
	Item1,
	Item2,
	Item3,
	Item4,
	Item5,
	Item6,
	Item7,
	Item8,
	Item9,
	ItemsOptimizeCatItems0Parser,
	ItemsOptimizeCatItems1Parser,
	ItemsOptimizeCatItems2Parser,
	ItemsOptimizeCatItems3Parser,
	ItemsOptimizeCatItems4Parser,
	ItemsOptimizeCatItems5Parser,
	ItemsOptimizeCatItems6Parser,
	ItemsOptimizeCatItems7Parser,
	ItemsOptimizeCatItems8Parser,
	ItemsOptimizeCatItems9Parser,
)
from .parsers_10_to_19 import (
	Item10,
	Item11,
	Item12,
	Item13,
	Item14,
	Item15,
	Item16,
	Item17,
	Item18,
	Item19,
	ItemsOptimizeCatItems10Parser,
	ItemsOptimizeCatItems11Parser,
	ItemsOptimizeCatItems12Parser,
	ItemsOptimizeCatItems13Parser,
	ItemsOptimizeCatItems14Parser,
	ItemsOptimizeCatItems15Parser,
	ItemsOptimizeCatItems16Parser,
	ItemsOptimizeCatItems17Parser,
	ItemsOptimizeCatItems18Parser,
	ItemsOptimizeCatItems19Parser,
)
from .parsers_21_to_26 import (
	Item20,
	Item21,
	Item22,
	Item23,
	Item24,
	Item25,
	Item26,
	ItemsOptimizeCatItems20Parser,
	ItemsOptimizeCatItems21Parser,
	ItemsOptimizeCatItems22Parser,
	ItemsOptimizeCatItems23Parser,
	ItemsOptimizeCatItems24Parser,
	ItemsOptimizeCatItems25Parser,
	ItemsOptimizeCatItems26Parser,
)

__all__ = [
	# 道具类别0-9
	'Item0',
	'Item1',
	'Item2',
	'Item3',
	'Item4',
	'Item5',
	'Item6',
	'Item7',
	'Item8',
	'Item9',
	# 道具类别10-19
	'Item10',
	'Item11',
	'Item12',
	'Item13',
	'Item14',
	'Item15',
	'Item16',
	'Item17',
	'Item18',
	'Item19',
	# 道具类别20-26
	'Item20',
	'Item21',
	'Item22',
	'Item23',
	'Item24',
	'Item25',
	'Item26',
	# 道具类别解析器
	'ItemsOptimizeCatItems0Parser',
	'ItemsOptimizeCatItems1Parser',
	'ItemsOptimizeCatItems2Parser',
	'ItemsOptimizeCatItems3Parser',
	'ItemsOptimizeCatItems4Parser',
	'ItemsOptimizeCatItems5Parser',
	'ItemsOptimizeCatItems6Parser',
	'ItemsOptimizeCatItems7Parser',
	'ItemsOptimizeCatItems8Parser',
	'ItemsOptimizeCatItems9Parser',
	'ItemsOptimizeCatItems10Parser',
	'ItemsOptimizeCatItems11Parser',
	'ItemsOptimizeCatItems12Parser',
	'ItemsOptimizeCatItems13Parser',
	'ItemsOptimizeCatItems14Parser',
	'ItemsOptimizeCatItems15Parser',
	'ItemsOptimizeCatItems16Parser',
	'ItemsOptimizeCatItems17Parser',
	'ItemsOptimizeCatItems18Parser',
	'ItemsOptimizeCatItems19Parser',
	'ItemsOptimizeCatItems20Parser',
	'ItemsOptimizeCatItems21Parser',
	'ItemsOptimizeCatItems22Parser',
	'ItemsOptimizeCatItems23Parser',
	'ItemsOptimizeCatItems24Parser',
	'ItemsOptimizeCatItems25Parser',
	'ItemsOptimizeCatItems26Parser',
	# 道具类别解析器
	'ItemsOptimizeCatParser',
]


# 解析器映射字典，用于动态查找
PARSERS = {
	'itemsOptimizeCat': ItemsOptimizeCatParser,
	'itemsOptimizeCatItems0': ItemsOptimizeCatItems0Parser,
	'itemsOptimizeCatItems1': ItemsOptimizeCatItems1Parser,
	'itemsOptimizeCatItems2': ItemsOptimizeCatItems2Parser,
	'itemsOptimizeCatItems3': ItemsOptimizeCatItems3Parser,
	'itemsOptimizeCatItems4': ItemsOptimizeCatItems4Parser,
	'itemsOptimizeCatItems5': ItemsOptimizeCatItems5Parser,
	'itemsOptimizeCatItems6': ItemsOptimizeCatItems6Parser,
	'itemsOptimizeCatItems7': ItemsOptimizeCatItems7Parser,
	'itemsOptimizeCatItems8': ItemsOptimizeCatItems8Parser,
	'itemsOptimizeCatItems9': ItemsOptimizeCatItems9Parser,
	'itemsOptimizeCatItems10': ItemsOptimizeCatItems10Parser,
	'itemsOptimizeCatItems11': ItemsOptimizeCatItems11Parser,
	'itemsOptimizeCatItems12': ItemsOptimizeCatItems12Parser,
	'itemsOptimizeCatItems13': ItemsOptimizeCatItems13Parser,
	'itemsOptimizeCatItems14': ItemsOptimizeCatItems14Parser,
	'itemsOptimizeCatItems15': ItemsOptimizeCatItems15Parser,
	'itemsOptimizeCatItems16': ItemsOptimizeCatItems16Parser,
	'itemsOptimizeCatItems17': ItemsOptimizeCatItems17Parser,
	'itemsOptimizeCatItems18': ItemsOptimizeCatItems18Parser,
	'itemsOptimizeCatItems19': ItemsOptimizeCatItems19Parser,
	'itemsOptimizeCatItems20': ItemsOptimizeCatItems20Parser,
	'itemsOptimizeCatItems21': ItemsOptimizeCatItems21Parser,
	'itemsOptimizeCatItems22': ItemsOptimizeCatItems22Parser,
	'itemsOptimizeCatItems23': ItemsOptimizeCatItems23Parser,
	'itemsOptimizeCatItems24': ItemsOptimizeCatItems24Parser,
	'itemsOptimizeCatItems25': ItemsOptimizeCatItems25Parser,
	'itemsOptimizeCatItems26': ItemsOptimizeCatItems26Parser,
}


def get_parser_by_filename(filename: str):
	"""
	根据配置文件名获取对应的解析器类

	Args:
		filename: 配置文件名（不含扩展名）

	Returns:
		对应的解析器类，如果未找到则返回 None
	"""
	return PARSERS.get(filename)
