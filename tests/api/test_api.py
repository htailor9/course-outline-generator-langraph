"""API end-to-end with FakeLLM: async jobs, artifacts, guard, errors, traversal."""

import time

import pytest
from fastapi.testclient import TestClient

from outline.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def runs_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTLINE_RUNS_DIR", str(tmp_path))
    return tmp_path


def _wait_done(run_id, timeout=60):
    for _ in range(timeout * 10):
        r = client.get(f"/v1/outline/runs/{run_id}")
        if r.status_code == 200 and r.json()["status"] in ("done", "failed"):
            return r.json()
        time.sleep(0.1)
    raise AssertionError("job did not finish")


def _generate(input43):
    r = client.post("/v1/outline/generate", json={**input43, "provider": "fake"})
    assert r.status_code == 202
    run_id = r.json()["run_id"]
    assert _wait_done(run_id)["status"] == "done"
    return run_id


def test_generate_and_fetch_artifacts(input43):
    run_id = _generate(input43)
    status = client.get(f"/v1/outline/runs/{run_id}").json()
    assert status["report"]["validation"] == [] and status["report"]["n_los"] == 43
    outline = client.get(f"/v1/outline/runs/{run_id}/outline")
    assert outline.status_code == 200 and outline.json()["label"] == "project"
    assert client.get(f"/v1/outline/runs/{run_id}/analysis").status_code == 200
    assert client.get(f"/v1/outline/runs/{run_id}/regeneration").status_code == 404


def test_generate_rejects_bad_prompt_before_queueing(input43):
    r = client.post(
        "/v1/outline/generate",
        json={**input43, "provider": "fake", "user_prompt": "buy pizza tomorrow"},
    )
    assert r.status_code == 400 and "unrelated" in r.json()["detail"]


def test_regenerate_all_scopes(input43):
    base = _generate(input43)
    for body in ({"unit": "all"}, {"unit": "1"}, {"unit": "1", "lesson": "1"}):
        r = client.post(
            "/v1/outline/regenerate",
            json={"baseline_run_id": base, "provider": "fake", **body},
        )
        assert r.status_code == 202
        st = _wait_done(r.json()["run_id"])
        assert st["status"] == "done", st
        rid = r.json()["run_id"]
        regen_md = client.get(f"/v1/outline/runs/{rid}/regeneration")
        # ticket id resolves via registry (run_dir known even though folder name differs)
        assert regen_md.status_code == 200


def test_regenerate_bad_selection_fails_with_message(input43):
    base = _generate(input43)
    r = client.post(
        "/v1/outline/regenerate",
        json={"baseline_run_id": base, "unit": "99", "provider": "fake"},
    )
    st = _wait_done(r.json()["run_id"])
    assert st["status"] == "failed" and "out of range" in st["error"]


def test_regenerate_unknown_baseline_404():
    r = client.post(
        "/v1/outline/regenerate", json={"baseline_run_id": "nope", "unit": "all"}
    )
    assert r.status_code == 404


def test_lesson_with_all_rejected(input43):
    base = _generate(input43)
    r = client.post(
        "/v1/outline/regenerate",
        json={
            "baseline_run_id": base,
            "unit": "all",
            "lesson": "1",
            "provider": "fake",
        },
    )
    assert r.status_code == 422


def test_list_runs(input43):
    run_id = _generate(input43)
    runs = client.get("/v1/outline/runs").json()
    assert any(r["run_id"] == run_id and r.get("valid") for r in runs)


def test_traversal_blocked():
    assert client.get("/v1/outline/runs/..%2F..%2Fetc/outline").status_code in (
        404,
        422,
    )


def test_health_and_swagger():
    assert client.get("/healthz").json() == {"ok": True}
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/docs").status_code == 200
