-- 웹 접속 로그 학습용 테이블 + 합성 데이터 시드
-- 실행: docker exec -i ch-playground clickhouse-client --user playground --password playground --multiquery < clickhouse/sql/seed_web_logs.sql

CREATE TABLE IF NOT EXISTS web_logs
(
    event_time  DateTime,
    ip          IPv4,
    method      LowCardinality(String),
    path        String,
    status      UInt16,
    bytes       UInt32,
    duration_ms UInt64,
    user_agent  String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, status);

-- 500만 행을 INSERT 한 번(=배치)으로. 최근 7일에 분포, status=500은 5%로 희귀.
INSERT INTO web_logs
SELECT
    now() - toIntervalSecond(rand() % 604800) AS event_time,
    toIPv4(concat(toString((rand() % 223) + 1), '.', toString(rand() % 256), '.', toString(rand() % 256), '.', toString(rand() % 256))) AS ip,
    ['GET', 'GET', 'GET', 'POST', 'PUT', 'DELETE'][(rand() % 6) + 1] AS method,
    ['/api/users', '/api/orders', '/login', '/health', '/api/products', '/static/app.js'][(rand() % 6) + 1] AS path,
    [200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,404,404,304,500][(rand() % 20) + 1] AS status,
    rand() % 50000 AS bytes,
    rand() % 2000 AS duration_ms,
    ['Mozilla/5.0 (Windows NT 10.0)', 'Mozilla/5.0 (Macintosh)', 'curl/8.4.0', 'PostmanRuntime/7.36', 'python-requests/2.31'][(rand() % 5) + 1] AS user_agent
FROM numbers(5000000);
