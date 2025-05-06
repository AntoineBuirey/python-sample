from version import Version
import pytest

def test_version_initialization():
    version = Version(1, 0, 0)
    assert version.major == 1
    assert version.minor == 0
    assert version.patch == 0
    assert version.prerelease is None
    assert version.metadata is None
    
def test_version_initialization_from_string():
    version = Version("1", "2", "3", "alpha", "meta")
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.prerelease == "alpha"
    assert version.metadata == "meta"

def test_version_from_string():
    version = Version.from_string("1.2.3-alpha+meta")
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.prerelease == "alpha"
    assert version.metadata == "meta"
    
def test_version_from_string_invalid():
    with pytest.raises(ValueError):
        Version.from_string("invalid.version.string")

@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata, expected_str",
    [
        (1, 0, 0, None, None, "1.0.0"),
        (1, 0, 0, "alpha", None, "1.0.0-alpha"),
        (1, 0, 0, None, "meta", "1.0.0+meta"),
        (1, 0, 0, "alpha", "meta", "1.0.0-alpha+meta"),
        (1, 2, 3, "beta.1", "build.123", "1.2.3-beta.1+build.123"),
    ],
    ids=[
        "no_prerelease_no_metadata",
        "prerelease_no_metadata",
        "no_prerelease_metadata",
        "prerelease_metadata",
        "prerelease_with_build",
    ]
)
def test_version_to_string(major, minor, patch, prerelease, metadata, expected_str):
    version = Version(major, minor, patch, prerelease, metadata)
    assert str(version) == expected_str

@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata, expected_repr",
    [
        (1, 0, 0, None, None, "Version(major=1, minor=0, patch=0, prerelease=None, metadata=None)"),
        (1, 0, 0, "alpha", None, "Version(major=1, minor=0, patch=0, prerelease=alpha, metadata=None)"),
        (1, 0, 0, None, "meta", "Version(major=1, minor=0, patch=0, prerelease=None, metadata=meta)"),
        (1, 0, 0, "alpha", "meta", "Version(major=1, minor=0, patch=0, prerelease=alpha, metadata=meta)"),
        (1, 2, 3, "beta.1", "build.123", "Version(major=1, minor=2, patch=3, prerelease=beta.1, metadata=build.123)")
    ],
    ids=[
        "no_prerelease_no_metadata",
        "prerelease_no_metadata",
        "no_prerelease_metadata",
        "prerelease_metadata",
        "prerelease_with_build",
    ]
)
def test_version_repr(major, minor, patch, prerelease, metadata, expected_repr):
    version = Version(major, minor, patch, prerelease, metadata)
    assert repr(version) == expected_repr
    
@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata",
    [
        (1, 0, 0, None, None),
        (1, 0, 0, "alpha", None),
        (1, 0, 0, None, "meta"),
        (1, 0, 0, "alpha", "meta"),
        (1, 2, 3, "beta.1", "build.123"),
    ],
    ids=[
        "no_prerelease_no_metadata",
        "prerelease_no_metadata",
        "no_prerelease_metadata",
        "prerelease_metadata",
        "prerelease_with_build",
    ]
)
def test_hash(major, minor, patch, prerelease, metadata):
    version = Version(major, minor, patch, prerelease, metadata)
    assert hash(version) == hash((major, minor, patch, prerelease, metadata))

@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata",
    [
        (1, 0, 0, None, None),
        (1, 0, 0, "alpha", None),
        (1, 0, 0, None, "meta"),
        (1, 0, 0, "alpha", "meta"),
        (1, 2, 3, "beta.1", "build.123"),
    ],
    ids=[
        "no_prerelease_no_metadata",
        "prerelease_no_metadata",
        "no_prerelease_metadata",
        "prerelease_metadata",
        "prerelease_with_build",
    ]
)
def test_version_equality_equals(major, minor, patch, prerelease, metadata):
    version1 = Version(major, minor, patch, prerelease, metadata)
    version2 = Version(major, minor, patch, prerelease, metadata)
    assert version1 == version2
    assert version1 is not version2  # Different instances should not be the same object

@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata",
    [
        (1, 0, 0, None, None),
        (1, 0, 0, "alpha", None),
        (1, 0, 0, None, "meta"),
        (1, 0, 0, "alpha", "meta"),
        (1, 2, 3, "beta.1", "build.123"),
    ],
    ids=[
        "no_prerelease_no_metadata",
        "prerelease_no_metadata",
        "no_prerelease_metadata",
        "prerelease_metadata",
        "prerelease_with_build",
    ]
)
def test_version_equality_not_equals(major, minor, patch, prerelease, metadata):
    version1 = Version(major, minor, patch, prerelease, metadata)
    version2 = Version(major + 1, minor, patch, prerelease, metadata)
    assert version1 != version2
    
def test_version_equality_different_metadata():
    version1 = Version(1, 0, 0, metadata="meta1")
    version2 = Version(1, 0, 0, metadata="meta2")
    assert version1 == version2  # Different metadata should not affect equality
    
def test_version_equality_different_types():
    version = Version(1, 0, 0)
    assert version != "1.0.0"  # Different types should not be equal
    assert version != 1.0  # Different types should not be equal

@pytest.mark.parametrize(
    "version1, version2",
    [
        (Version(1, 0, 0), Version(1, 0, 1)), # Same major and minor, different patch
        (Version(1, 0, 0), Version(1, 1, 0)), # Same major, different minor
        (Version(1, 0, 0), Version(2, 0, 0)), # Different major
        (Version(1, 0, 0, "alpha"), Version(1, 0, 0, "beta")), # Same major and minor, different prerelease
        (Version(1, 0, 0, "alpha"), Version(1, 0, 0)), # Same major and minor, with and without prerelease
        (Version(1, 0, 0, "alpha"), Version(1, 0, 0, "alpha.1")), # Same major and minor, different prerelease (sub version)
        (Version(1, 0, 0, "alpha"), Version(1, 0, 0, "beta.1")), # Same major and minor, different prerelease (main version)
        (Version(1, 0, 0, "0"), Version(1, 0, 0, "1")), # Same major and minor, different prerelease (numbers)
        (Version(1, 0, 0, "0.1"), Version(1, 0, 0, "0.2")), # Same major and minor, different prerelease (numbers, sub version)
    ],
    ids=[
        "same_major_minor_different_patch",
        "same_major_different_minor",
        "different_major",
        "same_major_minor_different_prerelease",
        "Same major and minor, with and without prerelease",
        "same_major_minor_different_prerelease (sub version)",
        "same_major_minor_different_prerelease (main version)",
        "same_major_minor_different_prerelease (numbers)",
        "Same major and minor, different prerelease (numbers, sub version)"
    ]
)
def test_version_lower_than_good(version1, version2):
    assert version1 < version2

@pytest.mark.parametrize(
    "version1, version2",
    [
        (Version(1, 0, 0), Version(1, 0, 0)), # Same version
        (Version(1, 0, 0), Version(1, 0, 0, "alpha")), # Same major and minor, with and without prerelease
        (Version(1, 0, 0, "alpha.1.0"), Version(1, 0, 0, "alpha.1.0")), # Same major and minor, different prerelease
        (Version(1, 0, 0, "alpha.1.1"), Version(1, 0, 0, "alpha.1.0")), # Same major and minor, different prerelease (sub version)
    ],
    ids=[
        "same_version",
        "same_major_minor_with_prerelease",
        "same_major_minor_different_prerelease",
        "same_major_minor_different_prerelease (sub version)",
    ]
)
def test_version_lower_than_bad(version1, version2):
    assert not version1 < version2  # Should not be less than or equal to


def test_version_greater_than():
    version1 = Version(1, 0, 1)
    version2 = Version(1, 0, 0)
    assert version1 > version2  # Should be greater than

def test_version_greater_or_equal():
    version1 = Version(1, 0, 0)
    version2 = Version(1, 0, 0)
    version3 = Version(1, 0, 1)
    assert version1 >= version2  # Should be greater than or equal to 
    assert version3 >= version1  # Should be greater than or equal to
    
def test_version_less_or_equal():
    version1 = Version(1, 0, 0)
    version2 = Version(1, 0, 1)
    version3 = Version(1, 0, 0)
    assert version1 <= version2  # Should be less than or equal to 
    assert version3 <= version1  # Should be less than or equal to


def test_version_increment_major():
    version = Version(1, 2, 3)
    version.major_increment()
    assert version.major == 2
    assert version.minor == 0
    assert version.patch == 0

def test_version_increment_minor():
    version = Version(1, 2, 3)
    version.minor_increment()
    assert version.major == 1
    assert version.minor == 3
    assert version.patch == 0

def test_version_increment_patch():
    version = Version(1, 2, 3)
    version.patch_increment()
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 4

def test_version_prerelease_increment():
    version = Version(1, 2, 3, "alpha.1")
    version.prerelease_increment()
    assert version.prerelease == "alpha.2"

def test_version_prerelease_increment_no_subversion():
    version = Version(1, 2, 3)
    with pytest.raises(ValueError):
        version.prerelease_increment()

def test_version_metadata_increment():
    version = Version(1, 2, 3, metadata="1.2")
    version.metadata_increment()
    assert version.metadata == "1.3"

def test_version_metadata_increment_no_metadata():
    version = Version(1, 2, 3)
    with pytest.raises(ValueError):
        version.metadata_increment()

def test_version_is_prerelease():
    version = Version(1, 2, 3, "alpha")
    assert version.is_prerelease() is True

def test_version_has_metadata():
    version = Version(1, 2, 3, metadata="meta")
    assert version.has_metadata() is True

@pytest.mark.parametrize(
    "major, minor, patch, prerelease, metadata",
    [
        ("a", 0, 0, None, None),
        (1, "b", 0, None, None),
        (1, 0, "c", None, None),
    ],
    ids=[
        "invalid_major",
        "invalid_minor",
        "invalid_patch",
    ]
)
def test_version_invalid_initialization(major, minor, patch, prerelease, metadata):
    with pytest.raises(ValueError):
        Version(major, minor, patch, prerelease, metadata)

def test_version_invalid_prerelease():
    with pytest.raises(ValueError):
        Version(1, 0, 0, prerelease="invalid@prerelease")

def test_version_invalid_metadata():
    with pytest.raises(ValueError):
        Version(1, 0, 0, metadata="invalid@metadata")


def test_version_major_decrement():
    version = Version(1, 2, 3)
    version.major_decrement()
    assert version.major == 0
    assert version.minor == 0
    assert version.patch == 0
    
def test_version_major_decrement_0():
    version = Version(0, 0, 0)
    with pytest.raises(ValueError):
        version.major_decrement()

def test_version_minor_decrement():
    version = Version(1, 2, 3)
    version.minor_decrement()
    assert version.major == 1
    assert version.minor == 1
    assert version.patch == 0

def test_version_minor_decrement_0():
    version = Version(1, 0, 0)
    with pytest.raises(ValueError):
        version.minor_decrement()
    
def test_version_patch_decrement():
    version = Version(1, 2, 3)
    version.patch_decrement()
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 2

def test_version_patch_decrement_0():
    version = Version(1, 2, 0)
    with pytest.raises(ValueError):
        version.patch_decrement()


def test_version_prerelease_decrement():
    version = Version(1, 2, 3, "alpha.2")
    version.prerelease_decrement()
    assert version.prerelease == "alpha.1"

def test_version_prerelease_decrement_no_subversion():
    version = Version(1, 2, 3, "alpha")
    with pytest.raises(ValueError):
        version.prerelease_decrement()

def test_version_prerelease_decrement_no_prerelease():
    version = Version(1, 2, 3)
    with pytest.raises(ValueError):
        version.prerelease_decrement()


# if __name__ == "__main__":
#     assert Version.from_string("1.0.0-alpha")       < Version.from_string("1.0.0-alpha.1") 
#     assert Version.from_string("1.0.0-alpha.1")     < Version.from_string("1.0.0-alpha.beta") 
#     assert Version.from_string("1.0.0-alpha.beta")  < Version.from_string("1.0.0-beta") 
#     assert Version.from_string("1.0.0-beta")        < Version.from_string("1.0.0-beta.2") 
#     assert Version.from_string("1.0.0-beta.2")      < Version.from_string("1.0.0-beta.11") 
#     assert Version.from_string("1.0.0-beta.11")     < Version.from_string("1.0.0-rc.1")
#     assert Version.from_string("1.0.0-rc.1")        < Version.from_string("1.0.0")
    
@pytest.mark.parametrize(
    "version1, version2",
    [
        (Version(1, 0, 0, "alpha"), Version(1, 0, 0, "alpha.1")),
        (Version(1, 0, 0, "alpha.1"), Version(1, 0, 0, "alpha.beta")),
        (Version(1, 0, 0, "alpha.beta"), Version(1, 0, 0, "beta")),
        (Version(1, 0, 0, "beta"), Version(1, 0, 0, "beta.2")),
        (Version(1, 0, 0, "beta.2"), Version(1, 0, 0, "beta.11")),
        (Version(1, 0, 0, "beta.11"), Version(1, 0, 0, "rc.1")),
        (Version(1, 0, 0, "rc.1"), Version(1, 0, 0, "rc.2")),
        (Version(1, 0, 0, "rc.2"), Version(1, 0, 0)),
    ],
    ids=[
        "alpha < alpha.1",
        "alpha.1 < alpha.beta",
        "alpha.beta < beta",
        "beta < beta.2",
        "beta.2 < beta.11",
        "beta.11 < rc.1",
        "rc.1 < rc.2",
        "rc.2 < 1.0.0",
    ]
)
def test_version_semver_example(version1, version2):
    assert version1 < version2