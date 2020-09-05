from typing import List, Dict, Callable, Union, Any, Tuple

"""
Contains classes that are used to encode and decode Lin Signals.

Signal encoding is specified in the LIN 2.1 Specification, section 9.2.6.1
"""

class ValueConverter():
	"""
	Value converter is used to convert Lin signal values from and into
	their human readable form
	"""

	def encode(self, value: Any) -> Union[int, List[int]]:
		"""
		Converts the human readable value into the raw bytes that will be sent
		"""
		raise NotImplementedError()

	def decode(self, value: Union[int, List[int]]) -> Any:
		"""
		Converts the received raw bytes into the human readable form
		"""
		raise NotImplementedError()

class PhysicalValue(ValueConverter):
	"""
	Maps values into a range of allowed values
	"""

	def __init__(self, phy_min: int, phy_max: int, scale: float, offset: float, unit: str = None):
		"""
		Specifies a new physical value range that this converter can map values into

		Args:
			
			phymin (int): the lowest raw integer this converter maps to (allowed value: 0-65535)
			
			phymax (int): the highest raw integer this converter maps to (allowed value: 0-65535)
			
			scale (float): the multiplier used when mapping values into this range
			
			offset(float): offset that's appended to the value after scaling
			
			unit(str): optional string representing the unit of this signal (e.g.: RPM, DEG)

		Examples:
			PhysicalValue(0, 255, 0.3922, 0, "%") creates a converter that maps values 0-100% into
			the 0-255 byte value range
		"""
		self.phy_min = phy_min
		self.phy_max = phy_max
		self.scale = scale
		self.offset = offset
		self.unit = unit

	def encode(self, value: Union[str, int, float]) -> int:
		"""
		Encodes the human readable value as an integer

		Args:

			value: 
				when value is a string the encoder will try to remove the unit, afterwards
				the value is mapped into the range

		Returns:

			The value encoded as an integer

		Raises:
			
			ValueError: if the value mapped outside of the physical value range
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
		"""
		Decodes the physical value into the human readable value

		Returns:

			The value as a floating point number

		Raises:
			
			ValueError: if the physical value is out of the range
		"""
		if value < self.phy_min or value > self.phy_max:
			raise ValueError("value: " + str(value) + " out of range (" + str(self.phy_min) + ", " + str(self.phy_max) + ")")
		
		return float(value * self.scale + self.offset)

class LogicalValue(ValueConverter):
	"""
	Maps value to a specific signal value
	"""

	def __init__(self, phy_value: int, info: str = None):
		"""
		Specifies a physical value to be mapped to a human readable value

		Args:

			phyvalue (int): LIN signal value

			info (str): Human readable value, when None encoding and decoding will
			use the phyvalue for testing equality

		Examples:

			LogicalValue(0, "OFF") creates a converter that will map the "OFF" value to
			the 0 byte value
		"""
		self.phy_value = phy_value
		self.info = info

	def encode(self, value: Union[str, int]) -> int:
		"""
		Encodes the human readable value into the physical value

		Args:

			value (str | int): value to encode, when signal info is None the value
			has to equal the physical value

		Returns:
			
			Physical value

		Raises:
			
			ValueError: when the value doesn't match the signal info

		"""
		if self.info is None and value == self.phy_value:
			return self.phy_value
		if value != self.info:
			raise ValueError("value: " + str(value) + " not equal to " + self.info)
		return self.phy_value

	def decode(self, value: int) -> Union[str, int]:
		"""
		Decodes the physical value into human readable value

		Args:

			value(int): value to decode

		Returns:

			Human readable value

		Raises:

			ValueError: when the value doesn't match the physical value
		"""
		if value != self.phy_value:
			raise ValueError("value: " + str(value) + " not equal to " + str(self.phy_value))
		return self.info

class LinSignalType:
	"""
	Equivalent to Signal encoding types in the LDF file, it contains multiple converters
	and will use them to encode and decode values
	"""

	def __init__(self, name, converters: List[ValueConverter]):
		self.name = name
		self._converters = converters

	def encode(self, value: Union[str, int, float]) -> int:
		"""
		Tries to encode the given value through the Physical and Logical value encoders

		Args:

			value: Value to encode

		Returns:

			Encoded value

		Raises:

			ValueError: when none of the converters were able to encode the value into a valid
			physical value
		"""
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
		"""
		Tries to decode the given value through the Physical and Logical value decoders

		Args:

			value: Value to decode

		Returns:

			Decoded value

		Raises:

			ValueError: when none of the converters were able to decode the value into a valid
			human readable value
		"""
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