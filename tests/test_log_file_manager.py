import os
import unittest

from config import TEST_LOG_FILE_PATH, TOMBSTONE
from kv_store.log_file_manager import LogFileManager


class TestLogFileManager(unittest.TestCase):
    def setUp(self):
        self.log_file_manager = LogFileManager(TEST_LOG_FILE_PATH)
        # Ensure a clean log file for each test
        with open(TEST_LOG_FILE_PATH, 'wb'):
            pass

    def tearDown(self):
        os.remove(TEST_LOG_FILE_PATH)

    def test_write_and_read_entry(self):
        key = 'key_test'
        value = 'value_test'
        offset = self.log_file_manager.write_entry(key, value)

        with open(TEST_LOG_FILE_PATH, 'rb') as log_file:
            read_key, read_value, _ = self.log_file_manager.read_entry(log_file, offset)
        self.assertEqual(key, read_key)
        self.assertEqual(value, read_value)

    def test_write_tombstone(self):
        key = 'tombstone_key'
        offset = self.log_file_manager.write_tombstone(key)

        with open(TEST_LOG_FILE_PATH, 'rb') as log_file:
            marker = log_file.read(1)
            self.assertEqual(marker, TOMBSTONE)
            key_length = log_file.read(1)
            self.assertEqual(len(key), int.from_bytes(key_length, 'big'))
            key_bytes = log_file.read(len(key))
            self.assertEqual(key_bytes.decode('UTF-8'), key)


if __name__ == '__main__':
    unittest.main()