import sys
from collections import deque

EMPTY = 0
OBSTACLE = 1
UNVISITED = -1

def bfs(grid, K):
    H, W = len(grid), len(grid[0])          # H=행 수, W=열 수
    # dist[r][c][k]: (행 r, 열 c)에 말 이동 k번 쓴 상태로 도달한 최소 동작 수
    dist = [[[UNVISITED] * (K + 1) for _ in range(W)] for _ in range(H)]
    dist[0][0][0] = 0                        # 시작 = 0 동작 (동작 수를 셈)

    dr = (-1, 1, 0, 0)
    dc = (0, 0, -1, 1)
    hdr = (-2, -2, -1, -1, 1, 1, 2, 2)      # 말(나이트) L자 8방향: 행 변화
    hdc = (1, -1, 2, -2, 2, -2, 1, -1)      #                       열 변화

    q = deque()
    q.append((0, 0, 0))                      # (행, 열, 말 이동 횟수)

    while q:
        r, c, k = q.popleft()

        if r == H - 1 and c == W - 1:
            return dist[r][c][k]

        # 일반 이동 (4방향): 상태 k 유지
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if not (0 <= nr < H and 0 <= nc < W):
                continue
            if dist[nr][nc][k] == UNVISITED and grid[nr][nc] == EMPTY:
                dist[nr][nc][k] = dist[r][c][k] + 1
                q.append((nr, nc, k))

        # 말 이동 (L자 8방향): k 한 번 소모
        if k < K:
            for d in range(8):
                nr, nc = r + hdr[d], c + hdc[d]
                if not (0 <= nr < H and 0 <= nc < W):
                    continue
                if dist[nr][nc][k + 1] == UNVISITED and grid[nr][nc] == EMPTY:
                    dist[nr][nc][k + 1] = dist[r][c][k] + 1
                    q.append((nr, nc, k + 1))

    return -1


def main():
    input = sys.stdin.readline

    K = int(input())
    W, H = map(int, input().split())

    grid = [list(map(int, input().split())) for _ in range(H)]
    print(bfs(grid, K))

if __name__ == "__main__":
    main()
