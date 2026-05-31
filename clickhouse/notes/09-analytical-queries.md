# 09. 분석 쿼리 — 집계·시간버킷·카디널리티 메모리

> `web_logs` 500만 행 위에서 실측. 소비자(쿼리 짜는 쪽)의 핵심.

## 시간버킷 + 조건부 집계

```sql
SELECT toStartOfHour(event_time) AS hour,
       count()               AS reqs,
       countIf(status = 500) AS errors
FROM web_logs GROUP BY hour ORDER BY hour;
```

- `toStartOfHour` = 시각을 시간 단위로 내림(버킷). 분=`toStartOfMinute`, 일=`toDate`/`toStartOfDay`.
- `countIf(조건)` = 조건부 카운트. 한 번 스캔으로 전체 수 + 에러 수 동시에.

## ⭐ 카디널리티 = GROUP BY 메모리 (실측)

같은 500만 행을 스캔해도 **그룹 수**에 따라 Peak memory가 극적으로 다름:

| GROUP BY | 그룹(distinct) 수 | Peak memory |
| --- | --- | --- |
| `status` | 4 | 3.2 MiB |
| `ip` | 57,088 | 33 MiB |
| `event_time` | 604,655 | 98 MiB |

- 그룹마다 RAM에 **누적 카운터 한 칸**(해시테이블) → 그룹 많을수록 메모리 ↑.
- [[01-resource-model]]의 "집계 메모리 ∝ 그룹 수"를 숫자로 확인.

## ⚠️ 압축 ≠ GROUP BY 메모리 (헷갈리기 쉬움)

둘 다 "중복 많으면 작다"라 착각하기 쉽지만 **메커니즘이 다름**:

| | 압축 ([[04-columnar-measured]]) | GROUP BY 메모리 ([[01-resource-model]]) |
| --- | --- | --- |
| 단계 | 디스크 **저장**할 때 | 쿼리 중 **RAM 집계**할 때 |
| 좌우 | 중복·정렬·엔트로피 | **그룹(distinct) 수** |
| 지표 | 디스크 크기, Processed(IO) | **Peak memory** |

- `GROUP BY status`가 가벼운 건 압축이 잘돼서가 아니라 **묶을 그룹이 4개뿐**이라서.

## 분위수 (p95)

```sql
SELECT path, round(avg(duration_ms)) AS avg_ms, quantile(0.95)(duration_ms) AS p95_ms
FROM web_logs GROUP BY path ORDER BY p95_ms DESC;
```

- `quantile(0.95)(col)` = 상위 5% 경계. avg는 이상치에 둔감, p95/p99는 "느린 꼬리"를 잡음 → SLA·알람에 사용.

## 실전 교훈 (온프레미스 제약)

- 수십억 행에서 `GROUP BY ip`/`user_id`(고카디) → 해시테이블 폭발 → 파드 메모리 초과로 쿼리 실패 + 공유 파드면 남까지 영향([[01-resource-model]] blast radius).
- **소비자 습관: "이 GROUP BY가 몇 그룹 만들까?"를 항상 가늠.** 시간버킷으로 묶으면 그룹이 확 줄어 안전.
