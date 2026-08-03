---
trigger: "L개 칸이 전부 조건을 만족하는가"를 한 줄로 쓰고 싶을 때. if 안에 제너레이터 표현식을 넣기 전에.
related_problems: [14890]
---

# all / any 와 제너레이터 truthiness 함정

## 언제 쓰나
연속 구간 검사(경사로, 활주로, 회문, 전부 같은 값인지)를 for/break 없이 한 줄로 쓸 때.

## 코드
```python
# 구간 전부 조건 만족
if all(h[r][c] == h[r][c + i] + 1 for i in range(1, L + 1)):
    ...

# 하나라도 만족
if any(h[r][c] == 0 for c in range(n)):
    ...
```
- `all`/`any` 모두 **short-circuit** → 직접 for/break와 시간복잡도 동일. 성능 손해 없음.
- 빈 iterable: `all([]) == True`, `any([]) == False`. (L=0 같은 경계에서 조용히 통과할 수 있음)

## 함정
- **`all` 을 빼먹으면 문법 에러가 안 난다.** `if (x == y for i in range(L)):` 는 제너레이터 **객체**를 만들고,
  객체는 항상 truthy → 비교가 한 번도 실행되지 않고 `if`가 무조건 통과. 가장 찾기 어려운 버그 유형.
  ```python
  bool(x == 1 for x in [9, 9, 9])   # True (!)
  ```
- 같은 이유로 `if (a and b for ...)`, `while (...)` 도 전부 무조건 참.
- 검사 도중 "어디서 깨졌는지" 인덱스가 필요하면 `all`로는 알 수 없다 → 그때는 명시적 for + break.

## 관련 개념
- [03-validity-flag.md](03-validity-flag.md) — 유효/무효를 플래그로 분리하는 구조
- [01-grid-template.md](01-grid-template.md) — 격자 경계 체크
