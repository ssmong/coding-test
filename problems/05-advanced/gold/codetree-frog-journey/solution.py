import sys
import heapq

INF = 1 << 30
DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def build_adj(N, g):
    """adj[k][r][c] = 점프력 k로 갈 수 있는 칸들. 격자만으로 정해지므로 딱 한 번."""
    adj = [[[[] for _ in range(N)] for _ in range(N)] for _ in range(6)]
    for k in range(1, 6):
        for r in range(N):
            for c in range(N):
                if g[r][c] != '.':
                    continue
                for dr, dc in DIRS:
                    nr, nc = r + k * dr, c + k * dc
                    if not (0 <= nr < N and 0 <= nc < N) or g[nr][nc] != '.':
                        continue                        # 밖이거나 착지 불가(S/#)
                    # 경유 칸은 #만 막는다 (S 위로 지나가는 건 허용)
                    if all(g[r + s * dr][c + s * dc] != '#' for s in range(1, k)):
                        adj[k][r][c].append((nr, nc))
    return adj


def shortest(N, adj, r1, c1, r2, c2):
    dist = [[[INF] * 6 for _ in range(N)] for _ in range(N)]
    dist[r1][c1][1] = 0
    pq = [(0, r1, c1, 1)]
    while pq:
        d, r, c, k = heapq.heappop(pq)
        if d > dist[r][c][k]:
            continue                                    # 힙에 남은 낡은 항목
        if r == r2 and c == c2:
            return d                                    # 도착 칸은 점프력 무관
        for nr, nc in adj[k][r][c]:                     # 점프: 1
            if d + 1 < dist[nr][nc][k]:
                dist[nr][nc][k] = d + 1
                heapq.heappush(pq, (d + 1, nr, nc, k))
        if k < 5:                                       # 증가: (k+1)^2
            w = d + (k + 1) * (k + 1)
            if w < dist[r][c][k + 1]:
                dist[r][c][k + 1] = w
                heapq.heappush(pq, (w, r, c, k + 1))
        for j in range(1, k):                           # 감소: 1
            if d + 1 < dist[r][c][j]:
                dist[r][c][j] = d + 1
                heapq.heappush(pq, (d + 1, r, c, j))
    return -1


def main():
    input = sys.stdin.readline

    N = int(input())
    g = [input().strip() for _ in range(N)]     # strip() 없으면 '\n'이 붙는다
    adj = build_adj(N, g)

    Q = int(input())
    out = []
    for _ in range(Q):
        r1, c1, r2, c2 = map(int, input().split())
        out.append(shortest(N, adj, r1 - 1, c1 - 1, r2 - 1, c2 - 1))
    print('\n'.join(map(str, out)))


if __name__ == "__main__":
    main()
