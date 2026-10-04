"""
Path Segment Splitter — split a path into its component segments.

This package exposes a single function, :func:`split_segments`, which breaks a
path string into a list of segments while separately reporting the drive
portion (drive letter or UNC prefix) and whether the path was rooted.

The implementation deliberately avoids :mod:`os.path` so that behaviour is
identical on every platform — a Windows-style path is parsed the same way
whether the code runs on Linux or Windows. The only separator recognised is
the forward slash (``/``). Backslashes are treated as ordinary filename
characters, not separators. This is a deliberate, documented decision: mixing
the two conventions in a single string is ambiguous, and picking one rule makes
behaviour predictable.

Public names
------------
- :func:`split_segments` — split a path string into segments.
"""

from .core import split_segments

__all__ = ["split_segments"]
