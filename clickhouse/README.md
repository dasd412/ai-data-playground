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
- [ ] 3단계: MergeTree 엔진 (정렬키/파티션/파트·병합)
- [ ] 4단계: 웹 접속 로그 적재
- [ ] 5단계: 분석 쿼리 (집계·시간버킷)
- [ ] 6단계: Materialized View
- [ ] 7단계: Python(clickhouse-connect) 적재·쿼리
