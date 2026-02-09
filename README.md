# Consistent Hashing with Node Rebalancing

## Overview

This project implements a **Consistent Hashing mechanism with virtual nodes and node rebalancing**. The system computes a deterministic **key → node mapping** for distributed systems such as caches, load balancers, or sharded storage.

The implementation focuses on:
- Uniform key distribution across nodes
- Minimal key movement during node addition and removal
- Deterministic and efficient key lookup
- Observability of rebalancing behavior

The system does **not store actual data**. It only determines which node should own a given key.

---

## System Context

The system assumes:
- A dynamic set of nodes (nodes can be added or removed)
- A large keyspace (user IDs, session tokens, object IDs, etc.)
- No central coordinator for key placement
- Read/write routing decisions based purely on hashing

This implementation computes **key ownership only**. Storage, replication, networking, and fault detection are intentionally out of scope.

---

## Design Decisions

### 1. Consistent Hash Ring

Both nodes and keys are mapped onto the same **circular hash space** (hash ring).

Key assignment rule:
- Hash the key
- Move clockwise on the ring
- Assign the key to the first node encountered

This ensures that only a small portion of keys are reassigned when cluster topology changes.

---

### 2. Deterministic Hashing

A deterministic hash function (MD5) is used to ensure:
- Same input always produces the same hash
- Consistent routing across time and across clients

Determinism guarantees that reads and writes for the same key always reach the same node.

---

### 3. Virtual Nodes (VNodes)

Each physical node is represented by multiple **virtual nodes** on the ring.

Benefits:
- Improves load distribution
- Reduces variance in key ownership
- Provides smoother balancing when the number of physical nodes is small

The number of virtual nodes per physical node is configurable.

---

### 4. Sorted Ring Structure

The ring is maintained using a **sorted data structure**, which enables:
- Efficient successor search
- Binary search based lookup
- O(log N) routing time

Where N is the total number of virtual nodes.

---

### 5. Separation of Concerns

The implementation is modular:

- `hash_function.py` → Hash logic
- `hash_ring.py` → Ring management and node operations
- `rebalancer.py` → Metrics and analysis
- `main.py` → Simulation and experiments

This improves readability, maintainability, and extensibility.

---

## Lookup Algorithm

For a given key:

1. Compute the hash of the key
2. Find the first node with hash ≥ key hash
3. If no such node exists, wrap around to the start of the ring
4. Return the corresponding physical node

This guarantees deterministic lookup with minimal remapping.

---

## Rebalancing Behavior

### Node Addition

When a node is added:
- Only keys between the predecessor virtual node and the new virtual node move
- All other keys remain unchanged

On average, approximately:

**Moved keys ≈ 1 / total_nodes**

---

### Node Removal

When a node is removed:
- Its key ranges move to the next clockwise successor
- No global reshuffling occurs
- No keys are lost

On average:

**Moved keys ≈ 1 / previous_total_nodes**

---

## Trade-offs

### Hash Function Choice

MD5 is used for simplicity and uniform distribution.

Pros:
- Deterministic
- Good distribution

Cons:
- Slower than non-cryptographic hashes (e.g., MurmurHash)

For production systems, MurmurHash or xxHash would be preferred.

---

### Virtual Node Overhead

Virtual nodes improve distribution but:
- Increase memory usage
- Increase ring size
- Increase node add/remove cost

This trade-off is acceptable for improved load balance.

---

### No Data Storage

The system does not include:
- Persistence
- Replication
- Networking
- Fault tolerance

These features can be added as extensions.

---

## Complexity Analysis

| Operation        | Time Complexity |
|------------------|----------------|
| Key Lookup       | O(log N)       |
| Node Addition    | O(K log N)     |
| Node Removal     | O(K log N)     |

Where:
- N = total virtual nodes
- K = virtual nodes per physical node

---

## Observability & Metrics

The system provides:

- Key distribution per node
- Number of keys moved during rebalancing
- Percentage of remapped keys

These metrics help verify:
- Uniform distribution
- Minimal movement property
- Effectiveness of virtual nodes

---

## Sample Output

Example distribution for 100,000 keys:

10.0.0.1 → 24980
10.0.0.2 → 25090
10.0.0.3 → 24870
10.0.0.4 → 25060

After adding a new node:

Keys moved: 23715
Percentage moved: 23.7%
Expected ≈ 25%

This confirms the minimal rebalancing behavior of consistent hashing.

---

## Virtual Node Effect

Increasing virtual nodes:
- Improves load balance
- Reduces distribution variance
- Makes key ownership more uniform

---

## Why Consistent Hashing?

| Method          | Keys moved when nodes change |
|-----------------|-------------------------------|
| Modulo hashing  | ~100%                         |
| Consistent hashing | ~1/N                      |

Consistent hashing is widely used in:
- Distributed caches (Redis, Memcached)
- Distributed databases
- Load balancers
- Object storage systems
- Microservice sharding

---

## Project Structure

hash_function.py
hash_ring.py
rebalancer.py
main.py
README.md


---

## Author

Manvi Gupta
