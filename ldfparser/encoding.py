"""
Contains classes that are used to encode and decode Lin Signals.

Signal encoding is specified in the LIN 2.1 Specification, section 9.2.6.1
"""
from typing import List, Union, Any

class ValueConverter():
    """
    Value converter is used to convert Lin signal values from and into
    their human readable form
    """

    def encode(self, value: Any, signal) -> Union[int, List[int]]:
        """
        Converts the human readable value into the raw bytes that will be sent
        """
        raise NotImplementedError()

    def decode(self, value: Union[int, List[int]], signal) -> Any:
        """
        Converts the received raw bytes into the human readable form
        """
        raise NotImplementedError()

class PhysicalValue(ValueConverter):
    """Value converter for physical values
    
    
    """

    def __init__(self, phy_min: int, phy_max: int, scale: float, offset: float, unit: str = None):
        self.phy_min = phy_min
        self.phy_max = phy_max
        self.scale = scale
        self.offset = offset
        self.unit = unit

    def encode(self, value: Union[str, int, float], signal) -> int:
        num = 0.0
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

    def decode(self, value: int, signal) -> float:
        if value < self.phy_min or value > self.phy_max:
            raise ValueError(f"value: {value} out of range ({self.phy_min}, {self.phy_max})")

        return float(value * self.scale + self.offset)

class LogicalValue(ValueConverter):

    def __init__(self, phy_value: int, info: str = None):
        self.phy_value = phy_value
        self.info = info

    def encode(self, value: Union[str, int], signal) -> int:
        if self.info is None and value == self.phy_value:
            return self.phy_value
        if self.info is not None and value == self.info:
            return self.phy_value
        raise ValueError(f"value: {value} not equal to signal info")

    def decode(self, value: int, signal) -> Union[str, int]:
        if value == self.phy_value:
            return self.info if self.info is not None else self.phy_value
        raise ValueError(f"value: {value} not equal to {self.phy_value}")

class BCDValue(ValueConverter):

    def encode(self, value: int, signal) -> List[int]:
        if value > 10**int(signal.width / 8):
            raise ValueError(f"cannot convert value {value} to bcd, out of {signal} bounds")
        bcd = []
        for i in range(int(signal.width / 8) - 1, -1, -1):
            bcd.append(value // 10**i % 10)
        return bcd

    def decode(self, value: List[int], signal) -> int:
        out = 0
        length = int(signal.width / 8)
        for i in range(length):
            out += value[i] * 10**(length - i - 1)
        return out

class ASCIIValue(ValueConverter):

    def encode(self, value: str, signal) -> List[int]:
        return list(value.encode())

    def decode(self, value: List[int], signal) -> str:
        return bytes(value).decode()

class LinSignalType:

    def __init__(self, name, converters: List[ValueConverter]):
        self.name = name
        self._converters = converters

    def encode(self, value: Union[str, int, float], signal) -> int:
        out = None
        for encoder in self._converters:
            try:
                out = encoder.encode(value, signal)
                break
            except ValueError:
                pass

        if out is None:
            raise ValueError(f"cannot encode {value} as {self.name}")
        return out

    def decode(self, value: int, signal) -> Union[str, int, float]:
        out = None
        for decoder in self._converters:
            try:
                out = decoder.decode(value, signal)
                break
            except ValueError:
                pass

        if out is None:
            raise ValueError(f"cannot decode {value} as {self.name}")
        return out
