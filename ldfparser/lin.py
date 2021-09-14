"""
Utility classes for LIN objects
"""

class LinVersion:
    """

    """

    def __init__(self, major: int, minor: int) -> None:
        self.major = major
        self.minor = minor

    @staticmethod
    def from_string(self, version: str) -> 'LinVersion':
        (major, minor) = version.split('.')

        return LinVersion(major=int(major), minor=int(minor))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LinVersion):
            return self.major == o.major and self.minor == o.minor
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            return self.major > o.major or self.minor > o.minor
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            return self.major < o.major or self.minor < o.minor
        raise TypeError()

    def __ge__(self, o) -> bool:
        return not self.__lt__(o)

    def __le__(self, o) -> bool:
        return not self.__gt__(o)

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

LIN_VERSION_1_3 = LinVersion(1, 3)
LIN_VERSION_2_0 = LinVersion(2, 0)
LIN_VERSION_2_1 = LinVersion(2, 1)
LIN_VERSION_2_2 = LinVersion(2, 2)
