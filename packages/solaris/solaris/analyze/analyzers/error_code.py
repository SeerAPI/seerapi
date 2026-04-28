from typing import TYPE_CHECKING

from seerapi_models.error_code import ErrorCode

from ..base import BaseDataSourceAnalyzer, DataImportConfig
from ..typing_ import AnalyzeResult

if TYPE_CHECKING:
	from solaris.parse.parsers.language import LanguageConfig


def _extract_key(key: str) -> str:
	return key.split('_')[-1]


class ErrorCodeAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(unity_paths=('language.json',))

	@classmethod
	def get_result_res_models(cls):
		return (ErrorCode,)

	def analyze(self):
		language_config: LanguageConfig = self._get_data('unity', 'language.json')
		error_code_map: dict[int, ErrorCode] = {}
		for item in language_config['root']['item']:
			if not item['key'].startswith('Error'):
				continue

			error_code = ErrorCode(
				id=int(_extract_key(item['key'])),
				name=item['key'],
				message=item['content'],
			)
			error_code_map[error_code.id] = error_code

		return (AnalyzeResult(model=ErrorCode, data=error_code_map),)
