from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass
class PageInfo:
    offset: int = field(default=0)
    limit: int = field(default=100)

    def __post_init__(self) -> None:
        if self.offset < 0:
            raise ValueError('offset must be greater than or equal to 0')
        if self.limit < 0:
            raise ValueError('limit must be greater than or equal to 0')


@dataclass
class PagedResponse(Generic[T]):
    results: AsyncGenerator[T, None]
    count: int
    next: PageInfo | None = None
    previous: PageInfo | None = None
    first: PageInfo | None = None
    last: PageInfo | None = None
