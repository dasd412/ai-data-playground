# ai-data-playground

데이터/AI 도구의 사용 원리와 흐름을 직접 체득하기 위한 개인 학습용 리포지토리.

> 학습 방식과 AI 활용 방침은 [CLAUDE.md](./CLAUDE.md) 참고.

## 구조

| 디렉터리 | 내용 |
| --- | --- |
| `langgraph/` | LangGraph 학습 |
| `vector_db/` | Vector DB 학습 |
| `graph_db/` | Graph DB 학습 |
| `clickhouse/` | ClickHouse 학습 |
| `infra/` | 로컬 인프라 (docker-compose 등) |

## 환경

- Python 3.12 (`.venv`)
- 의존성: `requirements.txt`

```bash
source .venv/bin/activate
pip install -r requirements.txt
```
