"""
Contains classes that are used to encode and decode Lin Signals.

Signal encoding is specified in the LIN 2.1 Specification, section 9.2.6.1
"""
from typing import List, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .signal import LinSignal

class ValueConverter():
    """
    Value converter is used to convert Lin signal values from and into
    their human readable form
    """

    def encode(self, value: Any, signal: 'LinSignal') -> Union[int, List[int]]:
        """
        Converts the human readable value into the raw bytes that will be sent
        """
        raise NotImplementedError()

    def decode(self, value: Union[int, List[int]], signal: 'LinSignal', keep_unit: bool = False) -> Any:
        """
        Converts the received raw bytes into the human readable form
        """
        raise NotImplementedError()

class PhysicalValue(ValueConverter):
    """
    Value converter for physical values

    A physical value encoder converts a range of values into a different range of values.

    :Example:

    `PhysicalValue(phy_min=0, phy_max=100, scale=50, offset=400, unit='rpm')` maps signal values
    from 0-100 into a range of 400 - 5400 rpm.
    """

    def __init__(self, phy_min: int, phy_max: int, scale: float, offset: float, unit: str = None):
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
    """
    Value converter for logical values

    A logical value encoder converts a particular value into another value.

    :Example:

    `LogicalValue(phy_value=0, unit='off')` maps the signal value `0` into `'off'`

    `LogicalValue(phy_value=1, unit='on')` maps the signal value `1` into `'on'`
    """

    def __init__(self, phy_value: int, info: str = None):
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
    """
    Value converter for Binary Coded Decimal values
    """

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
            out += value[i] * 10**(length - i - 1)
        return out

class ASCIIValue(ValueConverter):
    """
    Value converter for ASCII values
    """

    def encode(self, value: str, signal: 'LinSignal') -> List[int]:
        return list(value.encode())

    def decode(self, value: List[int], signal: 'LinSignal', keep_unit: bool = False) -> str:
        return bytes(value).decode()

class LinSignalEncodingType():
    """
    LinSignalEncodingType is used to encode and decode LIN signals

    An encoding type contains multiple value converters.

    :param name: Signal encoding type name
    :type name: `str`
    :param converters: Value converters in the encoding type
    :type converters: `List[ValueConverter]`

    :Example:

    ```
    LinSignalEncodingType(name="MotorSpeed",
                  [
                    LogicalValue(phy_value=0, info='off')
                    PhysicalValue(phy_min=1, phy_max=254, scale=10, offset=100, unit='rpm')
                    LogicalValue(phy_value=255, info='error')
                  ])
    ```
    """

    def __init__(self, name: str, converters: List[ValueConverter]):
        self.name: str = name
        self._converters: List[ValueConverter] = converters

    def encode(self, value: Union[str, int, float], signal: 'LinSignal') -> int:
        """
        Encodes the given value into the physical value
        """
        for encoder in self._converters:
            try:
                return encoder.encode(value, signal)
            except ValueError:
                pass
        raise ValueError(f"cannot encode '{value}' as {self.name}")

    def decode(self, value: int, signal: 'LinSignal', keep_unit: bool = False) -> Union[str, int, float]:
        """
        Decodes the given physical value into the signal value
        """
        for decoder in self._converters:
            try:
                return decoder.decode(value, signal, keep_unit)
            except ValueError:
                pass
        raise ValueError(f"cannot decode {value} as {self.name}")
