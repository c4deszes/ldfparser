import bitstruct

from typing import List, Dict, Union, Tuple

from .encoding import LinSignalType


class LinSignal:

	def __init__(self, name: str, width: int, init_value: Union[int, List[int]]):
		self.name: str = name
		self.width: int = width
		self.init_value: Union[int, List[int]] = init_value
		self.publisher = None
		self.subscribers = []

	def is_array(self):
		return isinstance(self.init_value, List)

	@staticmethod
	def create(name: str, width: int, init_value: Union[int, List[int]]):
		if isinstance(init_value, List):
			if width % 8 != 0:
				raise ValueError(f"array signal {name}:{width} must be a multiple of 8 long (8, 16, 24, ..)")
			if width < 8 or width > 64:
				raise ValueError(f"array signal {name}:{width} must be 8-64bits long")
			if len(init_value) != width / 8:
				raise ValueError(f"array signal {name}:{width} init value is invalid {len(init_value)}")
		if isinstance(init_value, int) and (width < 1 or width > 16):
			raise ValueError(f"scalar signal {name}:{width} must be 1-16bits long")
		return LinSignal(name, width, init_value)


class LinFrame:

	def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
		self.frame_id = frame_id
		self.name = name
		self.publisher = None
		self.length = length
		orderedSignals = sorted(signals.items(), key=lambda x: x[0])
		self.signals = [i[1] for i in orderedSignals]
		self._pattern = self._frame_pattern(length * 8, orderedSignals)
		self._packer = bitstruct.compile(self._pattern)

	def _frame_pattern(self, frame_bits: int, signals: List[Tuple[int, LinSignal]]) -> str:
		pattern = "<"
		offset = 0
		for signal in signals:
			if signal[0] < offset:
				raise ValueError(str(self) + ":" + str(signal[1]) + " overlapping")
			if signal[0] != offset:
				padding = signal[0] - offset
				pattern += f"p{padding}"
				offset += padding
			if offset + signal[1].width > frame_bits:
				raise ValueError(f"{signal[1]} with offset {signal[0]} spans outside {self}")
			if signal[1].is_array():
				pattern += "u8" * int(signal[1].width / 8)
			else:
				pattern += f"u{signal[1].width}"
			offset += signal[1].width
		if offset < frame_bits:
			pattern += f"p{frame_bits - offset}"
		return pattern

	def _get_signal(self, name: str):
		return next((x for x in self.signals if x.name == name), None)

	def raw(self, data: Dict[str, int]) -> bytearray:
		"""
		Returns a bytearray (frame content) by using the raw signal values provided
		"""
		message = []
		for signal in self.signals:
			if data.get(signal.name):
				if signal.is_array():
					message += data.get(signal.name)
				else:
					message.append(data.get(signal.name))
			else:
				if signal.is_array():
					message += signal.init_value
				else:
					message.append(signal.init_value)
		return self._flip_bytearray(self._packer.pack(*message))

	def data(self, data: Dict[str, Union[str, int, float]], converters: Dict[str, LinSignalType]) -> bytearray:
		"""
		Returns a bytearray (frame content) by using the human readable signal values
		"""
		converted = {}
		for value in data.items():
			if converters[value[0]] is None:
				raise ValueError('No encoder found for ' + value[0])
			converted[value[0]] = converters[value[0]].encode(value[1], self._get_signal(value[0]))
		return self.raw(converted)

	def parse_raw(self, data: bytearray) -> Dict[str, int]:
		"""
		Returns a mapping between Signal names and their raw physical values in the given message
		"""
		message = {}
		unpacked = self._packer.unpack(self._flip_bytearray(data))
		signal_index = 0
		i = 0
		while i < len(unpacked):
			if self.signals[signal_index].is_array():
				signal_size = int(self.signals[signal_index].width / 8)
				message[self.signals[signal_index].name] = list(unpacked[i:i + signal_size])
				i += signal_size - 1
			else:
				message[self.signals[signal_index].name] = unpacked[i]
			signal_index += 1
			i += 1
		return message

	def parse(self, data: bytearray, converters: Dict[str, LinSignalType]) -> Dict[str, Union[str, int, float]]:
		"""
		Returns a mapping between Signal names and their human readable value
		"""
		tmp = self.parse_raw(data)
		output = {}
		for value in tmp.items():
			if converters[value[0]] is None:
				raise ValueError('No decoder found for ' + value[0])
			output[value[0]] = converters[value[0]].decode(value[1], self._get_signal(value[0]))
		return output

	def _flip_bytearray(self, data: bytearray) -> bytearray:
		flipped = bytearray()
		for i in data:
			flipped.append(int('{:08b}'.format(i)[::-1], 2))
		return flipped
