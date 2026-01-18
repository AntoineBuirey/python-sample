#pylint: disable=line-too-long

"""
Version class to represent the version of the software.
Compliant with the Semantic Versioning 2.0.0 specification.
"""

import re
from itertools import zip_longest

class Version:
    """
    Class to represent the version of the software.
    
    Compliant with the Semantic Versioning 2.0.0 specification.
    See https://semver.org/lang/fr/spec/v2.0.0.html for more details.
    """

    _RE_PRELEASE_METADATA = re.compile(r'^[0-9a-zA-Z]+(?:\.[0-9a-zA-Z]+)*$')

    __VERSION_MAJOR = r"(?P<major>\d+)"
    __VERSION_MINOR = r"(?P<minor>\d+)"
    __VERSION_PATCH = r"(?P<patch>\d+)"
    __VERSION_PRERELEASE = r"(?P<prerelease>[0-9a-zA-Z]+(?:\.[0-9a-zA-Z]+)*)"
    __VERSION_METADATA = r"(?P<metadata>[0-9a-zA-Z]+(?:\.[0-9a-zA-Z]+)*)"
    __VERSION = ('^' + __VERSION_MAJOR
                     + r'\.'
                     + __VERSION_MINOR
                     + r'\.'
                     + __VERSION_PATCH
                     + r'(?:-' + __VERSION_PRERELEASE + r')?'
                     + r'(?:\+' + __VERSION_METADATA + r')?'
                     + '$')
    _RE_VERSION = re.compile(__VERSION)
    _4_DIGITS_VERSION = ( '^' + __VERSION_MAJOR
                     + r'\.'
                     + __VERSION_MINOR
                     + r'\.'
                     + __VERSION_PATCH
                     + r'\.'
                     + __VERSION_PRERELEASE
                    + r'(?:\+' + __VERSION_METADATA + r')?'
                    + '$')
    _RE_4_DIGITS_VERSION = re.compile(_4_DIGITS_VERSION)


    def __init__(self,
                 major: int|str,
                 minor: int|str,
                 patch: int|str,
                 prerelease : str|None = None,
                 metadata : str|None = None
                ):
        """
        Initialize the Version object.

        :param major: Major version number
        :param minor: Minor version number
        :param patch: Patch version number
        :param prerelease: Pre-release version (optional)
        :param metadata: Metadata (optional)
        """
        if isinstance(major, str):
            if not major.isdigit():
                raise ValueError(f"Invalid major version: {major}")
            major = int(major)
        if isinstance(minor, str):
            if not minor.isdigit():
                raise ValueError(f"Invalid minor version: {minor}")
            minor = int(minor)
        if isinstance(patch, str):
            if not patch.isdigit():
                raise ValueError(f"Invalid patch version: {patch}")
            patch = int(patch)
        if prerelease and not self._RE_PRELEASE_METADATA.match(prerelease):
            raise ValueError(f"Invalid pre-release version: {prerelease}")
        if metadata and not self._RE_PRELEASE_METADATA.match(metadata):
            raise ValueError(f"Invalid metadata: {metadata}")

        self.__major = major
        self.__minor = minor
        self.__patch = patch
        self.__prerelease = prerelease
        self.__metadata = metadata

    @classmethod
    def from_4_digits(cls, version_str: str):
        """
        Create a Version object from a 4 digits version string.

        :param version: 4 digits version string, separated by dots (e.g. "12.3.456.7")
        :return: Version object
        """
        # if not isinstance(version, str):
        #     raise ValueError(f"Invalid version string: {version}")
        # parts = version.split('.')
        # if len(parts) != 4:
        #     raise ValueError(f"Invalid version string: {version}")
        # major = int(parts[0] or 0)
        # minor = int(parts[1] or 0)
        # patch = int(parts[2] or 0)
        
        # if "+" in parts[3]:
        #     prerelease, metadata = parts[3].split("+", 1)
        # else:
        #     metadata = None
        #     prerelease = parts[3]
        
        # prerelease = prerelease or None
        # metadata = metadata or None
        # return Version(major, minor, patch, prerelease, metadata)
        match = cls._RE_4_DIGITS_VERSION.match(version_str)
        if not match:
            raise ValueError(f"Invalid version string: {version_str}")

        major = int(match.group('major') or 0)
        minor = int(match.group('minor') or 0)
        patch = int(match.group('patch') or 0)
        prerelease = match.group('prerelease') or None
        metadata = match.group('metadata') or None

        return cls(major, minor, patch, prerelease, metadata)

    @classmethod
    def from_string(cls, version_str: str):
        """
        Create a Version object from a version string.

        :param version_str: Version string
        :return: Version object
        """
        if cls._RE_4_DIGITS_VERSION.match(version_str):
            return cls.from_4_digits(version_str)

        match = cls._RE_VERSION.match(version_str)
        if not match:
            raise ValueError(f"Invalid version string: {version_str}")

        major = int(match.group('major'))
        minor = int(match.group('minor'))
        patch = int(match.group('patch'))
        prerelease = match.group('prerelease')
        metadata = match.group('metadata')

        return cls(major, minor, patch, prerelease, metadata)

    @classmethod
    def is_valid_string(cls, version_str: str) -> bool:
        """
        Check if a version string is valid.

        :param version_str: Version string
        :return: True if valid, False otherwise
        """
        return bool(cls._RE_VERSION.match(version_str)) or bool(cls._RE_4_DIGITS_VERSION.match(version_str))

    def __str__(self) -> str:
        """
        Return the version as a string.

        :return: Version string
        """
        version_str = f"{self.__major}.{self.__minor}.{self.__patch}"
        if self.__prerelease:
            version_str += f"-{self.__prerelease}"
        if self.__metadata:
            version_str += f"+{self.__metadata}"
        return version_str
    
    def to_python_version(self) -> str:
        """
        Return the version as a Python compatible version string.

        :return: Python compatible version string
        """
        version_str = f"{self.__major}.{self.__minor}.{self.__patch}"
        if self.__prerelease:
            prerelease = self.__prerelease.replace('.', '_').replace('-', '_')
            version_str += f".{prerelease}"
        if self.__metadata:
            metadata = self.__metadata.replace('.', '_').replace('-', '_')
            version_str += f".{metadata}"
        return version_str

    def __repr__(self) -> str:
        """
        Return a string representation of the Version object.

        :return: String representation
        """
        return f"Version(major={self.__major}, minor={self.__minor}, patch={self.__patch}, prerelease={self.__prerelease}, metadata={self.__metadata})"

    def __hash__(self):
        """
        Return the hash of the Version object.

        :return: Hash value
        """
        return hash((self.__major, self.__minor, self.__patch, self.__prerelease, self.__metadata))

    def __eq__(self, other : object) -> bool:
        """
        Check if two Version objects are equal.
        
        As defined in https://semver.org/lang/fr/#spec-item-10,
        the comparison is done on the major, minor, patch and pre-release version.
        Metadata is not considered for comparison.
        
        :param other: Other Version object
        :return: True if equal, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented
        return ( self.__major,  self.__minor,  self.__patch,  self.__prerelease) \
            == (other.major, other.minor, other.patch, other.prerelease)

    def __lt__(self, other : object) -> bool: #pylint: disable=too-many-return-statements
        """
        Compare two Version objects.
        
        As defined in https://semver.org/lang/fr/#spec-item-10,
        the comparison is done on the major, minor, patch and pre-release version.
        Metadata is not considered for comparison.

        :param other: Other Version object
        :return: True if this version is less than the other, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented

        if self.__major != other.major: # 1.0.0 < 2.0.0
            return self.__major < other.major
        if self.__minor != other.minor: # 1.1.0 < 1.2.0
            return self.__minor < other.minor
        if self.__patch != other.patch: # 1.1.1 < 1.1.2
            return self.__patch < other.patch

        # if self.__prerelease is None and other.prerelease is not None: # 1.0.0 < 1.0.0-alpha
        #     return False
        # if self.__prerelease is not None and other.prerelease is None: # 1.0.0-alpha < 1.0.0
        #     return True
        # if self.__prerelease is None and other.prerelease is None: # 1.0.0 < 1.0.0
        #     return False
        if self.__prerelease is None:
            return False # 1.0.0 > 1.0.0-alpha or 1.0.0 < 1.0.0
        if other.prerelease is None:
            return True # 1.0.0-alpha < 1.0.0
        
        # case like 1.0.0-alpha < 1.0.0-beta

        self_tokens = self.__prerelease.split('.')
        other_tokens = other.prerelease.split('.')
        for self_token, other_token in zip_longest(self_tokens, other_tokens, fillvalue=''):
            if self_token.isdigit() and other_token.isdigit():
                if int(self_token) != int(other_token):
                    return int(self_token) < int(other_token)
            else:
                if self_token != other_token:
                    return self_token < other_token
        return False

    def __gt__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is greater than the other, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented

        return other < self

    def __ge__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is greater than or equal to the other, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented

        return self > other or self == other

    def __le__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is less than or equal to the other, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented

        return self < other or self == other

    def __ne__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is not equal to the other, False otherwise
        """
        if not isinstance(other, Version): #pragma: no cover
            return NotImplemented

        return not self == other

    def major_increment(self) -> "Version":
        """
        Increment the major version.\n
        Reset minor and patch versions to 0.\n
        Reset pre-release and metadata to None.

        :return: self
        """
        self.__major += 1
        self.__minor = 0
        self.__patch = 0
        self.__prerelease = None
        self.__metadata = None
        return self

    def minor_increment(self) -> "Version":
        """
        Increment the minor version.\n
        Reset patch version to 0.\n
        Reset pre-release and metadata to None.

        :return: self
        """
        self.__minor += 1
        self.__patch = 0
        self.__prerelease = None
        self.__metadata = None
        return self

    def patch_increment(self) -> "Version":
        """
        Increment the patch version.\n
        Reset pre-release and metadata to None.
        
        :return: self
        """
        self.__patch += 1
        self.__prerelease = None
        self.__metadata = None
        return self

    def prerelease_increment(self) -> "Version":
        """
        Increment the pre-release version.\n
        Reset metadata to None.
        
        Support only prerelease version of the form `x.y.z-alpha.1` or `x.y.z-alpha.1.2`.\n
        
        :return: self
        """
        if self.__prerelease is None:
            raise ValueError("No pre-release version to increment")
        prerelease_parts = self.__prerelease.split('.')
        prerelease_parts[-1] = str(int(prerelease_parts[-1]) + 1)
        self.__prerelease = '.'.join(prerelease_parts)
        self.__metadata = None
        return self

    def metadata_increment(self) -> "Version":
        """
        Increment the metadata version.\n
        
        Support only metadata version of the form `x.y.z+1` or `x.y.z+1.2`.\n
        
        :return: self
        """
        if self.__metadata is None:
            raise ValueError("No metadata version to increment")
        metadata_parts = self.__metadata.split('.')
        metadata_parts[-1] = str(int(metadata_parts[-1]) + 1)
        self.__metadata = '.'.join(metadata_parts)
        return self

    def is_prerelease(self) -> bool:
        """
        Check if the version is a pre-release version.

        :return: True if pre-release, False otherwise
        """
        return self.__prerelease is not None

    def has_metadata(self) -> bool:
        """
        Check if the version has metadata.

        :return: True if metadata, False otherwise
        """
        return self.__metadata is not None

    def major_decrement(self) -> "Version":
        """
        Decrement the major version.\n
        Reset minor and patch versions to 0.\n
        Reset pre-release and metadata to None.

        :return: self
        """
        if self.__major == 0:
            raise ValueError("Cannot decrement major version below 0")
        self.__major -= 1
        self.__minor = 0
        self.__patch = 0
        self.__prerelease = None
        self.__metadata = None
        return self

    def minor_decrement(self) -> "Version":
        """
        Decrement the minor version.\n
        Reset patch version to 0.\n
        Reset pre-release and metadata to None.

        :return: self
        """
        if self.__minor == 0:
            raise ValueError("Cannot decrement minor version below 0")
        self.__minor -= 1
        self.__patch = 0
        self.__prerelease = None
        self.__metadata = None
        return self

    def patch_decrement(self) -> "Version":
        """
        Decrement the patch version.\n
        Reset pre-release and metadata to None.

        :return: self
        """
        if self.__patch == 0:
            raise ValueError("Cannot decrement patch version below 0")
        self.__patch -= 1
        self.__prerelease = None
        self.__metadata = None
        return self

    def prerelease_decrement(self) -> "Version":
        """
        Decrement the pre-release version.\n
        Reset metadata to None.

        :return: self
        """
        if self.__prerelease is None:
            raise ValueError("No pre-release version to decrement")
        prerelease_parts = self.__prerelease.split('.')
        if len(prerelease_parts) == 1:
            raise ValueError("Cannot decrement pre-release version below 0")
        prerelease_parts[-1] = str(int(prerelease_parts[-1]) - 1)
        self.__prerelease = '.'.join(prerelease_parts)
        self.__metadata = None
        return self

    @property
    def major(self) -> int:
        """
        Get the major version number.

        :return: Major version number
        """
        return self.__major
    
    @major.setter
    def major(self, value: int) -> None:
        """
        Set the major version number.

        :param value: Major version number
        """
        if not isinstance(value, int):
            raise ValueError(f"Invalid major version: {value}")
        self.__major = value

    @property
    def minor(self) -> int:
        """
        Get the minor version number.

        :return: Minor version number
        """
        return self.__minor

    @minor.setter
    def minor(self, value: int) -> None:
        """
        Set the minor version number.

        :param value: Minor version number
        """
        if not isinstance(value, int):
            raise ValueError(f"Invalid minor version: {value}")
        self.__minor = value

    @property
    def patch(self) -> int:
        """
        Get the patch version number.

        :return: Patch version number
        """
        return self.__patch

    @patch.setter
    def patch(self, value: int) -> None:
        """
        Set the patch version number.

        :param value: Patch version number
        """
        if not isinstance(value, int):
            raise ValueError(f"Invalid patch version: {value}")
        self.__patch = value

    @property
    def prerelease(self) -> str|None:
        """
        Get the pre-release version.

        :return: Pre-release version
        """
        return self.__prerelease

    @prerelease.setter
    def prerelease(self, value: str|None) -> None:
        """
        Set the pre-release version.

        :param value: Pre-release version
        """
        if value and not self._RE_PRELEASE_METADATA.match(value):
            raise ValueError(f"Invalid pre-release version: {value}")
        self.__prerelease = value

    @property
    def metadata(self) -> str|None:
        """
        Get the metadata version.

        :return: Metadata version
        """
        return self.__metadata

    @metadata.setter
    def metadata(self, value: str|None) -> None:
        """
        Set the metadata version.

        :param value: Metadata version
        """
        if value and not self._RE_PRELEASE_METADATA.match(value):
            raise ValueError(f"Invalid metadata version: {value}")
        self.__metadata = value
