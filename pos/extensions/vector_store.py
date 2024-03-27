import psycopg2
from llama_index.vector_stores.postgres import PGVectorStore

db_name = "vector_db"
host = "localhost"
password = "password"
port = "5432"
user = "hello_flask"


def init_vector_store():
    # conn = psycopg2.connect(connection_string)
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
