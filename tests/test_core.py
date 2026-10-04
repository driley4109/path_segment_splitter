import unittest

from path_segment_splitter import split_segments


class TestSplitSegments(unittest.TestCase):

    def test_absolute_unix_path(self):
        self.assertEqual(
            split_segments("/a/b/c"),
            (["a", "b", "c"], "", True),
        )

    def test_relative_unix_path(self):
        self.assertEqual(
            split_segments("a/b/c"),
            (["a", "b", "c"], "", False),
        )

    def test_trailing_slash(self):
        # The trailing slash produces an empty component which is dropped.
        self.assertEqual(
            split_segments("a/b/"),
            (["a", "b"], "", False),
        )

    def test_double_slash_collapses(self):
        self.assertEqual(
            split_segments("a//b"),
            (["a", "b"], "", False),
        )

    def test_root_only(self):
        self.assertEqual(
            split_segments("/"),
            ([], "", True),
        )

    def test_empty_string(self):
        self.assertEqual(
            split_segments(""),
            ([], "", False),
        )

    def test_single_segment_no_slash(self):
        self.assertEqual(
            split_segments("file.txt"),
            (["file.txt"], "", False),
        )

    def test_windows_drive_rooted(self):
        # The slash after the colon makes this rooted.
        self.assertEqual(
            split_segments("C:/foo/bar"),
            (["foo", "bar"], "C:", True),
        )

    def test_windows_drive_relative(self):
        # No slash after the colon — drive-relative, NOT rooted.
        self.assertEqual(
            split_segments("C:foo/bar"),
            (["foo", "bar"], "C:", False),
        )

    def test_windows_drive_only(self):
        self.assertEqual(
            split_segments("C:"),
            ([], "C:", False),
        )

    def test_unc_path(self):
        self.assertEqual(
            split_segments("//host/share/dir/file"),
            (["dir", "file"], "//host/share", True),
        )

    def test_unc_path_no_trailing_directory(self):
        # Exactly the UNC prefix and nothing else — still rooted.
        self.assertEqual(
            split_segments("//host/share"),
            ([], "//host/share", True),
        )

    def test_single_leading_slash_is_not_unc(self):
        # One leading slash is an ordinary absolute path, not a UNC share.
        self.assertEqual(
            split_segments("/host/share"),
            (["host", "share"], "", True),
        )

    def test_three_leading_slashes_not_unc(self):
        # The third slash is the root of the path body, so this is rooted but
        # has no drive.
        self.assertEqual(
            split_segments("///host/share"),
            (["host", "share"], "", True),
        )

    def test_unc_with_trailing_slash(self):
        self.assertEqual(
            split_segments("//host/share/dir/"),
            (["dir"], "//host/share", True),
        )

    def test_backslash_is_literal(self):
        # Backslashes are not separators; the whole thing is one segment.
        self.assertEqual(
            split_segments("a\\\\b"),
            (["a\\\\b"], "", False),
        )

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            split_segments(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
