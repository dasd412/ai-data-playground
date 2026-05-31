# 12. 실무용 요약집 (소비자/백엔드 치트시트)

> 한 장짜리 레퍼런스. 상세는 각 노트 링크 참고.

## 쿼리가 쌀 때 vs 비쌀 때

- ✅ `ORDER BY` **앞쪽 컬럼**으로 필터 → 블록 스킵 (쌈). leftmost prefix. ([[06-order-by-design]])
- ❌ 정렬키 아닌 컬럼 필터 → 풀스캔. 데이터 크면 느림. ([[05-consumer-query-cost]])
- 👉 **쿼리 전에 테이블 `ORDER BY`부터 확인**. `EXPLAIN indexes=1`로 `Granules N/M` 보면 스킵 됐는지 앎.

## GROUP BY 메모리

- 메모리 ∝ **distinct 그룹 수** (읽는 행 수 아님). ([[09-analytical-queries]])
- ❌ 고카디(`user_id`, `ip`) GROUP BY → 해시테이블 폭발 → 파드 메모리 초과.
- ✅ 시간버킷(`toStartOfHour`)·저카디 컬럼으로 묶어 그룹 수 줄이기.
- ⚠️ 압축(디스크) ≠ GROUP BY 메모리(RAM). 다른 메커니즘.

## 안티패턴 (하지 말 것)

- ❌ `SELECT *` — 컬럼 지향 이점 버림.
- ❌ `LIMIT` 없이 대량 행 fetch — 클라이언트(백엔드) OOM.
- ❌ 행 단위 INSERT — 파트 폭발(`too many parts`). ([[07-parts-and-merges]])

## 적재 (생산자)

- **배치로** (한 INSERT에 수천~수만 행). 파트는 INSERT 단위.
- 실시간 로그도 버퍼에 모았다 한 번에.

## 스키마 설계 (생산 시)

- **타입**: 저카디 → `LowCardinality(String)`, IP → `IPv4`, 작은 수 → `UInt16` 등. ([[04-columnar-measured]])
- **ORDER BY**: 자주 거르는/저카디 컬럼을 앞, **가장 흔한 쿼리**에 맞춰. 키는 짧게.
- **PARTITION BY**: 데이터 **수명 관리용**(보통 월 단위 시간), 쿼리 속도용 아님. ([[03-index-and-partitioning]])
- 자주 쓰는 집계 → **Materialized View** 사전집계. ([[10-materialized-view]])

## 자원/운영 (온프레미스 제약)

- 무거운 쿼리는 **공유 ClickHouse 파드 메모리 독식** → 다른 소비자까지 영향(blast radius). ([[01-resource-model]])
- `max_memory_usage` 초과 시 쿼리 실패. "내 쿼리가 메모리 얼마 쓸지" 가늠하는 감각이 핵심.

## Python (clickhouse-connect)

- HTTP **8123**, `get_client(host, port, username, password)`.
- 읽기: 파라미터 바인딩 `{name:Type}` (f-string 금지 — 인젝션). 서버에서 집계해 작은 결과만.
- 쓰기: `client.insert(table, data, column_names)` 배치. ([[11-python-client]])

## 진단 도구 (system 테이블)

- `EXPLAIN indexes = 1` → 블록 스킵(`Granules N/M`) 확인.
- `system.parts` → 파트 수/행/크기/level.
- `system.columns` → 컬럼별 압축률.
- 쿼리 끝의 `Processed rows` / `Peak memory` → 비용 즉시 확인.
