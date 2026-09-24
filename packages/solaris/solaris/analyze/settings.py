from pathlib import Path
from typing_extensions import Self

from pydantic import model_validator

from seerapi_models.metadata import ApiMetadata
from solaris.settings import ENV_PREFIX, SETTINGS_CONFIG, BaseSettings


class ApiMetadataSettings(ApiMetadata, BaseSettings): ...


class DataSourceDirSettings(BaseSettings):
    model_config = SETTINGS_CONFIG | {'env_prefix': f'{ENV_PREFIX}DATA_'}
    BASE_DIR: Path = Path('./source')
    PATCH_DIR: Path = Path(BASE_DIR, 'patch')
    HTML5_DIR: Path = Path(BASE_DIR, 'html5')
    UNITY_DIR: Path = Path(BASE_DIR, 'unity')
    FLASH_DIR: Path = Path(BASE_DIR, 'flash')

    @model_validator(mode='after')
    def combine_dirs(self) -> Self:
        # 分类目录未显式指定（环境变量或构造参数）时，一律从当前 BASE_DIR 派生，
        # 保证 BASE_DIR 来自 -w/--source-dir 或环境变量时子目录跟随变化
        for field_name, sub_dir in (
            ('PATCH_DIR', 'patch'),
            ('HTML5_DIR', 'html5'),
            ('UNITY_DIR', 'unity'),
            ('FLASH_DIR', 'flash'),
        ):
            if field_name not in self.model_fields_set:
                setattr(self, field_name, self.BASE_DIR / sub_dir)
        return self
