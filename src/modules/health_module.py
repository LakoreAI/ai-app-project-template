from collections.abc import Callable

from src.modules.base import BaseModules


class HealthModule(BaseModules):
    """Registry of health probes (datasources, LLM providers, external APIs, ...).

    A probe is a callable that raises if its target is unhealthy,
    e.g. `module.register("postgres", postgres_source.ping)`.
    """

    def __init__(self) -> None:
        super().__init__()
        self.probes: dict[str, Callable[[], None]] = {}

    def register(self, name: str, probe: Callable[[], None]) -> None:
        self.probes[name] = probe

    def check(self) -> dict:
        checks = {}
        for name, probe in self.probes.items():
            try:
                probe()
                checks[name] = {"ok": True, "detail": ""}
            except Exception as e:
                checks[name] = {"ok": False, "detail": str(e)}
        ok = all(c["ok"] for c in checks.values())
        return {"status": "ok" if ok else "degraded", "checks": checks}
