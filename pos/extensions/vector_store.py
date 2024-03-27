import psycopg2
from llama_index.vector_stores.postgres import PGVectorStore

from pos.config import DefaultConfig

db_name = DefaultConfig.PG_DB_NAME
host = DefaultConfig.PG_HOST
password = DefaultConfig.PG_PASSWORD
port = DefaultConfig.PG_PORT
user = DefaultConfig.PG_USER


def init_vector_store():
    conn = psycopg2.connect(
        dbname="postgres",
        host=host,
        password=password,
        port=port,
        user=user,
    )
    conn.autocommit = True

    with conn.cursor() as c:
        c.execute(f"DROP DATABASE IF EXISTS {db_name}")
        c.execute(f"CREATE DATABASE {db_name}")


def get_vector_store() -> PGVectorStore:
    vector_store = PGVectorStore.from_params(
        database=db_name,
        host=host,
        password=password,
        port=port,
        user=user,
        table_name="llama2_paper",
        embed_dim=384,  # openai embedding dimension
    )
    return vector_store
