# Path Segment Splitter

Splits a path string into a flat list of segments, separately reporting the
drive letter or UNC prefix and whether the path is rooted.

```python
from path_segment_splitter import split_segments

segments, drive, rooted = split_segments("//host/share/dir/file.txt")
# segments == ['dir', 'file.txt']
# drive    == '//host/share'
# rooted   == True

segments, drive, rooted = split_segments("C:/Projects/alpha/beta")
# segments == ['Projects', 'alpha', 'beta']
# drive    == 'C:'
# rooted   == True

segments, drive, rooted = split_segments("a/b/")
# segments == ['a', 'b']
# drive    == ''
# rooted   == False
```

## Why this exists

The standard library's `os.path` is platform-sensitive: `split` on Windows
treats backslashes as separators, on POSIX it does not. When you need to parse
path *strings* that may have originated on another platform — configuration
files, URLs, stored references — that inconsistency is a bug source.

This library picks one rule and applies it everywhere: the only separator is
the forward slash `/`. Backslashes are ordinary characters. Drive letters and
UNC prefixes are recognised because they appear in path strings that otherwise
use forward slashes, but Windows-native backslash paths are out of scope.

The trade-off is simplicity and predictability over native Windows support.
If your paths use backslashes, normalise them to forward slashes before
calling `split_segments`.

## Edge cases you will hit

- `C:foo` is drive-relative, so `rooted` is `False`. `C:/foo` is rooted.
  The colon alone does not imply a root.
- Trailing slashes are silently dropped: `"a/b/"` yields `['a', 'b']`.
  This matches conventional behaviour but is worth knowing.
- `///host/share` is **not** treated as UNC. Only exactly two leading slashes
  qualify; the third becomes the root slash of the body.
- `split_segments` returns a 3-tuple `(segments, drive, rooted)`, not a list.
  Unpack accordingly.

## Exported names

- `split_segments(path: str) -> tuple[list[str], str, bool]`

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
