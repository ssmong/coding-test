import sys
import heapq

UNVISITED = float('inf')

def dijkstra(graph, start, V):
    dist = [UNVISITED] * (V + 1)
    dist[start] = 0

    h = [(0, start)]    # (누적거리, 정점)

    while h:
        d, u = heapq.heappop(h)

        if d > dist[u]:
            continue

        for v, w in graph[u]:
            if (d + w) < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    
    return dist

def main():
    input = sys.stdin.readline

    V, E = map(int, input().split())
    K = int(input())

    graph = [[] for _ in range(V + 1)]
    for _ in range(E):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))

    dist = dijkstra(graph, K, V)

    print('\n'.join("INF" if dist[i] == UNVISITED else str(dist[i]) for i in range(1, V + 1)))

if __name__ == "__main__":
    main()