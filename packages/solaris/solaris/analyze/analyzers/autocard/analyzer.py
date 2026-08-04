from typing import cast

from seerapi_models import AutocardField
from seerapi_models.autocard import (
    Autocard,
    AutocardCardType,
    AutocardElementType,
    AutocardRole,
    PetAutocard,
    SpellAutocard,
    card_is_spell,
)
from seerapi_models.autocard.field_buff import Buff
from seerapi_models.build_model import BaseResModel
from seerapi_models.common import ResourceRef
from solaris.analyze.analyzers.autocard._general import BaseAutocardAnalyzer
from solaris.analyze.typing_ import AnalyzeResult


class AutocardCardAnalyzer(BaseAutocardAnalyzer):
    @classmethod
    def get_result_res_models(cls) -> tuple[type[BaseResModel], ...]:
        return (
            Autocard,
            PetAutocard,
            SpellAutocard,
            AutocardCardType,
            AutocardElementType,
            AutocardRole,
            AutocardField,
        )

    def analyze(self) -> tuple[AnalyzeResult, ...]:
        cards: dict[int, Autocard] = {}
        pet_autocard_map: dict[int, PetAutocard] = {}
        spell_autocard_map: dict[int, SpellAutocard] = {}

        for item in self.autocard_content_data.values():
            id_ = item['id']
            type_id = item['type']
            element_type_id = item['nature']

            awaken_card_id = None
            attack = None
            health = None
            is_awakened = bool(item['compose'])
            if not card_is_spell(type_id):
                awaken_card_id = item['compose_to']
                attack = item['attack']
                health = item['health']

            cards[id_] = Autocard(
                id=id_,
                name=item['name'],
                description=item['card_txt'],
                level=item['level'],
                cost=item['cost'],
                attack=attack,
                health=health,
                type=ResourceRef.from_model(AutocardCardType, id=type_id),
                element_type=ResourceRef.from_model(
                    AutocardElementType, id=element_type_id
                ),
                is_awakened=is_awakened,
                awaken_card=ResourceRef.from_model(Autocard, id=awaken_card_id)
                if awaken_card_id
                else None,
                is_token=type_id in (2, 4),
            )

        for card in cards.values():
            if card_is_spell(card.type.id) or card.awaken_card is None:
                continue
            awakened_card = cards.get(card.awaken_card.id)
            if awakened_card is None:
                continue
            awakened_card.non_awaken_card = ResourceRef.from_model(card)

        for card in cards.values():
            if card_is_spell(card.type.id):
                spell_autocard_map[card.id] = cast(SpellAutocard, card.to_detailed())
            else:
                pet_autocard_map[card.id] = cast(PetAutocard, card.to_detailed())

        types: dict[int, AutocardCardType] = {}
        for id_, item in self._get_data('patch', 'autocard_type.json').items():
            types[id_] = AutocardCardType(id=id_, name=item['name'], autocard=[])

        element_types: dict[int, AutocardElementType] = {}
        for id_, item in self.autocard_nature_data.items():
            element_types[id_] = AutocardElementType(
                id=id_, name=item['name'], autocard=[], role=[]
            )

        roles: dict[int, AutocardRole] = {}
        for id_, item in self.autocard_role_data.items():
            if id_ >= 10000:
                continue
            element_type_id = item['nature']
            if element_type_id == 0:
                element_type_id = 999
            is_passive_skill = not bool(item['skill_type'])
            if is_passive_skill:
                skill_cost = None
                skill_game_limit = None
                skill_round_limit = None
            else:
                skill_cost = item['skill_cost_num']
                skill_game_limit = item['skill_game_limit']
                skill_round_limit = item['skill_round_limit']
            roles[id_] = AutocardRole(
                id=id_,
                name=item['name'],
                description=item['desc'],
                health=item['health'],
                skill_desc=item['skill_txt'],
                skill_cost=skill_cost,
                skill_game_limit=skill_game_limit,
                skill_round_limit=skill_round_limit,
                element_type=ResourceRef.from_model(
                    AutocardElementType, id=element_type_id
                ),
                is_passive_skill=is_passive_skill,
            )

        for card in cards.values():
            if card.type.id in types:
                types[card.type.id].autocard.append(ResourceRef.from_model(card))
            if card.element_type.id in element_types:
                element_types[card.element_type.id].autocard.append(
                    ResourceRef.from_model(Autocard, id=card.id)
                )

        fields: dict[int, AutocardField] = {
            item['effectGroup']: AutocardField(
                id=item['effectGroup'], name=item['effectName'], buff_stage={}
            )
            for item in self.autocard_field_buff_data.values()
            if item['stageLevel'] == 0
        }

        for item in self.autocard_field_buff_data.values():
            group_id = item['effectGroup']
            if group_id not in fields:
                continue

            stage_level = item['stageLevel']
            buff = Buff(
                name=item['effectName'],
                description=item['effectTxt'],
                open_turn=item['opTurn'],
            )
            fields[group_id].buff_stage.setdefault(stage_level, []).append(buff)

        return (
            AnalyzeResult(model=Autocard, data=cards),
            AnalyzeResult(model=PetAutocard, data=pet_autocard_map),
            AnalyzeResult(model=SpellAutocard, data=spell_autocard_map),
            AnalyzeResult(model=AutocardCardType, data=types),
            AnalyzeResult(model=AutocardRole, data=roles),
            AnalyzeResult(model=AutocardElementType, data=element_types),
            AnalyzeResult(model=AutocardField, data=fields),
        )
