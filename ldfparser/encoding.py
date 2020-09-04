from typing import List, Dict, Callable, Union, Any, Tuple

class ValueConverter():
	def encode(self, value: Union[str, int, float]) -> int:
		raise NotImplementedError()

	def decode(self, value: int) -> Union[str, int, float]:
		raise NotImplementedError()

class PhysicalValue(ValueConverter):
	def __init__(self, phy_min: int, phy_max: int, scale: float, offset: float, unit: str = None):
		self.phy_min = phy_min
		self.phy_max = phy_max
		self.scale = scale
		self.offset = offset
		self.unit = unit

	def encode(self, value: Union[str, int, float]) -> int:
		"""

		"""
		num = 0.0
		if isinstance(value, str) and self.unit is not None and value.endswith(self.unit):
			num = float(value[:-len(self.unit)])
		else:
			num = float(value)
		
		raw = self.offset
		if self.scale != 0:
			raw = int((num - self.offset) / self.scale)
		
		if raw < self.phy_min or raw > self.phy_max:
			raise ValueError("value: " + str(raw) + " out of range (" + str(self.phy_min) + ", " + str(self.phy_max) + ")")
		
		return raw

	def decode(self, value: int) -> float:
		if value < self.phy_min or value > self.phy_max:
			raise ValueError("value: " + str(value) + " out of range (" + str(self.phy_min) + ", " + str(self.phy_max) + ")")
		
		return float(value * self.scale + self.offset)

class LogicalValue(ValueConverter):
	def __init__(self, phy_value: int, text: str):
		self.phy_value = phy_value
		self.text = text

	def encode(self, value: str) -> int:
		"""

		"""
		if not isinstance(value, str) or value != self.text:
			raise ValueError("value: " + str(value) + " not equal to " + self.text)
		return self.phy_value

	def decode(self, value: int) -> str:
		if not isinstance(value, int) or value != self.phy_value:
			raise ValueError("value: " + str(value) + " not equal to " + str(self.phy_value))
		return self.text

class LinSignalType:

	def __init__(self, name, converters: List[ValueConverter]):
		self.name = name
		self._converters = converters

	def encode(self, value: Union[str, int, float]) -> int:
		out = None
		for encoder in self._converters:
			try:
				out = encoder.encode(value)
				break
			except ValueError:
				pass
		
		if out is None:
			raise ValueError("cannot encode " + str(value) + " as " + self.name)
		return out

	def decode(self, value: int) -> Union[str, int, float]:
		out = None
		for decoder in self._converters:
			try:
				out = decoder.decode(value)
				break
			except ValueError:
				pass
		
		if out is None:
			raise ValueError("cannot decode " + str(value) + " as " + self.name)
		return out