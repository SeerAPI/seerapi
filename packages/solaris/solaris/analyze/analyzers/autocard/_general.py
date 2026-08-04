from abc import ABC
from functools import cached_property
from typing import TYPE_CHECKING

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig

if TYPE_CHECKING:
    from solaris.parse.parsers.autocard_content import (
        AutocardContentConfig,
        AutocardContentInfo,
    )
    from solaris.parse.parsers.autocard_nature import (
        AutocardNatureConfig,
        AutocardNatureInfo,
    )
    from solaris.parse.parsers.autocard_role import (
        AutocardRoleConfig,
        AutocardRoleInfo,
    )
    from solaris.parse.parsers.autocard_season_effect import (
        AutocardSeasonEffectConfig,
        AutocardSeasonEffectInfo,
    )


class BaseAutocardAnalyzer(BaseDataSourceAnalyzer, ABC):
    @classmethod
    def get_data_import_config(cls) -> DataImportConfig:
        return DataImportConfig(
            patch_paths=('autocard_type.json',),
            unity_paths=(
                'autocardContent.json',
                'autocardNature.json',
                'autocardRole.json',
                'autocardSeasonEffect.json',
            ),
        )

    @cached_property
    def autocard_content_data(self) -> dict[int, 'AutocardContentInfo']:
        data: AutocardContentConfig = self._get_data('unity', 'autocardContent.json')
        return {item['id']: item for item in data['data']}

    @cached_property
    def autocard_nature_data(self) -> dict[int, 'AutocardNatureInfo']:
        data: AutocardNatureConfig = self._get_data('unity', 'autocardNature.json')
        return {item['id']: item for item in data['data']}

    @cached_property
    def autocard_role_data(self) -> dict[int, 'AutocardRoleInfo']:
        data: AutocardRoleConfig = self._get_data('unity', 'autocardRole.json')
        return {item['id']: item for item in data['data']}

    @cached_property
    def autocard_field_buff_data(self) -> dict[int, 'AutocardSeasonEffectInfo']:
        data: AutocardSeasonEffectConfig = self._get_data(
            'unity', 'autocardSeasonEffect.json'
        )
        return {item['id']: item for item in data['data']}
