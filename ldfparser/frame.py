"""
LIN Frame utilities
"""
from typing import Dict, List, Tuple, Union

import bitstruct

from .signal import LinSignal
from .encoding import LinSignalEncodingType

class LinFrame():

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
        ordered_signals = sorted(signals.items(), key=lambda x: x[0])
        self.signal_map = ordered_signals
        self.signals = [i[1] for i in ordered_signals]
        pattern = self._frame_pattern(length * 8, ordered_signals)
        self._packer = bitstruct.compile(pattern)

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

    def data(self,
             data: Dict[str, Union[str, int, float]],
             converters: Dict[str, LinSignalEncodingType]) -> bytearray:
        """
        Returns a bytearray (frame content) by using the human readable signal values
        """
        converted = {}
        for value in data.items():
            if value[0] not in converters.keys():
                raise ValueError('No encoder found for ' + value[0])
            converted[value[0]] = converters[value[0]].encode(value[1], self._get_signal(value[0]))
        return self.raw(converted)

    def parse_raw(self, data: bytearray) -> Dict[str, int]:
        """
        Returns a mapping between Signal names and their raw physical values in the given message
        """
        message = {}
        unpacked = self._packer.unpack(LinUnconditionalFrame._flip_bytearray(data))
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

    def parse(self,
              data: bytearray,
              converters: Dict[str, LinSignalEncodingType]) -> Dict[str, Union[str, int, float]]:
        """
        Returns a mapping between Signal names and their human readable value
        """
        tmp = self.parse_raw(data)
        output = {}
        for value in tmp.items():
            if value[0] not in converters.keys():
                raise ValueError('No decoder found for ' + value[0])
            output[value[0]] = converters[value[0]].decode(value[1], self._get_signal(value[0]))
        return output

    @staticmethod
    def _flip_bytearray(data: bytearray) -> bytearray:
        flipped = bytearray()
        for i in data:
            flipped.append(int('{:08b}'.format(i)[::-1], 2))
        return flipped

class LinEventTriggeredFrame(LinFrame):
    # TODO: add schedule table reference

    def __init__(self, frame_id: int, name: str, frames: List[LinFrame]) -> None:
        super().__init__(frame_id, name)
        self.frames = frames
