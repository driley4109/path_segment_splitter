"""Core implementation for :func:`split_segments`."""

from __future__ import annotations
from typing import List, Tuple, Optional

# A small sentinel that can never collide with a real segment. Using a tuple
# rather than ``None`` lets callers distinguish "no drive" from "drive is the
# empty string" (which would be surprising, but logically distinct).
_NO_DRIVE: Tuple[str, str, str] = ("", "", "")


def _parse_drive(path: str) -> Tuple[str, str]:
    """Return ``(drive, rest)`` where ``drive`` covers the drive letter or UNC
    prefix and ``rest`` is the portion of ``path`` after it.

    Only two drive forms are recognised, both taken from Windows conventions:

    1. A drive letter followed by a colon, e.g. ``C:``. The colon is kept as
       part of the returned drive so callers can tell at a glance that a drive
       was present.
    2. A UNC prefix of exactly two leading slashes followed by a host name and
       a share name, e.g. ``//host/share``. The returned drive includes the
       host and share as the first two segments, plus the leading slashes.

    Anything else — including three or more leading slashes — is left
    untouched and returned with an empty drive. Three-slash paths are
    intentionally not treated as UNC because the third slash is the root slash
    of the path body, and collapsing it into the prefix would discard the
    "rooted" signal.
    """
    if len(path) >= 2 and path[1] == ":" and path[0].isalpha():
        return path[:2], path[2:]

    # UNC: exactly two leading slashes, a non-empty host, a slash, a non-empty
    # share, and then either end-of-string or a separator.
    if (
        len(path) >= 5
        and path[0] == "/"
        and path[1] == "/"
        and path[2] != "/"
        and "/" in path[2:]
    ):
        body = path[2:]
        host, _, share_and_rest = body.partition("/")
        share, _, rest = share_and_rest.partition("/")
        if share != "":
            drive = "//" + host + "/" + share
            return drive, rest

    return "", path


def split_segments(path: str) -> Tuple[List[str], str, bool]:
    """Split *path* into a list of non-empty segments.

    Returns a 3-tuple ``(segments, drive, rooted)``:

    - ``segments`` — every path component separated by a forward slash, with
      empty components (from ``//`` or a trailing slash) removed. The drive
      letter and the UNC host/share are **not** included here; they are
      reported separately in ``drive``.
    - ``drive`` — the drive letter (e.g. ``"C:"``) or UNC prefix (e.g.
      ``"//host/share"``), or the empty string if neither was present.
    - ``rooted`` — ``True`` when *path* begins with ``/`` once the drive has
      been stripped away. A drive letter alone does **not** make a path
      rooted: ``C:foo`` is a drive-relative path on Windows, so ``rooted`` is
      ``False`` for it.

    The separator is the forward slash only. Backslashes are kept as literal
    characters within segments. This keeps the function platform-independent
    and avoids the ambiguity of strings like ``C:\\foo`` where a human might
    read the backslash as a separator.

    Examples
    --------
    >>> split_segments("/a/b/c")
    (['a', 'b', 'c'], '', True)
    >>> split_segments("C:/foo/bar")
    (['foo', 'bar'], 'C:', True)
    >>> split_segments("//host/share/dir/file")
    (['dir', 'file'], '//host/share', True)
    >>> split_segments("a/b/")
    (['a', 'b'], '', False)
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    drive, rest = _parse_drive(path)

    rooted = rest.startswith("/") or bool(drive) and drive.startswith("//")

    # Trailing slashes are collapsed to nothing by ``split``, so they simply do
    # not produce an empty final segment. This is the conventional, expected
    # behaviour and is documented rather than made configurable.
    raw_segments = rest.split("/")
    segments = [s for s in raw_segments if s != ""]

    return segments, drive, rooted
