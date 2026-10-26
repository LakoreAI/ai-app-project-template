from src.config import settings
from src.data.base import DataSource


class PostgresSource(DataSource):
    def __init__(self, dsn: str = settings.postgres_dsn) -> None:
        self.dsn = dsn
        self.conn = None

    def connect(self) -> None:
        import psycopg  # optional dependency: uv add psycopg[binary]

        self.conn = psycopg.connect(self.dsn)

    def ping(self) -> None:
        if self.conn is None:
            raise RuntimeError("not connected")
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1")

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None
