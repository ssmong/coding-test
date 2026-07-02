import sys
import itertools

def solve(N, S):
    half = N // 2
    P = [[S[i][j] + S[j][i] for j in range(N)] for i in range(N)]
    full = set(range(N))
    best = {'min': float('inf')}

    def power(team):
        return sum(P[team[a]][team[b]]
                   for a in range(len(team)) for b in range(a + 1, len(team)))
    
    def backtrack(idx, start):
        if len(start) == half:
            link = [i for i in range(N) if i not in start]
            d = abs(power(link) - power(start))
            if d < best['min']:
                best['min'] = d
            return
        if idx == N:
            return
        
        backtrack(idx + 1, start + [idx])
        backtrack(idx + 1, start)

    backtrack(1, [0])

    """
    for combo in itertools.combinations(range(1, N), half - 1)::
        start = (0,) + combo
        link = list(full - set(start))
        d = abs(power(start) - power(link))
        if d < best:
            best = d
    return best
    """
    return best['min']


def main():
    input = sys.stdin.readline

    N = int(input())
    S = [list(map(int, input().split())) for _ in range(N)]

    mn = solve(N, S)

    print(mn)


if __name__ == "__main__":
    main()