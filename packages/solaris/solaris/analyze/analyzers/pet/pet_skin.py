from typing import TYPE_CHECKING

from seerapi_models import PetSkinSeries, PetSkinSeriesSubType
from seerapi_models.common import ResourceRef
from seerapi_models.pet import Pet, PetSkin, PetSkinCategory
from solaris.analyze.base import AnalyzeResult
from solaris.analyze.utils import CategoryMap

from ._general import BasePetAnalyzer

if TYPE_CHECKING:
    pass


class PetSkinAnalyzer(BasePetAnalyzer):
    @classmethod
    def get_result_res_models(cls):
        return (PetSkin, PetSkinCategory, PetSkinSeries, PetSkinSeriesSubType)

    def analyze(self):
        pet_skin_data = self.pet_skin_data
        pet_skin_reward_data = self.pet_skin_reward_data
        real_id_data: dict[int, int] = {
            id_: pet['real_id']
            for id_, pet in self.pet_origin_data.items()
            if id_ >= 1400000 and pet['real_id'] != 0
        }
        pet_skin_map: dict[int, PetSkin] = {}
        pet_skin_series_map: CategoryMap[int, PetSkinSeries, ResourceRef[PetSkin]] = (
            CategoryMap(category_key='skins')
        )
        pet_skin_series_sub_type_map: CategoryMap[
            int, PetSkinSeriesSubType, ResourceRef[PetSkin]
        ] = CategoryMap(category_key='skins')
        for series_id, reward_data in pet_skin_reward_data.items():
            series_model = PetSkinSeries(id=series_id, name=reward_data['name'])
            if subtypename := reward_data['subtypename']:
                series_ref = ResourceRef.from_model(series_model)
                for sub_type_id, sub_type_name in enumerate(
                    subtypename.split('_'), start=1
                ):
                    sub_type_id = series_id * 1000 + sub_type_id
                    sub_type_model = PetSkinSeriesSubType(
                        id=sub_type_id,
                        name=sub_type_name,
                        series=series_ref,
                    )
                    pet_skin_series_sub_type_map[sub_type_id] = sub_type_model
                    sub_type_ref = ResourceRef.from_model(sub_type_model)
                    series_model.sub_types.append(sub_type_ref)

            pet_skin_series_map[series_id] = series_model
        pet_skin_category_map: CategoryMap[
            int, PetSkinCategory, ResourceRef[PetSkin]
        ] = CategoryMap(category_key='skins')

        for skin_id, pet_skin in pet_skin_data.items():
            pet_id = pet_skin['mon_id']
            category_id = pet_skin.get('type', 0)
            series_id = pet_skin['skin_kind'][0]['skin_type']
            sub_type_name = str(pet_skin['skin_kind'][0]['year'])
            resource_id = 1400000 + skin_id
            if resource_id in real_id_data:
                resource_id = real_id_data[resource_id]

            pet_skin_model = PetSkin(
                id=skin_id,
                name=pet_skin['name'],
                resource_id=resource_id,
                enemy_resource_id=self.pet_left_and_right_data.get(resource_id),
                pet=ResourceRef.from_model(Pet, id=pet_id),
                category=ResourceRef.from_model(PetSkinCategory, id=category_id),
                series=ResourceRef.from_model(PetSkinSeries, id=series_id)
                if series_id
                else None,
            )
            pet_skin_map[skin_id] = pet_skin_model

            skin_ref = ResourceRef.from_model(pet_skin_model)

            if series_id > 0:
                pet_skin_series_map.add_element(series_id, skin_ref)
                if sub_type_name != 0:
                    for value in pet_skin_series_sub_type_map.values():
                        if value.name == sub_type_name:
                            pet_skin_model.sub_type = ResourceRef.from_model(
                                PetSkinSeriesSubType, id=value.id
                            )
                            pet_skin_series_sub_type_map.add_element(value.id, skin_ref)
                            break

            if category_id not in pet_skin_category_map:
                pet_skin_category_map[category_id] = PetSkinCategory(id=category_id)

        return (
            AnalyzeResult(model=PetSkin, data=pet_skin_map),
            AnalyzeResult(model=PetSkinCategory, data=pet_skin_category_map),
            AnalyzeResult(model=PetSkinSeries, data=pet_skin_series_map),
            AnalyzeResult(
                model=PetSkinSeriesSubType, data=pet_skin_series_sub_type_map
            ),
        )
