from collections.abc import Callable
from dataclasses import KW_ONLY, dataclass
from typing import Literal, TypeAlias

from seerapi_models.skill import SkillEffectParam

FormatMode: TypeAlias = Literal['+', '-', 'unsigned', 'value', 'none']


STAT_CHANGE_KWARGS_MAP = {
	0: {
		'split_char': '，',
	},
	16: {
		'format_mode': 'none',
		'split_char': '、',
	},
	24: {
		'format_mode': '-',
		'split_char': '，',
	},
}


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
	format_mode: FormatMode = 'value'
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

	@classmethod
	def from_num_args(
		cls,
		*args: int,
		num: int,
		format_mode: FormatMode = 'value',
		split_char: str = '、',
	) -> 'StatChange':
		array = [0] * 6
		for i in args:
			array[i] = num

		return cls(*array, format_mode=format_mode, split_char=split_char)


@dataclass
class RangeInfo:
	min: int
	max: int

	def __str__(self) -> str:
		if self.min == self.max:
			return f'{self.min}'
		return f'{self.min}~{self.max}'


InfoArgs: TypeAlias = list[int | object | str | None]
EffectArgs: TypeAlias = list[int]
InfoHandler: TypeAlias = Callable[[EffectArgs, InfoArgs], InfoArgs]


def effect_handler_21(effect_args: EffectArgs, info_args: InfoArgs) -> InfoArgs:
	range_info = RangeInfo(effect_args[0], effect_args[1])
	info_args[0] = range_info
	return info_args


def effect_handler_31(effect_args: EffectArgs, info_args: InfoArgs) -> InfoArgs:
	range_info = RangeInfo(effect_args[0], effect_args[1])
	info_args[0] = range_info
	return info_args


def effect_handler_41(effect_args: EffectArgs, info_args: InfoArgs) -> InfoArgs:
	range_info = RangeInfo(effect_args[0], effect_args[1])
	info_args[0] = range_info
	return info_args


def effect_handler_42(effect_args: EffectArgs, info_args: InfoArgs) -> InfoArgs:
	range_info = RangeInfo(effect_args[0], effect_args[1])
	info_args[0] = range_info
	return info_args


def effect_handler_174(effect_args: EffectArgs, info_args: InfoArgs) -> InfoArgs:
	num = effect_args[4]
	stat_args = [effect_args[1]]
	if effect_args[2] != -1:
		stat_args.append(effect_args[2])
	stat_change = StatChange.from_num_args(
		*stat_args,
		num=num,
		format_mode='none',
		split_char='和',
	)
	info_args[1] = stat_change
	return info_args


def effect_handler_default(
	effect_args: EffectArgs,
	param: SkillEffectParam,
	param_position: int,
	info_args: InfoArgs,
	*,
	type_combination_map: dict[int, str],
) -> InfoArgs:
	param_id = param.id
	kwargs = STAT_CHANGE_KWARGS_MAP.get(param_id, {})
	# param_id为16, 24表示这是一个StatChange（状态变化）参数
	if param_id in (0, 16, 24) and len(effect_args) >= 6:
		# 将6个参数合并为一个StatChange对象
		slice_ = slice(param_position, param_position + 6)
		info_args[slice_] = [StatChange(*effect_args[slice_], **kwargs)] + [None] * 5
		# 由于状态变化占用6个参数位置，所以填充5个None
	# 特别处理id为14的参数
	elif param_id == 14:
		info_args[param_position] = f'{effect_args[param_position]:+d}'
	elif param_id == 22:
		type_combination_id = effect_args[param_position]
		info_args[param_position] = type_combination_map[type_combination_id]
	# 如果参数有预定义的描述信息(param.infos)
	elif isinstance(param_infos := param.infos, list):
		pos = effect_args[param_position]
		try:
			# 使用参数值作为索引，在infos中查找对应的描述文本并使用
			info_args[param_position] = param_infos[pos]
		except IndexError:
			info_args[param_position] = pos

	return info_args


InfoHandlerMap: TypeAlias = dict[int, InfoHandler]


INFO_HANDLER_MAP: InfoHandlerMap = {
	21: effect_handler_21,
	31: effect_handler_31,
	41: effect_handler_41,
	42: effect_handler_42,
	174: effect_handler_174,
}
