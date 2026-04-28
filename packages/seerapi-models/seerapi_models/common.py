from collections.abc import Iterable
import inspect
from typing import (
    TYPE_CHECKING,
    Annotated,
    ClassVar,
    Generic,
    Literal,
    TypeVar,
    cast,
    overload,
)
from typing_extensions import Self

from pydantic import (
    AliasChoices,
    ConfigDict,
    WithJsonSchema,
    computed_field,
    field_serializer,
)
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import JSON, Column, Computed, Field, Numeric, Relationship

from ._utils import move_to_last
from .build_model import (
    BaseGeneralModel,
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)

if TYPE_CHECKING:
    from .effect import PetEffectORM, VariationEffectORM
    from .items import (
        EnergyBeadORM,
        EquipBonusORM,
        GemORM,
        SkillStoneEffectORM,
        SuitBonusORM,
    )
    from .pet import SoulmarkORM
    from .skill import SkillEffectType, SkillEffectTypeORM, SkillORM

BASE_DATA_URL = 'you_should_set_this_url.example.com'


TResModel = TypeVar('TResModel', bound=BaseResModel)
_TResModelArg = TypeVar('_TResModelArg', bound=BaseResModel)


class ResourceRef(BaseGeneralModel, Generic[TResModel]):
    """API资源类"""

    base_data_url: ClassVar[str] = BASE_DATA_URL

    id: int = Field(description='资源ID')
    url: str = Field(
        description='资源URL',
        schema_extra={'format': 'uri'},
    )

    @field_serializer('url', mode='plain')
    def _serialize_url(self, url: str) -> str:
        return url.replace(BASE_DATA_URL, self.base_data_url.removesuffix('/'))

    @classmethod
    def schema_path(cls) -> str:
        return 'common/resource_ref/'

    @classmethod
    def from_res_name(
        cls,
        id: int,
        resource_name: str,
        sub_path: str | None = None,
    ) -> Self:
        path_parts = filter(
            bool,
            [
                cls.base_data_url,
                resource_name,
                str(id),
                sub_path,
            ],
        )
        return cls(id=id, url='/'.join(cast(Iterable[str], path_parts)))

    @overload
    @classmethod
    def from_model(
        cls,
        model: _TResModelArg,
    ) -> 'ResourceRef[_TResModelArg]': ...

    @overload
    @classmethod
    def from_model(
        cls,
        model: type[_TResModelArg],
        *,
        id: int,
    ) -> 'ResourceRef[_TResModelArg]': ...

    @classmethod
    def from_model(
        cls,
        model: type[_TResModelArg] | _TResModelArg,
        *,
        id: int | None = None,
    ) -> 'ResourceRef[_TResModelArg]':
        if not inspect.isclass(model):
            id = model.id
        if id is None:
            raise ValueError('id is required')

        obj = cls.from_res_name(id=id, resource_name=model.resource_name())
        return cast(ResourceRef[_TResModelArg], obj)


class NamedResourceRef(ResourceRef[TResModel]):
    name: str | None = Field(default=None, description='资源名称')

    @classmethod
    def schema_path(cls) -> str:
        return 'common/named_resource_ref/'

    @classmethod
    def from_res_name(
        cls,
        id: int,
        resource_name: str,
        sub_path: str | None = None,
        *,
        name: str | None = None,
    ) -> Self:
        path_parts: list[str] = [
            cls.base_data_url,
            resource_name,
            str(id),
        ]
        if sub_path:
            path_parts.append(sub_path)
        return cls(id=id, url='/'.join(path_parts), name=name)

    @overload
    @classmethod
    def from_model(
        cls,
        model: _TResModelArg,
        *,
        name: str | None = None,
    ) -> 'NamedResourceRef[_TResModelArg]': ...

    @overload
    @classmethod
    def from_model(
        cls,
        model: type[_TResModelArg],
        *,
        id: int,
        name: str | None = None,
    ) -> 'NamedResourceRef[_TResModelArg]': ...

    @classmethod
    def from_model(
        cls,
        model: type[_TResModelArg] | _TResModelArg,
        *,
        id: int | None = None,
        name: str | None = None,
    ) -> 'NamedResourceRef[_TResModelArg]':
        if not inspect.isclass(model):
            id = model.id
            # 尝试从模型实例中获取name属性
            if name is None and hasattr(model, 'name'):
                name = getattr(model, 'name')
        if id is None:
            raise ValueError('id is required')

        obj = cls.from_res_name(id=id, resource_name=model.resource_name(), name=name)
        return cast(NamedResourceRef[_TResModelArg], obj)


class ApiResourceList(BaseGeneralModel, Generic[TResModel]):
    """API资源列表，兼容RFC 5988的Link标准"""

    count: int = Field(description='资源数量')
    next: str | None = Field(default=None, description='下一页URL')
    previous: str | None = Field(default=None, description='上一页URL')
    first: str | None = Field(default=None, description='第一页URL')
    last: str | None = Field(default=None, description='最后一页URL')
    results: list[NamedResourceRef[TResModel]] = Field(description='资源列表')

    @classmethod
    def schema_path(cls) -> str:
        return 'common/api_resource_list/'


class NamedData(BaseGeneralModel, Generic[TResModel]):
    data: dict[int, TResModel]

    @classmethod
    def schema_path(cls) -> str:
        return 'common/named_data/'


class EidEffect(BaseResModel, BaseGeneralModel, ConvertToORM['EidEffectORM']):
    # info: str | None = Field(
    #     default=None,
    #     description='效果描述，当效果描述为空时，该字段为null',
    # )
    args_num: int = Field(
        description='效果需要的参数数量，该值是从使用该效果的资源中推测得出的'
    )

    @classmethod
    def schema_path(cls) -> str:
        return 'common/eid_effect/'

    @classmethod
    def resource_name(cls) -> str:
        return 'eid_effect'

    @classmethod
    def get_orm_model(cls) -> type['EidEffectORM']:
        return EidEffectORM

    def to_orm(self) -> 'EidEffectORM':
        return EidEffectORM(id=self.id, args_num=self.args_num)


class EidEffectORM(EidEffect, table=True):
    in_use: list['EidEffectInUseORM'] = Relationship(back_populates='effect')


class EidEffectInUseBase(BaseResModelWithOptionalId):
    effect_args: list[int] | None = Field(
        default=None,
        description='效果参数，当效果参数为空时，该字段为null',
        sa_type=JSON,
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'eid_effect_in_use'


class EidEffectInUse(
    EidEffectInUseBase, BaseGeneralModel, ConvertToORM['EidEffectInUseORM']
):
    effect: 'ResourceRef[EidEffect]' = Field(description='效果引用')

    @classmethod
    def schema_path(cls) -> str:
        return 'common/eid_effect_in_use/'

    @classmethod
    def get_orm_model(cls) -> type['EidEffectInUseORM']:
        return EidEffectInUseORM

    def to_orm(self) -> 'EidEffectInUseORM':
        return EidEffectInUseORM(
            id=self.id,
            eid=self.effect.id,
            effect_args=self.effect_args,
        )


class EidEffectInUseORM(EidEffectInUseBase, table=True):
    eid: int = Field(foreign_key='eid_effect.id')
    effect: 'EidEffectORM' = Relationship(back_populates='in_use')
    # 特性，魂印，装备效果，etc...
    energy_bead: 'EnergyBeadORM' = Relationship(back_populates='effect_in_use')
    soulmark: 'SoulmarkORM' = Relationship(back_populates='effect_in_use')
    pet_effect: 'PetEffectORM' = Relationship(back_populates='effect_in_use')
    variation_effect: 'VariationEffectORM' = Relationship(
        back_populates='effect_in_use'
    )
    equip_bonus: 'EquipBonusORM' = Relationship(back_populates='effect_in_use')
    suit_bonus: 'SuitBonusORM' = Relationship(back_populates='effect_in_use')


AttrValue = Annotated[int | float, WithJsonSchema({'type': 'number'})]


class SixAttributesBase(BaseResModelWithOptionalId, BaseGeneralModel):
    """六维属性类"""

    atk: AttrValue = Field(sa_type=Numeric, description='攻击')
    def_: AttrValue = Field(
        sa_type=Numeric,
        sa_column_kwargs={'name': 'def', 'nullable': False},
        description='防御',
        schema_extra={
            'serialization_alias': 'def',
            'validation_alias': AliasChoices('def', 'def_'),
        },
    )
    sp_atk: AttrValue = Field(sa_type=Numeric, description='特攻')
    sp_def: AttrValue = Field(sa_type=Numeric, description='特防')
    spd: AttrValue = Field(sa_type=Numeric, description='速度')
    hp: AttrValue = Field(sa_type=Numeric, description='体力')

    percent: bool = Field(
        default=False,
        description='该对象描述的是否是百分比加成，如果为true，属性值为百分比值',
    )

    @classmethod
    def schema_path(cls) -> str:
        return 'common/six_attributes/'

    @classmethod
    def from_string(
        cls, value: str, *, hp_first: bool = False, percent: bool = False
    ) -> Self:
        """从字符串创建六维属性对象"""
        attributes = value.split(' ')
        if len(attributes) < 6:
            raise ValueError('无效的属性字符串')
        attributes = [int(attribute) for attribute in attributes[0:6]]
        return cls.from_list(attributes, hp_first=hp_first, percent=percent)

    @classmethod
    def from_list(
        cls, attributes: list[int], *, hp_first: bool = False, percent: bool = False
    ) -> Self:
        if len(attributes) < 6:
            raise ValueError('无效的属性列表')
        if hp_first:
            move_to_last(attributes, 0)
        return cls(
            atk=attributes[0],
            def_=attributes[1],
            sp_atk=attributes[2],
            sp_def=attributes[3],
            spd=attributes[4],
            hp=attributes[5],
            percent=percent,
        )


class SixAttributes(SixAttributesBase, BaseGeneralModel):
    @computed_field
    @property
    def total(self) -> float:
        """总属性值"""
        return self.atk + self.def_ + self.sp_atk + self.sp_def + self.spd + self.hp

    @classmethod
    def resource_name(cls) -> str:
        return 'six_attributes'

    def _calc_number(
        self,
        other: 'SixAttributesBase',
        *,
        operator: Literal['add', 'sub', 'percent_mul', 'percent_div'],
        swap: bool = False,
    ) -> Self:
        """逐属性计算，swap=True 时交换 self 和 other 的运算位置"""
        keys = ['atk', 'def_', 'sp_atk', 'sp_def', 'spd', 'hp']
        values: list[int | float] = []
        for key in keys:
            if swap:
                left, right = getattr(other, key), getattr(self, key)
            else:
                left, right = getattr(self, key), getattr(other, key)

            if operator == 'add':
                val = left + right
            elif operator == 'sub':
                val = left - right
            elif operator == 'percent_mul':
                val = left * (1 + right / 100)
            elif operator == 'percent_div':
                val = left * (1 - right / 100)

            values.append(val)

        return type(self)(
            atk=values[0],
            def_=values[1],
            sp_atk=values[2],
            sp_def=values[3],
            spd=values[4],
            hp=values[5],
        )

    def __add__(self, other) -> Self:
        """两个六维属性相加"""
        if not isinstance(other, SixAttributesBase):
            raise TypeError(f'Cannot add {type(self)} and {type(other)}')

        if self.percent and other.percent:
            obj = self._calc_number(other, operator='add')
            obj.percent = True
            return obj
        elif self.percent or other.percent:
            if self.percent:
                obj = self._calc_number(other, operator='percent_mul', swap=True)
            else:
                obj = self._calc_number(other, operator='percent_mul')
            obj.percent = False
            return obj
        else:
            return self._calc_number(other, operator='add')

    def __sub__(self, other) -> Self:
        """两个六维属性相减"""
        if not isinstance(other, SixAttributesBase):
            raise TypeError(f'Cannot sub {type(self)} and {type(other)}')

        if self.percent and other.percent:
            obj = self._calc_number(other, operator='sub')
            obj.percent = True
            return obj
        elif self.percent or other.percent:
            if self.percent:
                obj = self._calc_number(other, operator='percent_div', swap=True)
            else:
                obj = self._calc_number(other, operator='percent_div')
            obj.percent = False
            return obj
        else:
            return self._calc_number(other, operator='sub')

    def round(self, ndigits: int | None = None) -> Self:
        return type(self)(
            atk=round(self.atk, ndigits),
            def_=round(self.def_, ndigits),
            sp_atk=round(self.sp_atk, ndigits),
            sp_def=round(self.sp_def, ndigits),
            spd=round(self.spd, ndigits),
            hp=round(self.hp, ndigits),
            percent=self.percent,
        )


class SixAttributesORMBase(SixAttributesBase):
    model_config = ConfigDict(ignored_types=(declared_attr,))  # type: ignore

    @declared_attr
    def total(self):  # type: ignore
        return column_property(
            Column(
                Numeric,
                Computed('atk + def + sp_atk + sp_def + spd + hp'),
                nullable=False,
            )
        )

    def to_model(self) -> 'SixAttributes':
        return SixAttributes(
            atk=self.atk,
            def_=self.def_,
            sp_atk=self.sp_atk,
            sp_def=self.sp_def,
            spd=self.spd,
            hp=self.hp,
            percent=self.percent,
        )


class SkillEffectInUseBase(BaseResModelWithOptionalId):
    """描述一条“使用中的”技能效果"""

    info: str = Field(description='技能效果描述')
    analyze_info: str = Field(description='新版 Unity 端采用的格式化技能效果描述文本')
    args: list[int | float] | list[int] | list[float] = Field(
        description='技能效果参数列表',
        sa_type=JSON,
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_in_use'


class SkillEffectInUse(
    SkillEffectInUseBase, BaseGeneralModel, ConvertToORM['SkillEffectInUseORM']
):
    effect: 'ResourceRef[SkillEffectType]'

    @classmethod
    def schema_path(cls) -> str:
        return 'common/skill_effect_in_use/'

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectInUseORM']:
        return SkillEffectInUseORM

    def to_orm(self) -> 'SkillEffectInUseORM':
        return SkillEffectInUseORM(
            effect_id=self.effect.id,
            args=self.args,
            info=self.info,
            analyze_info=self.analyze_info,
        )


class SkillEffectInUseORM(SkillEffectInUseBase, table=True):
    effect_id: int = Field(foreign_key='skill_effect_type.id')
    effect: 'SkillEffectTypeORM' = Relationship(back_populates='in_use')
    skill: list['SkillORM'] = Relationship(
        sa_relationship_kwargs={
            'secondary': 'skilleffectlink',
        }
    )
    friend_skill: list['SkillORM'] = Relationship(
        sa_relationship_kwargs={
            'secondary': 'skillfriendskilleffectlink',
        }
    )
    gem: list['GemORM'] = Relationship(
        back_populates='skill_effect_in_use',
        sa_relationship_kwargs={
            'secondary': 'gemeffectlink',
        },
    )
    skill_stone_effect: list['SkillStoneEffectORM'] = Relationship(
        back_populates='effect',
        sa_relationship_kwargs={
            'secondary': 'skillstoneeffectlink',
        },
    )


__all__ = [
    'ApiResourceList',
    'EidEffect',
    'EidEffectInUse',
    'EidEffectInUseBase',
    'EidEffectInUseORM',
    'EidEffectORM',
    'NamedData',
    'NamedResourceRef',
    'ResourceRef',
    'SixAttributes',
    'SixAttributesBase',
    'SixAttributesORMBase',
    'SkillEffectInUse',
    'SkillEffectInUseBase',
    'SkillEffectInUseORM',
]
