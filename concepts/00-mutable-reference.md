---
trigger: 함수에 리스트/딕셔너리 넘겼는데 바깥에서도 바뀌는지 헷갈릴 때, 또는 반대로 수정했는데 안 바뀔 때
related_problems: [14499, 3190]
---

# 파이썬 변경 가능 객체(mutable) 참조 전달

## 언제 쓰나
- 함수에 리스트/딕셔너리 넘겨서 **안에서 수정**할 때 — 반환 필요한지 판단
- 같은 보드를 여러 함수가 건드리는 시뮬레이션
- `visited`, `board`, `dice`, `snake` 등 공유 상태 다룰 때
- 스냅샷 필요한지 (`deepcopy`) 판단할 때

## 핵심 규칙
파이썬 인자 전달은 **"객체 참조의 값 복사(pass-by-object-reference)"**.

| 타입 | 함수 안에서 수정 가능? | 바깥에 반영됨? |
|---|---|---|
| `list`, `dict`, `set`, 사용자 객체 | ✅ in-place 가능 | ✅ 반영됨 |
| `int`, `str`, `tuple`, `frozenset` | ❌ 불가 (불변) | — |

**구분점은 "이름 재할당"과 "내용 수정"이 다르다는 것.**

```python
def modify(lst):
    lst[0] = 99       # ✅ 내용 수정 → 바깥에 반영
    lst.append(4)     # ✅ 내용 수정 → 바깥에 반영

def reassign(lst):
    lst = [9, 9, 9]   # ❌ 이름 재할당 → 바깥과 연결 끊김

a = [1, 2, 3]
modify(a);   print(a)   # [99, 2, 3, 4]
reassign(a); print(a)   # [99, 2, 3, 4]  (변화 없음)
```

## `b = a` 자체가 복사가 아니다 — 참조(주소) 공유
함수 인자만이 아니라 **평범한 대입**도 똑같음. `b = a`는 객체를 복사하지 않고 **참조만 복사** → 항상 같은 주소.
```python
x = 1
y = x
print(x is y)      # True — 같은 객체(id 동일)
x = 2              # 1을 고친 게 아니라 x를 새 객체 2에 재바인딩
print(y)           # 1 — y는 여전히 원래 객체 1

a = [1, 2]
b = a
a.append(3)
print(b)           # [1, 2, 3] — 같은 리스트 in-place 변경 → b도 영향
```
- **불변(int/str/tuple):** in-place 변경 불가 → 재바인딩만 가능 → 값복사처럼 안전해 보임.
- **가변(list/dict):** 같은 객체를 in-place로 바꾸면 다른 이름에도 보임 → 진짜 함정. 원본 지키려면 `b = a[:]` / `deepcopy`.

## 코드 — 주사위/보드 패턴
```python
def roll(dice, d):
    t, b, n, s, e, w = dice
    # 인덱스 대입 = in-place 수정 → 바깥 dice도 바뀜
    dice[0], dice[4], dice[1], dice[5] = w, t, e, b
# 반환 불필요. 호출은 그냥 roll(dice, d)
```

vs. 새 리스트를 만드는 경우:
```python
def rotated(dice, d):
    return [w, b, n, s, t, dice[5]]   # 새 리스트
dice = rotated(dice, d)                # 받아야 함
```

## 함수 안에서 바깥 변수 접근 (LEGB)
함수가 인자로 안 받은 바깥 변수도 **읽기**는 그냥 됨 (LEGB 순서로 탐색: Local → Enclosing → Global → Built-in).

```python
gears = [deque(...) for _ in range(4)]   # 모듈 스코프

def rotate_all(start, direction):
    print(gears[0])         # ✅ 읽기 OK
    gears[0].rotate(1)      # ✅ mutate OK (메서드 호출)
    rot = [0] * 4           # ✅ 새 로컬 변수, 바깥과 무관
```

**단, 재할당은 `global` 선언 필요:**
```python
count = 0
def bad():
    count = count + 1   # UnboundLocalError
    # 좌변 = 가 보이는 순간 count는 로컬로 분류됨
    # 우변에서 읽으려는데 로컬에 아직 값 없음 → 에러
def good():
    global count
    count += 1
```

**기본 방침: 명시적 파라미터.** 보드·그래프·visited 같은 큰 상태도 인자로 받고 결과는 return. 이유:
- "이게 전역인지 인자인지" 매번 머리 굴리는 비용 > 시그니처 몇 글자 추가하는 비용
- Python에선 객체 참조 전달이라 인자로 넘겨도 복사 비용 0
- `main()`으로 감싸면 진짜 전역이 거의 없어짐 → 의도치 않은 상태 공유 사고 차단

**예외 (전역 허용):** 깊은 재귀 DFS에서 인자 개수가 부담될 때, `sys.setrecursionlimit`과 함께 전역 `visited` 사용. 핫 루프 안에서 호출되는 헬퍼는 전역이 미세하게 빠를 수 있음.

## 함정
- **`=` 대입은 수정이 아니라 재바인딩.** `lst = [...]` (함수 안) = 원본 안 바뀜.
- **슬라이스 대입은 in-place.** `lst[:] = [...]`는 내용 교체라서 바깥 반영됨. 전체 교체할 땐 이 관용구 유용.
- **얕은 복사 주의.** `new = old.copy()`나 `new = old[:]`는 2D 격자에서 행이 공유됨. 2D는 `copy.deepcopy(old)` 또는 `[row[:] for row in old]`.
- **동시 수정 버그.** 여러 객체가 같은 리스트를 가리키는데 한쪽에서 수정하면 다른 쪽도 바뀜. 시뮬레이션에서 "이번 턴 상태"와 "다음 턴 상태"를 같은 보드에 쓰면 꼬임 → 스냅샷 필요.
- **기본 인자 함정.** `def f(x, memo=[]):`의 `memo`는 호출 간 공유됨. 기본값으로 mutable 쓰지 말 것.

## 판별 체크리스트
함수 작성 전 자문:
1. 이 함수가 인자를 **수정**하나, **읽기만** 하나?
2. 수정한다면 **같은 객체를 바꾸나** (반환 불필요), **새 객체를 만드나** (반환 필요)?
3. 호출자가 원본을 보존해야 하나? → 함수 진입 시 `arr[:]` 또는 `deepcopy`로 복사.

## 관련 개념
- [00-data-structures.md](00-data-structures.md) — mutable/immutable 타입 분류
