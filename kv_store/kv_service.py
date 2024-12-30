import threading
from config import LOG_FILE_PATH, HASH_MAP_WAL_FILE
from kv_store.log_file_manager import LogFileManager
from kv_store.in_memory_hash_map_manager import InMemoryHashMapManager


class KeyValueService:
    def __init__(self, log_file_path=LOG_FILE_PATH, hash_map_wal_file=HASH_MAP_WAL_FILE):
        self.log_file_manager = LogFileManager(log_file_path)
        self.in_memory_hash_map_manager = InMemoryHashMapManager(hash_map_wal_file)
        self.in_memory_hash_map_manager.load_from_wal()
        self.lock = threading.Lock()

    def put_entry(self, key, value):
        with self.lock:
            offset = self.log_file_manager.write_entry(key, value)
            self.in_memory_hash_map_manager.update_hash_map(key, offset)

    def find_entry(self, key):
        offset = self.in_memory_hash_map_manager.get_offset(key)
        if offset is None:
            return None
        with open(self.log_file_manager.file_path, 'rb') as log_file:
            key, value, _ = self.log_file_manager.read_entry(log_file, offset)
            return value

    def delete_entry(self, key):
        with self.lock:
            offset = self.log_file_manager.write_tombstone(key)
            self.in_memory_hash_map_manager.update_hash_map(key, offset)

    def get_all_keys(self):
        return self.in_memory_hash_map_manager.get_all_keys()

    def init_hash_map(self):
        with open(self.log_file_manager.file_path, 'rb') as log_file:
            next_offset = None
            while True:
                if next_offset is None:
                    offset = log_file.tell()
                else:
                    offset = next_offset
                try:
                    key, value, next_offset = self.log_file_manager.read_entry(log_file, offset)
                except ValueError:
                    break
                if key is None:
                    break
                self.in_memory_hash_map_manager.update_hash_map(key, offset)

    def compact_log_file(self):
        with self.lock:
            self.in_memory_hash_map_manager.hash_map = self.log_file_manager.compact_log_file(self.in_memory_hash_map_manager.hash_map)

