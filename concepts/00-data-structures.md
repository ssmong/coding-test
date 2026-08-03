---
trigger: 파이썬 기본 자료구조가 헷갈릴 때. 무엇을 언제 쓰는지 + 시간 복잡도 함정.
related_problems: [3190, 1260, 2178]
---

# 파이썬 기본 자료구조 — 백준 관점

## 한눈 요약: 언제 무엇을 쓰나

| 필요 | 선택 | 핵심 이유 |
|---|---|---|
| 순서 있는 값들 (인덱스 접근) | `list` | 가장 범용 |
| **스택** (한쪽 끝만) | `list` + `append`/`pop` | 추가 import 없음 |
| **큐 / 양끝 큐** | `collections.deque` | `list.pop(0)`은 O(N) → 덱 필수 |
| 좌표, 고정 길이 묶음 | `tuple` | 불변 + 해시 가능 → dict/set 키로 사용 |
| **해시맵** (키 → 값) | `dict` | O(1) 조회/삽입/삭제 |
| 개수 세기 | `collections.Counter` | dict보다 관용구가 짧음 |
| **중복 없는 컬렉션 + O(1) 조회** | `set` | `x in list`는 O(N), `x in set`은 O(1) |
| 우선순위 (가장 작은/큰 것 반복 추출) | `heapq` (min-heap) | 다익스트라, 스케줄링 |

**절대 쓰지 말 것:** `queue.Queue` (멀티스레드용이라 단일스레드에선 deque보다 훨씬 느림)

---

## 1. list — 기본 배열 + 스택

파이썬의 `list`는 사실 "동적 배열". 가장 많이 쓴다.

```python
arr = []
arr = [0] * 5              # [0, 0, 0, 0, 0] — 초기화 관용구
arr = [[0] * M for _ in range(N)]   # 2D 격자. 주의: [[0]*M]*N 은 버그!

arr.append(x)              # 끝에 추가 — O(1)
x = arr.pop()              # 끝에서 제거 — O(1)
arr[i]                     # 인덱스 접근 — O(1)
len(arr)                   # 길이 — O(1)
```

### 스택으로 쓰기

한쪽 끝만 쓰면 스택. DFS 반복 버전, 괄호 짝 맞추기 등에 사용.

```python
stack = []
stack.append(x)            # push
top = stack.pop()          # pop
if stack: ...              # 비었는지
```

### ⚠️ 느린 연산 (백준 TLE 주범)

```python
arr.pop(0)                 # O(N) — 절대 큐로 쓰지 말 것
arr.insert(0, x)           # O(N)
del arr[i]                 # O(N)
x in arr                   # O(N) — list에서 `in` 검사 느림
arr.remove(x)              # O(N)
```

**규칙:** list에서 앞쪽/중간을 건드리는 연산이 핫루프에 들어가면 의심하라.

### 2D 격자 초기화 함정

```python
board = [[0] * M] * N      # ❌ 행들이 같은 객체를 공유! board[0][0]=1 하면 모든 행이 바뀜
board = [[0] * M for _ in range(N)]  # ✅ 각 행이 독립
```

이거 한 번 당하면 평생 안 잊는다. 격자 초기화는 항상 컴프리헨션으로.

---

## 2. tuple — 불변 묶음

`list`와 비슷하지만 **수정 불가**. 대신 **해시 가능** → dict 키나 set 원소로 쓸 수 있다.

```python
p = (3, 5)                 # 좌표
r, c = p                   # 언패킹
visited = set()
visited.add((3, 5))        # tuple이라 OK. list는 안 됨!
```

**언제 쓰나:** 좌표처럼 "고정 길이 + 바뀌지 않는 묶음"은 거의 항상 tuple. 뱀의 몸통 좌표(`(r, c)`)도 tuple로 저장.

---

## 3. dict — 해시맵

키로 값을 찾는다. 모든 기본 연산이 평균 O(1).

```python
d = {}
d['apple'] = 1
d['apple']                 # 1
'apple' in d               # O(1) 존재 확인
d.get('banana', 0)         # 없으면 0 — KeyError 방지 관용구
del d['apple']

for k, v in d.items():     # 키-값 동시 순회
    ...
```

### 카운팅 관용구 (자주 나옴)

```python
# 방법 A: get
count = {}
for x in arr:
    count[x] = count.get(x, 0) + 1

# 방법 B: Counter (더 짧음)
from collections import Counter
count = Counter(arr)       # {값: 개수}
```

### 3190 뱀에서의 활용

"시간 → 회전 방향" 매핑을 dict로 저장하면 "지금 이 초에 회전하나?"를 O(1)에 확인.

```python
turns = {}
for _ in range(L):
    x, c = input().split()
    turns[int(x)] = c
# 사용
if time in turns:
    ...
```

---

## 4. set — 중복 없는 집합

`dict`와 같은 해시 기반. 값만 저장. O(1) 조회.

```python
s = set()
s = {1, 2, 3}              # 빈 set은 set() — {} 은 빈 dict!
s.add(5)
s.discard(5)               # 없어도 에러 안 남 (remove는 에러 남)
5 in s                     # O(1)
len(s)
```

**언제 쓰나:** "이미 본 적 있는 좌표/값인가?"를 빠르게 확인할 때.

```python
# 사과 위치 저장 — 빠른 조회
apples = set()
for _ in range(K):
    r, c = map(int, input().split())
    apples.add((r, c))

# 사용
if (nr, nc) in apples:     # O(1)
    apples.remove((nr, nc))
```

### 함정: 빈 set 만들기

```python
s = {}                     # ❌ 이건 빈 dict!
s = set()                  # ✅
```

### "해시 가능(hashable)"이 무슨 뜻인가

`hash(x)` = 객체를 **정수 하나로 요약**하는 함수. `set`/`dict`가 O(1)인 이유 그 자체다.
```
s.add("abc")  →  hash("abc") % 크기 = 7번 칸  →  7번 칸에 저장
"abc" in s    →  hash("abc") % 크기 = 7번 칸  →  7번 칸만 확인 (전체 훑지 않음)
```
**mutable이 금지된 이유:** 넣은 뒤 내용이 바뀌면 해시값도 바뀐다 → 물건은 7번 칸에 있는데 3번 칸을 뒤지게 됨.
```python
k = [1, 2]; d = {k: 'v'}   # (가정) hash=A → A번 칸 저장
k.append(3)                 # 이제 hash=B
d[k]                        # B번 칸을 뒤짐 → 방금 넣은 걸 못 찾음
```
파이썬은 이 사고를 원천 차단하려고 mutable을 아예 unhashable로 만들었다. `TypeError`는 불편이 아니라 **안전장치**.
- 값이 같으면 해시도 같다(보장). 해시가 같다고 값이 같진 않다(충돌) → 칸을 찾은 뒤 `==`로 최종 확인.
- ⚠️ **불변성은 재귀적.** tuple이어도 **내용물에 mutable이 있으면 해시 불가:**
  `hash((1,2))` ✅ / `hash((1,(2,3)))` ✅ / `hash((1,[2]))` ❌
  → 좌표를 set에 넣을 때 `(r,c)`는 되고 `(r,[c])`는 안 되는 이유.

### frozenset — 불변 set (= 해시 가능한 set)

`set`은 mutable이라 **해시 불가** → 다른 set의 원소나 dict 키가 못 된다(`list`가 안 되는 것과 같은 이유). 그럴 때 `frozenset`.

| | 수정 | 해시 | set 원소·dict 키 |
|---|---|---|---|
| `list` / `set` | ✅ | ❌ | ❌ |
| `tuple` / `frozenset` | ❌ | ✅ | ✅ |

```python
seen = set()
seen.add({0, 1})                 # ❌ TypeError: unhashable type: 'set'
seen.add(frozenset({0, 1}))      # ✅
frozenset([0,1]) == frozenset([1,0])   # True — 순서 무관
```

**언제 쓰나:** "원소 모임 자체"를 키로 삼아 **중복 조합을 걸러낼 때**. 예 — 백트래킹 대칭 가지치기에서 "이 말이 뻗는 방향들의 집합"이 같으면 결과도 같으니 한 번만 탐색:
```python
key = frozenset(dirs_of(v, d))
if key in seen: continue
seen.add(key)
```
- `tuple`로도 되지만 **순서까지 따지므로** `tuple(sorted(...))`로 직접 정규화해야 함. frozenset은 그 정규화가 타입에 내장.
- ⚠️ **리터럴 문법 없음** — `{1,2}`는 set. 반드시 `frozenset([1,2])`. 빈 것은 `frozenset()`.
- ⚠️ 생성 비용이 tuple보다 큼. 수백만 번 만드는 핫 루프면 `tuple(sorted(...))`가 빠를 수 있음.

---

## 5. deque — 양끝 큐 (`collections.deque`)

양쪽 끝에서 넣고 빼기가 O(1). **BFS의 큐, 뱀 몸통 같은 양끝 연산의 필수 도구.**

```python
from collections import deque

q = deque()
q = deque([1, 2, 3])

# 오른쪽 끝
q.append(4)                # [1, 2, 3, 4]
x = q.pop()                # x=4

# 왼쪽 끝
q.appendleft(0)            # [0, 1, 2, 3]
x = q.popleft()            # x=0

q[0], q[-1]                # 양끝 조회
len(q), bool(q)
```

**"머리/꼬리"는 문제마다 의미가 달라진다.** 일반 큐(BFS)에선 "먼저 들어간 쪽 = 머리(front)"라고 부르지만, 뱀 같은 시뮬레이션에선 "새로 추가되는 쪽 = 머리"로 보는 게 자연스럽다. 그래서 이 노트에선 기본 설명에 **"오른쪽 끝 / 왼쪽 끝"** 이라는 중립 표기만 쓰고, 머리/꼬리 의미 부여는 각 관용구 안에서 정의한다.

### BFS 관용구

```python
from collections import deque

def bfs(graph, start, n):
    visited = [False] * (n + 1)
    visited[start] = True
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True   # ← enqueue 시점에 표시 (popleft 시점 X)
                q.append(v)
    return visited
```
자세한 템플릿은 [02-bfs-dfs.md](02-bfs-dfs.md) 참고.

### 뱀 몸통 (3190) 관용구

"머리 쪽에 추가, 꼬리 쪽에서 제거"가 한쪽→반대쪽 구조 그 자체. **이 노트의 뱀 관용구에선 오른쪽 끝 = 머리, 왼쪽 끝 = 꼬리**로 통일한다 (append가 자연스럽게 "새 머리 추가"가 되므로).

```python
snake = deque()
snake.append((1, 1))        # 시작 위치 (머리=꼬리)

# 매 초:
snake.append((nr, nc))      # 새 머리 (오른쪽 끝)
if not ate_apple:
    tail = snake.popleft()  # 꼬리 제거 (왼쪽 끝)
```

**규칙 하나 정해두기:** 반대 방향(`appendleft`로 머리 추가, `pop`으로 꼬리 제거)으로 해도 동작은 똑같다. 뭘 고르든 **한 문제 안에선 끝까지 지키기** — 중간에 뒤집히면 버그 투성이.

### 함정

- **`deque(X)`는 X를 펼친다 (생성자 한정).** `deque((0,0))`은 좌표가 아니라 원소 `0,0` 두 개 → `x,y=q.popleft()` 터짐. 튜플 하나를 시작점으로 넣으려면 `deque([(0,0)])` 또는 `q.append((0,0))`. **`append`는 펼치지 않고 통째로** 넣으므로 BFS 시작점은 `q.append((r,c,...))`가 안전.
- `q.pop(0)` **은 없다.** `popleft()`가 맞다.
- 빈 덱에서 `pop`하면 `IndexError` → `while q:` 가드.
- 중간 인덱스 접근 `q[k]`은 **O(N)**. 랜덤 액세스 많으면 list가 낫다.
- `x in q`도 O(N). 조회가 잦으면 `set`이나 보드 마커를 병행.

---

## 6. heapq — 우선순위 큐

"가장 작은 원소를 반복해서 꺼내고 싶다"는 상황에 쓴다. 다익스트라의 필수 도구. **min-heap만 있음** — max가 필요하면 값에 `-`를 붙여 넣는다.

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
x = heapq.heappop(h)       # 1 (항상 가장 작은 값)

# max-heap 흉내
heapq.heappush(h, -value)
x = -heapq.heappop(h)

# 튜플 저장 시 첫 원소 기준으로 정렬 (같으면 둘째)
heapq.heappush(h, (dist, node))   # 다익스트라: (거리, 정점)

top = h[0]                 # 안 꺼내고 최솟값 peek (읽기만 OK)
heapq.heapify(arr)         # 기존 리스트를 O(n)에 heap으로
while h: ...               # 빈 체크
```

**언제 쓰나:** 다익스트라, K번째로 큰/작은 값, "우선순위 기반 이벤트 처리".

### 함정
- **heap은 그냥 list지만 직접 건드리지 말 것.** `append`/`sort`/`h[i]=...` 금지(불변식 깨짐). 넣고 빼기는 무조건 `heappush`/`heappop`. `h[0]` 읽기만 예외.
- **원소는 비교 가능해야.** `(거리, 정점)`에서 거리 동률이면 정점끼리 비교 → 정점이 int면 OK, 비교 불가 객체면 `TypeError`.
- **decrease-key 없음.** 이미 든 값을 더 작게 갱신하는 기능이 없다 → 다익스트라는 **새 거리로 또 push**하고 pop 때 `if d > dist[u]: continue`로 stale 스킵 (안 하면 TLE).

---

## 요약 카드

시험장에서 10초 안에 결정할 수 있도록.

```
인덱스 접근만 → list
스택 → list (append/pop)
큐 / BFS → deque (popleft/append)
양끝 연산 (뱀, 윈도우) → deque
좌표·고정 묶음 → tuple
키→값 매핑 → dict
"본 적 있나?" O(1) 조회 → set
"가장 작은 것" 반복 추출 → heapq
```

## 관련 개념

- [01-grid-template.md](01-grid-template.md) — 격자 문제 기본 세팅에서 이 자료구조들이 어떻게 조합되는지
- [02-bfs-dfs.md](02-bfs-dfs.md) — BFS/DFS에서 deque/list 사용 패턴
- [00-input-parsing.md](00-input-parsing.md) — 입력을 이 자료구조들로 담는 관용구
