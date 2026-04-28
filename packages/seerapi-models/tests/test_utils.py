"""测试 _utils 模块中的工具函数"""

from seerapi_models._utils import move_to_first, move_to_last


class TestMoveToLast:
    """测试 move_to_last 函数"""

    def test_move_middle_element_to_last(self):
        """测试将中间元素移动到最后"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, 2)
        assert lst == [1, 2, 4, 5, 3]

    def test_move_first_element_to_last(self):
        """测试将第一个元素移动到最后"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, 0)
        assert lst == [2, 3, 4, 5, 1]

    def test_move_last_element_to_last(self):
        """测试将最后一个元素移动到最后（应该不变）"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, 4)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_single_element_list(self):
        """测试单元素列表"""
        lst = [1]
        move_to_last(lst, 0)
        assert lst == [1]

    def test_move_with_two_element_list(self):
        """测试两元素列表"""
        lst = [1, 2]
        move_to_last(lst, 0)
        assert lst == [2, 1]

    def test_move_with_negative_index(self):
        """测试负数索引（应该不进行操作）"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, -1)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_out_of_range_index(self):
        """测试超出范围的索引（应该不进行操作）"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, 10)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_empty_list(self):
        """测试空列表"""
        lst = []
        move_to_last(lst, 0)
        assert lst == []

    def test_move_with_string_list(self):
        """测试字符串列表"""
        lst = ['a', 'b', 'c', 'd']
        move_to_last(lst, 1)
        assert lst == ['a', 'c', 'd', 'b']

    def test_move_modifies_original_list(self):
        """测试函数是否修改原始列表而不是返回新列表"""
        lst = [1, 2, 3]
        original_id = id(lst)
        result = move_to_last(lst, 0)
        assert result is None
        assert id(lst) == original_id
        assert lst == [2, 3, 1]


class TestMoveToFirst:
    """测试 move_to_first 函数"""

    def test_move_middle_element_to_first(self):
        """测试将中间元素移动到第一位"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, 2)
        assert lst == [3, 1, 2, 4, 5]

    def test_move_last_element_to_first(self):
        """测试将最后一个元素移动到第一位"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, 4)
        assert lst == [5, 1, 2, 3, 4]

    def test_move_first_element_to_first(self):
        """测试将第一个元素移动到第一位（应该不变）"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, 0)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_single_element_list(self):
        """测试单元素列表"""
        lst = [1]
        move_to_first(lst, 0)
        assert lst == [1]

    def test_move_with_two_element_list(self):
        """测试两元素列表"""
        lst = [1, 2]
        move_to_first(lst, 1)
        assert lst == [2, 1]

    def test_move_with_negative_index(self):
        """测试负数索引（应该不进行操作）"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, -1)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_out_of_range_index(self):
        """测试超出范围的索引（应该不进行操作）"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, 10)
        assert lst == [1, 2, 3, 4, 5]

    def test_move_with_empty_list(self):
        """测试空列表"""
        lst = []
        move_to_first(lst, 0)
        assert lst == []

    def test_move_with_string_list(self):
        """测试字符串列表"""
        lst = ['a', 'b', 'c', 'd']
        move_to_first(lst, 2)
        assert lst == ['c', 'a', 'b', 'd']

    def test_move_modifies_original_list(self):
        """测试函数是否修改原始列表而不是返回新列表"""
        lst = [1, 2, 3]
        original_id = id(lst)
        result = move_to_first(lst, 2)
        assert result is None
        assert id(lst) == original_id
        assert lst == [3, 1, 2]


class TestMoveIntegration:
    """测试 move_to_first 和 move_to_last 的集成使用"""

    def test_move_to_last_then_first(self):
        """测试先移动到最后，再移动到第一位"""
        lst = [1, 2, 3, 4, 5]
        move_to_last(lst, 0)  # [2, 3, 4, 5, 1]
        move_to_first(lst, 4)  # [1, 2, 3, 4, 5]
        assert lst == [1, 2, 3, 4, 5]

    def test_move_to_first_then_last(self):
        """测试先移动到第一位，再移动到最后"""
        lst = [1, 2, 3, 4, 5]
        move_to_first(lst, 4)  # [5, 1, 2, 3, 4]
        move_to_last(lst, 0)  # [1, 2, 3, 4, 5]
        assert lst == [1, 2, 3, 4, 5]

    def test_multiple_moves(self):
        """测试多次移动操作"""
        lst = ['a', 'b', 'c', 'd', 'e']
        move_to_last(lst, 0)  # ['b', 'c', 'd', 'e', 'a']
        move_to_last(lst, 0)  # ['c', 'd', 'e', 'a', 'b']
        move_to_first(lst, 4)  # ['b', 'c', 'd', 'e', 'a']
        assert lst == ['b', 'c', 'd', 'e', 'a']
