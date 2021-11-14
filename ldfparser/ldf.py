"""
Lin Description File handler objects
"""
from typing import Union, Dict, List

from .lin import LinVersion
from .frame import LinFrame, LinUnconditionalFrame, LinEventTriggeredFrame
from .diagnostics import LinDiagnosticRequest, LinDiagnosticResponse
from .signal import LinSignal
from .encoding import LinSignalEncodingType
from .node import LinMaster, LinSlave

class LDF():
    # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    LDF is a container class that describes a LIN network
    """

    def __init__(self):
        self._source: Dict = None
        self._protocol_version: LinVersion = None
        self._language_version: LinVersion = None
        self._baudrate: int = None
        self._channel: str = None
        self._master: LinMaster = None
        self._slaves: Dict[str, LinSlave] = {}
        self._signals: Dict[str, LinSignal] = {}
        self._unconditional_frames: Dict[str, LinUnconditionalFrame] = {}
        self._event_triggered_frames: Dict[str, LinEventTriggeredFrame] = {}
        self._signal_encoding_types: Dict[str, LinSignalEncodingType] = {}
        self._signal_representations: Dict[LinSignal, LinSignalEncodingType] = {}
        self._master_request_frame: LinDiagnosticRequest = None
        self._slave_response_frame: LinDiagnosticResponse = None
        self._comments: List[str] = []

    def get_protocol_version(self) -> LinVersion:
        """Returns the protocol version of the LIN network"""
        return self._protocol_version

    def get_language_version(self) -> LinVersion:
        """Returns the LDF language version"""
        return self._language_version

    def get_baudrate(self) -> int:
        """Returns the baudrate of the LIN network"""
        return self._baudrate

    def get_channel(self) -> str:
        """Returns the channel name"""
        return self._channel

    def get_master(self) -> LinMaster:
        """
        Returns the master node controlling the LIN network

        :returns: LIN master
        :rtype: LinMaster
        """
        return self._master

    def get_slave(self, name: str) -> LinSlave:
        """
        Returns the LIN slave with the given name

        :param name: Name of the slave to find
        :type name: str
        :returns: LIN slave
        :rtype: LinSlave
        :raises: LookupError if the given slave is not found
        """
        slave = self._slaves.get(name)
        if slave is None:
            raise LookupError(f"No slave named '{name}' found!")
        return slave

    def get_slaves(self) -> List[LinSlave]:
        """
        Returns all slaves

        :returns: List of LIN slaves
        :rtype: List[LinSlave]
        """
        return self._slaves.values()

    def get_frame(self, frame_id: Union[int, str]) -> LinFrame:
        try:
            return self.get_unconditional_frame(frame_id)
        except LookupError:
            return self.get_event_triggered_frame(frame_id)

    def get_unconditional_frame(self, frame_id: Union[int, str]) -> LinUnconditionalFrame:
        """
        Returns the unconditional frame with the given name or id

        When `frame_id` is an integer the `LinUnconditionalFrame` with the given id will be returned

        When `frame_id` is a string the `LinUnconditionalFrame` with the given name will be returned

        :Example:
        Given an LDF:

        ```
        Frames {
            VL1_CEM_Frm1: 1, CEM {
                InternalLightsRequest, 0;
            }
        }
        ```

        `ldf.get_unconditional_frame(1)` and `ldf.get_unconditional_frame("VL1_CEM_Frm1")` will return the same value

        :param frame_id:
        :type frame_id: int or str
        :returns: Unconditional LIN frame
        :rtype: LinUnconditionalFrame
        :raises: LookupError if the given frame is not found
        """
        if isinstance(frame_id, str):
            frame = self._unconditional_frames.get(frame_id)
            if frame is None:
                raise LookupError(f"No frame named '{frame_id}' found!")
            return frame
        if isinstance(frame_id, int):
            frame = next((x for x in self.get_unconditional_frames() if x.frame_id == frame_id), None)
            if frame is None:
                raise LookupError(f"No frame with id '{frame_id}' (0x{frame_id:02x}) found!")
            return frame
        raise TypeError("'frame_id' must be int or str")

    def get_unconditional_frames(self) -> List[LinUnconditionalFrame]:
        """
        Returns all unconditional frames

        :returns: List of LIN frames
        :rtype: List[LinUnconditionalFrame]
        """
        return self._unconditional_frames.values()

    def get_event_triggered_frame(self, frame_id: Union[int, str]) -> LinEventTriggeredFrame:
        """
        Returns the event triggered frame with the given name or id

        :param frame_id:
        :type frame_id: int or str
        :returns: Event triggered LIN frame
        :rtype: LinEventTriggeredFrame
        :raises: LookupError if the given frame is not found
        """
        if isinstance(frame_id, str):
            frame = self._event_triggered_frames.get(frame_id)
            if frame is None:
                raise LookupError(f"No frame named '{frame_id}' found!")
            return frame
        if isinstance(frame_id, int):
            frame = next((x for x in self.get_event_triggered_frames() if x.frame_id == frame_id), None)
            if frame is None:
                raise LookupError(f"No frame with id '{frame_id}' (0x{frame_id:02x}) found!")
            return frame
        raise TypeError("'frame_id' must be int or str")

    def get_event_triggered_frames(self) -> List[LinEventTriggeredFrame]:
        """
        Returns all event triggered frames

        :returns: List of event triggered LIN frames
        :rtype: List[LinEventTriggeredFrame]
        """
        return self._event_triggered_frames.values()

    def get_signal(self, name: str) -> LinSignal:
        """
        Returns the signal with the given name

        :param name: Name of the signal to find
        :type name: str
        :returns: LIN signal
        :rtype: LinSignal
        :raises: LookupError if the given signal is not found
        """
        signal = self._signals.get(name)
        if signal is None:
            raise LookupError(f"No signal named '{name}' found!")
        return signal

    def get_signals(self) -> List[LinSignal]:
        """
        Returns all signals

        :returns: List of LIN signals
        :rtype: List[LinSignal]
        """
        return self._signals.values()

    # These properties are maintained in order to keep compatibility
    # with pre-0.10.0 versions

    @property
    def protocol_version(self) -> float:
        # pylint: disable=missing-function-docstring
        return float(self.get_protocol_version())

    @property
    def language_version(self) -> float:
        # pylint: disable=missing-function-docstring
        return float(self.get_language_version())

    @property
    def baudrate(self) -> int:
        # pylint: disable=missing-function-docstring
        return self.get_baudrate()

    @property
    def channel(self) -> str:
        # pylint: disable=missing-function-docstring
        return self.get_channel()

    @property
    def master(self) -> LinMaster:
        # pylint: disable=missing-function-docstring
        return self.get_master()

    @property
    def slaves(self) -> List[LinSlave]:
        # pylint: disable=missing-function-docstring
        return self.get_slaves()

    @property
    def signals(self) -> List[LinSignal]:
        # pylint: disable=missing-function-docstring
        return self.get_signals()

    @property
    def frames(self) -> List[LinUnconditionalFrame]:
        # pylint: disable=missing-function-docstring
        return self.get_unconditional_frames()

    @property
    def converters(self) -> Dict[str, LinSignalEncodingType]:
        return {sig.name: enc for (sig, enc) in self._signal_representations.items()}

    # These functions are maintained in order to keep compatibility
    # with pre-0.10.0 versions

    def signal(self, name: str) -> LinSignal:
        """
        Returns the signal with the given name.

        Deprecated, use `get_signal` instead, this method will be removed in 1.0.0
        """
        return self._signals.get(name)

    def frame(self, frame_id: Union[int, str]) -> LinUnconditionalFrame:
        """
        Returns the signal with the given name.

        Deprecated, use `get_unconditional_frame` instead, this method will be removed in 1.0.0
        """
        try:
            return self.get_unconditional_frame(frame_id)
        except LookupError:
            return None

    def slave(self, name: str) -> LinSlave:
        """
        Returns the slave with the given name.

        Deprecated, use `get_slave` instead, this method will be removed in 1.0.0
        """
        return self._slaves.get(name)
