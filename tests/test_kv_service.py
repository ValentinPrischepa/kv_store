import os
import unittest

from config import TEST_LOG_FILE_PATH, TEST_HASH_MAP_WAL_FILE
from kv_store.kv_service import KeyValueService


class TestKeyValueService(unittest.TestCase):
    def setUp(self):
        self.kv_service = KeyValueService(TEST_LOG_FILE_PATH, TEST_HASH_MAP_WAL_FILE)
        with open(TEST_LOG_FILE_PATH, 'wb'):
            pass
        with open(TEST_HASH_MAP_WAL_FILE, 'wb'):
            pass

    def tearDown(self):
        os.remove(TEST_LOG_FILE_PATH)
        os.remove(TEST_HASH_MAP_WAL_FILE)

    def test_put_and_find_entry(self):
        key = 'test_key'
        value = 'test_value'
        self.kv_service.put_entry(key, value)
        self.assertEqual(self.kv_service.find_entry(key), value)

    def test_delete_entry(self):
        key = 'test_key'
        value = 'test_value'
        self.kv_service.put_entry(key, value)
        self.kv_service.delete_entry(key)
        self.assertIsNone(self.kv_service.find_entry(key))

    def test_get_all_keys(self):
        keys = ["key1", "key2", "key3"]
        for i, key in enumerate(keys):
            self.kv_service.put_entry(key, f"value{i}")
        self.assertEqual(set(self.kv_service.get_all_keys()), set(keys))


if __name__ == '__main__':
    unittest.main()