---
trigger: 백준 문제 입력을 파싱할 때. 특히 혼합 타입(int + char) 줄이 있을 때.
related_problems: [3190]
---

# 입력 파싱 관용구

## 언제 쓰나

모든 백준 풀이의 첫 단계. sys.stdin 최적화와 타입 변환 패턴은 거의 고정이다.

## 코드

```python
import sys
input = sys.stdin.readline   # 반드시. input() 그대로는 느림.

# 1. 단일 정수
N = int(input())

# 2. 여러 정수 한 줄 → 고정 개수 변수
R, C = map(int, input().split())

# 3. 여러 정수 한 줄 → 리스트
arr = list(map(int, input().split()))

# 4. 혼합 타입 (int + char) — split은 모두 str을 주므로 개별 변환
x, c = input().split()
x = int(x)
# c는 그대로 'L' / 'D' 등

# 5. 여러 줄을 한 번에 (엄청 빠름, 줄 수가 많을 때)
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
# ...
```

## 격자에서 특정 값의 좌표 모으기 (`np.where` 대용)
Python엔 `np.where` 같은 내장이 없다. **이중 for가 정석**이되, 격자를 두 번 훑지 말고 **읽으면서 같이 수집**한다.
```python
board, pieces = [], []                   # pieces = [(r, c, 값), ...]
for r in range(n):
    row = list(map(int, input().split()))
    board.append(row)
    for c, v in enumerate(row):
        if v != 0:
            pieces.append((r, c, v))

# 이미 board가 있다면 한 줄로
pieces = [(r, c, board[r][c]) for r in range(n) for c in range(m) if board[r][c]]
# 종류별로 나눌 땐 defaultdict(list) → pieces[종류] = [(r, c), ...]
```
- 어느 쪽이든 O(n·m) 한 번. numpy도 같은 O(n·m)이고 상수만 작아 코테에선 이득 없음(+ 실전 시험 미사용 권장).
- **flat list로 모으면 백트래킹 깊이와 인덱스가 1:1**로 맞는다 — "말 K개 각각 방향 4택" 같은 `4^K` 전수 탐색에서 `backtrack(i)` ↔ `pieces[i]`. dict로 모으면 이 순서를 다시 만들어야 함.

### ⚠️ "수집"할 것과 "조회"할 것을 구분하라
값 종류가 여러 개라고 전부 좌표 리스트로 만들면 손해다. **역할별로 필요한 자료구조가 다르다.**
| 역할 | 예 | 필요한 것 |
|---|---|---|
| 순회·열거 대상 (백트래킹 깊이가 됨) | 방향 정할 내 말 | **순서 있는 list** |
| 도착했을 때만 판정하는 장애물 | 상대 말·벽 | **없음** — `board[nr][nc] == X` 즉석 조회 |
| 총량만 필요 | 빈 칸 수(정답의 분모) | **카운터 int** |
- 장애물 좌표를 따로 모으면 매번 `in` 검사(list면 O(K), set이어도 격자 조회보다 느림) → **격자에 이미 있는 정보를 두 번 저장**하는 셈. 격자가 곧 O(1) 해시맵이다.

## 함정

- **`input()` 그대로 쓰면 느리다.** `sys.stdin.readline`으로 재정의하는 게 백준 관용구. 재정의 안 하고 그대로 `sys.stdin.readline()`을 호출하면 개행 문자가 붙어서 `int()`엔 문제 없지만 문자열 비교(`c == 'L'`)는 `'L\n'` 때문에 실패할 수 있음 → **혼합 타입일 땐 `.split()` 해야 안전**.
- **`input().split()`은 항상 `list[str]`**이다. 한 개만 정수여도 `map(int, ...)` 뭉텅이로 변환 못 함. `x, c = input().split(); x = int(x)` 패턴으로 쪼개라.
- **`map(int, ...)` vs 리스트 컴프리헨션** — 둘 다 OK지만 map이 약간 더 빠르고 짧다. 백준 관용구는 map.
- **`list.pop(0)`은 O(N)**이다. 입력 자체에서 나오는 실수는 아니지만, 파싱 후 소비 패턴으로 쓰면 TLE. 소비 순서가 있다면 `deque.popleft()` 또는 인덱스 변수.
- **대량 입력**(N ≥ 10^5 줄)은 `sys.stdin.read().split()` 일괄 읽기가 훨씬 빠르다. 일반 시뮬레이션은 readline으로 충분.

## 관련 개념

- [01-grid-template.md](01-grid-template.md) — 격자 문제 기본 세팅
- [../templates/io.py](../templates/io.py) — I/O 템플릿 전체
