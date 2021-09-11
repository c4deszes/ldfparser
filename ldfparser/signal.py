"""

"""
from typing import List, Union

class LinSignal:
    """
    
    """

    def __init__(self, name: str, width: int, init_value: Union[int, List[int]]):
        self.name: str = name
        self.width: int = width
        self.init_value: Union[int, List[int]] = init_value
        self.publisher = None
        self.subscribers = []

    def is_array(self):
        """
        Returns whether the Signal is array type
        """
        return isinstance(self.init_value, List)

    @staticmethod
    def create(name: str, width: int, init_value: Union[int, List[int]]):
        """
        Factory method for creating LinSignal objects
        """
        if isinstance(init_value, List):
            if width % 8 != 0:
                raise ValueError(f"array signal {name}:{width} must be a multiple of 8 long (8, 16, 24, ..)")
            if width < 8 or width > 64:
                raise ValueError(f"array signal {name}:{width} must be 8-64bits long")
            if len(init_value) != width / 8:
                raise ValueError(f"array signal {name}:{width} init value is invalid {len(init_value)}")
        if isinstance(init_value, int) and (width < 1 or width > 16):
            raise ValueError(f"scalar signal {name}:{width} must be 1-16bits long")
        return LinSignal(name, width, init_value)
