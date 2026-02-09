from sortedcontainers import SortedDict
from hash_function import HashFunction


class ConsistentHashing:
    def __init__(self, num_replicas=3):
        self.num_replicas = num_replicas
        self.ring = SortedDict()
        self.nodes = set()

    def _prepare_key(self, node, index):
        return f"{node}_{index}"

    def add_node(self, node):
        if node in self.nodes:
            return

        self.nodes.add(node)

        for i in range(self.num_replicas):
            vnode_key = self._prepare_key(node, i)
            hash_value = HashFunction.hash(vnode_key)
            self.ring[hash_value] = node

    def remove_node(self, node):
        if node not in self.nodes:
            return

        self.nodes.remove(node)

        for i in range(self.num_replicas):
            vnode_key = self._prepare_key(node, i)
            hash_value = HashFunction.hash(vnode_key)

            if hash_value in self.ring:
                del self.ring[hash_value]

    def get_node(self, key):
        if not self.ring:
            return None

        hash_value = HashFunction.hash(key)

        idx = self.ring.bisect_left(hash_value)

        if idx == len(self.ring):
            idx = 0

        return self.ring[self.ring.keys()[idx]]
