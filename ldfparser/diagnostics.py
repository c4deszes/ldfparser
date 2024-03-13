from typing import Iterable, Dict

from .frame import LinUnconditionalFrame

# LIN Diagnostic Frame IDs
LIN_MASTER_REQUEST_FRAME_ID = 0x3C
LIN_SLAVE_RESPONSE_FRAME_ID = 0x3D

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

def rsid(sid: int) -> int:
    """
    Returns the response service identifier for a given service id

    Example:

    .. code-block:: python

        rsid(LIN_SID_READ_BY_ID)
        >>> 0xF2

    :param sid: Service identifier
    :type sid: int
    :returns: Response Service Identifier (RSID)
    :rtype: int
    """
    return sid + 0x40

LIN_PCI_SINGLE_FRAME = 0b0000
LIN_PCI_FIRST_FRAME = 0b0001
LIN_PCI_CONSECUTIVE_FRAME = 0b0010

def pci_byte(pci_type: int, length: int) -> int:
    """
    Returns protocol control information byte

    Example:
    >>> pci_byte(LIN_PCI_SINGLE_FRAME, 6)
    0x06

    :param pci_type: PCI Type (Single Frame, First Frame, etc.)
    :type pci_type: int
    :param length: PCI length \
        For Single Frame type this is the length of the frame \
        For First Frame type this the length of the unit divided by 256 \
        For Consecutive Frame type this is the remaining frame counter
    :type length:
    :returns: Calculated PCI byte
    :rtype: int
    """
    return (length & 0x0F) | (pci_type << 4)

class LinDiagnosticFrame(LinUnconditionalFrame):
    """Base class for diagnostic communication"""
    pass

class LinDiagnosticRequest(LinDiagnosticFrame):
    """LinDiagnosticRequest is used to encode standard diagnostic messages"""

    _FIELDS = ['NAD', 'PCI', 'SID', 'D1', 'D2', 'D3', 'D4', 'D5']

    def __init__(self, frame: LinDiagnosticFrame):
        super().__init__(frame.frame_id, frame.name, frame.length, dict(frame.signal_map))

    def encode_request(self, nad: int, pci: int, sid: int,
                       d1: int, d2: int, d3: int, d4: int, d5: int):
        """
        Encodes a diagnostic request into a frame

        Example:
        >>> encode_request(0x01, 0x06, LIN_SID_READ_BY_ID,
                           LIN_SID_READ_BY_ID_PRODUCT_ID, 0xFF, 0x7F, 0xFF, 0xFF)

        :param nad: Node Address
        :type nad: int
        :param pci: Protocol Control Information
        :type pci: int
        :param sid: Service Identifier
        :type sid: int
        :param d1: Data byte 1
        :type d1: int
        :param d2: Data byte 2
        :type d2: int
        :param d3: Data byte 3
        :type d3: int
        :param d4: Data byte 4
        :type d4: int
        :param d5: Data byte 5
        :type d5: int
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_raw([nad, pci, sid, d1, d2, d3, d4, d5])

    def encode_assign_nad(self, initial_nad: int, supplier_id: int, function_id: int,
                          new_nad: int) -> bytearray:
        """
        Encodes an AssignNAD diagnostic request into a frame

        Example:
        >>> encode_assign_nad(0x00, 0x7FFF, 0xFFFF, 0x01)

        :param initial_nad: Initial Node Address
        :type initial_nad: int
        :param supplier_id: Supplier ID
        :type supplier_id: int
        :param function_id: Function ID
        :type function_id: int
        :param new_nad: New Node Address
        :type new_nad: int
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(initial_nad, pci_byte(LIN_PCI_SINGLE_FRAME, 6),
                                   LIN_SID_ASSIGN_NAD,
                                   supplier_id & 0xFF, (supplier_id >> 8) & 0xFF,
                                   function_id & 0xFF, (function_id >> 8) & 0xFF,
                                   new_nad)

    def encode_conditional_change_nad(self, nad: int, identifier: int, byte: int,
                                      mask: int, invert: int, new_nad: int) -> bytearray:
        """
        Encodes an ConditionalChangeNAD diagnostic request into a frame

        Example:
        >>> encode_conditional_change_nad(0x7F, 0x01, 0x03, 0x01, 0xFF, 0x01)

        :param nad: Node Address
        :type nad: int
        :param identifier: Identifier
        :type identifier: int
        :param byte: Byte number
        :type byte: int
        :param mask: Byte mask
        :type mask: int
        :param invert: Invert mask
        :type invert: int
        :param new_nad: New Node Address
        :type new_nad: int
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(nad, pci_byte(LIN_PCI_SINGLE_FRAME, 6),
                                   LIN_SID_CONDITIONAL_CHANGE_NAD,
                                   identifier, byte, mask, invert,
                                   new_nad)

    def encode_data_dump(self, nad: int, data: Iterable[int]) -> bytearray:
        """
        Encodes a DataDump diagnostic request into a frame

        Example:
        >>> encode_data_dump(nad=0x01, data=[0x01, 0x00, 0x00, 0xFF, 0xFF])

        :param nad: Node Address
        :type nad: int
        :param data: User defined data of 5 bytes
        :type data: Iterable[int]
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(nad, pci_byte(LIN_PCI_SINGLE_FRAME, 6), LIN_SID_DATA_DUMP,
                                   data[0], data[1], data[2], data[3], data[4])

    def encode_save_configuration(self, nad: int) -> bytearray:
        """
        Encodes a SaveConfiguration diagnostic request into a frame

        Example:
        >>> encode_save_configuration(nad=0x01)

        :param nad: Node Address
        :type nad: int
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(nad, pci_byte(LIN_PCI_SINGLE_FRAME, 1),
                                   LIN_SID_SAVE_CONFIGURATION,
                                   0xFF, 0xFF, 0xFF, 0xFF, 0xFF)

    def encode_assign_frame_id_range(self, nad: int, start_index: int,
                                     pids: Iterable[int]) -> bytearray:
        """
        Encodes a AssignFrameIdRange diagnostic request into a frame

        Example:
        >>> encode_assign_frame_id_range(nad=0x01,
                                         start_index=0x00,
                                         pids=[0x32, 0x33, 0x34, 0x35])

        :param nad: Node Address
        :type nad: int
        :param start_index: First message index to assign
        :type start_index: int
        :params pids: Protected identifiers to assign
        :type pids: Iterable[int]
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(nad, pci_byte(LIN_PCI_SINGLE_FRAME, 6),
                                   LIN_SID_ASSIGN_FRAME_ID_RANGE,
                                   start_index,
                                   pids[0], pids[1], pids[2], pids[3])

    def encode_read_by_id(self, nad: int, identifier: int, supplier_id: int,
                          function_id: int) -> bytearray:
        """
        Encodes a ReadById diagnostic request into a frame

        Example:
        >>> encode_read_by_id(nad=0x01,
                              identifier=LIN_SID_READ_BY_ID_SERIAL_NUMBER,
                              supplier_id=0x7FFF,
                              function_id=0xFFFF)

        :param nad: Node Address
        :type nad: int
        :param identifier: Identifier to read
        :type identifier: int
        :param supplier_id: Supplier ID
        :type supplier_id: int
        :param function_id: Function ID
        :type function_id: int
        :returns: Encoded frame
        :rtype: bytearray
        """
        return self.encode_request(nad, pci_byte(LIN_PCI_SINGLE_FRAME, 6), LIN_SID_READ_BY_ID,
                                   identifier,
                                   supplier_id & 0xFF, (supplier_id >> 8) & 0xFF,
                                   function_id & 0xFF, (function_id >> 8) & 0xFF)

class LinDiagnosticResponse(LinDiagnosticFrame):
    """LinDiagnosticResponse is used to decode standard diagnostic responses"""

    _FIELDS = ['NAD', 'PCI', 'RSID', 'D1', 'D2', 'D3', 'D4', 'D5']

    def __init__(self, frame: LinDiagnosticFrame):
        super().__init__(frame.frame_id, frame.name, frame.length, dict(frame.signal_map))
        self._signal_remapper = dict(zip(map(lambda x: x[1].name, frame.signal_map),
                                         LinDiagnosticResponse._FIELDS))

    def decode_response(self, data: bytearray) -> Dict[str, int]:
        """
        Decodes a diagnostic response

        Example:
        >>> decode_response(bytearray([0x00,0x01,0xF0,0xFF,0xFF,0xFF,0xFF,0xFF]))
        {'NAD': 0x00, 'PCI': 0x01, 'RSID': 0xF0, ... }

        :param data: Frame content
        :type data: bytearray
        :returns: Dictionary of field keys and values
        :rtype: Dict[str, int]
        """
        message = self.decode_raw(data)
        return {self._signal_remapper[signal_name]: message[signal_name] for signal_name in message}
