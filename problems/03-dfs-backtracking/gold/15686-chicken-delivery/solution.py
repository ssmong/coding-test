import sys

EMPTY = 0
HOUSE = 1
CHICKEN = 2

def solve(houses, chickens, M):
    best = {'min': float('inf')}
    
    def dist(house, chicken):
        return abs(house[0] - chicken[0]) + abs(house[1] - chicken[1])
    
    def city_dist(chosen):
        _city_dist = 0
        for house in houses:
            house_dist = float('inf')
            for chicken in chosen:
                _house_dist = dist(house, chicken)
                if _house_dist < house_dist:
                    house_dist = _house_dist
            _city_dist += house_dist
        return _city_dist
    
    def backtrack(idx, chosen):
        if len(chosen) == M:
            d = city_dist(chosen)
            if d < best['min']:
                best['min'] = d
            return
        if idx == len(chickens):
            return
        
        backtrack(idx + 1, chosen + [chickens[idx]])
        backtrack(idx + 1, chosen)
    
    backtrack(0, [])
    return best['min']


def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    grid = [list(map(int, input().split())) for _ in range(N)]

    houses = []
    chickens = []

    for r in range(N):
        for c in range(N):
            if grid[r][c] == HOUSE:
                houses.append((r, c))
            elif grid[r][c] == CHICKEN:
                chickens.append((r, c))

    mn = solve(houses, chickens, M)
    print(mn)

if __name__ == "__main__":
    main()