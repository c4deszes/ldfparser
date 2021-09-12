"""
Utility classes for LIN objects
"""

class LinVersion:
    """

    """

    def __init__(self, version: float) -> None:
        self.version: float = version

    def __str__(self) -> str:
        return f"{self.version:.01f}"

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LinVersion):
            return self.version == o.version
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            return self.version > o.version
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            return self.version < o.version
        raise TypeError()

    def __ge__(self, o) -> bool:
        return not self.__lt__(o)

    def __le__(self, o) -> bool:
        return not self.__gt__(o)

LIN_VERSION_1_3 = LinVersion(1.3)
LIN_VERSION_2_0 = LinVersion(2.0)
LIN_VERSION_2_1 = LinVersion(2.1)
LIN_VERSION_2_2 = LinVersion(2.2)
