"""
LIN Signal
"""
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import LinNode
    from .encoding import LinSignalEncodingType
    from .frame import LinUnconditionalFrame

class LinSignal:

    def __init__(self, name: str, width: int, init_value: Union[int, List[int]],
                 publisher: 'LinNode' = None, subscribers: List['LinNode'] = None,
                 encoding_type: 'LinSignalEncodingType' = None,
                 frame: 'LinUnconditionalFrame' = None):
        """
        LinSignal describes the values contained in a LinFrame

        :param name: Signal
        :type name: str
        :param width: Signal size in bits
        :type width: int
        :param init_value: Signal's initial value, for array type signals a List should be passed
        :type init_value: Union[int, List[int]]
        :param publisher: Node that's publishing this signal, defaults to None
        :type publisher: LinNode, optional
        :param subscribers: Nodes that are listening to this signal, defaults to None
        :type subscribers: List[LinNode], optional
        :param encoding_type: Signal encoding type, defaults to None
        :type encoding_type: LinSignalEncodingType, optional
        :param frame: Frame that includes the signal, defaults to None
        :type frame: LinUnconditionalFrame, optional
        """
        self.name = name
        self.width = width
        self.init_value = init_value
        self.publisher = publisher
        self.subscribers = subscribers if subscribers is not None else []
        self.encoding_type = encoding_type
        self.frame = frame

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LinSignal):
            return self.name == o.name
        return False

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __hash__(self) -> int:
        return hash((self.name))

    def is_array(self) -> bool:
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
