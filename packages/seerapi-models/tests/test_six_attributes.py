"""测试 SixAttributesBase 类的方法"""

import pytest

from seerapi_models.common import SixAttributes


class TestFromString:
    """测试 from_string 类方法"""

    def test_from_string_basic(self):
        """测试基本字符串解析"""
        obj = SixAttributes.from_string('10 20 30 40 50 60')
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50
        assert obj.hp == 60
        assert obj.percent is False

    def test_from_string_with_percent(self):
        """测试带百分比标志的字符串解析"""
        obj = SixAttributes.from_string('5 10 15 20 25 30', percent=True)
        assert obj.atk == 5
        assert obj.def_ == 10
        assert obj.sp_atk == 15
        assert obj.sp_def == 20
        assert obj.spd == 25
        assert obj.hp == 30
        assert obj.percent is True

    def test_from_string_hp_first(self):
        """测试 hp 在首位的字符串解析"""
        obj = SixAttributes.from_string('100 10 20 30 40 50', hp_first=True)
        assert obj.hp == 100
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50

    def test_from_string_hp_first_with_percent(self):
        """测试 hp 在首位且带百分比标志的字符串解析"""
        obj = SixAttributes.from_string('50 5 10 15 20 25', hp_first=True, percent=True)
        assert obj.hp == 50
        assert obj.atk == 5
        assert obj.def_ == 10
        assert obj.sp_atk == 15
        assert obj.sp_def == 20
        assert obj.spd == 25
        assert obj.percent is True

    def test_from_string_with_extra_values(self):
        """测试包含多余值的字符串（应只取前6个）"""
        obj = SixAttributes.from_string('10 20 30 40 50 60 70 80 90')
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50
        assert obj.hp == 60

    def test_from_string_insufficient_values(self):
        """测试值不足的字符串（应抛出 ValueError）"""
        with pytest.raises(ValueError, match='无效的属性字符串'):
            SixAttributes.from_string('10 20 30')

    def test_from_string_empty(self):
        """测试空字符串（应抛出 ValueError）"""
        with pytest.raises(ValueError, match='无效的属性字符串'):
            SixAttributes.from_string('')

    def test_from_string_invalid_format(self):
        """测试无效格式的字符串（应抛出 ValueError）"""
        with pytest.raises(ValueError):
            SixAttributes.from_string('a b c d e f')

    def test_from_string_with_zeros(self):
        """测试全零值"""
        obj = SixAttributes.from_string('0 0 0 0 0 0')
        assert obj.atk == 0
        assert obj.def_ == 0
        assert obj.sp_atk == 0
        assert obj.sp_def == 0
        assert obj.spd == 0
        assert obj.hp == 0


class TestFromList:
    """测试 from_list 类方法"""

    def test_from_list_basic(self):
        """测试基本列表解析"""
        obj = SixAttributes.from_list([10, 20, 30, 40, 50, 60])
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50
        assert obj.hp == 60
        assert obj.percent is False

    def test_from_list_with_percent(self):
        """测试带百分比标志的列表解析"""
        obj = SixAttributes.from_list([5, 10, 15, 20, 25, 30], percent=True)
        assert obj.atk == 5
        assert obj.def_ == 10
        assert obj.sp_atk == 15
        assert obj.sp_def == 20
        assert obj.spd == 25
        assert obj.hp == 30
        assert obj.percent is True

    def test_from_list_hp_first(self):
        """测试 hp 在首位的列表解析"""
        obj = SixAttributes.from_list([100, 10, 20, 30, 40, 50], hp_first=True)
        assert obj.hp == 100
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50

    def test_from_list_hp_first_with_percent(self):
        """测试 hp 在首位且带百分比标志的列表解析"""
        obj = SixAttributes.from_list(
            [50, 5, 10, 15, 20, 25], hp_first=True, percent=True
        )
        assert obj.hp == 50
        assert obj.atk == 5
        assert obj.def_ == 10
        assert obj.sp_atk == 15
        assert obj.sp_def == 20
        assert obj.spd == 25
        assert obj.percent is True

    def test_from_list_with_extra_values(self):
        """测试包含多余值的列表（应只取前6个）"""
        obj = SixAttributes.from_list([10, 20, 30, 40, 50, 60, 70, 80])
        assert obj.atk == 10
        assert obj.def_ == 20
        assert obj.sp_atk == 30
        assert obj.sp_def == 40
        assert obj.spd == 50
        assert obj.hp == 60

    def test_from_list_insufficient_values(self):
        """测试值不足的列表（应抛出 ValueError）"""
        with pytest.raises(ValueError, match='无效的属性列表'):
            SixAttributes.from_list([10, 20, 30])

    def test_from_list_empty(self):
        """测试空列表（应抛出 ValueError）"""
        with pytest.raises(ValueError, match='无效的属性列表'):
            SixAttributes.from_list([])

    def test_from_list_modifies_original(self):
        """测试 hp_first 模式是否会修改原始列表"""
        original = [100, 10, 20, 30, 40, 50]
        obj = SixAttributes.from_list(original, hp_first=True)
        # 原始列表应该被修改（因为使用了 move_to_last）
        assert original == [10, 20, 30, 40, 50, 100]
        assert obj.hp == 100


class TestAddOperation:
    """测试加法运算符重载"""

    def test_add_normal_attributes(self):
        """测试普通属性相加"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 + obj2
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90
        assert result.percent is False

    def test_add_percent_attributes(self):
        """测试两个百分比属性相加"""
        obj1 = SixAttributes(
            atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60, percent=True
        )
        obj2 = SixAttributes(
            atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30, percent=True
        )
        result = obj1 + obj2
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90
        assert result.percent is True

    def test_add_percent_to_normal(self):
        """测试百分比属性与普通属性相加（百分比乘法）"""
        obj1 = SixAttributes(atk=100, def_=200, sp_atk=300, sp_def=400, spd=500, hp=600)
        obj2 = SixAttributes(
            atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60, percent=True
        )
        result = obj1 + obj2
        result = result.round()
        assert result.atk == 110  # 100 * 1 + (10 / 100).
        assert result.def_ == 240  # 200 * 1 + (20 / 100).
        assert result.sp_atk == 390  # 300 * 1 + (30 / 100).
        assert result.sp_def == 560  # 400 * 1 + (40 / 100).
        assert result.spd == 750  # 500 * 1 + (50 / 100).
        assert result.hp == 960  # 600 * 1 + (60 / 100).
        assert result.percent is False

    def test_add_normal_to_percent(self):
        """测试普通属性与百分比属性相加（百分比乘法）"""
        obj1 = SixAttributes(
            atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60, percent=True
        )
        obj2 = SixAttributes(atk=100, def_=200, sp_atk=300, sp_def=400, spd=500, hp=600)
        result = obj1 + obj2
        result = result.round()
        assert result.atk == 110  # 100 * (1 + 10 / 100).
        assert result.def_ == 240  # 200 * (1 + 20 / 100).
        assert result.sp_atk == 390  # 300 * (1 + 30 / 100).
        assert result.sp_def == 560  # 400 * (1 + 40 / 100).
        assert result.spd == 750  # 500 * (1 + 50 / 100).
        assert result.hp == 960  # 600 * (1 + 60 / 100).
        assert result.percent is False

    def test_add_with_zeros(self):
        """测试与零值相加"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=0, def_=0, sp_atk=0, sp_def=0, spd=0, hp=0)
        result = obj1 + obj2
        assert result.atk == 10
        assert result.def_ == 20
        assert result.sp_atk == 30
        assert result.sp_def == 40
        assert result.spd == 50
        assert result.hp == 60

    def test_add_type_error(self):
        """测试类型不匹配时抛出 TypeError"""
        obj = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        with pytest.raises(TypeError, match='Cannot add'):
            _ = obj + 10

    def test_add_preserves_original(self):
        """测试加法不修改原始对象"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 + obj2
        assert obj1.atk == 10
        assert obj2.atk == 5
        assert result.atk == 15


class TestSubOperation:
    """测试减法运算符重载"""

    def test_sub_normal_attributes(self):
        """测试普通属性相减"""
        obj1 = SixAttributes(atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 - obj2
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90
        assert result.percent is False

    def test_sub_percent_from_percent(self):
        """测试两个百分比属性相减"""
        obj1 = SixAttributes(
            atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120, percent=True
        )
        obj2 = SixAttributes(
            atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30, percent=True
        )
        result = obj1 - obj2
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90
        assert result.percent is True

    def test_sub_normal_from_percent(self):
        """测试从百分比属性减去普通属性"""
        obj1 = SixAttributes(
            atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120, percent=True
        )
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 - obj2
        result = result.round()
        assert result.atk == 4  # 5 * (1 - 20 / 100).
        assert result.def_ == 6  # 10 * (1 - 40 / 100).
        assert result.sp_atk == 6  # 15 * (1 - 60 / 100).
        assert result.sp_def == 4  # 20 * (1 - 80 / 100).
        assert result.spd == 0  # 25 * (1 - 100 / 100).
        assert result.hp == -6  # 30 * (1 - 120 / 100).
        assert result.percent is False

    def test_sub_percent_from_normal(self):
        """测试从普通属性减去百分比属性"""
        obj1 = SixAttributes(atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120)
        obj2 = SixAttributes(
            atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30, percent=True
        )
        result = obj1 - obj2
        result = result.round()
        assert result.atk == 19  # 20 * (1 - 5 / 100).
        assert result.def_ == 36  # 40 * (1 - 10 / 100).
        assert result.sp_atk == 51  # 60 * (1 - 15 / 100).
        assert result.sp_def == 64  # 80 * (1 - 20 / 100).
        assert result.spd == 75  # 100 * (1 - 25 / 100).
        assert result.hp == 84  # 120 * (1 - 30 / 100).
        assert result.percent is False

    def test_sub_with_zeros(self):
        """测试减去零值"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=0, def_=0, sp_atk=0, sp_def=0, spd=0, hp=0)
        result = obj1 - obj2
        assert result.atk == 10
        assert result.def_ == 20
        assert result.sp_atk == 30
        assert result.sp_def == 40
        assert result.spd == 50
        assert result.hp == 60

    def test_sub_negative_result(self):
        """测试减法产生负数结果"""
        obj1 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        obj2 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        result = obj1 - obj2
        assert result.atk == -5
        assert result.def_ == -10
        assert result.sp_atk == -15
        assert result.sp_def == -20
        assert result.spd == -25
        assert result.hp == -30

    def test_sub_type_error(self):
        """测试类型不匹配时抛出 TypeError"""
        obj = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        with pytest.raises(TypeError, match='Cannot sub'):
            _ = obj - 10

    def test_sub_preserves_original(self):
        """测试减法不修改原始对象"""
        obj1 = SixAttributes(atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 - obj2
        assert obj1.atk == 20
        assert obj2.atk == 5
        assert result.atk == 15


class TestCalcNumber:
    """测试 _calc_number 内部方法"""

    def test_calc_add(self):
        """测试加法运算"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1._calc_number(obj2, operator='add').round()
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90

    def test_calc_sub(self):
        """测试减法运算"""
        obj1 = SixAttributes(atk=20, def_=40, sp_atk=60, sp_def=80, spd=100, hp=120)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1._calc_number(obj2, operator='sub')
        assert result.atk == 15
        assert result.def_ == 30
        assert result.sp_atk == 45
        assert result.sp_def == 60
        assert result.spd == 75
        assert result.hp == 90

    def test_calc_percent_mul(self):
        """测试百分比乘法运算"""
        obj1 = SixAttributes(atk=100, def_=200, sp_atk=300, sp_def=400, spd=500, hp=600)
        obj2 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        result = obj1._calc_number(obj2, operator='percent_mul').round()
        assert result.atk == 110  # 100 * (1 + 10 / 100).
        assert result.def_ == 240  # 200 * (1 + 20 / 100).
        assert result.sp_atk == 390  # 300 * (1 + 30 / 100).
        assert result.sp_def == 560  # 400 * (1 + 40 / 100).
        assert result.spd == 750  # 500 * (1 + 50 / 100).
        assert result.hp == 960  # 600 * (1 + 60 / 100).

    def test_calc_percent_div(self):
        """测试百分比除法运算"""
        obj1 = SixAttributes(
            atk=1000, def_=2000, sp_atk=3000, sp_def=4000, spd=5000, hp=6000
        )
        obj2 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        result = obj1._calc_number(obj2, operator='percent_div').round()
        assert result.atk == 900  # 1000 * (1 - 10 / 100).
        assert result.def_ == 1600  # 2000 * (1 - 20 / 100).
        assert result.sp_atk == 2100  # 3000 * (1 - 30 / 100).
        assert result.sp_def == 2400  # 4000 * (1 - 40 / 100).
        assert result.spd == 2500  # 5000 * (1 - 50 / 100).
        assert result.hp == 2400  # 6000 * (1 - 60 / 100).


class TestRound:
    """测试 round 方法"""

    def test_round_default(self):
        """测试默认舍入（到整数）"""
        obj = SixAttributes(
            atk=10.4, def_=20.6, sp_atk=30.5, sp_def=40.1, spd=50.9, hp=60.3
        )
        result = obj.round()
        assert result.atk == 10
        assert result.def_ == 21
        assert result.sp_atk == 30  # Python 的 round 使用银行家舍入法
        assert result.sp_def == 40
        assert result.spd == 51
        assert result.hp == 60

    def test_round_to_one_decimal(self):
        """测试舍入到一位小数"""
        obj = SixAttributes(
            atk=10.46, def_=20.67, sp_atk=30.52, sp_def=40.18, spd=50.94, hp=60.33
        )
        result = obj.round(1)
        assert result.atk == 10.5
        assert result.def_ == 20.7
        assert result.sp_atk == 30.5
        assert result.sp_def == 40.2
        assert result.spd == 50.9
        assert result.hp == 60.3

    def test_round_to_two_decimals(self):
        """测试舍入到两位小数"""
        obj = SixAttributes(
            atk=10.456, def_=20.678, sp_atk=30.523, sp_def=40.189, spd=50.945, hp=60.331
        )
        result = obj.round(2)
        assert result.atk == 10.46
        assert result.def_ == 20.68
        assert result.sp_atk == 30.52
        assert result.sp_def == 40.19
        assert result.spd == 50.95
        assert result.hp == 60.33

    def test_round_preserves_percent_flag(self):
        """测试舍入保持 percent 标志"""
        obj = SixAttributes(
            atk=10.7,
            def_=20.3,
            sp_atk=30.5,
            sp_def=40.9,
            spd=50.1,
            hp=60.6,
            percent=True,
        )
        result = obj.round()
        assert result.atk == 11
        assert result.def_ == 20
        assert result.sp_atk == 30
        assert result.sp_def == 41
        assert result.spd == 50
        assert result.hp == 61
        assert result.percent is True

    def test_round_negative_values(self):
        """测试负数的舍入"""
        obj = SixAttributes(
            atk=-10.4, def_=-20.6, sp_atk=-30.5, sp_def=-40.1, spd=-50.9, hp=-60.3
        )
        result = obj.round()
        assert result.atk == -10
        assert result.def_ == -21
        assert result.sp_atk == -30
        assert result.sp_def == -40
        assert result.spd == -51
        assert result.hp == -60

    def test_round_already_integers(self):
        """测试已经是整数的值"""
        obj = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        result = obj.round()
        assert result.atk == 10
        assert result.def_ == 20
        assert result.sp_atk == 30
        assert result.sp_def == 40
        assert result.spd == 50
        assert result.hp == 60

    def test_round_zero_values(self):
        """测试零值的舍入"""
        obj = SixAttributes(atk=0.4, def_=0.6, sp_atk=0.5, sp_def=0.1, spd=0.9, hp=0.3)
        result = obj.round()
        assert result.atk == 0
        assert result.def_ == 1
        assert result.sp_atk == 0
        assert result.sp_def == 0
        assert result.spd == 1
        assert result.hp == 0

    def test_round_after_calculation(self):
        """测试计算后的舍入"""
        obj1 = SixAttributes(atk=100, def_=200, sp_atk=300, sp_def=400, spd=500, hp=600)
        obj2 = SixAttributes(
            atk=15, def_=15, sp_atk=15, sp_def=15, spd=15, hp=15, percent=True
        )
        result = obj1 + obj2  # 结果会有小数
        result = result.round()
        assert result.atk == 115  # 100 * 1.15 = 115.0
        assert result.def_ == 230  # 200 * 1.15 = 230.0
        assert result.sp_atk == 345  # 300 * 1.15 = 345.0
        assert result.sp_def == 460  # 400 * 1.15 = 460.0
        assert result.spd == 575  # 500 * 1.15 = 575.0
        assert result.hp == 690  # 600 * 1.15 = 690.0

    def test_round_complex_calculation(self):
        """测试复杂计算后的舍入"""
        obj1 = SixAttributes(atk=123, def_=234, sp_atk=345, sp_def=456, spd=567, hp=678)
        obj2 = SixAttributes(
            atk=13, def_=17, sp_atk=19, sp_def=23, spd=29, hp=31, percent=True
        )
        result = obj1 + obj2
        result = result.round()
        # 123 * 1.13 = 138.99 ≈ 139
        assert result.atk == 139
        # 234 * 1.17 = 273.78 ≈ 274
        assert result.def_ == 274
        # 345 * 1.19 = 410.55 ≈ 411
        assert result.sp_atk == 411
        # 456 * 1.23 = 560.88 ≈ 561
        assert result.sp_def == 561
        # 567 * 1.29 = 731.43 ≈ 731
        assert result.spd == 731
        # 678 * 1.31 = 888.18 ≈ 888
        assert result.hp == 888

    def test_round_preserves_original(self):
        """测试舍入不修改原始对象"""
        obj = SixAttributes(
            atk=10.7, def_=20.3, sp_atk=30.5, sp_def=40.9, spd=50.1, hp=60.6
        )
        result = obj.round()
        # 原始对象应保持不变
        assert obj.atk == 10.7
        assert obj.def_ == 20.3
        assert obj.sp_atk == 30.5
        assert obj.sp_def == 40.9
        assert obj.spd == 50.1
        assert obj.hp == 60.6
        # 结果对象应该被舍入
        assert result.atk == 11
        assert result.def_ == 20
        assert result.sp_atk == 30
        assert result.sp_def == 41
        assert result.spd == 50
        assert result.hp == 61

    def test_round_chain_with_operations(self):
        """测试舍入与其他操作的链式调用"""
        obj1 = SixAttributes(atk=100, def_=100, sp_atk=100, sp_def=100, spd=100, hp=100)
        obj2 = SixAttributes(
            atk=33, def_=33, sp_atk=33, sp_def=33, spd=33, hp=33, percent=True
        )

        # 链式调用: 加法 -> 舍入
        result = (obj1 + obj2).round()
        assert result.atk == 133  # 100 * 1.33 = 133.0
        assert result.def_ == 133

        # 多次操作后舍入
        obj3 = SixAttributes(
            atk=10, def_=10, sp_atk=10, sp_def=10, spd=10, hp=10, percent=True
        )
        result2 = (obj1 + obj2 - obj3).round()
        # (100 * 1.33) * 0.9 = 133 * 0.9 = 119.7 ≈ 120
        assert result2.atk == 120
        assert result2.def_ == 120


class TestIntegration:
    """集成测试"""

    def test_chain_operations(self):
        """测试链式操作"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        obj3 = SixAttributes(atk=2, def_=4, sp_atk=6, sp_def=8, spd=10, hp=12)
        result = obj1 + obj2 - obj3
        assert result.atk == 13  # 10 + 5 - 2
        assert result.def_ == 26  # 20 + 10 - 4
        assert result.sp_atk == 39  # 30 + 15 - 6
        assert result.sp_def == 52  # 40 + 20 - 8
        assert result.spd == 65  # 50 + 25 - 10
        assert result.hp == 78  # 60 + 30 - 12

    def test_from_string_then_add(self):
        """测试从字符串创建后进行运算"""
        obj1 = SixAttributes.from_string('10 20 30 40 50 60')
        obj2 = SixAttributes.from_string('5 10 15 20 25 30')
        result = obj1 + obj2
        assert result.atk == 15
        assert result.hp == 90

    def test_from_list_with_hp_first_then_operations(self):
        """测试使用 hp_first 创建后进行运算"""
        obj1 = SixAttributes.from_list([100, 10, 20, 30, 40, 50], hp_first=True)
        obj2 = SixAttributes.from_list([200, 5, 10, 15, 20, 25], hp_first=True)
        result = obj1 + obj2
        assert result.hp == 300
        assert result.atk == 15

    def test_total_property_after_operations(self):
        """测试运算后 total 属性是否正确"""
        obj1 = SixAttributes(atk=10, def_=20, sp_atk=30, sp_def=40, spd=50, hp=60)
        obj2 = SixAttributes(atk=5, def_=10, sp_atk=15, sp_def=20, spd=25, hp=30)
        result = obj1 + obj2
        assert result.total == 15 + 30 + 45 + 60 + 75 + 90  # 315

    def test_mixed_fixed_and_percent_chain(self):
        """测试混合固定数值和百分比数值的链式计算"""
        # 基础属性
        base = SixAttributes(atk=100, def_=100, sp_atk=100, sp_def=100, spd=100, hp=100)

        # 固定值加成 +50
        fixed_bonus = SixAttributes(
            atk=50, def_=50, sp_atk=50, sp_def=50, spd=50, hp=50
        )

        # 百分比加成 +20%
        percent_bonus = SixAttributes(
            atk=20, def_=20, sp_atk=20, sp_def=20, spd=20, hp=20, percent=True
        )

        # 百分比减成 -10%
        percent_debuff = SixAttributes(
            atk=10, def_=10, sp_atk=10, sp_def=10, spd=10, hp=10, percent=True
        )

        # 链式计算: base + fixed_bonus + percent_bonus - percent_debuff
        # 步骤 1: base + fixed_bonus = 150 (全属性)
        step1 = base + fixed_bonus
        assert step1.atk == 150
        assert step1.def_ == 150
        assert step1.percent is False

        # 步骤 2: 150 + 20% = 150 * (1 + 20/100) = 150 * 1.2 = 180
        step2 = step1 + percent_bonus
        assert step2.atk == 180
        assert step2.def_ == 180
        assert step2.sp_atk == 180
        assert step2.sp_def == 180
        assert step2.spd == 180
        assert step2.hp == 180
        assert step2.percent is False

        # 步骤 3: 180 - 10% = 180 * (1 - 10/100) = 180 * 0.9 = 162
        step3 = step2 - percent_debuff
        assert step3.atk == 162
        assert step3.def_ == 162
        assert step3.sp_atk == 162
        assert step3.sp_def == 162
        assert step3.spd == 162
        assert step3.hp == 162
        assert step3.percent is False

    def test_complex_mixed_calculation(self):
        """测试复杂的混合计算场景"""
        # 基础值
        base = SixAttributes(atk=80, def_=120, sp_atk=150, sp_def=90, spd=110, hp=200)

        # 装备固定加成
        equip = SixAttributes(atk=20, def_=30, sp_atk=40, sp_def=20, spd=15, hp=50)

        # 特性百分比加成 +25%
        ability = SixAttributes(
            atk=25, def_=25, sp_atk=25, sp_def=25, spd=25, hp=25, percent=True
        )

        # 刻印固定加成
        mark = SixAttributes(atk=15, def_=15, sp_atk=20, sp_def=10, spd=20, hp=30)

        # BUFF百分比加成 +30%
        buff = SixAttributes(
            atk=30, def_=30, sp_atk=30, sp_def=30, spd=30, hp=30, percent=True
        )

        # DEBUFF百分比减成 -15%
        debuff = SixAttributes(
            atk=15, def_=15, sp_atk=15, sp_def=15, spd=15, hp=15, percent=True
        )

        # 完整计算链: (((base + equip) + ability% + mark) + buff%) - debuff%
        result = base + equip + ability + mark + buff - debuff
        result = result.round()

        # 验证攻击力计算:
        # base.atk + equip.atk = 80 + 20 = 100
        # 100 * (1 + 25/100) = 100 * 1.25 = 125
        # 125 + mark.atk = 125 + 15 = 140
        # 140 * (1 + 30/100) = 140 * 1.3 = 182
        # 182 * (1 - 15/100) = 182 * 0.85 = 154.7 ≈ 155
        assert result.atk == 155

        # 验证体力计算:
        # base.hp + equip.hp = 200 + 50 = 250
        # 250 * 1.25 = 312.5 ≈ 312
        # 312 + mark.hp = 312 + 30 = 342
        # 342 * 1.3 = 444.6 ≈ 445
        # 445 * 0.85 = 378.25 ≈ 378
        assert result.hp == 378

        # 验证结果不是百分比
        assert result.percent is False

    def test_percent_only_chain(self):
        """测试纯百分比的链式计算"""
        # 多个百分比加成叠加
        percent1 = SixAttributes(
            atk=10, def_=10, sp_atk=10, sp_def=10, spd=10, hp=10, percent=True
        )
        percent2 = SixAttributes(
            atk=15, def_=15, sp_atk=15, sp_def=15, spd=15, hp=15, percent=True
        )
        percent3 = SixAttributes(
            atk=5, def_=5, sp_atk=5, sp_def=5, spd=5, hp=5, percent=True
        )

        # 百分比之间相加应该直接相加
        result = percent1 + percent2 + percent3
        assert result.atk == 30  # 10 + 15 + 5
        assert result.def_ == 30
        assert result.sp_atk == 30
        assert result.sp_def == 30
        assert result.spd == 30
        assert result.hp == 30
        assert result.percent is True

    def test_reverse_order_mixed_calculation(self):
        """测试不同顺序的混合计算"""
        base = SixAttributes(atk=100, def_=100, sp_atk=100, sp_def=100, spd=100, hp=100)
        percent = SixAttributes(
            atk=20, def_=20, sp_atk=20, sp_def=20, spd=20, hp=20, percent=True
        )

        # 固定值 + 百分比
        result1 = base + percent
        # 百分比 + 固定值（顺序相反）
        result2 = percent + base

        # 两种顺序应该得到相同结果
        assert result1.atk == result2.atk
        assert result1.def_ == result2.def_
        assert result1.sp_atk == result2.sp_atk
        assert result1.sp_def == result2.sp_def
        assert result1.spd == result2.spd
        assert result1.hp == result2.hp
        assert result1.percent == result2.percent

    def test_real_world_pet_stats_calculation(self):
        """测试真实世界的精灵属性计算场景"""
        # 精灵基础值
        pet_base = SixAttributes(
            atk=95, def_=88, sp_atk=120, sp_def=75, spd=102, hp=105
        )

        # 学习力 (最大值)
        learning = SixAttributes(atk=255, def_=255, sp_atk=0, sp_def=0, spd=0, hp=0)

        # 个体值加成 (满个体相当于额外加成)
        individual = SixAttributes(atk=31, def_=31, sp_atk=31, sp_def=31, spd=31, hp=31)

        # 性格加成 (例如: 攻击+10%, 特攻-10%)
        nature_bonus = SixAttributes(
            atk=10, def_=0, sp_atk=-10, sp_def=0, spd=0, hp=0, percent=True
        )

        # 计算最终属性: (基础 + 学习力 + 个体值) + 性格加成
        result = pet_base + learning + individual + nature_bonus
        result = result.round()
        # 验证攻击力: (95 + 255 + 31) * 1.1 = 381 * 1.1 = 419.1 ≈ 419
        assert result.atk == 419

        # 验证特攻: (120 + 0 + 31) * 0.9 = 151 * 0.9 = 135.9 ≈ 136
        assert result.sp_atk == 136

        # 验证防御: 88 + 255 + 31 = 374 (无性格影响)
        assert result.def_ == 374

        # 验证速度: 102 + 0 + 31 = 133 (无性格影响)
        assert result.spd == 133
