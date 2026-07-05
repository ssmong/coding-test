import sys

def solve(N):
    col   = [False] * N          # 열 사용 여부
    diag1 = [False] * (2*N - 1)  # ↘ 대각선: 인덱스 = r + c
    diag2 = [False] * (2*N - 1)  # ↙ 대각선: 인덱스 = r - c + (N-1)
    count = 0


def main():
    input = sys.stdin.readline
    N = int(input())
    ans = solve(N)
    print(ans)

if __name__ == "__main__":
    main()