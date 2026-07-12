import sys

DR = (-1, 1, 0, 0)
DC = (0, 0, -1, 1)

def solve(grid, N, M):
    best = 0
    mx = max(max(row) for row in grid)
    visited = [[False] * M for _ in range(N)]

    def path_dfs(r, c, depth, total):
        if (4 - depth) * mx + total <= best:
            return total
        if depth == 4:
            return total
        
        cur = total
        for d in range(4):
            nr = r + DR[d]
            nc = c + DC[d]
            if 0 <= nr < N and 0 <= nc < M and visited[nr][nc] == False:
                visited[nr][nc] = True
                ncur = path_dfs(nr, nc, depth + 1, total + grid[nr][nc])
                if ncur > cur:
                    cur = ncur
                visited[nr][nc] = False
        
        return cur
    
    def path_t(r, c):
        best_t = 0
        for skip in range(4):
            total = grid[r][c]
            ok = True
            for d in range(4):
                if d == skip:
                    continue
                nr, nc = r + DR[d], c + DC[d]
                if not (0 <= nr < N and 0 <= nc < M):
                    ok = False
                    break
                total += grid[nr][nc]
            if ok and total > best_t:
                best_t = total
        return best_t

        
    for r in range(N):
        for c in range(M):
            visited[r][c] = True
            cand = path_dfs(r, c, 1, grid[r][c])
            if cand > best:
                best = cand
            visited[r][c] = False

            cand = path_t(r, c)
            if cand > best:
                best = cand
    
    return best


def main():
    input = sys.stdin.readline

    N, M = map(int, input().split())

    grid = [list(map(int, input().split())) for _ in range(N)]
    ans = solve(grid, N, M)
    print(ans)


if __name__ == "__main__":
    main()