import bitstruct

from typing import List, Dict, Callable, Union, Any, Tuple
from collections import OrderedDict

from ldfparser.encoding import LinSignalType

class LinSignal:

	def __init__(self, name: str, width: int, init_value: List[int]):
		self.name = name
		self.width = width
		self.init_value = init_value

	def __str__(self):
		return "Signal(name=" + self.name + ")"

class LinFrame:

	def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
		self.frame_id = frame_id
		self.name = name
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
				pattern += "p" + str(padding)
				offset += padding
			if offset + signal[1].width > frame_bits:
				raise ValueError(str(self) + ":" + str(signal[1]) + " out of frame")
			pattern += "u" + str(signal[1].width)
			offset += signal[1].width
		if offset < frame_bits:
			pattern += "p" + str(frame_bits - offset)
		return pattern


	def raw(self, data: Dict[str, int]) -> bytearray:
		"""
		Returns a bytearray (frame content) by using the raw signal values provided
		"""
		message = []
		for signal in self.signals:
			if data.get(signal.name):
				message.append(data.get(signal.name))
			else:
				message.append(signal.init_value[0])
		return self._flip_bytearray(self._packer.pack(*message))

	def data(self, data: Dict[str, Union[str, int, float]], converters: Dict[str, LinSignalType]) -> bytearray:
		"""
		Returns a bytearray (frame content) by using the human readable signal values
		"""
		converted = {}
		for value in data.items():
			if converters[value[0]] is None:
				raise ValueError('No encoder found for ' + value[0])
			converted[value[0]] = converters[value[0]].encode(value[1])
		return self.raw(converted)

	def parse_raw(self, data: bytearray) -> Dict[str, int]:
		"""
		Returns a mapping between Signal names and their raw physical values in the given message
		"""
		message = {}
		unpacked = self._packer.unpack(self._flip_bytearray(data))
		for i in range(len(unpacked)):
			message[self.signals[i].name] = unpacked[i]
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
			output[value[0]] = converters[value[0]].decode(value[1])
		return output

	def compare(self, previous: bytearray, current: bytearray) -> Dict[str, int]:
		"""
		Returns a mapping between Signal names and their values, the result will
		only contain signals that have changed compared to the previous message
		"""
		prev = self.parse(previous)
		curr = self.parse(current)
		raise NotImplementedError()

	def __str__(self):
		return "Frame(id=" + str(self.frame_id) + ", name=" + self.name + ")"

	def _flip_bytearray(self, data: bytearray) -> bytearray:
		flipped = bytearray()
		for i in data:
			flipped.append(int('{:08b}'.format(i)[::-1], 2))
		return flipped

