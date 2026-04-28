from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

_TModel = TypeVar('_TModel', bound=SQLModel)


class ResModelMixin(SQLModel, ABC):
    @classmethod
    @abstractmethod
    def resource_name(cls) -> str:
        pass

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # type: ignore
        return cls.resource_name()


class BaseResModel(ResModelMixin, ABC):
    """资源模型抽象基类"""

    id: int = Field(description='资源ID', primary_key=True)

    # @classmethod
    # @abstractmethod
    # def get_api_comment(cls) -> APIComment:
    #     """获取模型的 OpenAPI 说明注释"""
    #     pass


class BaseResModelWithOptionalId(ResModelMixin, ABC):
    """资源模型抽象基类"""

    id: int | None = Field(
        default=None,
        primary_key=True,
        exclude=True,
    )


class ConvertToORM(ABC, Generic[_TModel]):
    @classmethod
    @abstractmethod
    def get_orm_model(cls) -> type[_TModel]:
        """获取SQLModel ORM模型类型"""
        pass

    @abstractmethod
    def to_orm(self) -> _TModel:
        """将Pydantic模型转为SQLModel ORM模型"""
        pass


class BaseGeneralModel(SQLModel, ABC):
    @classmethod
    @abstractmethod
    def schema_path(cls) -> str:
        pass


class BaseCategoryModel(BaseResModel, ABC, Generic[_TModel]): ...


__all__ = [
    'BaseCategoryModel',
    'BaseGeneralModel',
    'BaseResModel',
    'BaseResModelWithOptionalId',
    'ConvertToORM',
]
