import os
import unittest

from config import TEST_HASH_MAP_WAL_FILE
from kv_store.in_memory_hash_map_manager import InMemoryHashMapManager


class TestInMemoryHashMapManager(unittest.TestCase):
    def setUp(self):
        self.in_memory_hash_map_manageer = InMemoryHashMapManager(TEST_HASH_MAP_WAL_FILE)
        # Ensure a clean log file for each test
        with open(TEST_HASH_MAP_WAL_FILE, 'wb'):
            pass

    def tearDown(self):
        os.remove(TEST_HASH_MAP_WAL_FILE)

    def test_append_to_wal_load_from_wal(self):
        key = 'test_key'
        offset = 12345
        self.in_memory_hash_map_manageer.append_to_wal(key, offset)
        self.in_memory_hash_map_manageer.load_from_wal()
        self.assertEqual(self.in_memory_hash_map_manageer.get_offset(key), offset)

    def test_get_offset(self):
        key = 'test_key'
        offset = 12345
        self.in_memory_hash_map_manageer.update_hash_map(key, offset)
        self.assertEqual(self.in_memory_hash_map_manageer.get_offset(key), offset)

    def test_get_all_keys(self):
        keys = ['key1', 'key2', 'key3']
        for i, key in enumerate(keys):
            self.in_memory_hash_map_manageer.update_hash_map(key, i)
        self.assertEqual(set(self.in_memory_hash_map_manageer.get_all_keys()), set(keys))


if __name__ == '__main__':
    unittest.main()
