"""
Utility classes for LIN objects
"""
from typing import Union


class LinVersion:
    """
    LinVersion represents the LIN protocol and LDF language versions
    """

    def __init__(self, major: int, minor: int, use_j2602=False) -> None:
        self.major = major
        self.minor = minor
        self.use_j2602 = use_j2602

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
        elif isinstance(o, J2602Version):
            return self.major == 2 and self.minor == 0
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            if self.major > o.major:
                return True
            if self.major == o.major and self.minor > o.minor:
                return True
            return False
        elif isinstance(o, J2602Version):
            return (self.major == 2 and self.minor > 0) or self.major > 2
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, LinVersion):
            if self.major < o.major:
                return True
            if self.major == o.major and self.minor < o.minor:
                return True
            return False
        elif isinstance(o, J2602Version):
            return self.major < 2
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

    def __init__(self, revision: int, use_j2602: bool = False) -> None:
        self.revision = revision
        self.use_j2602 = use_j2602

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

class J2602Version:
    def __init__(self, major, minor, part):
        """
        Abstract the J2602 version.
        """
        self.major = major
        self.minor = minor
        self.part = part

    @staticmethod
    def from_string(version: str) -> 'J2602Version':
        """
        Create an instance from the version string.

        The version string J2602_1_2.0 will render:
            major=2, minor=0, part=1

        Support for J2602_1_2.0 is not implemented at this time.
        """
        if "J2602" not in version:
            raise ValueError(f'{version} is not an SAE J2602 version.')

        version = version.replace("J2602_", '')
        (part, versions) = version.split('_')
        major, minor = [int(value) for value in versions.split('.')]
        if major == 1:
            return J2602Version(major=major, minor=minor, part=int(part))

        raise ValueError(f'{version} is not supported yet.')

    def __str__(self) -> str:
        return f"J2602_{self.part}_{self.major}.{self.minor}"

    def __eq__(self, o: object) -> bool:
        """
        According to J2602-3_202110, section 7.1.3:
        “J2602_1_1.0” -> J2602:2012 and earlier -> based on LIN 2.0
        “J2602_1_2.0” -> J2602:2021 -> based on ISO 17987:2016

        Therefore,
        “J2602_1_1.0” is considered equal to LinVersion(2, 0)

        """
        if isinstance(o, J2602Version):
            return (
                self.major == o.major and
                self.minor == o.minor and
                self.part == o.part
            )
        elif isinstance(o, Iso17987Version):
            return False
        elif isinstance(o, LinVersion):
            return o == LIN_VERSION_2_0
        return False

    def __gt__(self, o) -> bool:
        if isinstance(o, J2602Version):
            return (
                self.major > o.major or
                (
                    self.major == o.major and self.minor > o.minor
                )
            )
        if isinstance(o, Iso17987Version):
            return False
        if isinstance(o, LinVersion):
            return o < LIN_VERSION_2_0
        raise TypeError()

    def __lt__(self, o) -> bool:
        if isinstance(o, J2602Version):
            return (
                self.major < o.major or
                (
                    self.major == o.major and self.minor < o.minor
                )
            )
        if isinstance(o, Iso17987Version):
            return True
        if isinstance(o, LinVersion):
            return o > LIN_VERSION_2_0
        raise TypeError()

    def __ge__(self, o) -> bool:
        return not self.__lt__(o)

    def __le__(self, o) -> bool:
        return not self.__gt__(o)

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

def parse_lin_version(version: str) -> Union[LinVersion, Iso17987Version, J2602Version]:
    for version_class in [LinVersion, Iso17987Version, J2602Version]:
        try:
            return version_class.from_string(version)
        except (ValueError, IndexError):
            pass

    raise ValueError(f'{version} is not a valid LIN version.')
