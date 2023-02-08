"""
Utility classes for LIN objects
"""
from typing import Union

class LinVersion:
    """
    LinVersion represents the LIN protocol and LDF language versions
    """

    def __init__(self, major: int, minor: int) -> None:
        self.major = major
        self.minor = minor

    @staticmethod
    def from_string(version: str) -> 'LinVersion':
        """
        Creates a LinVersion object from the given string

        :Example:
        `LinVersion.create('2.1')` will return `LinVersion(major=2, minor=1)`

        :param version: Version
        :type version: str
        :returns: LIN version
        :rtype: LinVersion
        """
        (major, minor) = version.split('.')

        return LinVersion(major=int(major), minor=int(minor))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __float__(self) -> float:
        # This function shall be removed once the properties on the LDF object
        # have been deprecated and removed
        return self.major + self.minor * 0.1

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LinVersion):
            return self.major == o.major and self.minor == o.minor
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            if self.major > o.major:
                return True
            if self.major == o.major and self.minor > o.minor:
                return True
            return False
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            if self.major < o.major:
                return True
            if self.major == o.major and self.minor < o.minor:
                return True
            return False
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

class Iso17987Version:
    
    def __init__(self, revision: int) -> None:
        self.revision = revision
    
    @staticmethod
    def from_string(version: str) -> 'Iso17987Version':
        (standard, revision) = version.split(':')

        return Iso17987Version(int(revision))

    def __str__(self) -> str:
        return f"ISO17987:{self.revision}"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Iso17987Version):
            return self.revision == o.revision
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, Iso17987Version):
            return (self.revision > o.revision)
        if isinstance(o, LinVersion):
            return True
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, Iso17987Version):
            return (self.revision < o.revision)
        if isinstance(o, LinVersion):
            return False
        raise TypeError()

    def __ge__(self, o) -> bool:
        return not self.__lt__(o)

    def __le__(self, o) -> bool:
        return not self.__gt__(o)

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

ISO17987_2015 = Iso17987Version(2015)

def parse_lin_version(version: str) -> Union[LinVersion, Iso17987Version]:
    try:
        return LinVersion.from_string(version)
    except ValueError:
        try:
            return Iso17987Version.from_string(version)
        except ValueError:
            raise ValueError(f'{version} is not a valid LIN version.')
