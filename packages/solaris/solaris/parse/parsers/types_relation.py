from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class TypeOpponentItem(TypedDict):
	"""类型对手项"""

	type: str
	multiple: float


class TypeRelationItem(TypedDict):
	"""类型关系项"""

	opponent: list[TypeOpponentItem]  # 对应 C# 的 Opponent 数组
	type: str


class _TypesRelationRoot(TypedDict):
	"""类型关系根节点"""

	relation: list[TypeRelationItem]  # 对应 C# 的 Relation 数组


class TypesRelationConfig(TypedDict):
	"""类型关系顶层数据"""

	root: _TypesRelationRoot


class TypesRelationParser(BaseParser[TypesRelationConfig]):
	"""类型关系配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'typesRelation.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'typesRelation.json'

	def parse(self, data: bytes) -> TypesRelationConfig:
		reader = BytesReader(data)
		result: TypesRelationConfig = {'root': {'relation': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有Relation数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			relation_count = reader.ReadSignedInt()

			for _ in range(relation_count):
				# 读取可选的Opponent数组
				opponent_items: list[TypeOpponentItem] = []
				if reader.ReadBoolean():
					opponent_count = reader.ReadSignedInt()

					for _ in range(opponent_count):
						# 按照IOpponentItem.Parse的顺序读取字段
						multiple = reader.ReadFloat()
						type_name = reader.read_utf(reader.read_u16())

						opponent_item = TypeOpponentItem(
							type=type_name, multiple=multiple
						)
						opponent_items.append(opponent_item)

				# 读取IRelationItem的type字段
				relation_type = reader.read_utf(reader.read_u16())

				relation_item = TypeRelationItem(
					opponent=opponent_items, type=relation_type
				)
				result['root']['relation'].append(relation_item)

		return result
