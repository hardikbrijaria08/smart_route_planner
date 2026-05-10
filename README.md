# 🗺 Smart Route Planner Using Graph Algorithms

A Python-based route planning system that computes optimal paths between cities using **BFS** and **Dijkstra's algorithm**, with support for user-defined cost and time constraints.

## 📌 Project Highlights
- **4 optimization modes**: fewest stops, shortest distance, lowest cost, fastest time
- Graph built with custom adjacency list using Python dictionaries
- Custom min-heap (via `heapq`) for efficient Dijkstra implementation
- Support for user-defined cities and constraint filtering (max budget, max time)
- Interactive CLI for custom route queries

## 🧠 Algorithms Used

### BFS — Fewest Stops
- Explores level by level (stop by stop)
- Guarantees minimum number of intermediate stops
- Time complexity: **O(V + E)**

### Dijkstra's Algorithm — Weighted Shortest Path
- Uses a min-heap priority queue for efficiency
- Can optimize for distance, cost, or time (configurable)
- Time complexity: **O((V + E) log V)**

## 📁 Project Structure
```
smart-route-planner/
│
├── route_planner.py    # Main: Graph, BFS, Dijkstra, CLI
├── requirements.txt    # Dependencies (standard library only)
└── README.md
```

## 🚀 How to Run

```bash
python route_planner.py
```

No external dependencies — uses Python standard library only.

## 💡 Sample Output

```
🗺  Route Planner: Delhi → Bangalore
════════════════════════════════════════════════

  ✅ Fewest Stops (BFS)
     Route : Delhi → Agra → Lucknow → ... → Bangalore
     Stops : 5
     Dist  : 2160 km   Cost: ₹3600   Time: 37 hrs

  ✅ Shortest Distance (Dijkstra)
     Route : Delhi → Jaipur → Mumbai → Hyderabad → Bangalore
     Stops : 4
     Dist  : 2130 km   Cost: ₹3250   Time: 35 hrs

  ✅ Lowest Cost (Dijkstra)
     Route : Delhi → Agra → Jaipur → Mumbai → Hyderabad → Bangalore
     Stops : 5
     Cost  : ₹3000   ...

  ✅ Fastest Route (Dijkstra)
     Route : Delhi → Jaipur → Mumbai → Hyderabad → Bangalore
     Time  : 35 hrs   ...
```

## 🔧 Key Design Decisions

| Decision | Reason |
|---|---|
| Adjacency list over matrix | Sparse graph; memory efficient |
| Min-heap for Dijkstra | O(log V) extraction vs O(V) for array |
| Bidirectional edges | Roads go both ways |
| Separate weight index | One Dijkstra function handles all 3 optimizations |
