# 11. Python에서 ClickHouse 쓰기 (clickhouse-connect)

> 백엔드/에이전트가 ClickHouse와 대화하는 실제 방식. 코드: `clickhouse/python/query_basics.py`

## 접속 (HTTP 8123)

```python
import clickhouse_connect
client = clickhouse_connect.get_client(
    host="localhost", port=8123,        # HTTP 인터페이스 (네이티브 9000 아님)
    username="playground", password="playground",
)
```

## 읽기 — 결과 받기

```python
result = client.query("SELECT ... GROUP BY ...")
result.result_rows     # [(값, 값), ...] 튜플 리스트 (파이썬 타입으로 변환됨: datetime, int)
result.column_names    # ('hour', 'reqs', ...)
```

## ⭐ 파라미터 바인딩 (인젝션 안전, 백엔드 필수)

```python
client.query(
    "SELECT count() FROM web_logs WHERE status = {st:UInt16}",   # 일반 문자열!
    parameters={"st": 200},
)
```

- `{이름:타입}`은 **clickhouse-connect의 서버사이드 파라미터 문법**, Python f-string 아님.
- ⚠️ f-string으로 하면: `:UInt16`를 포맷 스펙으로 오해해 깨지거나, 값을 SQL에 직접 박아 **인젝션 위험**.
- 값을 `parameters`로 따로 보내야 서버가 타입 검증하며 안전 바인딩.

## 쓰기 — 배치 적재 (황금률)

```python
client.insert(
    "web_logs",
    data,                              # [[event_time, ip, method, ...], ...] 행들의 리스트
    column_names=["event_time", "ip", "method", "path",
                  "status", "bytes", "duration_ms", "user_agent"],
)
```

- 각 행은 `column_names` **순서대로**. 타입 매칭: `event_time`=`datetime`, `ip`=`"9.9.9.9"`(IPv4 자동변환), 수치=`int`.
- 여러 행을 **한 번의 insert**로 = 파트 1개 ([[07-parts-and-merges]] 황금률). 행마다 insert 금지.

## 소비자 베스트 프랙티스 (코드로 체득)

- 읽기: 파라미터 바인딩 / 필요한 컬럼만 / **서버에서 집계**해 작은 결과만.
- 쓰기: **배치**로 묶어서.
- 대량 결과는 한 번에 받지 말고 스트리밍(`query_row_block_stream`) — [[05-consumer-query-cost]]의 `SELECT *` 안티패턴 회피.
