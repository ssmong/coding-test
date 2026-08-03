import sys

PLUS = 0
MINUS = 1
MUL = 2
DIV = 3

def solve(nums, ops, N):
    best = {'max': float('-inf'), 'min': float('inf')}

    def backtrack(idx, acc):
        if idx == N:
            if acc > best['max']: best['max'] = acc
            if acc < best['min']: best['min'] = acc
            return

        x = nums[idx]
        for t in range(4):
            if ops[t] == 0:
                continue

            if   t == PLUS:  new_acc = acc + x
            elif t == MINUS: new_acc = acc - x
            elif t == MUL:   new_acc = acc * x
            else:            new_acc = int(acc / x)

            ops[t] -= 1
            backtrack(idx + 1, new_acc)
            ops[t] += 1
    
    backtrack(1, nums[0])
    return best['max'], best['min']

def main():
    input = sys.stdin.readline

    N = int(input())
    nums = list(map(int, input().split()))
    ops = list(map(int, input().split()))
    mx, mn = solve(nums, ops, N)
    print(mx)
    print(mn)


if __name__ == "__main__":
    main()