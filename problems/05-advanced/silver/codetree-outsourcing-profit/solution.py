import sys

T = 0
P = 1

def solve(N, works):
    profit = {'best': 0}
    def backtrack(day, profits):
        if day == N:
            if profit['best'] < profits:
                profit['best'] = profits
            return
        if day < N:
            backtrack(day + 1, profits)
        if day + works[day][T] <= N:
            backtrack(day + works[day][T], profits + works[day][P])
        return

    backtrack(0, 0)
    return profit['best']



def main():
    input = sys.stdin.readline

    N = int(input().rstrip())
    works = [list(map(int, input().split())) for _ in range(N)]

    ans = solve(N, works)
    print(ans)

if __name__ == "__main__":
    main()
