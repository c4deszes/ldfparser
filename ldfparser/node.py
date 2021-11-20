"""
LIN Node utilities
"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .frame import LinFrame
    from .signal import LinSignal
    from .lin import LinVersion

LIN_SUPPLIER_ID_WILDCARD = 0x7FFF
LIN_FUNCTION_ID_WILDCARD = 0xFFFF

class LinProductId:
    """
    LinProductId identifies a node's manufacturer and product

    :param supplier_id: a number uniquely identifying the manufacturer of the node
    :type supplier_id: int
    :param function_id: a number assigned by the manufacturer that identifies the product
    :type function_id: int
    :param variant: an optional number identifying a variant of the product
    :type variant: int
    """

    def __init__(self, supplier_id: int, function_id: int, variant: int = 0):
        self.supplier_id: int = supplier_id
        self.function_id: int = function_id
        self.variant: int = variant

    @staticmethod
    def create(supplier_id: int, function_id: int, variant: int = 0):
        """
        Creates a new LinProductId object and validates it's fields
        """
        if supplier_id < 0 or supplier_id > 0x7FFF:
            raise ValueError(f"{supplier_id} is invalid, must be 0-32767")
        if function_id < 0 or function_id > 0xFFFF:
            raise ValueError(f"{function_id} is invalid, must be 0-65535 (16bit)")
        if variant < 0 or variant > 0xFF:
            raise ValueError(f"{variant} is invalid, must be 0-255 (8bit)")

        return LinProductId(supplier_id, function_id, variant)

    def __str__(self) -> str:
        return f"LinProductId(supplier=0x{self.supplier_id:02x},"\
               f"function=0x{self.function_id:02x},variant={self.variant})"

class LinNode:
    """
    Abstract LIN Node class

    Contains the following common attributes:

    :param name: Name of the node
    :type name: str
    :param subscribes_to: LIN signals that the node is subscribed to
    :type subscribes_to: List[LinSignal]
    :param publishes: LIN signals that the node is publishing
    :type publishes: List[LinSignal]
    :param publishes_frames: LIN frames that the node is publishing
    :type publishes_frames: List[LinFrame]
    """

    def __init__(self, name: str):
        self.name = name
        self.subscribes_to: List['LinSignal'] = []
        self.publishes: List['LinSignal'] = []
        self.publishes_frames: List['LinFrame'] = []

class LinMaster(LinNode):
    """
    LinMaster is a LinNode that controls communication on the network

    :param timebase: LIN network timebase in seconds
    :type timebase: float
    :param jitter: LIN network jitter in seconds
    :type jitter: float
    """

    def __init__(self, name: str, timebase: float, jitter: float):
        super().__init__(name)
        self.timebase: float = timebase
        self.jitter: float = jitter

class LinSlave(LinNode):
    """
    LinSlave is a LinNode that is listens to frame headers and publishes signals

    :param lin_protocol: LIN protocol version that the node conforms with
    :type lin_protocol: LinVersion
    :param configured_nad: Network address of the node after network setup
    :type configured_nad: int
    :param initial_nad: Initial network address of the node
    :type intial_nad: int
    :param product_id: Product identifier of the node
    :type product_id: LinProductId
    :param response_error: A signal that the node uses to indicate frame errors
    :type response_error: LinSignal
    :param fault_state_signals: Signals that the node uses to indicate operating errors
    :type fault_state_signals: List[LinSignal]
    :param p2_min:
    :type p2_min:
    :param st_min:
    :type st_min:
    :param n_as_timeout:
    :type n_as_timeout:
    :param n_cr_timeout:
    :type n_cr_timeout:
    :param configurable_frames:
    :type configurable_frames:
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.lin_protocol: 'LinVersion' = None
        self.configured_nad: int = None
        self.initial_nad: int = None
        self.product_id: LinProductId = None
        self.response_error: 'LinSignal' = None
        self.fault_state_signals: List['LinSignal'] = []
        self.p2_min: float = 0.05
        self.st_min: float = 0
        self.n_as_timeout: float = 1
        self.n_cr_timeout: float = 1
        self.configurable_frames = {}

class LinNodeCompositionConfiguration:

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.compositions: List[LinNodeComposition] = []

class LinNodeComposition:

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.nodes: List[LinSlave] = []
