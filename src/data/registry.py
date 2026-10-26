from src.config import settings
from src.data.base import DataSource
from src.data.milvus import MilvusSource
from src.data.postgres import PostgresSource


def build_datasources() -> dict[str, DataSource]:
    """Create the datasources that are configured in the environment (none, one or both)."""
    sources: dict[str, DataSource] = {}
    if settings.postgres_dsn:
        sources["postgres"] = PostgresSource(settings.postgres_dsn)
    if settings.milvus_uri:
        sources["milvus"] = MilvusSource(settings.milvus_uri)
    return sources
