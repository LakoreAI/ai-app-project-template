from src.config import settings
from src.data.base import DataSource


class MilvusSource(DataSource):
    def __init__(self, uri: str = settings.milvus_uri) -> None:
        self.uri = uri
        self.client = None

    def connect(self) -> None:
        from pymilvus import MilvusClient  # optional dependency: uv add pymilvus

        self.client = MilvusClient(uri=self.uri)

    def ping(self) -> None:
        if self.client is None:
            raise RuntimeError("not connected")
        self.client.list_collections()

    def close(self) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None
