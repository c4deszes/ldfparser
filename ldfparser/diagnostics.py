from typing import List
import serial

from ldfparser.frame import LinUnconditionalFrame
from ldfparser.signal import LinSignal

# NAD values (Specified in 4.2.3.2)
LIN_NAD_RESERVED                    = 0x00
LIN_NAD_SLAVE_NODE_RANGE            = range(0x01, 0x7E)
LIN_NAD_FUNCTIONAL_NODE_ADDRESS     = 0x7E
LIN_NAD_BROADCAST_ADDRESS           = 0x7F
LIN_NAD_FREE_RANGE                  = range(0x80, 0x100)

# Service identifiers (Specified in 4.2.3.4)
LIN_SID_RESERVED_RANGE1             = range(0, 0xB0)
LIN_SID_ASSIGN_NAD                  = 0xB0
LIN_SID_ASSIGN_FRAME_ID             = 0xB1
LIN_SID_READ_BY_ID                  = 0xB2
LIN_SID_CONDITIONAL_CHANGE_NAD      = 0xB3
LIN_SID_DATA_DUMP                   = 0xB4
LIN_SID_RESERVED                    = 0xB5
LIN_SID_SAVE_CONFIGURATION          = 0xB6
LIN_SID_ASSIGN_FRAME_ID_RANGE       = 0xB7
LIN_SID_RESERVED_RANGE2             = range(0xB8, 0x100)

# Read by identifier request IDs (Specified in 4.2.6.1)
LIN_SID_READ_BY_ID_PRODUCT_ID         = 0
LIN_SID_READ_BY_ID_SERIAL_NUMBER      = 1
LIN_SID_READ_BY_ID_RESERVED_RANGE1    = range(2, 32)
LIN_SID_READ_BY_ID_USER_DEFINED_RANGE = range(32, 64)
LIN_SID_READ_BY_ID_RESERVED_RANGE2    = range(64, 256)

def pci_byte(length: int):
    return length & 0x0F

def rsid(sid: int):
    return sid + 0x40

class LinDiagnosticRequest(LinUnconditionalFrame):

    def __init__(self, frame_id: int, name: str):
        super().__init__(frame_id, name, 8, {
            0:  LinSignal('NAD', 8, 0),
            8:  LinSignal('PCI', 8, 0),
            16: LinSignal('SID', 8, 0),
            24: LinSignal('D1', 8, 0xFF),
            32: LinSignal('D2', 8, 0xFF),
            40: LinSignal('D3', 8, 0xFF),
            48: LinSignal('D4', 8, 0xFF),
            56: LinSignal('D5', 8, 0xFF)
        })

    def encode_assign_nad(self, initial_nad: int, supplier_id: int, function_id: int,
                          new_nad: int) -> bytearray:
        """
        
        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x06, 'SID': LIN_SID_ASSIGN_NAD,
                                'D1': (supplier_id >> 8) & 0xFF, 'D2': supplier_id & 0xFF,
                                'D3': (function_id >> 8) & 0xFF, 'D4': function_id & 0xFF,
                                'D5': new_nad})

    def encode_conditional_change_nad(self, initial_nad: int, identifier: int, byte: int,
                                        mask: int, invert: int, new_nad: int) -> bytearray:
        """
        
        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x06,
                                'SID': LIN_SID_CONDITIONAL_CHANGE_NAD,
                                'D1': identifier, 'D2': byte, 'D3': mask, 'D4': invert,
                                'D5': new_nad})

    def encode_data_dump(self, initial_nad: int, data: bytearray) -> bytearray:
        """
        
        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x06, 'SID': LIN_SID_DATA_DUMP,
                                'D1': data[0], 'D2': data[1], 'D3': data[2], 'D4': data[3],
                                'D5': data[4]})

    def encode_save_configuration(self, initial_nad: int) -> bytearray:
        """
        
        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x01, 'SID': LIN_SID_SAVE_CONFIGURATION})

    def encode_assign_frame_id_range(self, initial_nad: int, start_index: int,
                                     pids: List[int]) -> bytearray:
        """
        
        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x06,
                                'SID': LIN_SID_ASSIGN_FRAME_ID_RANGE,
                                'D1': start_index,
                                'D2': pids[0], 'D3': pids[1], 'D4': pids[2], 'D5': pids[3]})

    def encode_read_by_id(self, initial_nad: int, identifier: int, supplier_id: int,
                          function_id: int) -> bytearray:
        """


        """
        return self.encode_raw({'NAD': initial_nad, 'PCI': 0x06, 'SID': LIN_SID_READ_BY_ID,
                                'D1': identifier,
                                'D2': (supplier_id >> 8) & 0xFF, 'D3': supplier_id & 0xFF,
                                'D4': (function_id >> 8) & 0xFF, 'D5': function_id & 0xFF})

class LinDiagnosticResponse(LinUnconditionalFrame):

    def __init__(self, frame_id: int, name: str):
        super().__init__(frame_id, name, 8, {
            0:  LinSignal('NAD', 8, 0),
            8:  LinSignal('PCI', 8, 0),
            16: LinSignal('RSID', 8, 0),
            24: LinSignal('D1', 8, 0xFF),
            32: LinSignal('D2', 8, 0xFF),
            40: LinSignal('D3', 8, 0xFF),
            48: LinSignal('D4', 8, 0xFF),
            56: LinSignal('D5', 8, 0xFF)
        })
