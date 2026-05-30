# 08. 웹 로그 스키마 설계 & 실측 검증

> 직접 설계한 `web_logs` 테이블에 500만 행 적재 후, 목표 쿼리로 설계를 검증.
> 시드: `clickhouse/sql/seed_web_logs.sql`

## 설계

```sql
CREATE TABLE web_logs (
    event_time DateTime, ip IPv4,
    method LowCardinality(String),   -- 저카디 → 압축 굿
    path String, status UInt16,
    bytes UInt32, duration_ms UInt64,
    user_agent String                -- 고카디 → LowCardinality 일부러 안 씀
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)    -- 수명 관리(월 단위), 쿼리속도 아님
ORDER BY (event_time, status);       -- B안: 시간범위 우선
```

- 목표 쿼리: **"최근 몇 시간 내 status=500 디버깅"**.
- PARTITION = 데이터 수명 관리용(월), ORDER BY = 쿼리 속도용. 역할 분담([[03-index-and-partitioning]]).

## "테이블 ORDER BY = 디스크 저장 순서" (정렬은 쓰기 때 1회)

- 데이터는 쓰는 순간 `(event_time, status)`로 **이미 정렬되어 디스크에 저장**됨.
- 쿼리 시엔 **정렬 안 함.** ① 인덱스로 블록 **스킵** + ② 남은 행 **필터(값 비교)**.
- 쿼리의 `ORDER BY` 절(결과 정렬)과 테이블 `ORDER BY`(저장 순서)는 다른 개념.

## 실측 검증 — `WHERE status=500 AND event_time >= now()-3h`

```
Processed 101.18k rows / 5M   (시간 스킵 성공, ~2%)
count = 4302,  Elapsed 0.011s
```

EXPLAIN indexes=1:

| 인덱스 단계 | granules | 비고 |
| --- | --- | --- |
| Min-Max / Partition | 612/612 | 데이터가 다 202605 → 못 거름(파티션 1개) |
| **PrimaryKey** (event_time, status) | **14/612** | event_time 범위로 블록 스킵 (주역) |

- `event_time`이 첫 키 → "최근 3시간"이 612→14 블록으로 스킵. ✅ 설계 의도대로.
- `status`는 2번째 키 → 블록 스킵엔 거의 안 쓰임. 14블록(101k행) 읽어 4302개 발견 = **답의 ~23배 읽음.**

## 결론: B 트레이드오프 실증

- B `(event_time, status)`: 시간범위 쿼리에 최적. status는 필터로 처리.
- A `(status, event_time)`였다면 500으로 직행해 더 적게 읽었을 것 (희귀값 디버깅 최적).
- 단 시간으로 이미 101k로 좁혀 0.011s → 실용상 B로 충분. **무엇을 첫 키로 두느냐 = 어떤 쿼리를 최적화하느냐.** ([[06-order-by-design]])
