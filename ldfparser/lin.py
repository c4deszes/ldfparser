import bitstruct

from typing import List, Dict, Callable, Union, Any, Tuple
from collections import OrderedDict

class LinSignal:

	def __init__(self, name: str, width: int, init_value: List[int]):
		self.name = name
		self.width = width
		self.init_value = init_value

class LinFrame:

	def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
		self.frame_id = frame_id
		self.name = name
		self.length = length
		orderedSignals = sorted(signals.items(), key=lambda x: x[0])
		self.signals = [i[1] for i in orderedSignals]
		self._pattern = LinFrame.frame_pattern(length * 8, orderedSignals)
		self._packer = bitstruct.compile(self._pattern)

	@staticmethod
	def frame_pattern(frame_bits: int, signals: List[Tuple[int, LinSignal]]) -> str:
		pattern = ""
		offset = 0
		for signal in signals:
			if signal[0] != offset:
				padding = signal[0] - offset
				pattern += "p" + padding
				offset += padding
			pattern += "u" + str(signal[1].width)
			offset += signal[1].width
		if offset < frame_bits:
			pattern += "p" + str(frame_bits - offset)
		return pattern


	def data(self, data: Dict[str, int]) -> bytearray:
		"""
		
		"""
		message = []
		for signal in self.signals:
			if data.get(signal.name):
				message.append(data.get(signal.name))
			else:
				message.append(signal.init_value[0])
		return self._packer.pack(*message)

	def parse(self, data: bytearray) -> Dict[str, int]:
		"""
		Returns a mapping between Signal names and their values in the given message
		"""
		message = {}
		unpacked = self._packer.unpack(data)
		for i in range(len(unpacked)):
			message[self.signals[i].name] = unpacked[i]
		return message

	def compare(self, previous: bytearray, current: bytearray) -> Dict[str, int]:
		"""
		Returns a mapping between Signals names and their values, the result will
		only contain signals that have changed compared to the previous message
		"""
		prev = self.parse(previous)
		curr = self.parse(current)

