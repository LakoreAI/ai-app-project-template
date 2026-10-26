from abc import ABC, abstractmethod


class DataSource(ABC):
    """A backing store (Postgres, Milvus, ...). Services receive one or more of these."""

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def ping(self) -> None:
        """Raise if the datasource is unreachable."""
