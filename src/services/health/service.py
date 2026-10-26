from src.modules.health_module import HealthModule


class HealthService:
    def __init__(self, health: HealthModule | None = None) -> None:
        self.health = health or HealthModule()

    def status(self) -> dict:
        return self.health.check()
