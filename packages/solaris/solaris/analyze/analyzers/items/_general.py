from functools import cached_property
from typing import TYPE_CHECKING, TypeAlias, cast

from seerapi_models.common import ResourceRef
from seerapi_models.items import Item, ItemCategory

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.typing import JSONObject
from solaris.utils import get_nested_value

if TYPE_CHECKING:
	from solaris.parse.parsers.items_optimize.base_item import BaseItemData, DataRoot
	from solaris.parse.parsers.items_optimize.items_optimize_cat import (
		ItemsOptimizeCatConfig,
	)
	from solaris.parse.parsers.items_tip import ItemTipItem


_ItemConfigType: TypeAlias = 'DataRoot[BaseItemData]'


def _range() -> range:
	return range(27)


def _merge_max_value(max_value: int, item_data: _ItemConfigType) -> _ItemConfigType:
	for item in item_data['root']['items']:
		if 'max' not in item or item['max'] == 0:
			item['max'] = max_value

	return item_data


class BaseItemAnalyzer(BaseDataSourceAnalyzer):
	def __init__(self) -> None:
		super().__init__()
		if 'unity' not in self.data:
			return

		for cat in self.item_category_data['root']['cats']:
			key = f'itemsOptimizeCatItems{cat["id"]}.json'
			item_data = self.get_category_items(cat['id'])
			self.data['unity'][key] = cast(
				JSONObject, _merge_max_value(cat['max'], item_data)
			)

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		unity_paths = [f'itemsOptimizeCatItems{i}.json' for i in _range()]
		return DataImportConfig(
			unity_paths=('itemsTip.json', 'itemsOptimizeCat.json', *unity_paths),
		)

	@cached_property
	def item_category_data(self) -> 'ItemsOptimizeCatConfig':
		return self._get_data('unity', 'itemsOptimizeCat.json')

	@cached_property
	def item_tip_data(self) -> dict[int, 'ItemTipItem']:
		return {
			data['id']: data
			for data in self._get_data('unity', 'itemsTip.json')['root']['item']
		}

	def get_category_items(self, category_id: int) -> _ItemConfigType:
		return self._get_data('unity', f'itemsOptimizeCatItems{category_id}.json')


class ItemAnalyzer(BaseItemAnalyzer):
	def _item_dict_to_model(self, item_data: list['BaseItemData']) -> dict[int, 'Item']:
		return {
			data['id']: Item(
				id=data['id'],
				name=data['name'],
				max=data['max'],
				desc=get_nested_value(self.item_tip_data, [data['id'], 'des']),
				category=ResourceRef.from_model(ItemCategory, id=data['cat_id']),
			)
			for data in item_data
		}

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		category_data: 'ItemsOptimizeCatConfig' = self._get_data(
			'unity', 'itemsOptimizeCat.json'
		)
		category_map: dict[int, 'ItemCategory'] = {}
		for category in category_data['root']['cats']:
			id_ = category['id']
			category_map[id_] = ItemCategory(
				id=id_,
				name=category['name'],
				max=category['max'],
			)

		item_map: dict[int, 'Item'] = {}
		for id_, category in category_map.items():
			item_data = self.get_category_items(id_)['root']['items']
			for item in item_data:
				category.item.append(ResourceRef.from_model(Item, id=item['id']))

			item_map.update(self._item_dict_to_model(item_data))

		return (
			AnalyzeResult(model=Item, data=item_map),
			AnalyzeResult(model=ItemCategory, data=category_map),
		)
