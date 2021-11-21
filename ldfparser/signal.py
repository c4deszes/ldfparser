"""
LIN Signal
"""
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import LinNode
    from .encoding import LinSignalEncodingType

class LinSignal:
    """
    LinSignal describes values contained inside LinFrames

    :param name: Name of the signal
    :type name: str
    :param width: Width of the signal in bits
    :type width: int
    :param init_value: Initial or default value of the signal
    :type init_value: int or List[int] in case of array signals
    :param publisher: Node that publishes the signal
    :type publisher: LinNode
    :param subscribers: Nodes that subscribe to the signal
    :type subscribers: List[LinNode]
    """

    def __init__(self, name: str, width: int, init_value: Union[int, List[int]]):
        self.name: str = name
        self.width: int = width
        self.init_value: Union[int, List[int]] = init_value
        self.publisher: 'LinNode' = None
        self.subscribers: List['LinNode'] = []
        self.encoding_type: 'LinSignalEncodingType' = None

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LinSignal):
            return self.name == o.name
        return False

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __hash__(self) -> int:
        return hash((self.name))

    def is_array(self):
        """
        Returns whether the Signal is array type

        :returns: `True` if the signal is an array
        :rtype: bool
        """
        return isinstance(self.init_value, List)

    @staticmethod
    def create(name: str, width: int, init_value: Union[int, List[int]]):
        """
        Creates a LinSignal object and validates it's fields
        """
        if isinstance(init_value, List):
            if width % 8 != 0:
                raise ValueError(f"array signal {name}:{width} must have a 8 * n width (8, 16, ..)")
            if width < 8 or width > 64:
                raise ValueError(f"array signal {name}:{width} must be 8-64bits long")
            if len(init_value) != width / 8:
                raise ValueError(f"array signal {name}:{width} init value doesn't match the width")
        if isinstance(init_value, int) and (width < 1 or width > 16):
            raise ValueError(f"scalar signal {name}:{width} must be 1-16 bits long")
        return LinSignal(name, width, init_value)
