# ClickHouse 학습 노트

개념·원리를 정리해 축적하는 공간. 특히 **시스템·자원 관점의 통찰**을 중점적으로 남긴다.

| # | 노트 | 내용 | 상태 |
| --- | --- | --- | --- |
| 01 | [자원 모델](./01-resource-model.md) | 집계·조인 메모리는 ClickHouse 파드에서 / 카디널리티 / 공유 자원 영향 범위 | ✅ |
| 02 | [데이터가 쌓일수록 느려진다면](./02-why-slow-over-time.md) | skip 설계: 정렬키·파티셔닝·TTL·사전집계 | ⚠️ 검증 예정 |
| 03 | [왜 빠른가](./03-index-and-partitioning.md) | 카디널리티·희소 인덱스·블록 스킵·파티션 프루닝 | ✅ |
| 04 | [실측: 컬럼 지향·압축](./04-columnar-measured.md) | 1천만 행으로 컬럼별 저장/압축/읽기량 측정 | ✅ 실측 |
| 05 | [소비자 관점: 쿼리 비용](./05-consumer-query-cost.md) | 블록 스킵 실측, 정렬키 아닌 쿼리, SELECT * 안티패턴 | ✅ 실측 |
| 06 | [ORDER BY 설계](./06-order-by-design.md) | 복합키 leftmost prefix, 전체 컬럼 키의 비용 | ✅ |
| 07 | [파트와 병합](./07-parts-and-merges.md) | INSERT=새 파트, 백그라운드 병합, 파트명 해독, 과파티셔닝 함정 | ✅ |
| 08 | [웹 로그 스키마 설계·검증](./08-weblog-schema-and-verify.md) | 직접 설계한 web_logs + 목표 쿼리 EXPLAIN 검증 (B 트레이드오프 실증) | ✅ 실측 |
| 09 | [분석 쿼리](./09-analytical-queries.md) | 시간버킷·countIf·분위수, 카디널리티별 GROUP BY 메모리(압축≠그룹메모리) | ✅ 실측 |
| 10 | [Materialized View](./10-materialized-view.md) | 적재 시 자동 사전집계, SummingMergeTree, 라이브 트리거 실증 | ✅ 실측 |
