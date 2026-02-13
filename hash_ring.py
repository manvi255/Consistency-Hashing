import bisect
from hash_function import HashFunction


class ConsistentHashing:
    def __init__(self, num_replicas=3):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []
        self.nodes = set()
        self.node_hashes = {}

    def _prepare_key(self, node, index):
        return f"{node}_{index}"

    def add_node(self, node):
        if node in self.nodes:
            return

        self.nodes.add(node)
        self.node_hashes[node] = []

        for i in range(self.num_replicas):
            vnode_key = self._prepare_key(node, i)
            hash_value = HashFunction.hash(vnode_key)

            while hash_value in self.ring:
                hash_value += 1

            bisect.insort(self.sorted_keys, hash_value)
            self.ring[hash_value] = node
            self.node_hashes[node].append(hash_value)

    def remove_node(self, node):
        if node not in self.nodes:
            return

        self.nodes.remove(node)

        for hash_value in self.node_hashes.get(node, []):
            if hash_value in self.ring:
                del self.ring[hash_value]
                index = bisect.bisect_left(self.sorted_keys, hash_value)
                if index < len(self.sorted_keys) and self.sorted_keys[index] == hash_value:
                    self.sorted_keys.pop(index)

        del self.node_hashes[node]

    def get_node(self, key):
        if not self.sorted_keys:
            return None

        hash_value = HashFunction.hash(key)
        idx = bisect.bisect_left(self.sorted_keys, hash_value)

        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]

