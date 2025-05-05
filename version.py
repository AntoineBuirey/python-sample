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
        if prerelease is not None and not isinstance(prerelease, str):
            raise ValueError(f"Invalid pre-release version: {prerelease}")
        if metadata is not None and not isinstance(metadata, str):
            raise ValueError(f"Invalid metadata: {metadata}")
        if prerelease and not self._RE_PRELEASE_METADATA.match(prerelease):
            raise ValueError(f"Invalid pre-release version: {prerelease}")
        if metadata and not self._RE_PRELEASE_METADATA.match(metadata):
            raise ValueError(f"Invalid metadata: {metadata}")

        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.metadata = metadata

    @classmethod
    def from_string(cls, version_str: str):
        """
        Create a Version object from a version string.

        :param version_str: Version string
        :return: Version object
        """
        match = cls._RE_VERSION.match(version_str)
        if not match:
            raise ValueError(f"Invalid version string: {version_str}")

        major = int(match.group('major'))
        minor = int(match.group('minor'))
        patch = int(match.group('patch'))
        prerelease = match.group('prerelease')
        metadata = match.group('metadata')

        return cls(major, minor, patch, prerelease, metadata)

    def __str__(self) -> str:
        """
        Return the version as a string.

        :return: Version string
        """
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version_str += f"-{self.prerelease}"
        if self.metadata:
            version_str += f"+{self.metadata}"
        return version_str

    def __repr__(self) -> str:
        """
        Return a string representation of the Version object.

        :return: String representation
        """
        return f"Version(major={self.major}, minor={self.minor}, patch={self.patch}, prerelease={self.prerelease}, metadata={self.metadata})"

    def __hash__(self):
        """
        Return the hash of the Version object.

        :return: Hash value
        """
        return hash((self.major, self.minor, self.patch, self.prerelease, self.metadata))

    def __eq__(self, other : object) -> bool:
        """
        Check if two Version objects are equal.
        
        As defined in https://semver.org/lang/fr/#spec-item-10,
        the comparison is done on the major, minor, patch and pre-release version.
        Metadata is not considered for comparison.
        
        :param other: Other Version object
        :return: True if equal, False otherwise
        """
        if not isinstance(other, Version):
            return NotImplemented
        return ( self.major,  self.minor,  self.patch,  self.prerelease) \
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
        if not isinstance(other, Version):
            return NotImplemented

        if self.major != other.major: # 1.0.0 < 2.0.0
            return self.major < other.major
        if self.minor != other.minor: # 1.1.0 < 1.2.0
            return self.minor < other.minor
        if self.patch != other.patch: # 1.1.1 < 1.1.2
            return self.patch < other.patch

        if self.prerelease is None and other.prerelease is not None: # 1.0.0 < 1.0.0-alpha
            return False
        if self.prerelease is not None and other.prerelease is None: # 1.0.0-alpha < 1.0.0
            return True
        if self.prerelease is not None and other.prerelease is not None: # 1.0.0-alpha < 1.0.0-beta
            self_tokens = self.prerelease.split('.')
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
        if not isinstance(other, Version):
            return NotImplemented

        return other < self

    def __ge__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is greater than or equal to the other, False otherwise
        """
        if not isinstance(other, Version):
            return NotImplemented

        return self > other or self == other

    def __le__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is less than or equal to the other, False otherwise
        """
        if not isinstance(other, Version):
            return NotImplemented

        return self < other or self == other

    def __ne__(self, other : object) -> bool:
        """
        Compare two Version objects.

        :param other: Other Version object
        :return: True if this version is not equal to the other, False otherwise
        """
        if not isinstance(other, Version):
            return NotImplemented

        return not self == other

    def major_increment(self) -> None:
        """
        Increment the major version.\n
        Reset minor and patch versions to 0.\n
        Reset pre-release and metadata to None.

        :return: None
        """
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.prerelease = None
        self.metadata = None

    def minor_increment(self) -> None:
        """
        Increment the minor version.\n
        Reset patch version to 0.\n
        Reset pre-release and metadata to None.

        :return: None
        """
        self.minor += 1
        self.patch = 0
        self.prerelease = None
        self.metadata = None

    def patch_increment(self) -> None:
        """
        Increment the patch version.\n
        Reset pre-release and metadata to None.
        
        :return: None
        """
        self.patch += 1
        self.prerelease = None
        self.metadata = None

    def prerelease_increment(self) -> None:
        """
        Increment the pre-release version.\n
        Reset metadata to None.
        
        Support only prerelease version of the form `x.y.z-alpha.1` or `x.y.z-alpha.1.2`.\n
        
        :return: None
        """
        if self.prerelease is None:
            raise ValueError("No pre-release version to increment")
        prerelease_parts = self.prerelease.split('.')
        prerelease_parts[-1] = str(int(prerelease_parts[-1]) + 1)
        self.prerelease = '.'.join(prerelease_parts)
        self.metadata = None

    def metadata_increment(self) -> None:
        """
        Increment the metadata version.\n
        
        Support only metadata version of the form `x.y.z+1` or `x.y.z+1.2`.\n
        
        :return: None
        """
        if self.metadata is None:
            raise ValueError("No metadata version to increment")
        metadata_parts = self.metadata.split('.')
        metadata_parts[-1] = str(int(metadata_parts[-1]) + 1)
        self.metadata = '.'.join(metadata_parts)

    def is_prerelease(self) -> bool:
        """
        Check if the version is a pre-release version.

        :return: True if pre-release, False otherwise
        """
        return self.prerelease is not None

    def has_metadata(self) -> bool:
        """
        Check if the version has metadata.

        :return: True if metadata, False otherwise
        """
        return self.metadata is not None


if __name__ == "__main__":
    assert Version.from_string("1.0.0-alpha")       < Version.from_string("1.0.0-alpha.1")
    assert Version.from_string("1.0.0-alpha.1")     < Version.from_string("1.0.0-alpha.beta")
    assert Version.from_string("1.0.0-alpha.beta")  < Version.from_string("1.0.0-beta")
    assert Version.from_string("1.0.0-beta")        < Version.from_string("1.0.0-beta.2")
    assert Version.from_string("1.0.0-beta.2")      < Version.from_string("1.0.0-beta.11")
    assert Version.from_string("1.0.0-beta.11")     < Version.from_string("1.0.0-rc.1")
    assert Version.from_string("1.0.0-rc.1")        < Version.from_string("1.0.0")
