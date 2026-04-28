from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.peak_pool import PeakExpertPool, PeakPool, PeakPoolVote
from seerapi_models.pet import Pet

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import CN_TZ

if TYPE_CHECKING:
	from solaris.parse.parsers.pvp_ban import PvpBanConfig
	from solaris.parse.parsers.pvp_ban_expert import PvpBanExpertConfig
	from solaris.parse.parsers.pvp_vote import PvpVoteConfig, PvpVoteInfo


def parse_pool_start_time(time_str: str) -> datetime:
	time_str = time_str[2:]
	time = datetime.strptime(time_str, '%Y%m%d')
	return time.replace(hour=10, tzinfo=CN_TZ)


class PeakPoolAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('pvpBan.json', 'pvpBanExpert.json', 'pvpVote.json')
		)

	@classmethod
	def get_result_res_models(cls):
		return (PeakPool, PeakExpertPool, PeakPoolVote)

	def _from_id_get_count(self, id: int) -> int:
		pvp_ban_data: PvpBanConfig = self._get_data('unity', 'pvpBan.json')
		for item in pvp_ban_data['data']:
			if item['id'] == id:
				return item['quantity']

		raise ValueError(f'ID {id} not found in pvpBan.json')

	def analyze(self):
		pvp_ban_data: PvpBanConfig = self._get_data('unity', 'pvpBan.json')
		pvp_ban_expert_data: PvpBanExpertConfig = self._get_data(
			'unity', 'pvpBanExpert.json'
		)
		pvp_vote_data: PvpVoteConfig = self._get_data('unity', 'pvpVote.json')

		peak_pool_map: dict[int, PeakPool] = {}
		peak_vote_pool_map: dict[int, PeakPoolVote] = {}
		pvp_vote_info: dict[int, PvpVoteInfo] = {
			item['id']: item for item in pvp_vote_data['data']
		}
		for item in pvp_ban_data['data']:
			count = item['quantity']
			start_time = parse_pool_start_time(str(item['subkey']))
			peak_pool = PeakPool(
				id=count,
				count=count,
				start_time=start_time,
				end_time=start_time + timedelta(weeks=4),
				pet=[ResourceRef.from_model(Pet, id=pet_id) for pet_id in item['name']],
			)
			peak_pool_map[count] = peak_pool

			vote_info = pvp_vote_info[item['id']]
			peak_vote_pool = PeakPoolVote(
				id=count,
				subkey=vote_info['subkey'],
				start_time=datetime.fromtimestamp(vote_info['time1'], CN_TZ),
				end_time=datetime.fromtimestamp(vote_info['time2'], CN_TZ),
				count=count,
				pet=[
					ResourceRef.from_model(Pet, id=int(pet_id))
					for pet_id in vote_info['name'].split(';')
				],
			)
			peak_vote_pool_map[count] = peak_vote_pool

		peak_expert_pool_map: dict[int, PeakExpertPool] = {}
		for item in pvp_ban_expert_data['data']:
			count = item['quantity']
			start_time = parse_pool_start_time(str(item['subkey_month']))
			peak_expert_pool = PeakExpertPool(
				id=count,
				count=count,
				start_time=start_time,
				end_time=start_time + timedelta(weeks=4),
				pet=[
					ResourceRef.from_model(Pet, id=int(pet_id))
					for pet_id in item['name'].split(';')
				],
			)
			peak_expert_pool_map[count] = peak_expert_pool

		return (
			AnalyzeResult(model=PeakPool, data=peak_pool_map),
			AnalyzeResult(model=PeakExpertPool, data=peak_expert_pool_map),
			AnalyzeResult(model=PeakPoolVote, data=peak_vote_pool_map),
		)
