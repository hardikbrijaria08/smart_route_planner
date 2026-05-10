"""
Smart Route Planner Using Graph Algorithms
==========================================
Computes optimal routes between cities using:
  - BFS (fewest stops)
  - Dijkstra's Algorithm (shortest distance or lowest cost)

Supports user-defined cities and time/cost constraints.

Author: Hardik Brijaria
"""

import heapq
from collections import defaultdict, deque


# ─────────────────────────────────────────────
# GRAPH DATA STRUCTURE
# ─────────────────────────────────────────────

class Graph:
    """
    Weighted directed graph using adjacency list.
    Each edge stores: (neighbor, distance_km, cost_inr, time_hrs)
    """

    def __init__(self):
        # adjacency list: city -> list of (neighbor, distance, cost, time)
        self.adj = defaultdict(list)
        self.cities = set()

    def add_edge(self, src, dest, distance, cost, time, bidirectional=True):
        """Add a route between two cities."""
        self.adj[src].append((dest, distance, cost, time))
        self.cities.add(src)
        self.cities.add(dest)
        if bidirectional:
            self.adj[dest].append((src, distance, cost, time))

    def display(self):
        """Print all routes in the graph."""
        print("\n📍 Available Routes:")
        print(f"{'From':<15} {'To':<15} {'Dist(km)':<12} {'Cost(₹)':<12} {'Time(hrs)'}")
        print("-" * 65)
        seen = set()
        for city in sorted(self.adj):
            for (neighbor, dist, cost, time) in self.adj[city]:
                key = tuple(sorted([city, neighbor]))
                if key not in seen:
                    print(f"{city:<15} {neighbor:<15} {dist:<12} {cost:<12} {time}")
                    seen.add(key)


# ─────────────────────────────────────────────
# ALGORITHM 1: BFS — Fewest Stops
# ─────────────────────────────────────────────

def bfs_fewest_stops(graph, start, end):
    """
    BFS finds the route with the minimum number of stops.
    Time Complexity: O(V + E)
    """
    if start == end:
        return [start], 0, 0, 0

    # Queue holds: (current_city, path_so_far, total_dist, total_cost, total_time)
    queue = deque([(start, [start], 0, 0, 0)])
    visited = {start}

    while queue:
        city, path, dist, cost, time = queue.popleft()

        for (neighbor, d, c, t) in graph.adj[city]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                new_dist = dist + d
                new_cost = cost + c
                new_time = time + t

                if neighbor == end:
                    return new_path, new_dist, new_cost, new_time

                visited.add(neighbor)
                queue.append((neighbor, new_path, new_dist, new_cost, new_time))

    return None, float('inf'), float('inf'), float('inf')  # no path found


# ─────────────────────────────────────────────
# ALGORITHM 2: Dijkstra — Shortest/Cheapest/Fastest
# ─────────────────────────────────────────────

def dijkstra(graph, start, end, optimize='distance'):
    """
    Dijkstra's algorithm with flexible optimization target.
    optimize: 'distance' | 'cost' | 'time'
    Time Complexity: O((V + E) log V) with min-heap
    """
    WEIGHT_INDEX = {'distance': 1, 'cost': 2, 'time': 3}
    w_idx = WEIGHT_INDEX[optimize]

    # Min-heap: (weight, city, path, distance, cost, time)
    heap = [(0, start, [start], 0, 0, 0.0)]
    visited = {}

    while heap:
        weight, city, path, dist, cost, time = heapq.heappop(heap)

        if city in visited:
            continue
        visited[city] = weight

        if city == end:
            return path, dist, cost, time

        for (neighbor, d, c, t) in graph.adj[city]:
            if neighbor not in visited:
                new_dist = dist + d
                new_cost = cost + c
                new_time = time + t

                # Choose the weight to optimize
                weights = [0, new_dist, new_cost, new_time]
                heapq.heappush(heap, (weights[w_idx], neighbor, path + [neighbor], new_dist, new_cost, new_time))

    return None, float('inf'), float('inf'), float('inf')  # no path


# ─────────────────────────────────────────────
# HELPER: Print Route Result
# ─────────────────────────────────────────────

def print_route(label, path, dist, cost, time):
    """Nicely format a route result."""
    if path is None:
        print(f"\n  ❌ {label}: No path found.")
        return
    print(f"\n  ✅ {label}")
    print(f"     Route : {' → '.join(path)}")
    print(f"     Stops : {len(path) - 1}")
    print(f"     Dist  : {dist} km")
    print(f"     Cost  : ₹{cost}")
    print(f"     Time  : {time} hrs")


# ─────────────────────────────────────────────
# ROUTE PLANNER: Query with Constraints
# ─────────────────────────────────────────────

def plan_route(graph, start, end, max_cost=None, max_time=None):
    """
    Plan a route and show all three optimization options.
    Filters results by user-defined constraints.
    """
    if start not in graph.cities or end not in graph.cities:
        print(f"\n❌ City not found. Available: {', '.join(sorted(graph.cities))}")
        return

    print(f"\n{'='*55}")
    print(f"  🗺  Route Planner: {start} → {end}")
    if max_cost: print(f"  💰 Budget Limit : ₹{max_cost}")
    if max_time: print(f"  ⏱  Time Limit   : {max_time} hrs")
    print(f"{'='*55}")

    results = {}

    # 1. Fewest stops (BFS)
    path, dist, cost, time = bfs_fewest_stops(graph, start, end)
    results['fewest_stops'] = (path, dist, cost, time)
    print_route("Fewest Stops (BFS)", path, dist, cost, time)

    # 2. Shortest distance (Dijkstra)
    path, dist, cost, time = dijkstra(graph, start, end, optimize='distance')
    results['shortest'] = (path, dist, cost, time)
    print_route("Shortest Distance (Dijkstra)", path, dist, cost, time)

    # 3. Cheapest route (Dijkstra)
    path, dist, cost, time = dijkstra(graph, start, end, optimize='cost')
    results['cheapest'] = (path, dist, cost, time)
    print_route("Lowest Cost (Dijkstra)", path, dist, cost, time)

    # 4. Fastest route (Dijkstra)
    path, dist, cost, time = dijkstra(graph, start, end, optimize='time')
    results['fastest'] = (path, dist, cost, time)
    print_route("Fastest Route (Dijkstra)", path, dist, cost, time)

    # Apply constraints
    if max_cost or max_time:
        print(f"\n  📋 Routes within your constraints:")
        found = False
        for label, (path, dist, cost, time) in results.items():
            if path is None:
                continue
            cost_ok = (max_cost is None or cost <= max_cost)
            time_ok = (max_time is None or time <= max_time)
            if cost_ok and time_ok:
                print(f"     ✅ {label.replace('_', ' ').title()} — ₹{cost}, {time} hrs")
                found = True
        if not found:
            print("     ❌ No routes found within your constraints.")


# ─────────────────────────────────────────────
# BUILD SAMPLE GRAPH (Indian Cities)
# ─────────────────────────────────────────────

def build_india_graph():
    """Build a sample graph of Indian city connections."""
    g = Graph()

    # (src, dest, distance_km, cost_inr, time_hrs)
    routes = [
        ("Delhi",     "Agra",       200,  350,  3.0),
        ("Delhi",     "Jaipur",     270,  450,  4.5),
        ("Delhi",     "Chandigarh", 250,  400,  4.0),
        ("Agra",      "Jaipur",     240,  400,  4.0),
        ("Agra",      "Lucknow",    340,  550,  5.5),
        ("Jaipur",    "Ahmedabad",  650, 1000, 10.0),
        ("Jaipur",    "Mumbai",    1150, 1800, 18.0),
        ("Lucknow",   "Varanasi",   300,  500,  5.0),
        ("Varanasi",  "Patna",      250,  400,  4.0),
        ("Patna",     "Kolkata",    560,  850,  9.0),
        ("Ahmedabad", "Mumbai",     520,  800,  8.0),
        ("Mumbai",    "Pune",       150,  250,  2.5),
        ("Mumbai",    "Hyderabad",  710, 1100, 12.0),
        ("Pune",      "Hyderabad",  560,  900,  9.0),
        ("Hyderabad", "Bangalore",  560,  900,  8.5),
        ("Bangalore", "Chennai",    350,  600,  6.0),
        ("Chennai",   "Kolkata",   1660, 2500, 26.0),
        ("Kolkata",   "Bhubaneswar",440,  700,  7.0),
        ("Bhubaneswar","Chennai",   1100,1700, 17.0),
    ]

    for src, dest, dist, cost, time in routes:
        g.add_edge(src, dest, dist, cost, time)

    return g


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚗 SMART ROUTE PLANNER — Indian Cities\n")

    g = build_india_graph()
    g.display()

    # Example queries
    plan_route(g, "Delhi", "Bangalore")
    plan_route(g, "Delhi", "Chennai", max_cost=2000, max_time=20)
    plan_route(g, "Jaipur", "Kolkata")

    # Interactive mode
    print(f"\n{'='*55}")
    print("  🔍 Custom Route Query")
    print(f"{'='*55}")
    print(f"  Available cities: {', '.join(sorted(g.cities))}")
    src = input("\n  Enter source city: ").strip()
    dst = input("  Enter destination city: ").strip()
    max_c = input("  Max budget in ₹ (press Enter to skip): ").strip()
    max_t = input("  Max time in hrs (press Enter to skip): ").strip()

    plan_route(
        g, src, dst,
        max_cost=int(max_c) if max_c else None,
        max_time=float(max_t) if max_t else None
    )
