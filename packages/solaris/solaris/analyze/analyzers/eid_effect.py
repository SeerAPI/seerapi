from collections.abc import Callable
from itertools import chain

from seerapi_models.common import EidEffect, EidEffectInUse
from seerapi_models.effect import PetEffect, VariationEffect
from seerapi_models.items import EnergyBead, Equip, SuitBonus
from seerapi_models.pet import Soulmark

from solaris.analyze.base import BaseAnalyzer, BasePostAnalyzer
from solaris.analyze.typing_ import AnalyzeResult, TResModelRequiredId

from .effect import NewSeAnalyzer
from .items.enegry_bead import EnergyBeadAnalyzer
from .items.equip import EquipAnalyzer
from .pet.soulmark import SoulmarkAnalyzer

EidEffectExtractor = Callable[[TResModelRequiredId], tuple[EidEffectInUse, str] | None]


def _extract_pet_effect(obj: PetEffect) -> tuple[EidEffectInUse, str]:
	return (obj.effect, obj.desc)


def _extract_variation_effect(obj: VariationEffect) -> tuple[EidEffectInUse, str]:
	return (obj.effect, obj.desc)


def _extract_equip_effect(obj: Equip) -> tuple[EidEffectInUse, str] | None:
	if obj.bonus and obj.bonus.eid_effect:
		return (obj.bonus.eid_effect, obj.bonus.desc)
	return None


def _extract_suit_bonus_effect(obj: SuitBonus) -> tuple[EidEffectInUse, str] | None:
	if obj.eid_effect:
		return (obj.eid_effect, obj.desc)
	return None


def _extract_energy_bead_effect(obj: EnergyBead) -> tuple[EidEffectInUse, str]:
	return (obj.effect, obj.desc)


def _extract_soulmark_effect(obj: Soulmark) -> tuple[EidEffectInUse, str] | None:
	if obj.effect:
		return (obj.effect, obj.desc)

	return None


class EidEffectAnalyzer(BasePostAnalyzer):
	"""分析并提取特性/特质数据"""

	@classmethod
	def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
		return (NewSeAnalyzer, EquipAnalyzer, EnergyBeadAnalyzer, SoulmarkAnalyzer)

	@classmethod
	def get_result_res_models(cls):
		return (EidEffect,)

	def _eid_ref_to_obj(self, eid_ref: EidEffectInUse) -> EidEffect:
		return EidEffect(
			id=eid_ref.effect.id,
			args_num=len(eid_ref.effect_args) if eid_ref.effect_args else 0,
		)

	def _collect_effects(
		self,
		analyzer_cls: type[BaseAnalyzer],
		model_cls: type[TResModelRequiredId],
		extractor: EidEffectExtractor,
	):
		"""从指定数据源收集效果引用"""
		for obj in self._get_input_data(analyzer_cls, model_cls).values():
			effect_ref = extractor(obj)
			if effect_ref is not None:
				yield self._eid_ref_to_obj(effect_ref[0])

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		# 定义数据源配置：(Analyzer类, Model类, 提取函数)
		sources = [
			(NewSeAnalyzer, PetEffect, _extract_pet_effect),
			(NewSeAnalyzer, VariationEffect, _extract_variation_effect),
			(EquipAnalyzer, Equip, _extract_equip_effect),
			(EquipAnalyzer, SuitBonus, _extract_suit_bonus_effect),
			(EnergyBeadAnalyzer, EnergyBead, _extract_energy_bead_effect),
			(SoulmarkAnalyzer, Soulmark, _extract_soulmark_effect),
		]

		# 使用链式迭代器收集所有效果
		chain_iter = chain.from_iterable(
			self._collect_effects(analyzer, model, extractor)
			for analyzer, model, extractor in sources
		)
		eid_effect_map = {eid_effect.id: eid_effect for eid_effect in chain_iter}

		return (AnalyzeResult(model=EidEffect, data=eid_effect_map),)
