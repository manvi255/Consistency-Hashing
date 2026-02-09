from hash_ring import ConsistentHashing
from rebalancer import Rebalancer

keys = [f"user{i}" for i in range(100000)]

print("Test 1: num_replicas = 1")

ring1 = ConsistentHashing(num_replicas=1)

ring1.add_node("NodeA")
ring1.add_node("NodeB")
ring1.add_node("NodeC")

rebalancer1 = Rebalancer(ring1)

distribution1 = rebalancer1.load_distribution(keys)

for node, count in distribution1.items():
    print(node, "→", count)

print("\nTest 2: num_replicas = 100")

ring2 = ConsistentHashing(num_replicas=100)

ring2.add_node("NodeA")
ring2.add_node("NodeB")
ring2.add_node("NodeC")

rebalancer2 = Rebalancer(ring2)

distribution2 = rebalancer2.load_distribution(keys)

for node, count in distribution2.items():
    print(node, "→", count)
