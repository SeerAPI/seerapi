import json
from pathlib import Path

from seerapi_models.skill import SkillEffectParam

from solaris.analyze.analyzers.skill.effect_handlers import (
	RangeInfo,
	StatChange,
	effect_handler_21,
	effect_handler_31,
	effect_handler_41,
	effect_handler_42,
	effect_handler_174,
	effect_handler_default,
)


class TestStatChange:
	"""测试 StatChange 类的基本功能"""

	def test_default_format_value(self):
		"""测试默认格式化模式（value）"""
		# 默认 format_mode 是 'value'
		# 正数显示 +N，负数显示 -N
		sc = StatChange(atk=1, def_=-1, sp_atk=0, sp_def=0, spd=2, acc=-2)
		assert str(sc) == '攻击+1、防御-1、速度+2、命中-2'

	def test_zero_values_skipped(self):
		"""测试零值被跳过"""
		# 所有零值应该返回空字符串
		sc = StatChange(atk=0, def_=0, sp_atk=0, sp_def=0, spd=0, acc=0)
		assert str(sc) == ''

	def test_format_mode_plus(self):
		"""测试正号格式化模式"""
		# format_mode='+' -> 总是 +abs(x)
		sc = StatChange(
			atk=1, def_=-1, sp_atk=0, sp_def=0, spd=0, acc=0, format_mode='+'
		)
		# +1 -> +1, -1 -> +1
		assert str(sc) == '攻击+1、防御+1'

	def test_format_mode_minus(self):
		"""测试负号格式化模式"""
		# format_mode='-' -> 总是 -abs(x)
		sc = StatChange(
			atk=1, def_=-1, sp_atk=0, sp_def=0, spd=0, acc=0, format_mode='-'
		)
		# +1 -> -1, -1 -> -1
		assert str(sc) == '攻击-1、防御-1'

	def test_format_mode_unsigned(self):
		"""测试无符号格式化模式"""
		# format_mode='unsigned' -> abs(x)
		sc = StatChange(
			atk=1, def_=-1, sp_atk=0, sp_def=0, spd=0, acc=0, format_mode='unsigned'
		)
		assert str(sc) == '攻击1、防御1'

	def test_format_mode_none(self):
		"""测试无数字格式化模式"""
		# format_mode='none' -> 数字部分为空字符串
		sc = StatChange(
			atk=1, def_=-1, sp_atk=0, sp_def=0, spd=0, acc=0, format_mode='none'
		)
		assert str(sc) == '攻击、防御'

	def test_custom_split_char(self):
		"""测试自定义分隔符"""
		sc = StatChange(
			atk=1, def_=1, sp_atk=0, sp_def=0, spd=0, acc=0, split_char='; '
		)
		assert str(sc) == '攻击+1; 防御+1'

	def test_all_stats(self):
		"""测试所有属性都有值的情况"""
		sc = StatChange(atk=1, def_=2, sp_atk=3, sp_def=4, spd=5, acc=6)
		expected = '攻击+1、防御+2、特攻+3、特防+4、速度+5、命中+6'
		assert str(sc) == expected

	def test_negative_values(self):
		"""测试负值"""
		sc = StatChange(atk=-2, def_=-3, sp_atk=0, sp_def=0, spd=0, acc=0)
		assert str(sc) == '攻击-2、防御-3'

	def test_mixed_positive_negative(self):
		"""测试正负混合值"""
		sc = StatChange(atk=5, def_=-3, sp_atk=2, sp_def=-1, spd=0, acc=4)
		assert str(sc) == '攻击+5、防御-3、特攻+2、特防-1、命中+4'

	def test_from_num_args_single_stat(self):
		"""测试 from_num_args 方法 - 单个属性"""
		sc = StatChange.from_num_args(0, num=3)  # 0 = 攻击
		assert str(sc) == '攻击+3'

	def test_from_num_args_multiple_stats(self):
		"""测试 from_num_args 方法 - 多个属性"""
		sc = StatChange.from_num_args(0, 2, num=2)  # 0 = 攻击, 2 = 特攻
		assert str(sc) == '攻击+2、特攻+2'

	def test_from_num_args_with_format_mode(self):
		"""测试 from_num_args 方法 - 带格式化模式"""
		sc = StatChange.from_num_args(1, 3, num=1, format_mode='none', split_char='和')
		assert str(sc) == '防御和特防'

	def test_from_num_args_all_stats(self):
		"""测试 from_num_args 方法 - 所有属性"""
		sc = StatChange.from_num_args(0, 1, 2, 3, 4, 5, num=1, format_mode='unsigned')
		assert str(sc) == '攻击1、防御1、特攻1、特防1、速度1、命中1'


class TestRangeInfo:
	"""测试 RangeInfo 类"""

	def test_range_same_min_max(self):
		"""测试最小值和最大值相同的情况"""
		ri = RangeInfo(min=5, max=5)
		assert str(ri) == '5'

	def test_range_different_min_max(self):
		"""测试最小值和最大值不同的情况"""
		ri = RangeInfo(min=3, max=7)
		assert str(ri) == '3~7'

	def test_range_zero(self):
		"""测试零值范围"""
		ri = RangeInfo(min=0, max=0)
		assert str(ri) == '0'


class TestEffectHandler21:
	"""测试 effect_handler_21 函数"""

	def test_basic_range_creation(self):
		"""测试基本范围创建"""
		effect_args = [3, 7, 2]
		info_args: list[int | object | str | None] = [None, None, None]
		result = effect_handler_21(effect_args, info_args)

		assert isinstance(result[0], RangeInfo)
		assert str(result[0]) == '3~7'
		assert result[1] is None
		assert result[2] is None

	def test_same_min_max(self):
		"""测试最小值和最大值相同"""
		effect_args = [5, 5, 10]
		info_args: list[int | object | str | None] = [None, None, None]
		result = effect_handler_21(effect_args, info_args)

		assert str(result[0]) == '5'


class TestEffectHandler31:
	"""测试 effect_handler_31 函数"""

	def test_basic_range_creation(self):
		"""测试基本范围创建"""
		effect_args = [2, 4]
		info_args: list[int | object | str | None] = [None, None]
		result = effect_handler_31(effect_args, info_args)

		assert isinstance(result[0], RangeInfo)
		assert str(result[0]) == '2~4'

	def test_single_value(self):
		"""测试单一值"""
		effect_args = [1, 1]
		info_args: list[int | object | str | None] = [None, None]
		result = effect_handler_31(effect_args, info_args)

		assert str(result[0]) == '1'


class TestEffectHandler41:
	"""测试 effect_handler_41 函数"""

	def test_basic_range_creation(self):
		"""测试基本范围创建"""
		effect_args = [1, 3]
		info_args: list[int | object | str | None] = [None, None]
		result = effect_handler_41(effect_args, info_args)

		assert isinstance(result[0], RangeInfo)
		assert str(result[0]) == '1~3'


class TestEffectHandler42:
	"""测试 effect_handler_42 函数"""

	def test_basic_range_creation(self):
		"""测试基本范围创建"""
		effect_args = [2, 5]
		info_args: list[int | object | str | None] = [None, None]
		result = effect_handler_42(effect_args, info_args)

		assert isinstance(result[0], RangeInfo)
		assert str(result[0]) == '2~5'


class TestEffectHandler174:
	"""测试 effect_handler_174 函数"""

	def test_single_stat(self):
		"""测试单个属性提升"""
		effect_args = [0, 0, -1, 50, 2]  # 提升攻击等级+2
		info_args: list[int | object | str | None] = [None, None, None, None, None]
		result = effect_handler_174(effect_args, info_args)

		assert isinstance(result[1], StatChange)
		assert str(result[1]) == '攻击'

	def test_two_stats(self):
		"""测试两个属性提升"""
		effect_args = [0, 0, 2, 50, 1]  # 提升攻击和特攻
		info_args: list[int | object | str | None] = [None, None, None, None, None]
		result = effect_handler_174(effect_args, info_args)

		assert isinstance(result[1], StatChange)
		assert str(result[1]) == '攻击和特攻'

	def test_defense_and_sp_def(self):
		"""测试防御和特防提升"""
		effect_args = [0, 1, 3, 100, 3]  # 提升防御和特防
		info_args: list[int | object | str | None] = [None, None, None, None, None]
		result = effect_handler_174(effect_args, info_args)

		assert str(result[1]) == '防御和特防'


class TestEffectStringFormatting:
	"""测试效果描述字符串格式化功能"""

	def load_effect_info(self):
		"""加载效果信息JSON文件"""
		json_path = Path(__file__).parent / 'effect_info.json'
		with open(json_path, encoding='utf-8') as f:
			return json.load(f)

	def format_description(self, template: str, info_args: list) -> str:
		"""根据模板和参数生成最终描述字符串"""
		result = template.format(*info_args)
		return result

	def test_effect_21_formatting(self):
		"""测试效果21的完整格式化：作用{0}回合，每回合反弹对手1/{2}的伤害"""
		effect_info = self.load_effect_info()
		effect_21 = next(e for e in effect_info if e['id'] == 21)

		# 效果参数：最小回合3，最大回合7，反弹比例2
		effect_args = [3, 7, 2]

		# 处理参数
		result = effect_handler_21(effect_args, list(effect_args))

		# 格式化描述
		description = self.format_description(effect_21['info'], result)

		assert description == '作用3~7回合，每回合反弹对手1/2的伤害'

	def test_effect_21_formatting_same_rounds(self):
		"""测试效果21当最小和最大回合相同时的格式化"""
		effect_info = self.load_effect_info()
		effect_21 = next(e for e in effect_info if e['id'] == 21)

		# 效果参数：最小回合5，最大回合5，反弹比例3
		effect_args = [5, 5, 3]

		# 处理参数
		result = effect_handler_21(effect_args, list(effect_args))

		# 格式化描述
		description = self.format_description(effect_21['info'], result)

		assert description == '作用5回合，每回合反弹对手1/3的伤害'

	def test_effect_31_formatting(self):
		"""测试效果31的完整格式化：1回合做{0}次攻击"""
		effect_info = self.load_effect_info()
		effect_31 = next(e for e in effect_info if e['id'] == 31)

		# 效果参数：最小次数2，最大次数4
		effect_args = [2, 4]

		# 处理参数
		result = effect_handler_31(effect_args, list(effect_args))

		# 格式化描述
		description = self.format_description(effect_31['info'], result)

		assert description == '1回合做2~4次攻击'

	def test_effect_41_formatting(self):
		"""测试效果41的完整格式化：{0}回合本方受到的火系攻击伤害减半"""
		effect_info = self.load_effect_info()
		effect_41 = next(e for e in effect_info if e['id'] == 41)

		# 效果参数：最小回合1，最大回合3
		effect_args = [1, 3]

		# 处理参数
		result = effect_handler_41(effect_args, list(effect_args))

		# 格式化描述
		description = self.format_description(effect_41['info'], result)

		assert description == '1~3回合本方受到的火系攻击伤害减半'

	def test_effect_42_formatting(self):
		"""测试效果42的完整格式化：{0}回合自己使用电招式伤害×2"""
		effect_info = self.load_effect_info()
		effect_42 = next(e for e in effect_info if e['id'] == 42)

		# 效果参数：最小回合2，最大回合5
		effect_args = [2, 5]

		# 处理参数
		result = effect_handler_42(effect_args, list(effect_args))

		# 格式化描述
		description = self.format_description(effect_42['info'], result)

		assert description == '2~5回合自己使用电招式伤害×2'

	def test_effect_174_formatting_single_stat(self):
		"""测试效果174的完整格式化：{0}回合内，若对手使用属性攻击则{3}%自身{1}等级+{4}"""
		effect_info = self.load_effect_info()
		effect_174 = next(e for e in effect_info if e['id'] == 174)

		# 效果参数：回合数范围[0,0]，属性为攻击(0)，无第二属性(-1)，触发概率50%，等级+2
		effect_args = [0, 0, -1, 50, 2]

		# 处理参数
		result = effect_handler_174(effect_args, list(effect_args))

		# 格式化描述（注意：result[0]是回合数范围，result[1]是属性变化）
		# 对于回合数，我们需要手动处理
		result[0] = RangeInfo(effect_args[0], effect_args[0])
		description = self.format_description(effect_174['info'], result)

		assert description == '0回合内，若对手使用属性攻击则50%自身攻击等级+2'

	def test_effect_174_formatting_two_stats(self):
		"""测试效果174的完整格式化：两个属性提升"""
		effect_info = self.load_effect_info()
		effect_174 = next(e for e in effect_info if e['id'] == 174)

		# 效果参数：回合数范围[0,0]，第一属性为攻击(0)，第二属性为特攻(2)，触发概率50%，等级+1
		effect_args = [0, 0, 2, 50, 1]

		# 处理参数
		result = effect_handler_174(effect_args, list(effect_args))

		# 补充回合数范围
		result[0] = RangeInfo(effect_args[0], effect_args[0])
		description = self.format_description(effect_174['info'], result)

		assert description == '0回合内，若对手使用属性攻击则50%自身攻击和特攻等级+1'


class TestEffectHandlerDefault:
	"""测试 effect_handler_default 函数"""

	def test_stat_change_param_id_0(self):
		"""测试 StatChange 参数（param_id=0）"""
		effect_args = [1, -1, 2, -2, 3, -3, 100]
		info_args: list[int | object | str | None] = [None] * 7
		param = SkillEffectParam(id=0, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert isinstance(result[0], StatChange)
		assert str(result[0]) == '攻击+1，防御-1，特攻+2，特防-2，速度+3，命中-3'
		# 后续5个位置应该是 None
		assert result[1] is None
		assert result[2] is None

	def test_stat_change_param_id_16(self):
		"""测试 StatChange 参数（param_id=16，format_mode='none'）"""
		effect_args = [1, 1, 0, 0, 0, 0]
		info_args: list[int | object | str | None] = [None] * 6
		param = SkillEffectParam(id=16, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert isinstance(result[0], StatChange)
		assert str(result[0]) == '攻击、防御'

	def test_stat_change_param_id_24(self):
		"""测试 StatChange 参数（param_id=24，format_mode='-'）"""
		effect_args = [2, 2, 0, 0, 0, 0]
		info_args: list[int | object | str | None] = [None] * 6
		param = SkillEffectParam(id=24, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert isinstance(result[0], StatChange)
		assert str(result[0]) == '攻击-2，防御-2'

	def test_param_id_14_positive(self):
		"""测试 param_id=14（特殊格式化）- 正数"""
		effect_args = [5, 10]
		info_args: list[int | object | str | None] = [None, None]
		param = SkillEffectParam(id=14, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert result[0] == '+5'

	def test_param_id_14_negative(self):
		"""测试 param_id=14（特殊格式化）- 负数"""
		effect_args = [-3, 10]
		info_args: list[int | object | str | None] = [None, None]
		param = SkillEffectParam(id=14, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert result[0] == '-3'

	def test_param_id_22_type_combination(self):
		"""测试 param_id=22（属性组合映射）"""
		effect_args = [5, 10]
		info_args: list[int | object | str | None] = [None, None]
		param = SkillEffectParam(id=22, infos=None)
		type_combination_map = {5: '火系', 10: '水系'}

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map=type_combination_map
		)

		assert result[0] == '火系'

	def test_param_with_infos(self):
		"""测试带有预定义描述信息的参数"""
		effect_args = [1, 2]
		info_args: list[int | object | str | None] = [None, None]
		param = SkillEffectParam(id=99, infos=['零', '一', '二', '三'])

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		assert result[0] == '一'

	def test_param_with_infos_second_position(self):
		"""测试在第二个位置使用预定义描述信息"""
		effect_args = [10, 2, 20]
		info_args: list[int | object | str | None] = [None, None, None]
		param = SkillEffectParam(id=99, infos=['状态A', '状态B', '状态C'])

		result = effect_handler_default(
			effect_args, param, 1, info_args, type_combination_map={}
		)

		assert result[0] is None
		assert result[1] == '状态C'
		assert result[2] is None

	def test_stat_change_at_different_position(self):
		"""测试在不同位置的 StatChange"""
		effect_args = [100, 1, -1, 0, 0, 0, 0, 200]
		info_args: list[int | object | str | None] = [None] * 8
		param = SkillEffectParam(id=0, infos=None)

		result = effect_handler_default(
			effect_args, param, 1, info_args, type_combination_map={}
		)

		assert result[0] is None
		assert isinstance(result[1], StatChange)
		assert str(result[1]) == '攻击+1，防御-1'
		assert result[7] is None

	def test_no_special_handling(self):
		"""测试没有特殊处理的普通参数"""
		effect_args = [42, 99]
		info_args: list[int | object | str | None] = [None, None]
		param = SkillEffectParam(id=999, infos=None)

		result = effect_handler_default(
			effect_args, param, 0, info_args, type_combination_map={}
		)

		# 没有特殊处理，info_args 应该保持不变
		assert result[0] is None
		assert result[1] is None
