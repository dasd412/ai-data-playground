"""ClickHouse를 Python에서 쓰기 — clickhouse-connect 기본.

실행: .venv/bin/python clickhouse/python/query_basics.py
"""
from collections.abc import Sequence

import clickhouse_connect
from datetime import datetime
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.query import QueryResult


def get_client():
    # HTTP 8123으로 접속 (네이티브 9000 아님). 첫날 포트 얘기 그대로.
    return clickhouse_connect.get_client(
        host="localhost",
        port=8123,
        username="playground",
        password="playground",
    )

def count_by_status(client:Client,status_param:int)->int:
    # status를 인자로 받어서 개수 반환
    result=client.query(
        "SELECT count() FROM web_logs WHERE status ={status_param:UInt16}",
        parameters={"status_param":status_param},
    )

    return result.result_rows[0][0]

def insert_logs(client:Client,data:Sequence):
    client.insert(
        "web_logs",
        data,
        column_names=[
            "event_time","ip","method","path",
            "status","bytes","duration_ms","user_agent"
        ],
    )

def main():
    client = get_client()

    rows = [
        # event_time,        ip,          method, path,        status, bytes, duration_ms, user_agent
        [datetime.now(), "9.9.9.9", "GET", "/api/test", 200, 123, 10, "py-client"],
        [datetime.now(), "9.9.9.8", "POST", "/login", 500, 0, 250, "py-client"],
        [datetime.now(), "9.9.9.7", "GET", "/health", 200, 88, 5, "py-client"],
    ]

    # 쿼리: 시간대별 요청 수 + 500 에러 수.
    # 서버에서 집계해서 "작은 결과만" 받는다 (notes/05 안티패턴 회피).
    result = client.query(
        """
        SELECT toStartOfHour(event_time) AS hour,
               count()               AS reqs,
               countIf(status = 500) AS errors
        FROM web_logs
        GROUP BY hour
        ORDER BY hour
        LIMIT 5
        """
    )

    print("columns:", result.column_names)
    for row in result.result_rows:
        print(row)

    before = count_by_status(client, 200)
    insert_logs(client, rows)
    after = count_by_status(client, 200)
    print(f"200 개수: {before} → {after}")  # 3건 중 200이 2개니까 +2


if __name__ == "__main__":
    main()
