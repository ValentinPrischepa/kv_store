import hashlib


def calculate_checksum(value):
    return hashlib.md5(value).digest()
