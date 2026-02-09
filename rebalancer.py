from collections import defaultdict

class Rebalancer:
    def __init__(self, ring):
        self.ring = ring

    def map_keys(self, keys):
        return {key: self.ring.get_node(key) for key in keys}

    def count_moved_keys(self, before, after):
        return sum(1 for k in before if before[k] != after[k])

    def load_distribution(self, keys):
        dist = defaultdict(int)
        for key in keys:
            dist[self.ring.get_node(key)] += 1
        return dict(dist)
