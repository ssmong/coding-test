# BFS와 DFS — 그래프 탐색 기초

> 백준 1260을 풀기 전에 읽어야 할 개념 노트.
> 모든 코드는 **명시적 파라미터** 스타일 (`bfs(graph, start, n)`). 이유는 [memory: feedback_explicit_params](../).

## 1. 그래프 표현

코딩테스트에서 그래프를 코드에 담는 두 가지 방식:

### 인접 리스트 (Adjacency List) — **권장**
```python
graph = [[] for _ in range(n + 1)]   # 1-indexed
graph[u].append(v)
graph[v].append(u)                    # 양방향이면
```
- 공간 O(V + E), 희소 그래프(간선 적음)에 유리. 삼성 코테는 거의 다 이쪽.

### 인접 행렬 (Adjacency Matrix)
```python
adj = [[False] * (n + 1) for _ in range(n + 1)]
adj[u][v] = adj[v][u] = True
```
- 공간 O(V²). N ≤ 500 정도일 때만 고려. 두 정점 연결 여부 확인이 O(1).

### 간선 리스트 (Edge List) — 특정 알고리즘 전용
```python
edges = [(w, u, v) for ...]   # 보통 가중치 먼저
```
- "특정 정점의 이웃 꺼내기"가 **O(E)** (전부 스캔) → BFS/DFS/다익스트라엔 **부적합** (O(V·E) → TLE).
- 맞는 곳: **크루스칼(MST)**처럼 "모든 간선을 가중치 순으로 한 번 훑는" 알고리즘. 접근 패턴이 "정점별 이웃"이 아니라 "전체 간선 순회"일 때만.
- 규칙: **자료구조는 알고리즘의 접근 패턴에 맞춘다.** 이웃 조회가 핫이면 인접 리스트.

---

## 2. DFS (깊이 우선 탐색)

한 방향으로 끝까지 들어갔다가 막히면 되돌아온다. **재귀** 또는 **명시적 스택**으로 구현.

### 재귀 버전
```python
import sys
sys.setrecursionlimit(10**6)

def dfs(graph, u, visited):
    visited[u] = True
    # 방문 시 작업(출력, 카운트 등)
    for v in graph[u]:
        if not visited[v]:
            dfs(graph, v, visited)

# 호출
visited = [False] * (n + 1)
dfs(graph, 1, visited)
```

> 깊은 재귀가 예상되면 인자를 줄이고 싶을 수 있음. 그땐 `visited`만 클로저/지역으로 캡처하는 inner 함수 패턴 사용. 격자 DFS처럼 깊이가 10⁶ 갈 수 있는 경우는 **BFS로 우회**가 더 안전.

### 스택 버전 (재귀 깊이 위험할 때)
```python
def dfs(graph, start, n):
    visited = [False] * (n + 1)
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        # 방문 시 작업
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    return visited
```

**주의:** 스택 버전은 재귀와 방문 순서가 다를 수 있다. "정점 번호가 작은 것부터" 같은 조건이 있다면 재귀 버전이 자연스럽다. 스택 버전은 인접 리스트를 **내림차순**으로 정렬해야 같은 순서가 나온다 (LIFO).

---

## 3. BFS (너비 우선 탐색)

가까운 것부터 차례대로. **큐**로 구현. 가중치 없는 그래프에서 **최단 거리**를 구할 때 필수.

```python
from collections import deque

def bfs(graph, start, n):
    visited = [False] * (n + 1)
    visited[start] = True
    q = deque([start])
    while q:
        u = q.popleft()
        # 방문 시 작업 ← 문제별: 출력/카운트/합산 등. 비워둬도 BFS는 동작.
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True       # ← popleft 시점이 아니라 enqueue 시점에!
                q.append(v)
    return visited
```

**용어 구분:**
- **방문 표시** = `visited[v] = True` (이미 큐에 넣었다는 기록)
- **방문 시 작업** = `popleft` 직후 자리 (꺼낸 노드로 실제 작업 — 출력, 카운트, 거리 갱신 등)

**가장 흔한 버그:** `visited`를 `popleft`할 때 표시하면 같은 노드가 큐에 여러 번 들어간다 → 큐 폭발(TLE/MLE), 거리 BFS면 거리 오염. 룰: **"큐에 넣는 순간 표시. 꺼낼 때 아님."**

### 왜 "처음 도달 = 최단"인가 (BFS 최단 보장의 근거)
큐가 FIFO라 **거리 작은 칸부터 전부 처리된 뒤** 다음 거리로 넘어간다. 거리 `d`짜리를 꺼내면 그 이웃은 `d+1`을 받아 **큐 맨 뒤**로 가므로, 큐 안의 거리는 항상 오름차순.
→ 어떤 칸을 **처음 만지는 순간이 도달 가능한 최소 거리.** 더 짧은 경로가 있었다면 더 이른 층에서 먼저 닿았을 것이므로(모순), 나중 도착은 항상 같거나 더 길다.
→ 그래서 **첫 방문 때 거리 확정 + 이후 재방문 무시**가 안전. `dist == -1`(미방문) 검사 하나로 최단이 자동 보장.
- 단, **간선 가중치가 다르면 이 성질이 깨진다** → 다익스트라/0-1 BFS 필요. 가중치 없는 격자·그래프에서만 성립.
- 상태 차원 BFS(예: 2206)는 `(좌표, 상태)`를 노드로 보면 같은 성질이 **각 상태 층 안에서** 성립.

### visited는 최적화가 아니라 생존 조건 (동전의 양면)
- **버려도 됨(정당성):** 위 성질 → 이미 방문한 노드에 나중에 또 도달 = 반드시 같거나 긴 경로 → 버려도 최단 안 놓침.
- **반드시 버려야 함(필요성):** 안 버리면 같은 상태를 무한 재방문 → 큐 폭발. 특히 **되돌아가는 사이클**(구슬 탈출: 오른쪽→왼쪽→오른쪽… A↔B 영원히)이 있으면 **프로그램이 안 끝남**(무한루프/MLE). 사이클 없어도 여러 경로 재도달로 **지수 폭발** → visited가 "상태 수만큼"으로 눌러 선형화.
- 즉 정당성(①) 덕에 안심하고 버리고, 그 버림이 필요성(②) 무한루프를 막는다. **상태공간 탐색에서 visited는 선택이 아님.**

### BFS 큐: deque인가 heapq인가
"BFS=무조건 deque"가 아니라 **간선 비용**에 따라 갈린다. FIFO가 최단을 보장하는 건 **모든 비용이 같을 때뿐.**

| 간선 비용 | 자료구조 | 넣는 법 | 예 |
|---|---|---|---|
| 전부 1 (균일) | `deque` | `append` + `popleft` (FIFO) | 7576, 2206, 1600 |
| 0 또는 1 | `deque` | 0이면 `appendleft`, 1이면 `append` (0-1 BFS) | 13549 |
| 제각각 (양수) | `heapq` | `heappush` (작은 비용 우선) = 다익스트라 | 1916, 1753 |

비용이 섞이면 "큐 앞 = 최소 거리" 불변식이 깨져서, 작은 비용을 앞으로 보내거나(0-1 BFS) 항상 최소를 꺼내는 힙(다익스트라)이 필요.

**BFS = "가중치가 전부 1인 다익스트라"의 특수경우.** 공통 엔진은 "아직 확정 안 된 것 중 **가장 가까운 노드를 꺼내 확장**"(꺼내는 순간 최단 확정). 차이는 "가장 가까운 것"을 싸게 찾는 법뿐:
- BFS: 비용 균일 → **FIFO 순서 = 거리 순서** 공짜 → 큐로 충분, enqueue 때 visited 1번.
- 다익스트라: 비용 제각각 → FIFO론 거리순 깨짐 → **heap으로 매번 최소 추출** + 완화 + stale 스킵.
- 무가중치엔 BFS로 충분(log 없음). 가중치 다를 때만 heap. **음수 간선이면 다익스트라도 실패** → 벨만-포드/SPFA.

### 거리 측정 변형
`visited`를 `dist`로 합쳐서 한 배열로 처리:
```python
def bfs_dist(graph, start, n):
    dist = [-1] * (n + 1)        # -1 = 미방문
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

---

## 4. 정점 번호가 작은 것부터 방문하려면

인접 리스트를 미리 정렬한다:
```python
for i in range(1, n + 1):
    graph[i].sort()
```
정렬 후 DFS는 자연스럽게 작은 번호부터 깊이 들어가고, BFS도 작은 번호부터 큐에 들어간다.

---

## 5. 격자(2D) 위 BFS/DFS

삼성 코테에서 가장 많이 나오는 형태. 그래프를 명시적으로 만들지 않고 **방향 벡터**로 이웃을 계산. 자세한 템플릿은 [02-bfs-grid.md](02-bfs-grid.md) 참고.

```python
dx = (-1, 1, 0, 0)   # 상 하 좌 우
dy = (0, 0, -1, 1)

for d in range(4):
    nx, ny = x + dx[d], y + dy[d]
    if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
        ...
```
8방향이면 dx, dy를 8개. 자세한 건 [templates/grid.py](../templates/grid.py).

---

## 6. 시간 복잡도

| 알고리즘 | 인접 리스트 | 인접 행렬 |
|---|---|---|
| BFS | O(V + E) | O(V²) |
| DFS | O(V + E) | O(V²) |

V = 정점 수, E = 간선 수.

---

## 7. 언제 BFS, 언제 DFS?

| 상황 | 선택 |
|---|---|
| 가중치 없는 최단 거리 | **BFS** |
| 모든 경로/조합 탐색, 백트래킹 | **DFS** (재귀) |
| 사이클 탐지, 위상 정렬 | DFS |
| 동시에 퍼지는 시뮬레이션 (불, 바이러스) | BFS 멀티소스 |
| 격자에서 깊이가 큼 (N×M ≥ 10⁵) | BFS 우선, DFS면 스택 버전 |
| **모든 조합/순열 열거 → 최선/유효 찾기** | **DFS/백트래킹** |

**핵심 한 줄:** BFS = "**최단/최소 몇 번?**", DFS/백트래킹 = "**모든 경우 만들어보고 그중 최선/유효**".

### 왜 "열거"는 BFS가 아니라 백트래킹인가
조합/순열을 다 만드는 문제(연산자 끼워넣기, N-Queen, 부분집합)는 "최단 거리"가 없어 BFS 대상이 아니다. 백트래킹이 맞는 이유:
- **점진적 구성 + 되돌리기:** 한 칸 정하고 깊이 들어갔다, 끝나면 되돌려(backtrack) 다음 선택. DFS의 "갔다 돌아옴"이 곧 이 구조.
- **메모리 O(깊이):** 지금 만드는 후보 하나만 들고 다님. BFS로 조합을 풀면 **모든 부분 후보를 큐에 동시에** → 지수적 메모리 폭발.
- **가지치기:** 부분 후보가 가망 없으면 그 아래 전체를 즉시 잘라냄. BFS는 레벨로 펼쳐서 이 타이밍이 어색.

---

## 8. 전체 main() 패턴

```python
import sys
from collections import deque
input = sys.stdin.readline

def bfs(graph, start, n):
    dist = [-1] * (n + 1)
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def main():
    n, m = map(int, input().split())
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    dist = bfs(graph, 1, n)
    print(max(dist))

main()
```

이 패턴이 기본형. 모든 큰 데이터는 인자로 전달, 결과는 return. `n`도 인자로 (어차피 `len(graph)-1`로 구할 수도 있지만 가독성).

---

## 9. 첫 문제

[문제로 가기 → problems/02-bfs/silver/1260-dfs-and-bfs/](../problems/02-bfs/silver/1260-dfs-and-bfs/problem.md)
