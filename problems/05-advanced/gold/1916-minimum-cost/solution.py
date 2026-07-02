import sys
import heapq

INF = float('inf')

def dijkstra(graph, N, start, end):
    dist = [INF] * (N + 1)    # start -> i 최단거리
    dist[start] = 0

    h = [(0, start)]    # (누적거리, 정점)

    while h:
        d, u = heapq.heappop(h)
        if u == end:
            return dist
        if d > dist[u]:
            continue

        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    
    return dist

def main():
    input = sys.stdin.readline

    N = int(input())
    M = int(input())

    graph = [[] for _ in range(N + 1)]
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))

    start, end = map(int, input().split())

    dist = dijkstra(graph, N, start, end)
    print(dist[end])

if __name__ == "__main__":
    main()