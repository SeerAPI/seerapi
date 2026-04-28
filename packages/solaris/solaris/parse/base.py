from abc import ABC, abstractmethod
import json
import os
from typing import Any, Generic, TypeVar

T = TypeVar('T')


def _to_json(data: Any) -> str:
	return json.dumps(data, indent=2, ensure_ascii=False)


class BaseParser(ABC, Generic[T]):
	"""解析器基类"""

	def load_source_config(self) -> bytes:
		"""加载源配置文件"""
		filename = self.source_config_filename()
		if not os.path.exists(filename):
			raise FileNotFoundError(
				f'配置文件不存在: {filename}，'
				f'请检查工作目录和设置的文件名是否正确'
				f'工作目录: {os.getcwd()}'
			)
		with open(filename, 'rb') as f:
			return f.read()

	def save_parsed_config(self, data: T) -> None:
		"""保存解析后的配置文件"""
		filename = self.parsed_config_filename()
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(_to_json(data))

	@classmethod
	@abstractmethod
	def source_config_filename(cls) -> str:
		"""源配置文件名"""
		pass

	@classmethod
	@abstractmethod
	def parsed_config_filename(cls) -> str:
		"""解析后的配置文件名"""
		pass

	@abstractmethod
	def parse(self, data: bytes) -> T:
		"""解析数据"""
		pass


__all__ = ['BaseParser']
