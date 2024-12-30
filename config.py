VALUE_LENGTH_SIZE = 2  # 2 bytes for value length
KEY_LENGTH_SIZE = 1  # 1 byte for key length (assuming keys are less than 256 characters)
CHECKSUM_SIZE = 16  # MD5 checksum size
LOG_FILE_PATH = 'data/kv_store.log'
HASH_MAP_SNAPSHOT_FILE = 'data/hash_map_snapshot.bin'
HASH_MAP_WAL_FILE = 'data/hash_map_wal.bin'
TOMBSTONE = b'\x00'
ENTRY_MARKER = b'\x01'

# Test-specific conf
TEST_LOG_FILE_PATH = 'data/test_kv_store.log'
TEST_HASH_MAP_WAL_FILE = 'data/test_hash_map_wal.bin'
