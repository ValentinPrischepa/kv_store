import time
from kv_store.kv_service import KeyValueService


def benchmark(store, num_operations):
    start_time = time.time()

    # Write operations
    for i in range(num_operations):
        key = f'key{i}'
        value = f'value{i}'
        store.put_entry(key, value)

    write_time = time.time()
    write_throughput = num_operations / (write_time - start_time)

    # Read operations
    for i in range(num_operations):
        key = f'key{i}'
        store.find_entry(key)

    read_time = time.time()
    read_throughput = num_operations / (read_time - write_time)

    return write_throughput, read_throughput


if __name__ == "__main__":
    store = KeyValueService()
    num_operations = 10000

    write_throughput, read_throughput = benchmark(store, num_operations)

    print(f'Write Throughput: {write_throughput} operations/second')
    print(f'Read Throughput: {read_throughput} operations/second')
