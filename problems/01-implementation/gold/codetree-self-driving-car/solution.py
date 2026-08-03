import sys

ROAD = 0
HUMAN = 1

# CCW
DR = (-1, 0, 1, 0)
DC = (0, 1, 0, -1)

def solve(n, m, r, c, d, roads):
    visited = [[False] * m for _ in range(n)]
    visited[r][c] = True
    area = 1

    while True:
        # step 1 & 2
        moved = False
        for i in range(4):
            d = (d + 3) % 4
            nr, nc = r + DR[d], c + DC[d]
            if visited[nr][nc] == False and roads[nr][nc] == ROAD:
                visited[nr][nc] = True
                moved = True
                area += 1
                r, c = nr, nc
                break

        # step 3
        if moved == False:
            nr, nc = r - DR[d], c - DC[d]
            if roads[nr][nc] == HUMAN:
                break
            else:
                r, c = nr, nc

    return area



def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    x, y, d = map(int, input().split())

    roads = [list(map(int, input().split())) for _ in range(n)]

    ans = solve(n, m, x, y, d, roads)
    print(ans)

if __name__ == "__main__":
    main()
