---
trigger: "모든 조합/순열을 다 시도해 최선/유효를 찾는" 문제 (연산자 배치, N명 중 K명 고르기, 순열, N-Queen). 최단거리 아님.
related_problems: [14888, 14889, 15686, 9663]
---

# 백트래킹 템플릿 — 선택 → 재귀 → 되돌리기

## 언제 쓰나
"최단 몇 번?"이 아니라 **"모든 경우를 만들어보고 그중 최선/유효"**일 때. (BFS와 구분: [02-bfs-dfs.md](02-bfs-dfs.md) §7)

## 심장: 빌리고-복구
```python
choose(x)          # 이 선택을 함 (상태 변경)
backtrack(다음)     # 더 깊이
unchoose(x)        # ★ 되돌리기 (상태 복구) — 이게 "무르기"
```
이 한 쌍이 백트래킹 전부. **복구를 빼먹으면** 형제 가지에 이전 선택이 새서 오답.

## 패턴 A — 개수로 가지치기 (14888 연산자)
같은 종류가 여럿이면 **개수만** 관리 → 자동 비구분(중복 가지 제거).
```python
for t in range(K):              # 선택 종류
    if cnt[t] == 0: continue
    cnt[t] -= 1                  # 빌림
    backtrack(idx + 1, 새상태)
    cnt[t] += 1                  # 복구
```

## 패턴 B — 인덱스 선택/미선택 (14889 N중 K 고르기, 조합)
```python
def bt(i, chosen):
    if len(chosen) == K:
        ... 평가 ...; return
    if i == N: return           # 다 봤는데 K 못 채움
    chosen.append(i); bt(i + 1, chosen); chosen.pop()   # i 선택 + 복구
    bt(i + 1, chosen)                                    # i 미선택
```
> 조합은 **`i+1`부터** 재귀해야 순서 중복 안 생김(같은 집합 두 번 X).

## 패턴 C — 개수 세기 (9663 N-Queen)
"몇 가지?"는 **각 호출이 자기 서브트리 개수를 return → 부모가 합산.** nonlocal/전역 불필요.
```python
def place(row):
    if row == N: return 1        # 한 행에 1개씩 다 놓음 → 완성 1가지
    total = 0
    for c in range(N):
        if 놓을수있으면:          # col[c], diag1[row+c], diag2[row-c+N-1] 로 O(1)
            표시(True); total += place(row + 1); 복구(False)
    return total
```
- **대각선 O(1) 충돌:** ↘는 `row+col` 일정, ↙는 `row-col` 일정 → 불리언 배열 2개면 지난 퀸 `not in` 스캔 불필요. `row-col`은 음수 가능 → **`+(N-1)` 오프셋, 배열 크기 `2N-1`**.
- **행 충돌 자동 해결:** `place(row)`가 한 행씩 내려가니 같은 행 체크 불필요.
- ⚠️ 누적값을 **int 인자로** 받아 `+=1` ❌ — 정수는 immutable이라 호출자에 반영 안 됨. **return 합산** 또는 `nonlocal`만 통함. (컨테이너 `[0]` 트릭도 되지만 지저분)

## itertools vs 직접 백트래킹
`itertools`는 표준 라이브러리라 항상 허용·관용적. **선택 기준:**
| 상황 | 도구 |
|---|---|
| 순수 "n중 k 고르기 / 순열 / 곱집합", **가지치기 없음** | `itertools.combinations/permutations/product` (재귀 오버헤드 없어 더 빠름) |
| **가지치기** 필요 / 부분상태 의존 분기 / 조기종료 (N-Queen, 연구소, 스도쿠) | **직접 백트래킹** |
- 핵심: itertools는 **전부 생성**해 중간에 못 걸러. 가지치기가 크면 백트래킹이 노드를 훨씬 덜 봐서 이김. 가지치기 없으면 itertools가 빠름(C레벨, 재귀 호출 오버헤드 없음).
- ⚠️ 성능 최적화 시 `sum(genexpr)`를 explicit Python `for`로 바꾸지 말 것 — 오히려 느려질 수 있음(측정으로 확인).

## 함정
- **복구(`+= 1` / `pop()` / `visited=False`) 누락** — 가장 흔한 버그.
- **base case 위치:** 완성됐을 때(`idx==N`, `len==K`) 평가하고 `return`.
- 결과(max/min/count)는 **클로저나 인자**로 — 모듈 전역 피하기.
- 재귀 깊이 크면(>10⁴) `sys.setrecursionlimit`. 보통 코테 백트래킹은 얕음(N≤20).

## 관련 개념
- [02-bfs-dfs.md](02-bfs-dfs.md) — 왜 열거는 BFS 아닌 백트래킹인지 (§7)
