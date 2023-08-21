"""LIN schedule related objects"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .frame import LinFrame
    from .node import LinNode

class ScheduleTable():

    def __init__(self, name: str) -> None:
        """
        ScheduleTable holds schedule entries

        :param name: Schedule name
        :type name: str
        """
        self.name = name
        self.schedule: List[ScheduleTableEntry] = []

class ScheduleTableEntry():

    def __init__(self, delay: float = 0.0) -> None:
        """
        Base class for schedule entries

        :param delay: Delay in the schedule, defaults to 0.0
        :type delay: float, optional
        """
        self.delay = delay

class LinFrameEntry(ScheduleTableEntry):

    def __init__(self, frame: 'LinFrame' = None) -> None:
        """
        Entry for requesting unconditional frames

        :param frame: LIN Frame, defaults to None
        :type frame: LinFrame, optional
        """
        super().__init__()
        self.frame: 'LinFrame' = None

class MasterRequestEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        """
        Entry for standard diagnostic request
        """
        super().__init__()

class SlaveResponseEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        """
        Entry for standard diagnostic response
        """
        super().__init__()

class AssignNadEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None) -> None:
        """
        Entry for AssignNAD diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        """
        super().__init__()
        self.node: 'LinNode' = node

class AssignFrameIdRangeEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None,
                 frame_index: int = 0, pids: List[int] = None) -> None:
        """
        Entry for AssignFrameIdRange diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        :param frame_index: Starting index in the request, defaults to 0
        :type frame_index: int, optional
        :param pids: New frame id values, defaults to None
        :type pids: List[int], optional
        """
        super().__init__()
        self.node = node
        self.frame_index = frame_index
        self.pids = pids if pids is not None else []

class ConditionalChangeNadEntry(ScheduleTableEntry):

    def __init__(self, nad: int = 0, _id: int = 0, byte: int = 0,
                 mask: int = 0, inv: int = 0, new_nad: int = 0) -> None:
        super().__init__()
        self.nad = nad
        self.id = _id
        self.byte = byte
        self.mask = mask
        self.inv = inv
        self.new_nad = new_nad

class DataDumpEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None, data: List[int] = None) -> None:
        """
        Entry for DataDump diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        :param data: Data to send, defaults to None
        :type data: List[int], optional
        """
        super().__init__()
        self.node = node
        self.data = data if data is not None else []

class SaveConfigurationEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None) -> None:
        """
        Entry for SaveConfiguration diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        """
        super().__init__()
        self.node = node

class AssignFrameIdEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None, frame: 'LinFrame' = None) -> None:
        """
        Entry for AssignFrameId diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        :param frame: Frame to assign, defaults to None
        :type frame: LinFrame, optional
        """
        super().__init__()
        self.node = node
        self.frame = frame

class UnassignFrameIdEntry(ScheduleTableEntry):

    def __init__(self, node: 'LinNode' = None, frame: 'LinFrame' = None) -> None:
        """
        Entry for UnassignFrameId diagnostic request

        :param node: LIN Node to send the request to, defaults to None
        :type node: LinNode, optional
        :param frame: Frame to unassign, defaults to None
        :type frame: LinFrame, optional
        """
        super().__init__()
        self.node = node
        self.frame = frame

class FreeFormatEntry(ScheduleTableEntry):

    def __init__(self, data: List[int] = None) -> None:
        """
        Entry for FreeFormat diagnostic commands

        :param data: Frame content to send, defaults to None
        :type data: List[int], optional
        """
        super().__init__()
        self.data = data if data is not None else []
