import re
from typing import Any

from seerapi_models.common import ResourceRef
from seerapi_models.pet import (
	Pet,
	PetArchiveStoryBook,
	PetArchiveStoryEntry,
	PetEncyclopediaEntry,
)

from solaris.analyze.typing_ import AnalyzeResult
from solaris.analyze.utils import create_category_map

from ._general import BasePetAnalyzer


def get_height_or_weight(text: Any) -> float | None:
	if not text:
		return None
	if isinstance(text, (int, float)):
		return text

	match = re.findall(r'-?\d+\.\d+|-?\d+', text)
	if not match:
		return None

	return float(match[0])


class PetEncyclopediaAnalyzer(BasePetAnalyzer):
	@classmethod
	def get_result_res_models(cls):
		return (PetEncyclopediaEntry, PetArchiveStoryBook)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		results = {}
		for id_, data in self.pet_encyclopedia_data.items():
			food = data.get('Food', '未知')
			if food == '未知':
				food = None
			foundin = data.get('Foundin', '--')
			if foundin == '--':
				foundin = None

			height = get_height_or_weight(data.get('Height', 0))
			weight = get_height_or_weight(data.get('Weight', 0))
			entry = PetEncyclopediaEntry(
				id=id_,
				name=data['DefName'],
				has_sound=bool(data.get('hasSound')),
				height=height,
				weight=weight,
				foundin=foundin,
				food=food,
				introduction=data.get('Features', ''),
				pet=ResourceRef.from_model(Pet, id=id_),
			)
			results[id_] = entry
		return (
			AnalyzeResult(
				model=PetEncyclopediaEntry,
				data=results,
			),
		)


class PetArchiveStoryAnalyzer(BasePetAnalyzer):
	def analyze(self) -> tuple[AnalyzeResult, ...]:
		book_map = create_category_map(
			self._get_data('patch', 'pet_archive_story_book.json'),
			model_cls=PetArchiveStoryBook,
			array_key='entries',
		)
		entry_map: dict[int, PetArchiveStoryEntry] = {}
		for id_, data in self.pet_archive_story_book_data.items():
			content = data.get('txt')
			if not content:
				continue

			story_id = data['storyid']
			entry = PetArchiveStoryEntry(
				id=id_,
				content=content,
				pet=ResourceRef.from_model(Pet, id=data['monid']),
				book=ResourceRef.from_model(PetArchiveStoryBook, id=story_id),
			)
			entry_map[id_] = entry
			ref = ResourceRef.from_model(entry)
			book_map.add_element(story_id, ref)

		return (
			AnalyzeResult(model=PetArchiveStoryEntry, data=entry_map),
			AnalyzeResult(model=PetArchiveStoryBook, data=book_map),
		)
