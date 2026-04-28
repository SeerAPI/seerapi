from typing import TYPE_CHECKING, Any, cast

from seerapi_models import (
	AvatarFrame,
	AvatarHead,
	Emoji,
	HomepageBackground,
	NamecardBackground,
	NicknameBackground,
)

from ..base import BaseDataSourceAnalyzer, DataImportConfig
from ..typing_ import AnalyzeResult

if TYPE_CHECKING:
	from solaris.parse.parsers.profilephoto import ProfilephotoConfig


class DecorationAnalyzer(BaseDataSourceAnalyzer):
	"""装饰品分析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('profilephoto.json',),
		)

	@classmethod
	def get_result_res_models(cls):
		return (
			AvatarHead,
			AvatarFrame,
			NamecardBackground,
			NicknameBackground,
			HomepageBackground,
		)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		profilephoto_data: 'ProfilephotoConfig' = self._get_data(
			'unity', 'profilephoto.json'
		)
		type_map = {
			1: AvatarHead,
			2: AvatarFrame,
			3: NamecardBackground,
			4: HomepageBackground,
			5: NicknameBackground,
			6: Emoji,
		}
		result: dict[int, AnalyzeResult] = {
			id_: AnalyzeResult(model=model, data={}) for id_, model in type_map.items()
		}
		for item in profilephoto_data['root']['item']:
			id_ = item['id']
			type_id = item['type']
			model = type_map[type_id]
			obj = model(
				id=id_,
				name=item['name'],
				desc=item['desc'],
				icon_id=item['icon'],
			)
			cast(dict[int, Any], result[type_id].data)[id_] = obj

		return tuple(result.values())
