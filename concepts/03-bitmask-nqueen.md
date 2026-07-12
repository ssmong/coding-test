---
trigger: 백트래킹 상태(사용한 열/대각선/원소 집합, 원소 ≤ ~20개)를 불리언 배열 대신 정수 비트로 들고 싶을 때
related_problems: [9663]
---

# 비트마스크 백트래킹 (N-Queen)

## 언제 쓰나
작은 집합 상태를 int 하나로 표현. **인자로 넘기면 undo 자체가 사라진다.**

## 코드
~~~python
def solve(N):
    full = (1 << N) - 1                # N개 열이 전부 1
    def place(cols, ld, rd):           # 셋 다 "현재 행에서 막힌 열" 마스크
        if cols == full: return 1      # 열 N개 소진 = 퀸 N개 (row 변수 불필요)
        total = 0
        avail = full & ~(cols | ld | rd)   # 놓을 수 있는 열들
        while avail:
            bit = avail & -avail       # 최하위 1비트 = 이번에 놓을 열
            avail -= bit
            total += place(cols | bit, (ld | bit) << 1 & full, (rd | bit) >> 1)
        return total
    return place(0, 0, 0)
~~~

## 핵심 발상
- 대각선에 전역 이름(`r+c`)을 붙이는 대신 **"다음 행에서 막히는 열"로 투영** — (r,c) 퀸은 r+1행의 c−1, c+1을 막으니 **행 내려가기 = 시프트 1회**.
- 상태를 mutate하지 않고 **새 정수를 인자로 전달** → 복구 누락/비대칭 버그가 구조적으로 불가능 (배열 버전에서 겪은 `diag1[c]` 복구 실수가 아예 없음).

## 함정
- `<< 1` 뒤 `& full` 생략: 정답은 유지되나 int가 계속 자라서 느려짐.
- **CPython 실측 이득은 ~1.2배뿐** (9663 N=14: 9.4s → 7.9s) — 재귀 호출 오버헤드가 지배해서 노드당 연산 절감이 희석됨. "2~3배"는 C/PyPy 이야기. CPython에서 크게 줄이려면 **노드 수 자체를 줄여야** (첫 행 좌우대칭 절반 탐색 ≈ 2배).
- `avail & -avail`(최하위 비트)은 2의 보수 트릭 — 처음 쓰면 `bin()`으로 한 번 찍어 확인.

## 관련 개념
- [03-backtracking.md](03-backtracking.md) — 배열 + 복구 버전 (패턴 C)
