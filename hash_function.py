import hashlib

class HashFunction:
    @staticmethod
    def hash(key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
