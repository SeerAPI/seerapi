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
		self.HTML5_DIR = self.HTML5_DIR
		self.PATCH_DIR = self.PATCH_DIR
		self.UNITY_DIR = self.UNITY_DIR
		self.FLASH_DIR = self.FLASH_DIR
		return self
