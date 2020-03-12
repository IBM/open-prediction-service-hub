#!/usr/bin/env python3
import unittest


from dynamic_hosting.core.util import storage_root, DEFAULT_STORAGE_ROOT_DIR_NAME


class TestFindingStorageRoot(unittest.TestCase):
    def test_dir_name(self):
        self.assertTrue(storage_root().is_dir())
        self.assertEqual(storage_root().name, DEFAULT_STORAGE_ROOT_DIR_NAME)


if __name__ == '__main__':
    unittest.main()
