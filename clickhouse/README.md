# ClickHouse

ClickHouse 학습 노트 및 실습 코드.

- 공식 문서: https://clickhouse.com/docs
- 📓 개념 정리: [notes/](./notes/)

## 로컬 기동 / 종료

```bash
# 기동
docker compose -f infra/clickhouse/docker-compose.yml up -d
# 종료 (데이터 유지)
docker compose -f infra/clickhouse/docker-compose.yml stop
# 완전 삭제 (데이터까지 날림)
docker compose -f infra/clickhouse/docker-compose.yml down -v
```

## 접속

| 인터페이스 | 포트 | 접속 방법 |
| --- | --- | --- |
| 네이티브 TCP | 9000 | `docker exec -it ch-playground clickhouse-client --user playground --password playground` |
| HTTP | 8123 | `curl -u playground:playground "http://localhost:8123/?query=SELECT version()"` |

- 학습용 계정: `playground` / `playground`

## 진행 로그

- [x] 1단계: Docker 기동 + 접속 확인 (HTTP 8123 / 네이티브 9000)
- [x] 2단계: 행 vs 컬럼 저장 차이 눈으로 확인 (압축률·읽기량 실측 → notes/04)
- [x] 3단계: MergeTree 엔진 — 블록 스킵(notes/05), ORDER BY 설계(notes/06), 파트·병합(notes/07)
- [x] 4단계: 웹 접속 로그 스키마 설계·적재 (web_logs 5M행, seed_web_logs.sql) → notes/08
- [x] 5단계: 분석 쿼리 (시간버킷·countIf·분위수, 카디널리티별 GROUP BY 메모리 실측) → notes/09
- [ ] 6단계: Materialized View (적재 시 자동 사전집계)
- [ ] 7단계: Python(clickhouse-connect) 적재·쿼리 — 백엔드에서 소비

### 후보 (선택, 원래 동기와 직결)

- [ ] 8단계: TTL / 데이터 수명 — "5년치 느려짐" 함정의 나머지 반쪽 (notes/02 마무리)
- [ ] 9단계: 분산 (샤딩·복제) — 온프레미스 k8s 멀티노드 현실
- [ ] 10단계: 실시간 적재 패턴 (Kafka 엔진 / Buffer 등) — "실시간·알람" 관심사
- [ ] 11단계: ScyllaDB vs ClickHouse 전환 의사결정 (캡스톤)
