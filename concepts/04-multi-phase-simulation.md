---
trigger: 지문이 "1단계 → 2단계 → 3단계" 로 나뉜 시뮬인데 사이클 수(k)가 커서 시간이 빠듯할 때
related_problems: [16235, 20055]
---

# 다단계 시뮬레이션 — 단계를 나누되, 스캔은 합치기

## 언제 쓰나
- 지문이 "각 사이클마다 ①먹고 ②죽고 ③번식하고 ④양분추가" 식으로 단계가 명시된 문제
- k가 1000회쯤 되고 원소 수가 수천 개라 **사이클당 전수스캔 횟수**가 그대로 상수배가 되는 경우

## 원칙 1 — 코드는 지문 단계 순서대로 쓴다
먼저 정확성. `# Step 1 / 2 / 3` 주석을 달고 지문 문장과 1:1로 맞춘다. 단계를 섞으면 "같은 턴 안에서 서로 영향" 버그가 난다.

## 원칙 2 — 그 다음, 같은 컬렉션을 두 번 훑는 단계를 찾아 합친다
정확성이 확보된 뒤에만. **뒤 단계의 판정 조건이 앞 단계에서 이미 계산된 값이면**, 앞 단계에서 결과만 수집해두면 뒤 단계의 전수스캔이 통째로 사라진다.

```python
# ❌ Step 1에서 나이를 올리고, Step 3에서 전체를 다시 훑어 5의 배수를 찾음
for r in range(n):
    for c in range(n):
        for age in board[r][c]:          # 두 번째 전수스캔
            if age % 5 == 0: ...

# ✅ 나이를 올리는 그 순간 이미 알 수 있다 — 칸 단위로 개수만 모아둔다
breeders = []
for r in range(n):
    for c in range(n):
        nbreed = 0
        while cell:
            age = cell.popleft()
            if left >= age:
                left -= age; age += 1; push(age)
                if age % 5 == 0: nbreed += 1     # 여기서 확정
        if nbreed: breeders.append((r, c, nbreed))
for r, c, cnt in breeders: ...                   # 번식 칸 수만큼만 순회
```
실측(n=10, k=1000, 생존 8300마리): **2.01s → 0.52s**. 알고리즘은 그대로, 스캔 횟수만 절반.

## 원칙 3 — 정렬 불변식이 있으면 조기 `break`
컨테이너가 오름차순이면 "하나가 실패 = 뒤는 전부 실패"인 경우가 많다. 검사 자체를 건너뛴다.
```python
else:                              # 이 놈이 굶었다
    dead_food += age >> 1
    while cell:                    # 뒤는 전부 더 늙음 -> 검사 없이 일괄
        dead_food += cell.popleft() >> 1
    break
```
불변식을 **만들고 유지하는** 방법 자체는 [01-sorted-invariant-deque.md](01-sorted-invariant-deque.md) 참고 (여기선 그걸 속도로 바꿔 쓰는 쪽만 다룬다).

## 함정
- **누적 컨테이너를 안쪽 루프에서 재생성.** `dead = []`를 `for c` 안에 두면 마지막 칸 것만 살아남고 조용히 틀린다. 누적 리스트는 **사이클 루프 바로 아래**에 선언. (실제 발생: 죽은 바이러스 중 마지막 칸 것만 양분이 됨)
- **합치면 안 되는 단계도 있다.** 죽은 원소의 양분이 *다른 칸*으로 갈 수 있는 문제라면 Step 2를 Step 1에 접으면 안 된다(같은 칸으로만 가는 게 확인됐을 때만 안전).
- **핫 루프 캐싱은 마지막에.** `food_r = food[r]`, `push = alive.append`는 정확성이 끝난 뒤 얹는다. 먼저 하면 디버깅이 어려워진다.

## 관련 개념
- [01-sorted-invariant-deque.md](01-sorted-invariant-deque.md) — 매 턴 재정렬 없이 순서 유지 (이 노트의 전제)
- [00-mutable-reference.md](00-mutable-reference.md) — 칸마다 `deque` 만들 때 `[deque()] * n` 공유 함정
- [01-grid-template.md](01-grid-template.md) — 격자 순회·방향 벡터
