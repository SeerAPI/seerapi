from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class UnbindMintinfoItem(TypedDict):
	"""解绑刻印信息项"""

	mintmark_id: int  # 对应 C# 的 MintmarkID
	need_consume_num: int  # 对应 C# 的 NeedConsumeNum


class UnbindActivity(TypedDict):
	"""解绑活动"""

	unbindmintinfo: list[UnbindMintinfoItem]  # 对应 C# 的 Unbindmintinfo 数组


class UnbindMintinfoConfig(TypedDict):
	"""解绑刻印信息顶层数据"""

	unbind_activity: UnbindActivity | None  # 对应 C# 的 UnbindActivity


class UnbindMintinfoParser(BaseParser[UnbindMintinfoConfig]):
	"""解绑刻印信息配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Unbindmintinfo.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'unbindMintinfo.json'

	def parse(self, data: bytes) -> UnbindMintinfoConfig:
		reader = BytesReader(data)
		result: UnbindMintinfoConfig = {'unbind_activity': None}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 读取UnbindActivity数据
		unbind_activity: UnbindActivity | None = None
		if reader.ReadBoolean():
			# 读取Unbindmintinfo数组
			unbindmintinfo_items: list[UnbindMintinfoItem] = []
			if reader.ReadBoolean():
				item_count = reader.ReadSignedInt()

				for _ in range(item_count):
					# 按照IUnbindmintinfoItem.Parse的顺序读取字段
					mintmark_id = reader.ReadSignedInt()
					need_consume_num = reader.ReadSignedInt()

					item = UnbindMintinfoItem(
						mintmark_id=mintmark_id, need_consume_num=need_consume_num
					)
					unbindmintinfo_items.append(item)

			unbind_activity = UnbindActivity(unbindmintinfo=unbindmintinfo_items)

		result['unbind_activity'] = unbind_activity

		return result
