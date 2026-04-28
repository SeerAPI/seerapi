from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ResistanceSpecifiedItem(TypedDict):
	"""抗性特定道具项"""

	exchange_ctrl_sp: str  # 对应 C# 的 ExchangeCtrlSp
	exchange_weak_sp: str  # 对应 C# 的 ExchangeWeakSp
	target_ctrl_sp: str  # 对应 C# 的 TargetCtrlSp
	target_weak_sp: str  # 对应 C# 的 TargetWeakSp
	exchange_ctrl_cnt: int  # 对应 C# 的 ExchangeCtrlCnt
	exchange_weak_cnt: int  # 对应 C# 的 ExchangeWeakCnt
	id: int  # 对应 C# 的 ID
	target_ctrl_cnt: int  # 对应 C# 的 TargetCtrlCnt
	target_weak_cnt: int  # 对应 C# 的 TargetWeakCnt


class _ResistanceSpecifiedRoot(TypedDict):
	"""抗性特定道具根节点"""

	item: list[ResistanceSpecifiedItem]


class ResistanceSpecifiedItemConfig(TypedDict):
	"""抗性特定道具顶层数据"""

	root: _ResistanceSpecifiedRoot


class ResistanceSpecifiedItemParser(BaseParser[ResistanceSpecifiedItemConfig]):
	"""抗性特定道具配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'ResistanceSpecifiedItem.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'resistanceSpecifiedItem.json'

	def parse(self, data: bytes) -> ResistanceSpecifiedItemConfig:
		reader = BytesReader(data)
		result: ResistanceSpecifiedItemConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()

			for _ in range(count):
				# 按照IItemItem.Parse的顺序读取字段
				exchange_ctrl_cnt = reader.ReadSignedInt()
				exchange_ctrl_sp = reader.ReadUTFBytesWithLength()
				exchange_weak_cnt = reader.ReadSignedInt()
				exchange_weak_sp = reader.ReadUTFBytesWithLength()
				id = reader.ReadSignedInt()
				target_ctrl_cnt = reader.ReadSignedInt()
				target_ctrl_sp = reader.ReadUTFBytesWithLength()
				target_weak_cnt = reader.ReadSignedInt()
				target_weak_sp = reader.ReadUTFBytesWithLength()

				item = ResistanceSpecifiedItem(
					exchange_ctrl_sp=exchange_ctrl_sp,
					exchange_weak_sp=exchange_weak_sp,
					target_ctrl_sp=target_ctrl_sp,
					target_weak_sp=target_weak_sp,
					exchange_ctrl_cnt=exchange_ctrl_cnt,
					exchange_weak_cnt=exchange_weak_cnt,
					id=id,
					target_ctrl_cnt=target_ctrl_cnt,
					target_weak_cnt=target_weak_cnt,
				)
				result['root']['item'].append(item)

		return result
