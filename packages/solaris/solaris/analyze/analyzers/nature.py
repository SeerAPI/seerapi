from typing import TYPE_CHECKING

from seerapi_models.common import SixAttributes
from seerapi_models.nature import Nature

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult

if TYPE_CHECKING:
	from solaris.parse.parsers.nature import NatureConfig


def _convert_percent(value: float) -> float:
	"""将小数转换为百分比（例如1.1倍转换为10%加成），如果value为1，则返回0"""
	if value == 1:
		return 0
	return round((value - 1) * 100, 2)


class NatureAnalyzer(BaseDataSourceAnalyzer):
	"""精灵性格修正分析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('nature.json',),
		)

	@classmethod
	def get_result_res_models(cls):
		return (Nature,)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		"""分析精灵性格修正"""
		data: 'NatureConfig' = self._get_data('unity', 'nature.json')
		nature_map: dict[int, Nature] = {}
		for item in data['root']['nature']:
			id_ = item['id']
			nature = Nature(
				id=id_,
				name=item['name'],
				des=item['des'],
				des2=item['des2'],
				attributes=SixAttributes(
					atk=_convert_percent(item['atk']),
					def_=_convert_percent(item['def']),
					sp_atk=_convert_percent(item['sp_atk']),
					sp_def=_convert_percent(item['sp_def']),
					spd=_convert_percent(item['spd']),
					hp=0,
					percent=True,
				),
			)
			nature_map[id_] = nature

		return (AnalyzeResult(Nature, nature_map),)
