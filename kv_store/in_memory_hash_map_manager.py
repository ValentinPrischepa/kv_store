import pickle
from config import HASH_MAP_WAL_FILE


class InMemoryHashMapManager:
    def __init__(self, wal_file=HASH_MAP_WAL_FILE):
        self.hash_map = {}
        self.wal_file = wal_file

    def append_to_wal(self, key, offset):
        with open(self.wal_file, 'ab') as f:
            pickle.dump((key, offset), f)

    def load_from_wal(self):
        try:
            with open(self.wal_file, 'rb') as f:
                while True:
                    try:
                        key, offset = pickle.load(f)
                        self.hash_map[key] = offset
                    except EOFError:
                        break
        except FileNotFoundError:
            pass

    def update_hash_map(self, key, offset):
        self.append_to_wal(key, offset)
        self.hash_map[key] = offset

    def get_offset(self, key):
        return self.hash_map.get(key)

    def get_all_keys(self):
        return list(self.hash_map.keys())
