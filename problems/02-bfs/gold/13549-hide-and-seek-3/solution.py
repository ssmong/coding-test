import sys
from collections import deque

INF = float('inf')

def bfs(n, k):
    limit = max(n, 2*k)
    dist = [INF] * (limit + 1)
    dist[n] = 0

    q = deque([n])

    while q:
        x = q.popleft()

        for nx, w in ((x + 1, 1), (x - 1, 1), (2 * x, 0)):
            if 0 <= nx <= limit and dist[x] + w < dist[nx]:
                dist[nx] = dist[x] + w
                q.appendleft(nx) if w == 0 else q.append(nx)
        
    return dist[k]

def main():
    input = sys.stdin.readline
    
    N, K = map(int, input().split())
    print(bfs(N, K))

if __name__ == "__main__":
    main()