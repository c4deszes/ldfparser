"""
Lin Description File handler objects
"""
from typing import Union, Dict, List
import warnings

from .lin import LinVersion
from .frame import LinFrame
from .signal import LinSignal
from .encoding import LinSignalType
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
        self._frames: Dict[str, LinFrame] = {}
        self._converters: Dict[str, LinSignalType] = {}
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
        """
        Returns the unconditional frame with the given name or id

        When `frame_id` is an integer the `LinFrame` with the given id will be returned

        When `frame_id` is a string the `LinFrame` with the given name will be returned

        :Example:
        Given an LDF:

        ```
        Frames {
            VL1_CEM_Frm1: 1, CEM {
                InternalLightsRequest, 0;
            }
        }
        ```

        `ldf.get_frame(1)` and `ldf.get_frame("VL1_CEM_Frm1")` will return the same value

        :param frame_id:
        :type frame_id: int or str
        :returns: LIN frame
        :rtype: LinFrame
        :raises: LookupError if the given frame is not found
        """
        if isinstance(frame_id, str):
            frame = self._frames.get(frame_id)
            if frame is None:
                raise LookupError(f"No frame named '{frame_id}' found!")
            return frame
        if isinstance(frame_id, int):
            frame = next((x for x in self.frames if x.frame_id == frame_id), None)
            if frame is None:
                raise LookupError(f"No frame with id '{frame_id}' (0x{frame_id:02x}) found!")
            return frame
        raise TypeError("'frame_id' must be int or str")

    def get_frames(self) -> List[LinFrame]:
        """
        Returns all unconditional frames

        :returns: List of LIN frames
        :rtype: List[LinFrame]
        """
        return self._frames.values()

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
    def frames(self) -> List[LinFrame]:
        # pylint: disable=missing-function-docstring
        return self.get_frames()

    @property
    def converters(self) -> Dict[str, LinSignalType]:
        return self._converters

    # These functions are maintained in order to keep compatibility
    # with pre-0.10.0 versions

    def signal(self, name: str) -> LinSignal:
        """
        Returns the signal with the given name.

        Deprecated, use `get_signal` instead, this method will be removed in 1.0.0
        """
        warnings.warn("'signal(x)' is deprecated, use 'get_signal(x)' instead", DeprecationWarning)
        return self._signals.get(name)

    def frame(self, frame_id: Union[int, str]) -> LinFrame:
        """
        Returns the signal with the given name.

        Deprecated, use `get_signal` instead, this method will be removed in 1.0.0
        """
        warnings.warn("'frame(x)' is deprecated, use 'get_frame(x)' instead", DeprecationWarning)
        return self.get_frame(frame_id)

    def slave(self, name: str) -> LinSlave:
        """
        Returns the slave with the given name.

        Deprecated, use `get_slave` instead, this method will be removed in 1.0.0
        """
        warnings.warn("'slave(x)' is deprecated, use 'get_slave(x)' instead", DeprecationWarning)
        return self._slaves.get(name)
