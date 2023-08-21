"""
Contains classes that are used to encode and decode Lin Signals.

Signal encoding is specified in the LIN 2.1 Specification, section 9.2.6.1
"""
from typing import List, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .signal import LinSignal

class ValueConverter():

    def __init__(self) -> None:
        """
        Value converter is used to convert Lin signal values from and into their human readable form

        Converters shall be reversible, meaning that encoding a value then decoding that output shall
        return the original value.
        """
        pass

    def encode(self, value: Any, signal: 'LinSignal') -> Union[int, List[int]]:
        """
        Converts the human readable value into the raw bytes that will be sent

        :param value: Signal value
        :type value: Any
        :param signal: LIN Signal context
        :type signal: LinSignal
        :return: Raw data as an integer, array signals should return a list
        :rtype: Union[int, List[int]]
        """
        raise NotImplementedError()

    def decode(self, value: Union[int, List[int]], signal: 'LinSignal', keep_unit: bool = False) -> Any:
        """
        Converts the received raw bytes into the human readable form

        :param value: Raw data to convert, array signals have to be passed as a list
        :type value: Union[int, List[int]]
        :param signal: LIN Signal context
        :type signal: LinSignal
        :param keep_unit: when True physical values will have the unit applied and will be
                          returned as strings, defaults to False
        :type keep_unit: bool, optional
        :return: Signal value
        :rtype: Any
        """
        raise NotImplementedError()

class PhysicalValue(ValueConverter):

    def __init__(self, phy_min: int, phy_max: int, scale: float, offset: float, unit: str = None):
        """
        A physical value encoder converts a range of values into a different range of values.

        The formula from raw values into physical values is:

        .. math:: raw * scale + offset

        Example of a raw speed signal in the range of 0-100 being mapped to a the 1000-6000 RPM range:

        .. code-block:: python

            converter = PhysicalValue(phy_min=0, phy_max=100, scale=50, offset=1000, unit='RPM')
            converter.encode("4000 RPM", signal)
            >>> 60
            converter.decode(0, signal)
            >>> "1000 RPM"

        :param phy_min: Minimum raw value
        :type phy_min: int
        :param phy_max: Maximum raw value
        :type phy_max: int
        :param scale: Raw values are multiplied by this value
        :type scale: float
        :param offset: Raw values are offset by this value
        :type offset: float
        :param unit: Physical value unit, e.g.: °C (temperature) or RPM (angular speed),
                     defaults to None
        :type unit: str, optional
        """
        # pylint: disable=too-many-arguments
        self.phy_min = phy_min
        self.phy_max = phy_max
        self.scale = scale
        self.offset = offset
        self.unit = unit

    def encode(self, value: Union[str, int, float], signal: 'LinSignal') -> int:
        if isinstance(value, str) and self.unit is not None and value.endswith(self.unit):
            num = float(value[:-len(self.unit)])
        else:
            num = float(value)

        raw = self.offset
        if self.scale != 0:
            raw = int((num - self.offset) / self.scale)

        if raw < self.phy_min or raw > self.phy_max:
            raise ValueError(f"value: {raw} out of range ({self.phy_min}, {self.phy_max})")

        return raw

    def decode(self, value: int, signal: 'LinSignal', keep_unit: bool = False) -> float:
        if value < self.phy_min or value > self.phy_max:
            raise ValueError(f"value: {value} out of range ({self.phy_min}, {self.phy_max})")

        decoded = float(value * self.scale + self.offset)
        if keep_unit:
            return f"{decoded:.03f} {self.unit}"
        return decoded

class LogicalValue(ValueConverter):

    def __init__(self, phy_value: int, info: str = None):
        """
        A logical value encoder converts a particular value into another value.

        Example of switch value (0/1) being mapped to an on/off values:

        .. code-block:: python

            converter = PhysicalValue(phy_min=0, phy_max=100, scale=50, offset=1000, unit='RPM')
            off_value = LogicalValue(phy_value=0, info='off')
            on_value = LogicalValue(phy_value=1, info='on')
            off_value.encode("off", signal)
            >>> 0
            off_value.decode(1, signal)
            >>> ValueError

        :param phy_value: Physical/Raw value
        :type phy_value: int
        :param info: String value associated with the physical value, defaults to None
        :type info: str, optional
        """
        self.phy_value = phy_value
        self.info = info

    def encode(self, value: Union[str, int], signal: 'LinSignal') -> int:
        if self.info is None and value == self.phy_value:
            return self.phy_value
        if self.info is not None and value == self.info:
            return self.phy_value
        raise ValueError(f"value: {value} not equal to signal info")

    def decode(self, value: int, signal: 'LinSignal', keep_unit: bool = False) -> Union[str, int]:
        if value == self.phy_value:
            return self.info if self.info is not None else self.phy_value
        raise ValueError(f"value: {value} not equal to {self.phy_value}")

class BCDValue(ValueConverter):

    def __init__(self) -> None:
        """
        A BCD value converter interprets raw values as binary coded decimals.

        Example 3 element array signal being converted into a BCD value:

        .. code-block:: python

            converter = BCDValue()
            convert.encode(123, signal)
            >>> [1, 2, 3]
        """
        super().__init__()

    def encode(self, value: int, signal: 'LinSignal') -> List[int]:
        if value > 10**int(signal.width / 8):
            raise ValueError(f"cannot convert value {value} to bcd, out of {signal} bounds")
        bcd = []
        for i in range(int(signal.width / 8) - 1, -1, -1):
            bcd.append(value // 10**i % 10)
        return bcd

    def decode(self, value: List[int], signal: 'LinSignal', keep_unit: bool = False) -> int:
        out = 0
        length = int(signal.width / 8)
        for i in range(length):
            if value[i] > 9:
                raise ValueError('bcd digit larger than 9')
            out += value[i] * 10**(length - i - 1)
        return out

class ASCIIValue(ValueConverter):

    def __init__(self) -> None:
        """
        An ASCII value converter interprets raw values as ASCII encoded strings.

        Example 3 element array signal being converted into a ASCII value:

        .. code-block:: python

            converter = ASCIIValue()
            convert.encode("abc", signal)
            >>> [0x61, 0x62, 0x63]
        """
        super().__init__()

    def encode(self, value: str, signal: 'LinSignal') -> List[int]:
        return list(value.encode())

    def decode(self, value: List[int], signal: 'LinSignal', keep_unit: bool = False) -> str:
        return bytes(value).decode()

class LinSignalEncodingType():

    def __init__(self, name: str, converters: List[ValueConverter]):
        """
        LinSignalEncodingType encapsulates multiple value converters and then decides on one to use.

        Example of a motor's speed signal being mapped to different values.

        .. code-block:: python

            encoder = LinSignalEncodingType("MotorSpeedEncoder", [
                LogicalValue(phy_value=0, info='off')
                PhysicalValue(phy_min=1, phy_max=254, scale=10, offset=100, unit='rpm')
                LogicalValue(phy_value=255, info='error')
            ])
            encoder.encode("off")
            >>> 0
            encoder.decode(255)
            >>> "error"

        :param name: Encoding type name
        :type name: str
        :param converters: Value converters associated with the encoding type
        :type converters: List[ValueConverter]
        """
        self.name: str = name
        self._converters: List[ValueConverter] = converters
        self._signals: List['LinSignal'] = []

    def encode(self, value: Union[str, int, float], signal: 'LinSignal') -> int:
        """
        Encodes the given signal value into the physical/raw value

        :param value: Signal value
        :type value: Union[str, int, float]
        :param signal: LIN Signal context
        :type signal: LinSignal
        :raises ValueError: when the value cannot be converted
        :return: Physical/Raw value
        :rtype: int
        """
        for encoder in self._converters:
            try:
                return encoder.encode(value, signal)
            except ValueError:
                pass
        raise ValueError(f"cannot encode '{value}' as {self.name}")

    def decode(self, value: int, signal: 'LinSignal', keep_unit: bool = False) -> Union[str, int, float]:
        """
        Decodes the physical/raw value and returns the signal's value

        :param value: Physical/Raw value
        :type value: int
        :param signal: LIN Signal context
        :type signal: LinSignal
        :param keep_unit: when True physical values will have the unit applied and will be
                          returned as strings, defaults to False
        :type keep_unit: bool, optional
        :raises ValueError: when the value cannot be converted
        :return: Signal value
        :rtype: Union[str, int, float]
        """
        for decoder in self._converters:
            try:
                return decoder.decode(value, signal, keep_unit)
            except ValueError:
                pass
        raise ValueError(f"cannot decode {value} as {self.name}")

    def get_converters(self) -> List[ValueConverter]:
        """Returns the value converters under the encoding type

        :return: _description_
        :rtype: List[ValueConverter]
        """
        return self._converters

    def get_signals(self) -> List['LinSignal']:
        """
        Returns the signals associated with the encoding type in the LDF

        :return: List of LIN signal objects
        :rtype: List[LinSignal]
        """
        return self._signals
