from collections.abc import Mapping
from typing import Any, TypeVar, cast

from seerapi_models.build_model import ConvertToORM
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, inspect, select
from sqlmodel.main import FieldInfo

from solaris.analyze.typing_ import ResModel


def is_mapped_class(cls: type) -> bool:
	if model_config := getattr(cls, 'model_config', None):
		return model_config.get('table', False)

	return False


def create_foreign_key_name(name: str) -> str:
	return f'{name}_id'


def get_class_by_tablename(table_fullname: str) -> type[SQLModel] | None:
	"""返回映射到表的类引用。

	:param table_fullname: 表全名的字符串。
	:return: 类引用或 None。
	"""
	for c in SQLModel._sa_registry._class_registry.values():
		if hasattr(c, '__table__') and c.__table__.fullname == table_fullname:  # type: ignore
			return cast(type[SQLModel], c)


class DBManager:
	engine: Engine | None = None

	def __init__(self, db_url: str, echo: bool = False, **kwargs) -> None:
		self._kwargs = {'url': db_url, 'echo': echo, **kwargs}

	def init(self) -> None:
		self.engine = create_engine(**self._kwargs)
		SQLModel.metadata.create_all(self.engine)

	@property
	def initialized(self) -> bool:
		return self.engine is not None

	def get_session(self) -> Session:
		return Session(self.engine)


T = TypeVar('T')


def write_once(session: Session, data: T) -> T:
	"""写入单条数据到数据库并返回刷新后的实例。

	将数据对象添加到数据库会话中，提交事务，并刷新对象以获取数据库生成的字段值（如自增ID）。

	Args:
		session: SQLModel数据库会话实例，用于执行数据库操作
		data: 要写入的数据对象，必须是SQLModel实例或兼容的ORM对象

	Returns:
		写入并刷新后的数据对象，包含数据库生成的字段值（如ID、时间戳等）

	"""
	session.add(data)
	session.commit()
	session.refresh(data)
	return data


def get_orm_relationship_ref(model: type[SQLModel]) -> dict[str, type]:
	"""获取SQLModel模型中所有关系字段的信息

	遍历模型的所有字段，识别出具有关系约束的字段，并解析其关系引用关系。

	Args:
		model: 要分析的SQLModel模型类

	Returns:
		字典，键为当前模型中的关系字段名，值为被引用的表模型类
	"""
	return {
		name: rel.mapper.class_ for name, rel in inspect(model).relationships.items()
	}


def get_orm_link_relationship(model: type[SQLModel]) -> dict[str, type[SQLModel]]:
	"""获取SQLModel模型中所有外键字段的信息

	遍历模型的所有字段，识别出具有外键约束的字段，并解析其外键引用关系。

	Args:
		model: 要分析的SQLModel模型类

	Returns:
		字典，键为当前模型中的外键字段名，值为被引用的表模型类
	"""
	link_relationships = {}
	for name, field in model.__sqlmodel_relationships__.items():
		link_model: type[SQLModel] | None = None
		if field.link_model is not None:
			link_model = field.link_model
		elif field.sa_relationship_kwargs is not None:
			link_table_name = field.sa_relationship_kwargs.get('secondary')
			if link_table_name is None:
				continue
			link_model = get_class_by_tablename(link_table_name)
		else:
			continue
		link_relationships[name] = link_model

	return link_relationships


def get_orm_foreign_key_info(
	model: type[SQLModel],
) -> dict[str, tuple[type[SQLModel], str]]:
	"""获取SQLModel模型中所有外键字段的信息

	遍历模型的所有字段，识别出具有外键约束的字段，并解析其外键引用关系。

	Args:
		model: 要分析的SQLModel模型类

	Returns:
		字典，键为当前模型中的外键字段名，值为元组(被引用的表模型类, 被引用表中的字段名)
	"""
	foreign_key_names = {}
	for name, field in model.model_fields.items():
		field = cast(FieldInfo, field)
		if field.foreign_key is None:
			continue

		foreign_key_name, field_name = field.foreign_key.split('.')
		foreign_key_table = get_class_by_tablename(foreign_key_name)
		if foreign_key_table is None:
			raise ValueError(f'Foreign key table {foreign_key_name} not found')

		foreign_key_names[name] = (foreign_key_table, field_name)
	return foreign_key_names


def get_item_id(session: Session, item: Any) -> int:
	"""获取关联数据的ID

	先检查输入的item是否存在ID，如果存在则直接返回，否则会自动写入数据库并返回ID

	Args:
		session: 数据库会话
		item: 关联数据项

	Returns:
		数据项的ID

	Raises:
		ValueError: 当数据项没有ID时抛出异常
	"""
	item_id = getattr(item, 'id', None)
	if item_id is None:
		if isinstance(item, ConvertToORM):
			item = item.to_orm()
		if is_mapped_class(type(item)):
			item_id = write_once(session, item).id
		else:
			raise ValueError(f'Invalid item type: {type(item)}')

	if item_id is None:
		raise ValueError(f'Item {item} has no id')

	return item_id


def write_result_to_db(session: Session, data: Mapping[int, ResModel]) -> None:
	"""将分析结果写入数据库

	Args:
		session: 数据库会话
		data: 分析结果，键为ID，值为模型实例
	"""
	for model_id, model in data.items():
		orm_obj = None
		if isinstance(model, ConvertToORM):
			orm_obj = model.to_orm()
		elif is_mapped_class(type(model)):
			orm_obj = model
		else:
			continue

		orm_type = type(orm_obj)
		orm_obj.id = orm_obj.id or model_id
		if (
			session.exec(select(orm_type).where(orm_type.id == orm_obj.id)).first()
			is None
		):
			session.add(orm_obj)

		relationship_ref = get_orm_relationship_ref(orm_type)
		for field_name, _ in relationship_ref.items():
			if (rel_obj := getattr(orm_obj, field_name, None)) is None:
				continue

			id_field_name = create_foreign_key_name(field_name)
			if not hasattr(rel_obj, id_field_name):
				continue

			rel_id = get_item_id(session, rel_obj)
			setattr(orm_obj, id_field_name, rel_id)

		# 获取当前ORM对象的链接关系表信息并遍历每个链接关系
		link_relationships = get_orm_link_relationship(orm_type)
		for field_name, link_model in link_relationships.items():
			current_model_field = None
			target_model_field = None

			# 通过 SQLAlchemy 关系属性的 synchronize_pairs
			# 确定链接表中的字段映射，
			# 可正确处理自引用多对多的情况
			mapper = inspect(orm_type)
			rel_prop = mapper.relationships[field_name]  # type: ignore
			if rel_prop.secondary is not None:
				for _, link_col in rel_prop.synchronize_pairs:
					current_model_field = link_col.key
				for _, col in rel_prop.secondary_synchronize_pairs:
					target_model_field = col.key
			else:
				fk_info = get_orm_foreign_key_info(link_model)
				for fk_name, (fk_tbl, _) in fk_info.items():
					if fk_tbl is orm_type:
						current_model_field = fk_name
					else:
						target_model_field = fk_name

			# 遍历原始模型中的关联数据，为每个数据创建链接表对象
			for item in getattr(model, field_name, []) or []:
				if current_model_field is None or target_model_field is None:
					raise ValueError(
						'Current model field or target model '
						f'field is not found: {field_name}'
					)
				# 获取关联数据ID
				item_id = get_item_id(session, item)
				# 创建链接表的实例对象
				link_obj = link_model(
					**{
						current_model_field: orm_obj.id,
						target_model_field: item_id,
					}
				)
				statement = select(link_model).where(
					getattr(link_model, current_model_field) == orm_obj.id,
					getattr(link_model, target_model_field) == item_id,
				)
				if session.exec(statement).first() is None:
					session.add(link_obj)

	session.commit()
