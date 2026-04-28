"""Bytes reader utilities.

根据反编译的 C# ByteUtil 实现的 Python 版本，提供：
- 基础类型读取（按小端序）：有符号/无符号整型、浮点、布尔、字节
- UTF-8 固定长度字符串读取
- 位数组转换（从低位到高位）

同时提供 `BytesReader` 封装类以便按游标顺序读取。
"""

from __future__ import annotations

import struct

# 常量，对齐 C# 中的长度定义
BYTE_LEN: int = 1
SHORT_LEN: int = 2
INT_LEN: int = 4
LONG_LEN: int = 8
FLOAT_LEN: int = 4
DOUBLE_LEN: int = 8


def _ensure_available(data: bytes, index: int, size: int) -> None:
	if size < 0:
		raise ValueError('size must be non-negative')
	if index < 0:
		raise IndexError('index must be non-negative')
	if index + size > len(data):
		raise IndexError(
			f'reading {size} bytes from index {index} exceeds buffer length {len(data)}'
		)


def to_bit_array(value: int, length: int) -> list[bool]:
	"""按位生成布尔数组（低位在前），与 C# 实现一致。

	value 的类型视为无符号整型位模式。length < 0 将抛出 ValueError。
	"""
	if length < 0:
		raise ValueError('length must be non-negative')
	result: list[bool] = [False] * length
	v = int(value) & ((1 << (max(length, 1))) - 1) if length > 0 else int(value)
	for i in range(length):
		result[i] = (v & 1) == 1
		v >>= 1
	return result


def read_unsigned_byte(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, BYTE_LEN)
	return data[index], index + 1


def read_signed_byte(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, BYTE_LEN)
	b = data[index]
	value = b - 256 if b > 127 else b
	return value, index + 1


def read_boolean(data: bytes, index: int) -> tuple[bool, int]:
	_ensure_available(data, index, BYTE_LEN)
	return (data[index] != 0), index + 1


def read_signed_short(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, SHORT_LEN)
	(value,) = struct.unpack_from('<h', data, index)
	return int(value), index + SHORT_LEN


def read_unsigned_short(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, SHORT_LEN)
	(value,) = struct.unpack_from('<H', data, index)
	return int(value), index + SHORT_LEN


def read_signed_int(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, INT_LEN)
	(value,) = struct.unpack_from('<i', data, index)
	return int(value), index + INT_LEN


def read_unsigned_int(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, INT_LEN)
	(value,) = struct.unpack_from('<I', data, index)
	return int(value), index + INT_LEN


def read_long(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, LONG_LEN)
	(value,) = struct.unpack_from('<q', data, index)
	return int(value), index + LONG_LEN


def read_ulong(data: bytes, index: int) -> tuple[int, int]:
	_ensure_available(data, index, LONG_LEN)
	(value,) = struct.unpack_from('<Q', data, index)
	return int(value), index + LONG_LEN


def read_float(data: bytes, index: int) -> tuple[float, int]:
	_ensure_available(data, index, FLOAT_LEN)
	(value,) = struct.unpack_from('<f', data, index)
	return float(value), index + FLOAT_LEN


def read_double(data: bytes, index: int) -> tuple[float, int]:
	_ensure_available(data, index, DOUBLE_LEN)
	(value,) = struct.unpack_from('<d', data, index)
	return float(value), index + DOUBLE_LEN


def read_utf_bytes(data: bytes, length: int, index: int) -> tuple[str, int]:
	"""读取固定长度的 UTF-8 字符串（不含长度前缀）。"""
	if length < 0:
		raise ValueError('length must be non-negative')
	_ensure_available(data, index, length)
	end = index + length
	return data[index:end].decode('utf-8'), end


class BytesReader:
	"""顺序读取封装，等价于 C# 的按引用索引自增语义。"""

	def __init__(self, data: bytes, position: int = 0) -> None:
		self._data = data
		self._pos = position

	@property
	def position(self) -> int:
		return self._pos

	def remaining(self) -> int:
		return len(self._data) - self._pos

	def eof(self) -> bool:
		return self._pos >= len(self._data)

	def seek(self, position: int) -> None:
		if position < 0 or position > len(self._data):
			raise IndexError('position out of range')
		self._pos = position

	def skip(self, count: int) -> None:
		self.seek(self._pos + count)

	def read_u8(self) -> int:
		value, self._pos = read_unsigned_byte(self._data, self._pos)
		return value

	def read_i8(self) -> int:
		value, self._pos = read_signed_byte(self._data, self._pos)
		return value

	def read_bool(self) -> bool:
		value, self._pos = read_boolean(self._data, self._pos)
		return value

	def read_i16(self) -> int:
		value, self._pos = read_signed_short(self._data, self._pos)
		return value

	def read_u16(self) -> int:
		value, self._pos = read_unsigned_short(self._data, self._pos)
		return value

	def read_i32(self) -> int:
		value, self._pos = read_signed_int(self._data, self._pos)
		return value

	def read_u32(self) -> int:
		value, self._pos = read_unsigned_int(self._data, self._pos)
		return value

	def read_i64(self) -> int:
		value, self._pos = read_long(self._data, self._pos)
		return value

	def read_u64(self) -> int:
		value, self._pos = read_ulong(self._data, self._pos)
		return value

	def read_f32(self) -> float:
		value, self._pos = read_float(self._data, self._pos)
		return value

	def read_f64(self) -> float:
		value, self._pos = read_double(self._data, self._pos)
		return value

	def read_utf(self, length: int) -> str:
		value, self._pos = read_utf_bytes(self._data, length, self._pos)
		return value

	# C# 风格别名
	def ReadUnsignedByte(self) -> int:
		return self.read_u8()

	def ReadSignedByte(self) -> int:
		return self.read_i8()

	def ReadBoolean(self) -> bool:
		return self.read_bool()

	def ReadSignedShort(self) -> int:
		return self.read_i16()

	def ReadUnsignedShort(self) -> int:
		return self.read_u16()

	def ReadSignedInt(self) -> int:
		return self.read_i32()

	def ReadUnsignedInt(self) -> int:
		return self.read_u32()

	def ReadLong(self) -> int:
		return self.read_i64()

	def ReadUlong(self) -> int:
		return self.read_u64()

	def ReadFloat(self) -> float:
		return self.read_f32()

	def ReadDouble(self) -> float:
		return self.read_f64()

	def ReadUTFByte(self, length: int) -> str:
		return self.read_utf(length)

	def ReadUTFBytesWithLength(self) -> str:
		length = self.ReadUnsignedShort()
		return self.read_utf(length)


__all__ = [
	'BYTE_LEN',
	'DOUBLE_LEN',
	'FLOAT_LEN',
	'INT_LEN',
	'LONG_LEN',
	'SHORT_LEN',
	'BytesReader',
	'read_boolean',
	'read_double',
	'read_float',
	'read_long',
	'read_signed_byte',
	'read_signed_int',
	'read_signed_short',
	'read_ulong',
	'read_unsigned_byte',
	'read_unsigned_int',
	'read_unsigned_short',
	'read_utf_bytes',
	'to_bit_array',
]
