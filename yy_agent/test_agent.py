import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("agent", Path(__file__).with_name("agent.py"))
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)

class AgentTests(unittest.TestCase):
    def test_links_accept_only_official_bounties(self):
        p = agent.Links()
        p.feed('<a href="/bounty/chess-01">yes</a><a href="https://evil.test/bounty/no">no</a><a href="/bounty/../bad">bad</a>')
        self.assertEqual(p.slugs, {"chess-01"})
    def test_unknown_fees_are_blocked(self):
        self.assertTrue(agent.free_entry({"entry_fee": None}))
        self.assertFalse(agent.free_entry({"entry_fee": {"amount": "0.50"}}))
        self.assertFalse(agent.free_entry({"entry_fee": "unknown"}))
    def test_slug_traversal_blocked(self):
        with self.assertRaises(ValueError):
            agent.requirements("../../secret")
    def test_external_url_blocked_before_request(self):
        with self.assertRaises(ValueError):
            agent.fetch("https://evil.test/")
    def test_paid_run_never_starts_executor(self):
        with patch.object(agent, "requirements", return_value={"competition":{"status":"open"}, "entry_fee":1}), patch.object(agent.subprocess, "Popen") as process:
            with self.assertRaises(ValueError):
                agent.run_task("test-01", Path("/unused"), 10)
            process.assert_not_called()
    def test_closed_run_blocked(self):
        with patch.object(agent, "requirements", return_value={"competition":{"status":"closed"}}):
            with self.assertRaises(ValueError):
                agent.run_task("test-01", Path("/unused"), 10)
    def test_report_does_not_mean_verified(self):
        class FakeProcess:
            returncode = 0
            def __init__(self, *args, **kwargs):
                work = Path(args[0][args[0].index("-C") + 1])
                (work / "result.json").write_text('{"status":"submitted","submission_id":"claimed"}')
            def communicate(self, *args, **kwargs): return (None, None)
            def poll(self): return 0
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            req = {"competition":{"status":"open"}, "entry_fee":None}
            with patch.object(agent, "requirements", return_value=req), patch.object(agent.shutil, "which", return_value="/codex"), patch.object(agent.subprocess, "run"), patch.object(agent.subprocess, "Popen", FakeProcess):
                state = agent.run_task("test-01", root, 10)
            self.assertFalse(state["submission_verified"])
            self.assertEqual(state["state"], "needs_review")
            self.assertFalse((root / ".running").exists())
    def test_lock_blocks_duplicate_runs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".running").write_text("")
            with patch.object(agent, "requirements", return_value={"competition":{"status":"open"}}), patch.object(agent.shutil, "which", return_value="/codex"):
                with self.assertRaises(RuntimeError):
                    agent.run_task("test-01", root, 10)
            self.assertTrue((root / ".running").exists())
    def test_atomic_state(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "state.json"
            agent.save(p, {"state":"blocked"})
            self.assertEqual(agent.json.loads(p.read_text()), {"state":"blocked"})
            self.assertFalse(p.with_suffix(".tmp").exists())

if __name__ == "__main__":
    unittest.main()
