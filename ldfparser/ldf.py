"""
Lin Description File handler objects
"""
from typing import Union, Dict, List

from .lin import LinVersion
from .frame import LinFrame, LinSporadicFrame, LinUnconditionalFrame, LinEventTriggeredFrame
from .diagnostics import LinDiagnosticFrame, LinDiagnosticRequest, LinDiagnosticResponse
from .signal import LinSignal
from .encoding import LinSignalEncodingType
from .node import LinMaster, LinSlave
from .schedule import ScheduleTable

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
        self._diagnostic_signals: Dict[str, LinSignal] = {}
        self._unconditional_frames: Dict[str, LinUnconditionalFrame] = {}
        self._event_triggered_frames: Dict[str, LinEventTriggeredFrame] = {}
        self._sporadic_frames: Dict[str, LinSporadicFrame] = {}
        self._diagnostic_frames: Dict[str, LinDiagnosticFrame] = {}
        self._signal_encoding_types: Dict[str, LinSignalEncodingType] = {}
        self._signal_representations: Dict[LinSignal, LinSignalEncodingType] = {}
        self._master_request_frame: LinDiagnosticRequest = None
        self._slave_response_frame: LinDiagnosticResponse = None
        self._schedule_tables: Dict[str, ScheduleTable] = {}
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

    def get_frame(self, frame_id: Union[int, str]) -> Union[LinUnconditionalFrame, LinEventTriggeredFrame, LinSporadicFrame]:
        try:
            return self.get_unconditional_frame(frame_id)
        except LookupError:
            pass
        try:
            return self.get_event_triggered_frame(frame_id)
        except LookupError:
            pass
        try:
            return self.get_sporadic_frame(frame_id)
        except LookupError as exc:
            raise exc

    @staticmethod
    def _find_frame(frame_id: Union[int, str], collection: Dict[str, LinFrame]) -> LinFrame:
        if isinstance(frame_id, str):
            frame = collection.get(frame_id)
            if frame is None:
                raise LookupError(f"No frame named '{frame_id}' found!")
            return frame
        if isinstance(frame_id, int):
            frame = next((x for x in collection.values() if x.frame_id == frame_id), None)
            if frame is None:
                raise LookupError(f"No frame with id '{frame_id}' (0x{frame_id:02x}) found!")
            return frame
        raise TypeError("'frame_id' must be int or str")

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
        return LDF._find_frame(frame_id, self._unconditional_frames)

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
        return LDF._find_frame(frame_id, self._event_triggered_frames)

    def get_event_triggered_frames(self) -> List[LinEventTriggeredFrame]:
        """
        Returns all event triggered frames

        :returns: List of event triggered LIN frames
        :rtype: List[LinEventTriggeredFrame]
        """
        return self._event_triggered_frames.values()

    def get_sporadic_frame(self, frame_id: str) -> LinSporadicFrame:
        """
        Returns the sporadic frame with the given name

        :param frame_id:
        :type frame_id: str
        :returns: Sporadic LIN frame
        :rtype: LinSporadicFrame
        :raises: LookupError if the given frame is not found
        """
        frame = self._sporadic_frames.get(frame_id)
        if frame is None:
            raise LookupError(f"No frame named '{frame_id}' found!")
        return frame

    def get_sporadic_frames(self) -> List[LinSporadicFrame]:
        """
        Returns all sporadic frames

        :returns: List of sporadic LIN frames
        :rtype: List[LinSporadicFrame]
        """
        return self._sporadic_frames.values()

    def get_diagnostic_frame(self, frame_id: Union[int, str]) -> LinDiagnosticFrame:
        """
        Returns the diagnostic frame with the given name or id

        :param frame_id:
        :type frame_id: int or str
        :returns: Diagnostic LIN frame
        :rtype: LinDiagnosticFrame
        :raises: LookupError if the given frame is not found
        """
        return LDF._find_frame(frame_id, self._diagnostic_frames)

    def get_diagnostic_frames(self) -> List[LinDiagnosticFrame]:
        """
        Returns all diagnostic frames

        :returns: List of diagnostic LIN frames
        :rtype: List[LinDiagnosticFrame]
        """
        return self._diagnostic_frames.values()

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

    def get_diagnostic_signal(self, name: str) -> LinSignal:
        """
        Returns the diagnostic signal with the given name

        :param name: Name of the diagnostic signal to find
        :type name: str
        :returns: Diagnostic signal
        :rtype: LinSignal
        :raises: LookupError if the given diagnostic signal is not found
        """
        signal = self._diagnostic_signals.get(name)
        if signal is None:
            raise LookupError(f"No diagnostic signal named '{name}' found!")
        return signal

    def get_diagnostic_signals(self) -> List[LinSignal]:
        """
        Returns all diagnostic signal

        :returns: List of Diagnostic signals
        :rtype: List[LinSignal]
        """
        return self._diagnostic_signals.values()

    def get_schedule_table(self, name: str) -> ScheduleTable:
        """
        Returns the schedule table with the given name

        :param name: Name of the schedule table to find
        :type name: str
        :returns: Schedule table
        :rtype: ScheduleTable
        :raises: LookupError if the given schedule table is not found
        """
        schedule = self._schedule_tables.get(name)
        if schedule is None:
            raise LookupError(f"No schedule table named '{name}' found!")
        return schedule

    def get_schedule_tables(self) -> List[ScheduleTable]:
        """
        Returns all schedule tables

        :returns: List of Schedule tables
        :rtype: List[ScheduleTable]
        """
        return self._schedule_tables.values()

    def get_signal_encoding_type(self, name: str) -> LinSignalEncodingType:
        """
        Returns the signal encoding type with the given name

        :param name: Name of the signal encoding type to find
        :type name: str
        :returns: Signal encoding type
        :rtype: LinSignalEncodingType
        :raises: LookupError if the given signal encoding type is not found
        """
        encoding_type = self._signal_encoding_types.get(name)
        if encoding_type is None:
            raise LookupError(f"No signal encoding type named '{name}' found!")
        return encoding_type

    def get_signal_encoding_types(self) -> List[LinSignalEncodingType]:
        """
        Returns all signal encoding types

        :returns: List of Signal encoding types
        :rtype: List[LinSignalEncodingType]
        """
        return self._signal_encoding_types.values()

    @property
    def master_request_frame(self) -> LinDiagnosticRequest:
        return self._master_request_frame

    @property
    def slave_response_frame(self) -> LinDiagnosticResponse:
        return self._slave_response_frame

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

    @property
    def comments(self) -> List[str]:
        return self._comments

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
