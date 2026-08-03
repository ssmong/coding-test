---
trigger: 일렬로 나열된 항목을 앞에서부터 "한다/안 한다" 고르는데, 하면 뒤 몇 칸을 건너뛰는 유형 (퇴사·외주수익, 구간 스케줄링, 최대 수익/최소 비용). "최단 몇 번?" 아님.
related_problems: [14501]
---

# take-or-skip → 1D DP (선형 구간 스케줄링)

## 언제 쓰나
날/구간을 하나씩 보며 **이번 걸 한다(수익 +p, `t`칸 점유 후 `day+t`로 점프) / 안 한다(`day+1`로)** 두 갈래.
겹치지 않는 부분집합의 값 최대화. 퇴사(14501)·외주수익이 전형.

## 코드 — 뒤에서 채우는 DP (O(N), 재귀·재귀제한 불필요)
~~~python
def solve(N, works):            # works[day] = (t, p), day는 0-index
    dp = [0] * (N + 1)          # dp[d] = d일부터 얻는 최대 수익, dp[N]=0
    for day in range(N - 1, -1, -1):
        t, p = works[day]
        dp[day] = dp[day + 1]                        # 안 함
        if day + t <= N:                             # 휴가 안에 끝나면
            dp[day] = max(dp[day], p + dp[day + t])  # 함
    return dp[0]
~~~
백트래킹 동치: `bt(day)` = skip `bt(day+1)` + (fit면) take `p+bt(day+t)`, base `day==N`→0.
단 백트래킹은 **O(2^N)** (실측 N=25 ~8s) — N 상한 크면 반드시 DP.

## 함정
- **0-index 경계는 `day+t <= N`** (`< N` 아님). `day`부터 `t`칸 점유 = `[day, day+t-1]`,
  마지막 점유일 `day+t-1 <= N-1` ⟺ `day+t <= N`. **`day+t`는 인덱스가 아니라 "끝난 다음 첫 빈 날"** — `N`이면 딱 맞게 끝난 것이라 OK, `>N`만 초과.
- **베이스 케이스 `day==N`은 조건과 무관하게 무조건 종료.** 백트래킹에서 `return`을 "best 갱신될 때만" 안쪽 `if`에 두면, 갱신 안 될 때 `works[N]` 접근 → IndexError.
- 스킵은 `day+1` **한 칸**. `for d in range(t)`로 여러 칸 건너뛰려 하면 `d=0`에서 자기자신 재호출(무한재귀) + 중복 열거. 나머지 스킵은 재귀/DP가 알아서 전개.

## 관련 개념
- [03-backtracking.md](03-backtracking.md) — 선택/미선택 패턴 B, 상계 컷
