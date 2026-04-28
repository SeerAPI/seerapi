def move_to_last(lst: list, index: int) -> None:
    """
    将列表中指定索引位置的元素移动到列表的最后一位。

    Args:
            lst: 要操作的列表
            index: 要移动的元素的索引位置

    """
    if 0 <= index < len(lst):
        # 弹出指定位置的元素并添加到列表末尾
        element = lst.pop(index)
        lst.append(element)


def move_to_first(lst: list, index: int) -> None:
    """
    将列表中指定索引位置的元素移动到列表的第一位。

    Args:
            lst: 要操作的列表
            index: 要移动的元素的索引位置

    """
    if 0 <= index < len(lst):
        element = lst.pop(index)
        lst.insert(0, element)
