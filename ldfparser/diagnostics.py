from typing import Iterable, Dict

from ldfparser.frame import LinUnconditionalFrame
from ldfparser.signal import LinSignal

# NAD values (Specified in 4.2.3.2)
LIN_NAD_RESERVED = 0x00
LIN_NAD_SLAVE_NODE_RANGE = range(0x01, 0x7E)
LIN_NAD_FUNCTIONAL_NODE_ADDRESS = 0x7E
LIN_NAD_BROADCAST_ADDRESS = 0x7F
LIN_NAD_FREE_RANGE = range(0x80, 0x100)

# Service identifiers (Specified in 4.2.3.4)
LIN_SID_RESERVED_RANGE1 = range(0, 0xB0)
LIN_SID_ASSIGN_NAD = 0xB0
LIN_SID_ASSIGN_FRAME_ID = 0xB1
LIN_SID_READ_BY_ID = 0xB2
LIN_SID_CONDITIONAL_CHANGE_NAD = 0xB3
LIN_SID_DATA_DUMP = 0xB4
LIN_SID_RESERVED = 0xB5
LIN_SID_SAVE_CONFIGURATION = 0xB6
LIN_SID_ASSIGN_FRAME_ID_RANGE = 0xB7
LIN_SID_RESERVED_RANGE2 = range(0xB8, 0x100)

# Read by identifier request IDs (Specified in 4.2.6.1)
LIN_SID_READ_BY_ID_PRODUCT_ID = 0
LIN_SID_READ_BY_ID_SERIAL_NUMBER = 1
LIN_SID_READ_BY_ID_RESERVED_RANGE1 = range(2, 32)
LIN_SID_READ_BY_ID_USER_DEFINED_RANGE = range(32, 64)
LIN_SID_READ_BY_ID_RESERVED_RANGE2 = range(64, 256)

def pci_byte(length: int):
    return length & 0x0F

def rsid(sid: int):
    return sid + 0x40

class LinDiagnosticFrame(LinUnconditionalFrame):
    pass

class LinDiagnosticRequest(LinDiagnosticFrame):

    def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
        super().__init__(frame_id, name, length, signals)

    def encode_assign_nad(self, initial_nad: int, supplier_id: int, function_id: int,
                          new_nad: int) -> bytearray:
        return self.encode_raw([initial_nad, pci_byte(6), LIN_SID_ASSIGN_NAD,
                                supplier_id & 0xFF, (supplier_id >> 8) & 0xFF,
                                function_id & 0xFF, (function_id >> 8) & 0xFF,
                                new_nad])

    def encode_conditional_change_nad(self, nad: int, identifier: int, byte: int,
                                      mask: int, invert: int, new_nad: int) -> bytearray:
        return self.encode_raw([nad, pci_byte(6),
                                LIN_SID_CONDITIONAL_CHANGE_NAD,
                                identifier, byte, mask, invert,
                                new_nad])

    def encode_data_dump(self, nad: int, data: Iterable[int]) -> bytearray:
        return self.encode_raw([nad, pci_byte(6), LIN_SID_DATA_DUMP,
                                data[0], data[1], data[2], data[3], data[4]])

    def encode_save_configuration(self, nad: int) -> bytearray:
        return self.encode_raw([nad, pci_byte(1), LIN_SID_SAVE_CONFIGURATION,
                                0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

    def encode_assign_frame_id_range(self, nad: int, start_index: int,
                                     pids: Iterable[int]) -> bytearray:
        return self.encode_raw([nad, pci_byte(6),
                                LIN_SID_ASSIGN_FRAME_ID_RANGE,
                                start_index,
                                pids[0], pids[1], pids[2], pids[3]])

    def encode_read_by_id(self, nad: int, identifier: int, supplier_id: int,
                          function_id: int) -> bytearray:
        return self.encode_raw([nad, pci_byte(6), LIN_SID_READ_BY_ID,
                                identifier,
                                supplier_id & 0xFF, (supplier_id >> 8) & 0xFF,
                                function_id & 0xFF, (function_id >> 8) & 0xFF])

class LinDiagnosticResponse(LinDiagnosticFrame):

    def __init__(self, frame_id: int, name: str, length: int, signals: Dict[int, LinSignal]):
        super().__init__(frame_id, name, length, signals)
