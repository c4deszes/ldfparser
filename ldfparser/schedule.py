
from typing import List

from .frame import LinFrame
from .node import LinNode

class ScheduleTable():

    def __init__(self, name: str) -> None:
        self.name = name
        self.schedule: List[ScheduleTableEntry] = []

class ScheduleTableEntry():

    def __init__(self) -> None:
        self.delay = 0

class UnconditionalFrameEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.frame: LinFrame = None

class MasterRequestEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()

class SlaveResponseEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()

class AssignNadEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.node: LinNode = None

class AssignFrameIdRangeEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.node: LinNode = None
        self.pids = []

class ConditionalChangeNadEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.nad: int = 0
        self.id: int = 0
        self.byte: int = 0
        self.mask: int = 0
        self.inv: int = 0
        self.new_nad: int = 0

class DataDumpEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.node: LinNode = None
        self.data: List[int] = []

class SaveConfigurationEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.node: LinNode = None

class AssignFrameIdEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.node: LinNode = None
        self.frame: LinFrame = None

class FreeFormatEntry(ScheduleTableEntry):

    def __init__(self) -> None:
        super().__init__()
        self.data: List[int] = []
