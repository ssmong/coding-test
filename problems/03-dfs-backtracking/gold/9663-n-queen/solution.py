import sys

def solve(N):
    col   = [False] * N          # 열 c에 퀸 있음?
    diag1 = [False] * (2*N - 1)  # ↗ 대각선: 인덱스 = r + c
    diag2 = [False] * (2*N - 1)  # ↘ 대각선: 인덱스 = r - c + (N-1)

    def place(r):
        if r == N:
            return 1
        total = 0
        for c in range(N):
            if col[c] or diag1[r + c] or diag2[r - c + N - 1]:
                continue
            col[c], diag1[r + c], diag2[r - c + N - 1] = True, True, True
            total += place(r + 1)
            col[c], diag1[r + c], diag2[r - c + N - 1] = False, False, False
            
        return total
    
    return place(0)


def main():
    input = sys.stdin.readline
    N = int(input())
    ans = solve(N)
    print(ans)

if __name__ == "__main__":
    main()