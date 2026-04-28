from typing_extensions import Self

from pydantic import ValidationError
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

ENV_PREFIX = 'SOLARIS_'
SETTINGS_CONFIG = SettingsConfigDict(
	env_ignore_empty=True,
	env_prefix=ENV_PREFIX,
)


class CreateSettingsError(ValueError):
	def __init__(self, message: str) -> None:
		self.message = message
		super().__init__(message)


class BaseSettings(PydanticBaseSettings):
	model_config = SETTINGS_CONFIG

	@classmethod
	def create_settings(
		cls,
		msg_maps: dict[str, str] | None = None,
		**init_kwargs,
	) -> Self:
		"""创建 settings 类的实例，支持自定义错误消息映射。

		Args:
			msg_maps: 字段名到自定义错误消息的映射字典，用于替换默认的验证错误消息
			**init_kwargs: 传递给 settings 类构造函数的关键字参数，None 值会被过滤掉

		Returns:
			Self: 创建的 settings 类实例

		Raises:
			SettingsError: 当 settings 类验证失败时抛出，包含格式化的错误消息
		"""
		msg_maps = msg_maps or {}
		init_kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
		try:
			return cls(**init_kwargs)
		except ValidationError as e:
			err_msg_list = []
			for error in e.errors():
				loc = '.'.join(str(i) for i in error['loc'])
				msg = msg_maps.get(loc, error['msg'])
				err_msg_list.append(f'{loc}: {msg}')

			raise CreateSettingsError('\n'.join(err_msg_list))
