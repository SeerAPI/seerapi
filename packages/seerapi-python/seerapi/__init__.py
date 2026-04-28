import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from ._client import SeerAPI
from ._models import PagedResponse, PageInfo

P = ParamSpec('P')
T = TypeVar('T')


def async_to_sync(async_func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, T]:
    """
    将异步函数包装为同步函数的装饰器。

    这个装饰器会创建一个新的事件循环来运行异步函数，避免与现有事件循环冲突。
    适用于在同步代码中调用异步函数的场景。

    Args:
        async_func: 要包装的异步函数

    Returns:
        返回一个同步版本的函数，调用时会自动处理事件循环

    Example:
        ```python
        @async_to_sync
        async def fetch_data(url: str) -> dict:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()

        # 可以像普通同步函数一样调用
        data = fetch_data("https://api.example.com/data")
        ```
    """

    @wraps(async_func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # 尝试获取当前运行的事件循环
        try:
            _ = asyncio.get_running_loop()
        except RuntimeError:
            # 没有运行中的事件循环，使用 asyncio.run
            return asyncio.run(async_func(*args, **kwargs))
        else:
            # 已经在事件循环中运行，需要在新线程中创建新的事件循环
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                return future.result()

    return wrapper


__all__ = ['PageInfo', 'PagedResponse', 'SeerAPI', 'async_to_sync']
