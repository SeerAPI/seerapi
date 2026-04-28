from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ArchivesBook(TypedDict):
	bookid: int
	chapterid: int
	chaptername: str
	id: int
	txt: list[str]
	txtdivide: list[int]


class ArchivesBookConfig(TypedDict):
	data: list[ArchivesBook]


class ArchivesBookParser(BaseParser[ArchivesBookConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'archivesBook.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'archivesBook.json'

	def parse(self, data: bytes) -> ArchivesBookConfig:
		reader = BytesReader(data)
		if not reader.read_bool():
			return ArchivesBookConfig(data=[])

		result = ArchivesBookConfig(data=[])
		for _ in range(reader.read_i32()):
			bookid = reader.read_i32()
			chapterid = reader.read_i32()
			chaptername_len = reader.read_u16()
			chaptername = reader.read_utf(chaptername_len)
			id = reader.read_i32()
			txt = []
			if reader.read_bool():
				txt_count = reader.read_i32()
				txt = [reader.read_utf(reader.read_u16()) for _ in range(txt_count)]

			txtdivide = []
			if reader.read_bool():
				txtdivide_count = reader.read_i32()
				txtdivide = [reader.read_i32() for _ in range(txtdivide_count)]

			result['data'].append(
				ArchivesBook(
					bookid=bookid,
					chapterid=chapterid,
					chaptername=chaptername,
					id=id,
					txt=txt,
					txtdivide=txtdivide,
				)
			)

		return result


class ArchivesStoryInfo(TypedDict):
	classid: int
	classname: str
	id: int
	isrec: int
	monid: int
	monname: str
	samemonid: str | None
	storyid: int
	txt: str


class ArchivesStoryConfig(TypedDict):
	data: list[ArchivesStoryInfo]


class ArchivesStoryParser(BaseParser[ArchivesStoryConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'archivesStory.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'archivesStory.json'

	def parse(self, data: bytes) -> ArchivesStoryConfig:
		result = ArchivesStoryConfig(data=[])
		reader = BytesReader(data)
		if not reader.read_bool():
			return result

		for _ in range(reader.read_i32()):
			story_info = ArchivesStoryInfo(
				classid=reader.read_i32(),
				classname=reader.ReadUTFBytesWithLength(),
				id=reader.read_i32(),
				isrec=reader.read_i32(),
				monid=reader.read_i32(),
				monname=reader.ReadUTFBytesWithLength(),
				samemonid=(
					'_'.join(str(reader.read_i32()) for _ in range(reader.read_i32()))
					if reader.read_bool()
					else None
				),
				storyid=reader.read_i32(),
				txt=reader.ReadUTFBytesWithLength(),
			)
			result['data'].append(story_info)

		return result


# petbook 配置结构与解析器
class _PbPlaceItem(TypedDict):
	"""地点条目"""

	desc: str
	go: str
	redirect: str
	mintmark: list[int]
	id: int
	image_id: int
	label: int
	mon_id: int
	type: int


class _PbBranch(TypedDict):
	"""分支信息"""

	title: str
	id: int
	intro: str
	place: list[_PbPlaceItem]


class _PbTypeItem(TypedDict):
	"""类型条目"""

	branch: list[_PbBranch]
	id: int


class _PbPetDataItem(TypedDict):
	"""热点精灵数据"""

	tag_b: list[int]
	id: int
	pid: int
	tag_a: int


class _PbItem(TypedDict):
	"""热点信息条目"""

	intro: str
	place: list[_PbPlaceItem]


class _PbHotPet(TypedDict):
	pet_data: list[_PbPetDataItem]
	type: list[_PbTypeItem]


class _PbHotspot(TypedDict):
	item: _PbItem | None


class _PbMonsterItem(TypedDict):
	"""精灵条目（petbook）"""

	def_name: str
	features: str
	target: str
	id: int


class _PbRecMintmark(TypedDict):
	place: list[_PbPlaceItem]


class _PbRoot(TypedDict):
	hot_pet: _PbHotPet | None
	hotspot: _PbHotspot | None
	monster: list[_PbMonsterItem]
	rec_mintmark: _PbRecMintmark | None


class PetBookConfig(TypedDict):
	root: _PbRoot


class PetBookParser(BaseParser[PetBookConfig]):
	"""解析 petbook.bytes（正式服百科）"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'petbook.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petbook.json'

	def parse(self, data: bytes) -> PetBookConfig:
		reader = BytesReader(data)
		result: PetBookConfig = {
			'root': {
				'hot_pet': None,
				'hotspot': None,
				'monster': [],
				'rec_mintmark': None,
			}
		}
		if not reader.read_bool():
			return result

		# HotPet（可选）
		if reader.read_bool():
			pet_data: list[_PbPetDataItem] = []
			if reader.read_bool():
				n = reader.read_i32()
				for _ in range(n):
					item_tag_a = reader.read_i32()
					tag_b: list[int] = []
					if reader.read_bool():
						m = reader.read_i32()
						tag_b = [reader.read_i32() for _ in range(m)]
					item_id = reader.read_i32()
					item_pid = reader.read_i32()
					pet_data.append(
						{
							'tag_b': tag_b,
							'id': item_id,
							'pid': item_pid,
							'tag_a': item_tag_a,
						}
					)

			types: list[_PbTypeItem] = []
			if reader.read_bool():
				n = reader.read_i32()
				for _ in range(n):
					types.append(self._read_type_item(reader))

			result['root']['hot_pet'] = {'pet_data': pet_data, 'type': types}

		# Hotspot（可选）
		if reader.read_bool():
			item_obj: _PbItem | None = None
			if reader.read_bool():
				intro = reader.ReadUTFBytesWithLength()
				places = []
				if reader.read_bool():
					pcnt = reader.read_i32()
					for _ in range(pcnt):
						places.append(self._read_place_pb(reader))
				item_obj = {'intro': intro, 'place': places}
			result['root']['hotspot'] = {'item': item_obj}

		# Monster（可选数组）
		if reader.read_bool():
			mcnt = reader.read_i32()
			for _ in range(mcnt):
				result['root']['monster'].append(self._read_monster_pb(reader))

		# RecMintmark（可选）
		if reader.read_bool():
			places: list[_PbPlaceItem] = []
			if reader.read_bool():
				pcnt = reader.read_i32()
				for _ in range(pcnt):
					places.append(self._read_place_pb(reader))
			result['root']['rec_mintmark'] = {'place': places}

		return result

	def _read_type_item(self, reader: BytesReader) -> _PbTypeItem:
		branches: list[_PbBranch] = []
		if reader.read_bool():
			b_cnt = reader.read_i32()
			for _ in range(b_cnt):
				branches.append(self._read_branch_item(reader))
		id = reader.read_i32()
		return {'branch': branches, 'id': id}

	def _read_branch_item(self, reader: BytesReader) -> _PbBranch:
		id = reader.read_i32()
		intro = reader.ReadUTFBytesWithLength()
		places: list[_PbPlaceItem] = []
		if reader.read_bool():
			ccnt = reader.read_i32()
			for _ in range(ccnt):
				places.append(self._read_place_pb(reader))

		title = reader.ReadUTFBytesWithLength()
		return {
			'title': title,
			'id': id,
			'intro': intro,
			'place': places,
		}

	def _read_place_pb(self, reader: BytesReader) -> _PbPlaceItem:
		desc = reader.ReadUTFBytesWithLength()
		go = reader.ReadUTFBytesWithLength()
		pid = reader.read_i32()
		image_id = reader.read_i32()
		label = reader.read_i32()
		mintmark: list[int] = []
		if reader.read_bool():
			m = reader.read_i32()
			mintmark = [reader.read_i32() for _ in range(m)]
		redirect = reader.ReadUTFBytesWithLength()
		mon_id = reader.read_i32()
		type_val = reader.read_i32()
		return {
			'desc': desc,
			'go': go,
			'redirect': redirect,
			'mintmark': mintmark,
			'id': pid,
			'image_id': image_id,
			'label': label,
			'mon_id': mon_id,
			'type': type_val,
		}

	def _read_monster_pb(self, reader: BytesReader) -> _PbMonsterItem:
		def_name = reader.ReadUTFBytesWithLength()
		features = reader.ReadUTFBytesWithLength()
		mid = reader.read_i32()
		target = reader.ReadUTFBytesWithLength()
		return {
			'def_name': def_name,
			'features': features,
			'target': target,
			'id': mid,
		}


# pet_advance 配置结构与解析器
class _PaBackItem(TypedDict):
	"""回收条目"""

	desc: str
	id: int
	is_back: int
	monster_id: int
	per_need_coin_b: int
	task_id: int


class _PaBackMonsters(TypedDict):
	back: list[_PaBackItem]
	free_cnt: int
	refresh_add_cost: int
	refresh_base_cost: int
	refresh_max_cost: int


class _PaExchange(TypedDict):
	item_id: list[int]
	product_id: list[int]


class _PaRace(TypedDict):
	new_race: list[int]
	old_race: list[int]


class _PaSpMove(TypedDict):
	sp_moves: list[int]


class _PaExMove(TypedDict):
	extra_moves: int


class _PaAdvEffect(TypedDict):
	des: str
	id: int


class _PaAdvances(TypedDict):
	adv_effect: _PaAdvEffect | None
	ex_move: _PaExMove | None
	race: _PaRace | None
	sp_move: _PaSpMove | None
	adv_type: int
	monster_id: int


class _PaBattle(TypedDict):
	task: list['_PaTaskItem']
	free_battle_key: int


class _PaTaskItem(TypedDict):
	advances: _PaAdvances | None
	battle: _PaBattle | None
	desc: str
	exchange: _PaExchange | None
	all_progress: int
	battle_boss: int
	id: int
	out_item_key: int
	per_cost_coin_a: int


class _PaRoot(TypedDict):
	back_monsters: _PaBackMonsters | None
	task: list[_PaTaskItem]


class PetAdvanceConfig(TypedDict):
	root: _PaRoot


class PetAdvanceParser(BaseParser[PetAdvanceConfig]):
	"""解析 pet_advance.bytes（进化/养成）"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pet_advance.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petAdvance.json'

	def parse(self, data: bytes) -> PetAdvanceConfig:
		reader = BytesReader(data)
		result: PetAdvanceConfig = {'root': {'back_monsters': None, 'task': []}}
		if not reader.read_bool():
			return result

		# BackMonsters（可选）
		if reader.read_bool():
			back_list: list[_PaBackItem] = []
			free_cnt = 0
			refresh_add_cost = 0
			refresh_base_cost = 0
			refresh_max_cost = 0
			if reader.read_bool():
				n = reader.read_i32()
				for _ in range(n):
					# IBackItem: ID, IsBack, MonsterId, PerNeedCoinB, TaskId, desc
					bid = reader.read_i32()
					is_back = reader.read_i32()
					monster_id = reader.read_i32()
					per_need_coin_b = reader.read_i32()
					task_id = reader.read_i32()
					desc = reader.ReadUTFBytesWithLength()
					back_list.append(
						{
							'id': bid,
							'is_back': is_back,
							'monster_id': monster_id,
							'per_need_coin_b': per_need_coin_b,
							'task_id': task_id,
							'desc': desc,
						}
					)
			free_cnt = reader.read_i32()
			refresh_add_cost = reader.read_i32()
			refresh_base_cost = reader.read_i32()
			refresh_max_cost = reader.read_i32()
			result['root']['back_monsters'] = {
				'back': back_list,
				'free_cnt': free_cnt,
				'refresh_add_cost': refresh_add_cost,
				'refresh_base_cost': refresh_base_cost,
				'refresh_max_cost': refresh_max_cost,
			}

		# Task 数组（可选）存在于 Root.Task 的布尔里（由 IRoot 控制）
		if reader.read_bool():
			n = reader.read_i32()
			for _ in range(n):
				result['root']['task'].append(self._read_task_item(reader))

		return result

	def _read_task_item(self, reader: BytesReader) -> _PaTaskItem:
		# ITaskItem 读取顺序：
		#    Advances?
		# -> AllProgress
		# -> Battle?
		# -> BattleBoss
		# -> Desc
		# -> Exchange?
		# -> ID
		# -> OutItemKey
		# -> PerCostCoinA
		adv: _PaAdvances | None = None
		if reader.read_bool():
			adv = self._read_advances(reader)
		all_progress = reader.read_i32()
		battle: _PaBattle | None = None
		if reader.read_bool():
			battle = self._read_battle(reader)
		battle_boss = reader.read_i32()
		desc = reader.ReadUTFBytesWithLength()
		exchange: _PaExchange | None = None
		if reader.read_bool():
			exchange = self._read_exchange(reader)
		id_val = reader.read_i32()
		out_item_key = reader.read_i32()
		per_cost_coin_a = reader.read_i32()
		return {
			'advances': adv,
			'battle': battle,
			'desc': desc,
			'exchange': exchange,
			'all_progress': all_progress,
			'battle_boss': battle_boss,
			'id': id_val,
			'out_item_key': out_item_key,
			'per_cost_coin_a': per_cost_coin_a,
		}

	def _read_exchange(self, reader: BytesReader) -> _PaExchange:
		item_id: list[int] = []
		product_id: list[int] = []
		if reader.read_bool():
			n = reader.read_i32()
			item_id = [reader.read_i32() for _ in range(n)]
		if reader.read_bool():
			n = reader.read_i32()
			product_id = [reader.read_i32() for _ in range(n)]
		return {'item_id': item_id, 'product_id': product_id}

	def _read_battle(self, reader: BytesReader) -> _PaBattle:
		free_battle_key = reader.read_i32()
		tasks: list[_PaTaskItem] = []
		if reader.read_bool():
			n = reader.read_i32()
			for _ in range(n):
				tasks.append(self._read_task_item(reader))
		return {'task': tasks, 'free_battle_key': free_battle_key}

	def _read_race(self, reader: BytesReader) -> _PaRace:
		new_race: list[int] = []
		old_race: list[int] = []
		if reader.read_bool():
			n = reader.read_i32()
			new_race = [reader.read_i32() for _ in range(n)]
		if reader.read_bool():
			n = reader.read_i32()
			old_race = [reader.read_i32() for _ in range(n)]
		return {'new_race': new_race, 'old_race': old_race}

	def _read_advances(self, reader: BytesReader) -> _PaAdvances:
		adv_effect: _PaAdvEffect | None = None
		if reader.read_bool():
			des = reader.ReadUTFBytesWithLength()
			id_val = reader.read_i32()
			adv_effect = {'des': des, 'id': id_val}
		adv_type = reader.read_i32()
		monster_id = reader.read_i32()
		race: _PaRace | None = None
		if reader.read_bool():
			race = self._read_race(reader)
		ex_move: _PaExMove | None = None
		if reader.read_bool():
			ex_move = {'extra_moves': reader.read_i32()}
		sp_move: _PaSpMove | None = None
		if reader.read_bool():
			sp_list: list[int] = []
			if reader.read_bool():
				n = reader.read_i32()
				sp_list = [reader.read_i32() for _ in range(n)]
			sp_move = {'sp_moves': sp_list}
		return {
			'adv_effect': adv_effect,
			'ex_move': ex_move,
			'race': race,
			'sp_move': sp_move,
			'adv_type': adv_type,
			'monster_id': monster_id,
		}
