"""Job registry: lifecycle, failure capture, restart fallback."""

import asyncio

from outline.jobs import JobRegistry


async def test_job_success_and_failure(tmp_path):
    reg = JobRegistry()

    async def ok():
        return (tmp_path / "r1", {"n_los": 1})

    async def boom():
        raise RuntimeError("provider exploded")

    jid = reg.submit("r1", ok())
    jid2 = reg.submit("r2", boom())
    for _ in range(100):
        await asyncio.sleep(0.01)
        if (
            reg.status(jid)["status"] == "done"
            and reg.status(jid2)["status"] == "failed"
        ):
            break
    assert reg.status(jid)["status"] == "done"
    assert reg.status(jid)["run_dir"] == str(tmp_path / "r1")
    assert reg.status(jid)["report"] == {"n_los": 1}
    assert (
        reg.status(jid2)["status"] == "failed"
        and "exploded" in reg.status(jid2)["error"]
    )


async def test_systemexit_message_captured(tmp_path):
    reg = JobRegistry()

    async def guard():
        raise SystemExit("--unit 99 out of range; course has 4 content units")

    reg.submit("g1", guard())
    for _ in range(100):
        await asyncio.sleep(0.01)
        if reg.status("g1")["status"] == "failed":
            break
    assert "out of range" in reg.status("g1")["error"]


async def test_resolve_unknown_job_falls_back_to_folder(tmp_path):
    reg = JobRegistry()
    (tmp_path / "old-run").mkdir()
    (tmp_path / "old-run" / "report.json").write_text("{}", encoding="utf-8")
    assert reg.resolve("old-run", tmp_path)["status"] == "done"
    assert reg.resolve("nope", tmp_path)["status"] == "unknown"
