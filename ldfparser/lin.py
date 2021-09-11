"""
Utility classes for LIN objects
"""

class LinVersion:
    """
    
    """

    def __init__(self, version: float) -> None:
        self.version : float = version

    def __str__(self) -> str:
        return f"{self.version:.01f}"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, (float, int)):
            return self.version == o
        if isinstance(o, LinVersion):
            return self.version == o.version
        raise False

    def __gt__(self, o) -> bool:
        if isinstance(o, (float, int)):
            return self.version > o
        if isinstance(o, LinVersion):
            return self.version > o.version
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, (float, int)):
            return self.version < o
        if isinstance(o, LinVersion):
            return self.version < o.version
        raise TypeError()

    def __ge__(self, o) -> bool:
        if isinstance(o, (float, int)):
            return self.version >= o
        if isinstance(o, LinVersion):
            return self.version >= o.version
        raise TypeError()

    def __le__(self, o) -> bool:
        if isinstance(o, (float, int)):
            return self.version <= o
        if isinstance(o, LinVersion):
            return self.version <= o.version
        raise TypeError()
