from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.element_type import ElementType, TypeCombination

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import split_string_arg

if TYPE_CHECKING:
	from solaris.parse.parsers.skilltype import SkillType


class ElementTypeAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('skillType.json',),
		)

	@classmethod
	def get_result_res_models(cls):
		return (ElementType, TypeCombination)

	def analyze(self):
		data = self._get_data('unity', 'skillType.json')
		element_type_data: dict[int, SkillType] = {
			item['id']: item for item in data['root']['item']
		}

		element_type_map: dict[int, ElementType] = {}
		combination_map: dict[int, TypeCombination] = {}
		for id_, item in element_type_data.items():
			if item['is_dou'] == 0:
				element_type = ElementType(
					id=item['id'],
					name=item['cn'],
					name_en=item['en'][0],
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
