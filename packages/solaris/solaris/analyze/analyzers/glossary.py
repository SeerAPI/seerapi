from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.glossary import GlossaryEntry
from seerapi_models.pet import Pet

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult

if TYPE_CHECKING:
	from solaris.parse.parsers.effect_des import EffectDesConfig


class GlossaryAnalyzer(BaseDataSourceAnalyzer):
	"""术语分析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('effectDes.json',),
		)

	@classmethod
	def get_result_res_models(cls) -> tuple[type[GlossaryEntry], ...]:
		return (GlossaryEntry,)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		effect_des: EffectDesConfig = self._get_data('unity', 'effectDes.json')
		result: dict[int, GlossaryEntry] = {}
		for item in effect_des['root']['item']:
			id_ = item['id']
			glossary_entry = GlossaryEntry(
				id=id_,
				name=item['kinddes'],
				desc=item['desc'],
				kind=item['kind'],
				link=[
					ResourceRef.from_model(GlossaryEntry, id=int(link))
					for link in val.split(' ')
				]
				if (val := item['link'])
				else None,
				pet=[
					ResourceRef.from_model(Pet, id=int(monster))
					for monster in val.split(',')
				]
				if (val := item['monster']) and val != '0'
				else None,
			)
			result[id_] = glossary_entry

		return (AnalyzeResult(GlossaryEntry, result),)
