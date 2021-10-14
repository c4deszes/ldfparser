"""
LIN Frame utilities
"""
import warnings
from typing import Dict, List, Tuple, Union

import bitstruct

from .signal import LinSignal
from .encoding import LinSignalEncodingType

class LinFrame():
    # pylint: disable=too-few-public-methods
    """
    LinFrame is a transport layer level object that represents transactions
    between the LinMaster and LinSlaves

    Every frame has a unique identifier `frame_id` or often referred to as protected identifier or
    PID for short.

    :param frame_id: Frame identifier
    :type frame_id: int
    :param name: Name of the frame
    :type name: str
    """

    def __init__(self, frame_id: int, name: str) -> None:
        self.frame_id = frame_id
        self.name = name

class LinUnconditionalFrame(LinFrame):
    """
    LinUnconditionalFrame represents an unconditional frame consisting of signals
    """

    def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
        super().__init__(frame_id, name)
        self.publisher = None
        self.length = length
        self.signal_map = sorted(signals.items(), key=lambda x: x[0])
        self._packer = LinUnconditionalFrame._frame_pattern(self.length, self.signal_map)

    @staticmethod
    def _frame_pattern(
            frame_size: int,
            signals: List[Tuple[int, LinSignal]]) -> bitstruct.CompiledFormat:
        """
        Converts a frame layout into a bitstructure formatting string

        Example:
            {
                offset = 0, LinSignal(width=6),
                offset = 8, LinSignal(width=8),
                offset = 16, LinSignal(width=1),
                offset = 17, LinSignal(width=1)
            }

            would yield 'u6p2u8u1u1p6' as the frame pattern given a frame size of 3 bytes

        :param frame_size: The size of the frame in bytes
        :type frame_size: int
        :param signals: List of signals and offsets that represent the frame layout
        :type signals: List[Tuple[int, LinSignal]] where the tuple's first element is the offset
                        and the second element is the signal object

        :raises: ValueError if the signals inside the frame would overlap or span outside the frame
        :returns: Bitstruct packer object
        :rtype: bitstruct.CompiledFormat
        """
        pattern = "<"
        frame_bits = frame_size * 8
        frame_offset = 0
        for (offset, signal) in signals:
            if offset < frame_offset:
                raise ValueError(f"{signal} is overlapping ")
            if offset != frame_offset:
                padding = offset - frame_offset
                pattern += f"p{padding}"
                frame_offset += padding
            if frame_offset + signal.width > frame_bits:
                raise ValueError(f"{signal} with offset {offset} spans outside frame!")
            if signal.is_array():
                pattern += "u8" * int(signal.width / 8)
            else:
                pattern += f"u{signal.width}"
            frame_offset += signal.width
        if frame_offset < frame_bits:
            pattern += f"p{frame_bits - frame_offset}"
        return bitstruct.compile(pattern)

    def _get_signal(self, name: str):
        return next((signal for _, signal in self.signal_map if signal.name == name), None)

    @staticmethod
    def _flip_bytearray(data: bytearray) -> bytearray:
        flipped = bytearray()
        for i in data:
            flipped.append(int('{:08b}'.format(i)[::-1], 2))
        return flipped

    def encode(self,
               data: Dict[str, Union[str, int, float]],
               encoding_types: Dict[str, LinSignalEncodingType] = None) -> bytearray:
        """
        Encodes signal values into the LIN frame content

        Example:
            {
                "MotorSpeed": 1000.0,
                "MotorDirection": "CCW"
            }

        :param data: Mapping of signal names to values, signals that are not supplied will default
                    to their initial values
        :type data: Dict[str, Union[str, int, float]] where each key is a signal name and each
                    value is string for logical value and integer or float for physical values
        :param encoding_types: Mapping of signal names to encoding types
        :type encoding_types: Dict[str, LinSignalEncodingType]

        :raises: ValueError if there's no encoding type and the supplied value cannot be encoded
                 as is (float and string values)
        """
        converted = {}
        for (signal_name, value) in data.items():
            signal = self._get_signal(signal_name)
            if encoding_types is not None and signal_name in encoding_types:
                converted[signal_name] = encoding_types[signal_name].encode(value, signal)
            elif signal.encoding_type is not None:
                converted[signal_name] = signal.encoding_types[signal_name].encode(value, signal)
            elif isinstance(value, int):
                converted[signal_name] = value
            else:
                raise ValueError(f'No encoding type found for {signal_name} ({value})')
        return bytearray()

    def encode_raw(self, data: Dict[str, int]) -> bytearray:
        """
        Encodes signal values into the LIN frame content

        Example:
            {
                "MotorSpeed": 1000,
                "MotorDirection": 2
            }

        :param data: Mapping of signal names to values, signals that are not supplied will default
                    to their initial values
        :type data: Dict[str, int] where each key is a signal name and each value is an integer
        :param encoding_types: Mapping of signal names to encoding types
        :type encoding_types: Dict[str, LinSignalEncodingType]
        :returns: LinFrame content
        :rtype: bytearray
        """
        message = []
        for (_, signal) in self.signal_map:
            if signal.name in data.keys():
                if signal.is_array():
                    message += data.get(signal.name)
                else:
                    message.append(data.get(signal.name))
            else:
                if signal.is_array():
                    message += signal.init_value
                else:
                    message.append(signal.init_value)
        return LinUnconditionalFrame._flip_bytearray(self._packer.pack(*message))

    def decode(self,
               data: bytearray,
               encoding_types: Dict[str, LinSignalEncodingType] = None) -> Dict[str, Union[str, int, float]]:
        """
        Decodes a LIN frame into the signals that it contains

        Example:
            data = 0xFC 0x38
            frame_layout = u6p2u8u1u1p6

        """
        parsed = self.parse_raw(data)
        converted = {}
        for (signal_name, value) in parsed.items():
            signal = self._get_signal(signal_name)
            if encoding_types is not None and signal_name in encoding_types:
                converted[signal_name] = encoding_types[signal_name].decode(value, signal)
            elif signal.encoding_type is not None:
                converted[signal_name] = signal.encoding_types[signal_name].decode(value, signal)
            elif isinstance(value, int):
                converted[signal_name] = value
            else:
                raise ValueError(f'No encoding type found for {signal_name} ({value})')
        return converted

    def decode_raw(self,
                   data: bytearray) -> Dict[str, int]:
        """
        Decodes a LIN frame into the signals that it contains

        Example:
            data = 0xFC 0x30 0xFF,
            frame_layout = u6p2u1u1p6u8

            would yield the following dictionary {
                'Signal1': 63,
                'Signal2': 1,
                'Signal3': 1,
                'Signal4': 255
            }

        :param data: LinFrame content as a bytearray
        :type data: bytearray
        :returns: mapping of signal names to signal values
        :rtype: Dict[str, int]
        """
        unpacked = self._packer.unpack(LinUnconditionalFrame._flip_bytearray(data))
        message = {}
        signal_index = 0
        index = 0
        while index < len(unpacked):
            if self.signal_map[signal_index][1].is_array():
                array_size = int(self.signal_map[signal_index][1].width / 8)
                message[self.signal_map[signal_index][1].name] = list(unpacked[index:index + array_size])
                index += array_size - 1
            else:
                message[self.signal_map[signal_index][1].name] = unpacked[index]
            signal_index += 1
            index += 1
        return message

    # These methods are kept for compatibility with versions before 0.11.0

    def raw(self, data: Dict[str, int]) -> bytearray:
        """
        Returns a bytearray (frame content) by using the raw signal values provided

        Deprecated, use 'encode_raw' instead
        """
        warnings.warn(
            "raw is deprecated, use 'encode_raw' instead, will be removed in 1.0.0",
            DeprecationWarning)

        return self.encode_raw(data)

    def data(self,
             data: Dict[str, Union[str, int, float]],
             converters: Dict[str, LinSignalEncodingType]) -> bytearray:
        """
        Returns a bytearray (frame content) by using the human readable signal values

        Deprecated, use 'encode' instead
        """
        warnings.warn(
            "data is deprecated, use 'encode' instead, will be removed in 1.0.0",
            DeprecationWarning)

        converted = {}
        for (signal_name, value) in data.items():
            if signal_name not in converters.keys():
                raise ValueError(f'No encoder found for {signal_name}')
            converted[signal_name] = converters[signal_name].encode(value, self._get_signal(signal_name))
        return self.encode_raw(converted)

    def parse_raw(self, data: bytearray) -> Dict[str, int]:
        """
        Returns a mapping between Signal names and their raw physical values in the given message

        Deprecated, use 'decode_raw' instead
        """
        warnings.warn(
            "parse_raw is deprecated, use 'decode_raw' instead, will be removed in 1.0.0",
            DeprecationWarning)

        return self.decode_raw(data)

    def parse(self,
              data: bytearray,
              converters: Dict[str, LinSignalEncodingType]) -> Dict[str, Union[str, int, float]]:
        """
        Returns a mapping between Signal names and their human readable value

        Deprecated, use 'decode' instead
        """
        warnings.warn(
            "data is deprecated, use 'encode' instead, will be removed in 1.0.0",
            DeprecationWarning)

        parsed = self.decode_raw(data)
        output = {}
        for (signal_name, value) in parsed.items():
            if signal_name not in converters.keys():
                raise ValueError(f'No decoder found for {signal_name}')
            output[signal_name] = converters[signal_name].decode(value, self._get_signal(signal_name))
        return output

class LinEventTriggeredFrame(LinFrame):
    # pylint: disable=too-few-public-methods
    """
    LinEventTriggeredFrame is LinFrame in the schedule table that can contain different
    unconditional frames from different nodes
    """
    # TODO: add schedule table reference

    def __init__(self, frame_id: int, name: str, frames: List[LinUnconditionalFrame] = []) -> None:
        super().__init__(frame_id, name)
        self.frames = frames
