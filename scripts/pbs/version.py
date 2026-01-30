from __future__ import annotations

import itertools, packaging.version, re, unittest
from typing import Any, NamedTuple, Tuple, Union

__all__ = [ 'VERSION_PATTERN', 'InvalidVersion', 'Version', 'parse' ]

CmpPrePostDevType = Union[
    packaging.version.InfinityType,
    packaging.version.NegativeInfinityType,
    Tuple[str, int]
]

LocalType = Tuple[Union[int, str], ...]

CmpLocalType = Union[
    packaging.version.NegativeInfinityType,
    Tuple[Union[Tuple[int, str], Tuple[packaging.version.NegativeInfinityType, Union[int, str]]], ...],
]

PortableType = Tuple[Union[int, str], ...]

CmpPortableType = Union[
    packaging.version.NegativeInfinityType,
    Tuple[Union[Tuple[int, str], Tuple[packaging.version.NegativeInfinityType, Union[int, str]]], ...],
]

CmpKey = Tuple[
    Tuple[int, ...],
    CmpPrePostDevType,
    CmpPrePostDevType,
    CmpPrePostDevType,
    CmpLocalType,
    CmpPortableType,
]

class _Version(NamedTuple):
    release: tuple[int, ...]
    pre: tuple[str, int] | None
    post: tuple[str, int] | None
    dev: tuple[str, int] | None
    local: LocalType | None
    portable: PortableType | None

class InvalidVersion(ValueError):
    """Raised when a version string is not a valid version.

    >>> Version("invalid")
    Traceback (most recent call last):
        ...
    packaging.version.InvalidVersion: Invalid version: 'invalid'
    """

class _BaseVersion:
    _key: tuple[Any, ...]

    def __hash__(self) -> int:
        return hash(self._key)

    # Please keep the duplicated `isinstance` check
    # in the six comparisons hereunder
    # unless you find a way to avoid adding overhead function calls.
    def __lt__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key < other._key

    def __le__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key <= other._key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key == other._key

    def __ge__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key >= other._key

    def __gt__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key > other._key

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key != other._key

# Deliberately not anchored to the start and end of the string, to make it
# easier for 3rd party code to reuse
_VERSION_PATTERN = r"""
    v?
    (?:
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            (?P<pre_sep>[-_\.]?)
            (?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)
            [-_\.]?
            (?P<pre_n>[0-9a-z]+)?
        )?
        (?P<post>                                         # post release
            (?:
                (?P<post_sep1>-)
                (?P<post_n1>[0-9]+)
            )
            |
            (?:
                (?P<post_sep2>[-_\.]?)
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            (?P<dev_sep>[-_\.]?)
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:                                                   # local version (json-c)
        (?P<local_sep>[-_])
        (?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*)
    )?
    (?:p(?P<portable>[0-9]))?                             # portable version (OpenSSH)
"""

"""
A string containing the regular expression used to match a valid version.

The pattern is not anchored at either end, and is intended for embedding in larger
expressions (for example, matching a version number as part of a file name). The
regular expression should be compiled with the ``re.VERBOSE`` and ``re.IGNORECASE``
flags set.

:meta hide-value:
"""
VERSION_PATTERN = _VERSION_PATTERN

def _split(version: str, separators: str | re.Pattern = re.compile(r'([-_\.])')):
    if isinstance(separators, str):
        separators = re.compile(separators)

    result = re.split(separators, version)

    return [ (None, result[0]), *zip(result[1::2], result[2::2]) ]

def _join(parts: tuple[str, str]):
    result = ""

    for sep, part in parts:
        if sep is not None:
            result = sep.join([ result, str(part) ])
        else:
            result += str(part)

    return result

def _parse_letter_version(
    sep: str | None, letter: str | None, number: str | bytes | SupportsInt | None
) -> tuple[str, int] | None:
    if letter:
        number = int(number) if number else None

        return sep, letter, number

    assert not letter
    if number:
        # We assume if we are given a number, but we are not given a letter
        # then this is using the implicit post release syntax (e.g. 1.0-1)
        if not sep:
            letter = "post"
        else:
            letter = ""

        return sep, letter, int(number)

    return None

_local_version_separators = re.compile(r"([\._-])")

def _parse_local_version(separator: str | None, local: str | None) -> LocalType | None:
    """
    Takes a string like abc.1.twelve and turns it into ("abc", ".", 1, ".", "twelve").
    """
    if local is not None:
        return (separator, tuple(
            (sep, part.lower()) if not part.isdigit() else (sep, int(part))
            for sep, part in _split(local, _local_version_separators)
        ))
    return None

_portable_version_separators = re.compile(r"[\._-]")

def _parse_portable_version(portable: str | None) -> PortableType | None:
    """
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    """
    if portable is not None:
        return tuple(
            part.lower() if not part.isdigit() else int(part)
            for part in _portable_version_separators.split(portable)
        )
    return None

def _cmpkey(
    release: tuple[int, ...],
    pre: tuple[str, int] | None,
    post: tuple[str, int] | None,
    dev: tuple[str, int] | None,
    local: LocalType | None,
    portable: str | None,
) -> CmpKey:
    # When we compare a release version, we want to compare it with all of the
    # trailing zeros removed. So we'll use a reverse the list, drop all the now
    # leading zeros until we come to something non zero, then take the rest
    # re-reverse it back into the correct order and make it a tuple and use
    # that for our sorting key.
    _release = tuple(
        reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(release))))
    )

    # We need to "trick" the sorting algorithm to put 1.0.dev0 before 1.0a0.
    # We'll do this by abusing the pre segment, but we _only_ want to do this
    # if there is not a pre or a post segment. If we have one of those then
    # the normal sorting rules will handle this case correctly.
    if pre is None and post is None and dev is not None:
        _pre: CmpPrePostDevType = packaging.version.NegativeInfinity
    # Versions without a pre-release (except as noted above) should sort after
    # those with one.
    elif pre is None:
        _pre = packaging.version.Infinity
    else:
        _pre = pre

    # Versions without a post segment should sort before those with one.
    if post is None:
        _post: CmpPrePostDevType = packaging.version.NegativeInfinity

    else:
        _post = post

    # Versions without a development segment should sort after those with one.
    if dev is None:
        _dev: CmpPrePostDevType = packaging.version.Infinity

    else:
        _dev = dev

    if local is None:
        # Versions without a local segment should sort before those with one.
        _local: CmpLocalType = packaging.version.NegativeInfinity
    else:
        # Versions with a local segment need that segment parsed to implement
        # the sorting rules in PEP440.
        # - Alpha numeric segments sort before numeric segments
        # - Alpha numeric segments sort lexicographically
        # - Numeric segments sort numerically
        # - Shorter versions sort before longer versions when the prefixes
        #   match exactly
        _local = tuple(
            (i, "") if isinstance(i, int) else (packaging.version.NegativeInfinity, i) for i in local
        )

    if portable is None:
        _portable: CmpLocalType = packaging.version.NegativeInfinity
    else:
        _portable = tuple(
            (i, "") if isinstance(i, int) else (packaging.version.NegativeInfinity, i) for i in portable
        )

    return _release, _pre, _post, _dev, _local, _portable

class Version(_BaseVersion):
    """This class abstracts handling of a project's versions.

    A :class:`Version` instance is comparison aware and can be compared and
    sorted using the standard Python interfaces.

    >>> v1 = Version("1.0a5")
    >>> v2 = Version("1.0")
    >>> v1
    <Version('1.0a5')>
    >>> v2
    <Version('1.0')>
    >>> v1 < v2
    True
    >>> v1 == v2
    False
    >>> v1 > v2
    False
    >>> v1 >= v2
    False
    >>> v1 <= v2
    True
    """

    _regex = re.compile(r"^\s*" + VERSION_PATTERN + r"\s*$", re.VERBOSE | re.IGNORECASE)
    _key: CmpKey

    def __init__(self, version: str) -> None:
        """Initialize a Version object.

        :param version:
            The string representation of a version which will be parsed and normalized
            before use.
        :raises InvalidVersion:
            If the ``version`` does not conform to PEP 440 in any way then this
            exception will be raised.
        """

        # Validate the version and parse it into pieces
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion(f"Invalid version: {version!r}")

        # Store the parsed out pieces of the version
        try:
            self._version = _Version(
                release = tuple(int(i) for i in match.group("release").split(".")),
                pre = _parse_letter_version(match.group("pre_sep"), match.group("pre_l"), match.group("pre_n")),
                post = _parse_letter_version(match.group("post_sep1") or match.group("post_sep2"), match.group("post_l"), match.group("post_n1") or match.group("post_n2")),
                dev = _parse_letter_version(match.group("dev_sep"), match.group("dev_l"), match.group("dev_n")),
                local = _parse_local_version(match.group("local_sep"), match.group("local")),
                portable = _parse_portable_version(match.group("portable")),
            )
        except Exception as e:
            raise InvalidVersion(f"Invalid version: {version!r} ({e})")

        # Generate a key which will be used for sorting
        self._key = _cmpkey(
            self._version.release,
            self._version.pre,
            self._version.post,
            self._version.dev,
            self._version.local,
            self._version.portable,
        )

    def __repr__(self) -> str:
        """A representation of the Version that shows all internal state.

        >>> Version('1.0.0')
        <Version('1.0.0')>
        """
        return f"<Version('{self}')>"

    def __str__(self) -> str:
        """A string representation of the version that can be round-tripped.

        >>> str(Version("1.0a5"))
        '1.0a5'
        """
        parts = []

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        # Pre-release
        if self.pre is not None:
            parts.append("".join(str(x) for x in self._version.pre if x))

        if self.post is not None:
            parts.append("".join(str(x) for x in self._version.post))

        # Local version segment
        if self.local is not None:
            sep, local = self._version.local
            parts.append(f"{sep}{_join(local)}")

        # Portable version segment
        if self.portable is not None:
            parts.append(f"p{self.portable}")

        return "".join(parts)

    @property
    def release(self) -> tuple[int, ...]:
        """The components of the "release" segment of the version.

        >>> Version("1.2.3").release
        (1, 2, 3)
        >>> Version("2.0.0").release
        (2, 0, 0)
        >>> Version("1!2.0.0.post0").release
        (2, 0, 0)

        Includes trailing zeroes but not the epoch or any pre-release / development /
        post-release suffixes.
        """
        return self._version.release

    @property
    def pre(self) -> tuple[str, int] | None:
        """The pre-release segment of the version.

        >>> print(Version("1.2.3").pre)
        None
        >>> Version("1.2.3a1").pre
        ('a', 1)
        >>> Version("1.2.3b1").pre
        ('b', 1)
        >>> Version("1.2.3rc1").pre
        ('rc', 1)
        """
        if self._version.pre:
            sep, letter, pre = self._version.pre
            return "".join([letter, str(pre) if pre else ""])
        else:
            return self._version.pre

    @property
    def post(self) -> tuple[str, int] | None:
        if self._version.post:
            sep, letter, post = self._version.post
            return "".join([letter, str(post) if post else ""])
        else:
            return self._version.post

    @property
    def dev(self) -> tuple[str, int] | None:
        if self._version.dev:
            sep, letter, dev = self._version.post
            return "".join([letter, str(dev) if dev else ""])
        else:
            return self._version.dev

    @property
    def local(self) -> str | None:
        """The local version segment of the version.

        >>> print(Version("1.2.3").local)
        None
        >>> Version("1.2.3+abc").local
        'abc'
        """
        if self._version.local:
            sep, local = self._version.local
            return _join(local)
        else:
            return None

    @property
    def portable(self) -> str | None:
        if self._version.portable:
            return ".".join(str(x) for x in self._version.portable)
        else:
            return None

    @property
    def public(self) -> str:
        """The public portion of the version.

        >>> Version("1.2.3").public
        '1.2.3'
        >>> Version("1.2.3+abc").public
        '1.2.3'
        >>> Version("1!1.2.3dev1+abc").public
        '1!1.2.3.dev1'
        """
        return str(self).split("-", 1)[0]

    @property
    def base(self) -> str:
        """The "base version" of the version.

        >>> Version("1.2.3").base
        '1.2.3'
        >>> Version("1.2.3+abc").base
        '1.2.3'
        >>> Version("1!1.2.3dev1+abc").base
        '1!1.2.3'

        The "base version" is the public version of the project without any pre or post
        release markers.
        """
        parts = []

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        return "".join(parts)

    @property
    def major(self) -> int:
        """The first item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").major
        1
        """
        return self.release[0] if len(self.release) >= 1 else 0

    @property
    def minor(self) -> int:
        """The second item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").minor
        2
        >>> Version("1").minor
        0
        """
        return self.release[1] if len(self.release) >= 2 else 0

    @property
    def micro(self) -> int:
        """The third item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").micro
        3
        >>> Version("1").micro
        0
        """
        return self.release[2] if len(self.release) >= 3 else 0

    @property
    def is_prerelease(self):
        return self.dev is not None or self.pre is not None

def parse(version: str) -> Version:
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)

class Tests(unittest.TestCase):
    def test_simple(self):
        string = '1.2.3'
        # check that reconstruction is idempotent and that the major, minor
        # and micro components are properly parsed
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.micro, 3)

    def test_pre(self):
        # check that reconstruction is idempotent and that the pre-release
        # segment can be properly parsed
        string = '4.2a'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.pre, 'a')

        string = '4.2a1'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.pre, 'a1')

        string = '6.15.0-rc7'
        version = Version(string)
        # check that reconstruction is idempotent and that the pre-release
        # segment can be properly parsed
        self.assertEqual(string, str(version))
        self.assertEqual(version.pre, 'rc7')

        v1 = Version('6.15.0-rc7')
        v2 = Version('6.15.0-rc8')
        self.assertTrue(v1 < v2)

        version = Version('1.7.0beta89')
        self.assertTrue(version.is_prerelease)

    def test_post(self):
        # check that reconstruction is idempotent and that the post segment
        # can be properly parsed
        string = '0.18-20240915'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.base, '0.18')
        self.assertEqual(version.post, '20240915')

    def test_local(self):
        # check that reconstruction is idempotent and the local segment can
        # be properly parsed
        string = '6.15.0-next-20250526'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.base, '6.15.0')
        self.assertEqual(version.local, 'next-20250526')

        # check that release segment takes precedence over local part
        v1 = Version('6.14.0-next-20250526')
        v2 = Version('6.15.0-next-20250526')
        self.assertTrue(v1 < v2)

        # check that local part is properly compared
        v1 = Version('6.15.0-next-20250523')
        v2 = Version('6.15.0-next-20250526')
        self.assertTrue(v1 < v2)

        # check that reconstructing the version is idempotent and that both
        # the pre-releease and local segments can be properly parsed
        string = '6.15.0-rc7-next-20250526'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.base, '6.15.0')
        self.assertEqual(version.pre, 'rc7')
        self.assertEqual(version.local, 'next-20250526')

    def test_portable(self):
        # check that reconstruction is idempotent and that the portable
        # segment can be properly parsed
        string = '9.9p1'
        version = Version(string)
        self.assertEqual(string, str(version))
        self.assertEqual(version.portable, '1')

        # check that release version takes precedence over the portable
        # segment and that comparison between portable versions works
        v1 = Version('9.9p1')
        v2 = Version('9.9p2')
        v3 = Version('9.10p1')
        v4 = Version('10.0p1')

        self.assertTrue(v1 < v2)
        self.assertTrue(v1 < v3)
        self.assertTrue(v2 < v3)
        self.assertTrue(v3 < v4)
