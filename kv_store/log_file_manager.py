import os
import struct
from config import VALUE_LENGTH_SIZE, KEY_LENGTH_SIZE, CHECKSUM_SIZE, LOG_FILE_PATH, TOMBSTONE, ENTRY_MARKER
from utils import calculate_checksum


class LogFileManager:
    def __init__(self, file_path=LOG_FILE_PATH):
        self.file_path = file_path

    def write_entry(self, key, value):
        with open(self.file_path, 'ab') as log_file:
            offset = log_file.tell()  # Get the current file offset
            key_bytes = key.encode('utf-8')
            value_bytes = value.encode('utf-8')
            key_length_bytes = struct.pack('B', len(key_bytes))
            value_length_bytes = struct.pack('H', len(value_bytes))
            checksum = calculate_checksum(
                ENTRY_MARKER + key_length_bytes + key_bytes + value_length_bytes + value_bytes)
            log_entry = ENTRY_MARKER + key_length_bytes + key_bytes + value_length_bytes + value_bytes + checksum
            log_file.write(log_entry)
            return offset

    def write_tombstone(self, key):
        with open(self.file_path, 'ab') as log_file:
            offset = log_file.tell()
            key_bytes = key.encode('utf-8')
            log_entry = TOMBSTONE + struct.pack('B', len(key_bytes)) + key_bytes
            log_file.write(log_entry)
            return offset

    @staticmethod
    def read_entry(log_file, offset):
        if offset is not None:
            log_file.seek(offset)

        marker = log_file.read(1)
        if not marker:
            return None, None, None

        if marker == TOMBSTONE:
            key_length_bytes = log_file.read(KEY_LENGTH_SIZE)
            if not key_length_bytes:
                return None, None, None

            key_length = struct.unpack('B', key_length_bytes)[0]
            key_bytes = log_file.read(key_length)
            if len(key_bytes) != key_length:
                return None, None, None
            key = key_bytes.decode('utf-8')
            return key, None, None

        elif marker == ENTRY_MARKER:
            key_length_bytes = log_file.read(KEY_LENGTH_SIZE)
            if not key_length_bytes:
                return None, None, None
            key_length = struct.unpack('B', key_length_bytes)[0]
            key_bytes = log_file.read(key_length)
            if not key_bytes:
                return None, None, None
            value_length_bytes = log_file.read(VALUE_LENGTH_SIZE)
            value_length = struct.unpack('H', value_length_bytes)[0]
            value_bytes = log_file.read(value_length)
            checksum = log_file.read(CHECKSUM_SIZE)
            if calculate_checksum(marker + key_length_bytes + key_bytes + value_length_bytes + value_bytes) != checksum:
                raise ValueError("Data corruption detected")

            key = key_bytes.decode('utf-8')
            value = value_bytes.decode('utf-8')
            return key, value, log_file.tell()

        else:
            raise ValueError('Unknown entry marker (or no marker) has been used')

    def compact_log_file(self, current_hash_map):
        new_log_file_path = self.file_path + '.compact'
        new_hash_map = {}

        with open(new_log_file_path, 'wb') as new_log_file:
            with open(self.file_path, 'rb') as log_file:
                try:
                    for key, offset in current_hash_map.items():
                        key, value, offset = self.read_entry(log_file, offset)
                        if key is None:
                            break
                        if value is not None:
                            new_offset = self.write_entry(key, value)
                            new_hash_map[key] = new_offset
                except ValueError:
                    raise ValueError('Compaction has failed')

            os.rename(new_log_file_path, self.file_path)
            return new_hash_map






