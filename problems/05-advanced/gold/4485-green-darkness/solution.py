import sys
import heapq

INF = float('inf')

def solve(grid, N):
    loss = [[INF] * N for _ in range(N)]
    loss[0][0] = grid[0][0]

    h = [(grid[0][0], 0, 0)]

    dr = (-1, 1, 0, 0)
    dc = (0, 0, -1, 1)

    while h :
        d, r, c = heapq.heappop(h)
        if d > loss[r][c]:
            continue

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            
            nd = d + grid[nr][nc]
            if  nd < loss[nr][nc]:
                loss[nr][nc] = nd
                heapq.heappush(h, (nd, nr, nc))

    return loss[-1][-1]


def main():
    input = sys.stdin.readline
    
    k = 1
    while True:
        N = int(input())
        if N == 0:
            break

        grid = [list(map(int, input().split())) for _ in range(N)]
        loss = solve(grid, N)
        print(f"Problem {k}: {loss}")
              
        k = k + 1

if __name__ == "__main__":
    main()