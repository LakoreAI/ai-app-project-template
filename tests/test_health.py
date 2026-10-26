from src.modules.health_module import HealthModule


def test_health_without_datasources(client):
    assert client.get("/health").json() == {"status": "ok", "checks": {}}


def test_health_module_reports_failing_probe():
    def boom():
        raise RuntimeError("down")

    m = HealthModule()
    m.register("good", lambda: None)
    m.register("bad", boom)
    result = m.check()
    assert result["status"] == "degraded"
    assert result["checks"]["good"]["ok"] is True
    assert result["checks"]["bad"] == {"ok": False, "detail": "down"}
