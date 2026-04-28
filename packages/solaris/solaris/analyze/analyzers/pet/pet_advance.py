from typing import TYPE_CHECKING, Any, cast

from seerapi_models import Pet, PetAdvance, Skill, Soulmark
from seerapi_models.build_model import BaseResModel
from seerapi_models.common import ResourceRef, SixAttributes

from solaris.analyze.analyzers.pet._general import BasePetAnalyzer
from solaris.analyze.typing_ import AnalyzeResult

if TYPE_CHECKING:
	pass


class PetAdvanceAnalyzer(BasePetAnalyzer):
	@classmethod
	def get_result_res_models(cls) -> tuple[type[BaseResModel], ...]:
		return (PetAdvance,)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		result: dict[int, PetAdvance] = {}
		for pet_id, task in self.pet_advance_data.items():
			if not (advance_data := task['advances']):
				continue

			id_ = task['id']
			skills: list[ResourceRef[Skill]] = []

			if sp_moves := advance_data['sp_move']:
				skills.extend(
					ResourceRef.from_model(Skill, id=skill_id)
					for skill_id in sp_moves['sp_moves']
				)

			if ex_moves := advance_data['ex_move']:
				skills.append(ResourceRef.from_model(Skill, id=ex_moves['extra_moves']))

			soulmark_id = self.eid_to_soulmark_id_map.get(task['new_eff_id'])
			if soulmark_id:
				soulmark = ResourceRef.from_model(Soulmark, id=soulmark_id[0])
			else:
				raise ValueError('没有在神谕觉醒数据中找到魂印')

			resource = PetAdvance(
				id=id_,
				pet=ResourceRef.from_model(Pet, id=pet_id),
				skill=skills,
				soulmark=soulmark,
				base_stats=SixAttributes.from_list(
					cast(Any, advance_data['race'])['new_race'], hp_first=True
				),
			)
			result[id_] = resource

		return (AnalyzeResult(model=PetAdvance, data=result),)
