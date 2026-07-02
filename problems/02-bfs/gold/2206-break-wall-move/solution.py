import sys
from collections import deque

EMPTY, WALL = '0', '1'
UNVISITED = -1

def bfs(grid, n, m):
    # BFS dim: dist[x][y][b]
    #   b = 부순 벽 개수 (0 or 1)
    #   값 = 해당 (칸, 상태)에 도달한 최단 칸 수
    dist = [[[UNVISITED] *2 for _ in range(m)] for _ in range(n)]

    q = deque()
    dist[0][0][0] = 1
    q.append((0, 0, 0))

    dx = (-1, 1, 0, 0)
    dy = (0, 0, -1, 1)

    while q:
        x, y, b = q.popleft()

        if x == n - 1 and y == m - 1:
            return dist[x][y][b]

        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            if not (0 <= nx < n and 0 <= ny < m):
                continue

            if grid[nx][ny] == EMPTY:
                if dist[nx][ny][b] == UNVISITED:
                    dist[nx][ny][b] = dist[x][y][b] + 1
                    q.append((nx, ny, b))
            
            elif grid[nx][ny] == WALL and b == 0:
                if dist[nx][ny][1] == UNVISITED:
                    dist[nx][ny][1] = dist[x][y][0] + 1
                    q.append((nx, ny, 1))
    return -1 
    

def main():
    input = sys.stdin.readline

    N, M = map(int, input().split())
    grid = [input().strip() for _ in range(N)]
    print(bfs(grid, N, M))

if __name__ == "__main__":
    main()