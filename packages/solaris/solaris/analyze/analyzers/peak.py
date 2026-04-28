from datetime import datetime, timedelta
import re
from typing import TYPE_CHECKING

from seerapi_models.peak import PeakSeason

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import CN_TZ

if TYPE_CHECKING:
	from solaris.parse.parsers.pvp_achieve import PvpAchieveConfig
	from solaris.parse.parsers.pvp_task import PvpTaskConfig


class PeakSeasonAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(unity_paths=('pvpTask.json', 'pvpAchieve.json'))

	@classmethod
	def get_result_res_models(cls):
		return (PeakSeason,)

	def analyze(self):
		pvp_achieve_data: PvpAchieveConfig = self._get_data('unity', 'pvpAchieve.json')
		season: str | None = None
		for achieve in pvp_achieve_data['data']:
			match = re.search(r'\d+', achieve.get('title', ''))
			if match:
				season = match.group()
				break
		if not season:
			raise ValueError('未找到赛季编号')

		pvp_task_data: PvpTaskConfig = self._get_data('unity', 'pvpTask.json')
		start_time: datetime | None = None
		for task in pvp_task_data['data']:
			if task.get('id') == 1:
				start_time = datetime.strptime(str(task['subkey']), '%Y%m%d')
				start_time = start_time.replace(hour=10, tzinfo=CN_TZ)
				break

		if not start_time:
			raise ValueError('未找到赛季开始时间')

		peak_season = PeakSeason(
			id=1,
			start_time=start_time,
			end_time=start_time + timedelta(days=91),
		)
		return (
			AnalyzeResult(
				model=PeakSeason,
				data={1: peak_season},
			),
		)
