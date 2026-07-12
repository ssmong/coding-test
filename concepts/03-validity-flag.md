---
trigger: 완전탐색에서 "구성 칸이 전부 격자 안일 때만 유효"를 판정할 때. 무효를 어떻게 표시할지 고를 때.
related_problems: [14500]
---

# 유효성 표시: 매직 sentinel(0) vs valid 플래그

## 언제 쓰나
고정 모양(테트로미노 등)을 격자에 놓을 때 "구성 칸이 하나라도 밖이면 무효." 이 무효를 max 후보에서 어떻게 뺄까.

## 함정: `cur = 0` sentinel은 값 도메인에 조용히 의존
```python
for d in range(4):
    ...
    if 밖이면:
        cur = 0; break     # 무효를 0으로 → max에서 안 뽑히길 기대
results.append(cur)
return max(results)
```
- **격자값이 전부 ≥1이면 맞다** — 유효 합 ≥4 > 0이라 무효(0)는 절대 안 이김. (14500이 이 경우)
- **값이 0/음수 가능하면 깨짐** — 무효(0)가 음수합 유효 조각을 이기거나, 합이 0인 유효 조각과 구분 불가. "모든 값 양수"라는 **숨은 가정**에 의존 → 제약 바뀌면 조용히 오답.

## 더 튼튼한 구조: valid 플래그로 분리
```python
best_t = 0
for skip in range(4):            # T = 중심 + 이웃4 중 하나 빼기 (4회전)
    total = grid[r][c]; ok = True
    for d in range(4):
        if d == skip: continue
        nr, nc = r+DR[d], c+DC[d]
        if not (0 <= nr < N and 0 <= nc < M):
            ok = False; break
        total += grid[nr][nc]
    if ok and total > best_t:     # ★ 유효할 때만 후보
        best_t = total
return best_t
```
- "유효한가(`ok`)"와 "합이 얼마(`total`)"를 **분리** → 값 도메인 가정 불필요. 리스트도 안 만들고 러닝 max.

## 함정
- sentinel 0은 "빼먹으면 틀린다"가 아니라 **"조건 바뀌면 틀린다"** — 코테선 통과해도 왜 안전한지(값 ≥1) 근거를 알고 써야 함.

## 관련 개념
- [03-backtracking.md](03-backtracking.md) — T는 경로 DFS로 못 만들어 따로 처리
