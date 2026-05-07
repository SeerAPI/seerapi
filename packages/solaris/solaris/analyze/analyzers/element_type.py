from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.element_type import (
    ElementType,
    ElementTypeRelation,
    TypeCombination,
)
from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import split_string_arg

if TYPE_CHECKING:
    from solaris.parse.parsers.skilltype import SkillType
    from solaris.parse.parsers.types_relation import TypesRelationConfig


class ElementTypeAnalyzer(BaseDataSourceAnalyzer):
    @classmethod
    def get_data_import_config(cls) -> DataImportConfig:
        return DataImportConfig(
            unity_paths=('skillType.json', 'typesRelation.json'),
        )

    @classmethod
    def get_result_res_models(cls):
        return (ElementType, TypeCombination)

    def analyze(self):
        data = self._get_data('unity', 'skillType.json')
        element_type_data: dict[int, SkillType] = {
            item['id']: item for item in data['root']['item']
        }

        name_to_id: dict[str, int] = {
            item['en'][0]: item['id']
            for item in element_type_data.values()
            if item['is_dou'] == 0
        }

        relation_data: TypesRelationConfig = self._get_data(
            'unity', 'typesRelation.json'
        )
        relations_by_name: dict[str, list[ElementTypeRelation]] = {}
        for rel in relation_data['root']['relation']:
            source_name = rel['type']
            relations_by_name[source_name] = [
                ElementTypeRelation(
                    target_type=ResourceRef.from_model(
                        ElementType, id=name_to_id[opp['type']]
                    ),
                    multiple=opp['multiple'],
                )
                for opp in rel['opponent']
                if opp['type'] in name_to_id
            ]

        element_type_map: dict[int, ElementType] = {}
        combination_map: dict[int, TypeCombination] = {}
        for id_, item in element_type_data.items():
            if item['is_dou'] == 0:
                element_type = ElementType(
                    id=item['id'],
                    name=item['cn'],
                    name_en=item['en'][0],
                    relations=relations_by_name[item['en'][0]],
                )
                element_type_map[id_] = element_type

        for id_, item in element_type_data.items():
            if item['is_dou'] == 1:
                comp1, comp2 = split_string_arg(item['att'])
            else:
                comp1 = id_
                comp2 = None
            combination = TypeCombination(
                id=id_,
                name=item['cn'],
                name_en='_'.join(item['en']),
                primary=ResourceRef.from_model(ElementType, id=comp1),
                secondary=ResourceRef.from_model(ElementType, id=comp2)
                if comp2
                else None,
            )
            combination_map[id_] = combination

        return (
            AnalyzeResult(model=ElementType, data=element_type_map),
            AnalyzeResult(model=TypeCombination, data=combination_map),
        )
