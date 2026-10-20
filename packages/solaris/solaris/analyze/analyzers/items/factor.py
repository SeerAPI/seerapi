from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.factor_design import FactorDesign
from seerapi_models.items import Factor, Item
from seerapi_models.pet import Pet, Soulmark
from seerapi_models.skill import Skill
from solaris.analyze.analyzers.factor_design import DesignAnalyzer
from solaris.analyze.base import (
    BaseAnalyzer,
    BaseDataSourcePostAnalyzer,
    DataImportConfig,
)
from solaris.analyze.typing_ import AnalyzeResult

from ._general import ItemAnalyzer

if TYPE_CHECKING:
    from solaris.parse.parsers.fragment import FragmentConfig


class FactorAnalyzer(BaseDataSourcePostAnalyzer):
    """整理因子道具的兑换条件和关联资源。"""

    @classmethod
    def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
        return (ItemAnalyzer, DesignAnalyzer)

    @classmethod
    def get_data_import_config(cls) -> DataImportConfig:
        return DataImportConfig(unity_paths=('fragment.json',))

    @classmethod
    def get_result_res_models(cls):
        return (Factor,)

    def analyze(self) -> tuple[AnalyzeResult[Factor], ...]:
        data: FragmentConfig = self._get_data('unity', 'fragment.json')
        results: dict[int, Factor] = {}
        if data['root'] is None:
            return (AnalyzeResult(Factor, results),)

        items = self._get_input_data(ItemAnalyzer, Item)
        designs = self._get_input_data(DesignAnalyzer, FactorDesign)
        design_refs = {
            design.reward.id: ResourceRef.from_model(design)
            for design in designs.values()
        }
        for fragment in data['root']['fragment']:
            item_id = fragment['id']
            pet_id = fragment['monster_id']
            item = items[item_id]
            skill_id = fragment['move_id']
            soulmark_id = fragment['effect_id']
            need_pet_id = fragment['needmon_id']
            results[item_id] = Factor(
                id=item_id,
                name=item.name,
                pet_limit=bool(fragment['pet_limit']),
                pet_consume=fragment['pet_consume'],
                skill_consume=fragment['moves_consume'] if skill_id else None,
                soulmark_consume=fragment['new_se_consume'] if soulmark_id else None,
                item=ResourceRef.from_model(item),
                design=design_refs.get(item_id),
                need_pet=ResourceRef.from_model(Pet, id=need_pet_id)
                if need_pet_id
                else None,
                pet=ResourceRef.from_model(Pet, id=pet_id),
                skill=ResourceRef.from_model(Skill, id=skill_id) if skill_id else None,
                soulmark=ResourceRef.from_model(Soulmark, id=soulmark_id)
                if soulmark_id
                else None,
            )

        return (AnalyzeResult(Factor, results),)
