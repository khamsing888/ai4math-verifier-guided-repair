"""Unit tests for ReplayableErrorStore (Tuần 2 deliverable)."""

import os
import tempfile
import unittest
from src.error_store import CandidateErrorRecord, ReplayableErrorStore


class TestReplayableErrorStore(unittest.TestCase):
    def setUp(self):
        self.store = ReplayableErrorStore()

    def test_add_and_deduplicate(self):
        rec1 = CandidateErrorRecord(
            candidate_id="ERR-TEST-1",
            problem_id="PROB-1",
            statement_natural="Test problem",
            candidate_code="theorem t1 : 1 = 1 := by rfl",
            compiler_diagnostics=[]
        )
        # Duplicate with same code
        rec2 = CandidateErrorRecord(
            candidate_id="ERR-TEST-2",
            problem_id="PROB-1",
            statement_natural="Test problem duplicate",
            candidate_code="theorem t1 : 1 = 1 := by rfl",
            compiler_diagnostics=[]
        )
        self.assertTrue(self.store.add_record(rec1))
        self.assertFalse(self.store.add_record(rec2))  # Deduplicated

    def test_load_from_sample_dataset(self):
        loaded = self.store.load_from_dataset("data_sample/error_dataset_50.json")
        self.assertEqual(loaded, 50)
        train_records = self.store.list_records(split="train")
        holdout_records = self.store.list_records(split="holdout")
        self.assertGreater(len(train_records), 0)
        self.assertGreater(len(holdout_records), 0)
        self.assertEqual(len(train_records) + len(holdout_records), 50)

    def test_replay_candidate(self):
        rec = CandidateErrorRecord(
            candidate_id="ERR-REPLAY-1",
            problem_id="PROB-REPLAY",
            statement_natural="Need colon",
            candidate_code="theorem foo (n : Nat) n > 0",
            compiler_diagnostics=[{"severity": "error", "message": "expected ':'", "line": 1, "column": 23}]
        )
        self.store.add_record(rec)

        def mock_fix(code, diag):
            return {"success": True, "repaired_code": code.replace(" n > 0", " : n > 0"), "strategy": "rule_colon"}

        result = self.store.replay_candidate("ERR-REPLAY-1", mock_fix)
        self.assertEqual(result["status"], "REPAIRED")
        self.assertTrue(result["replay_entry"]["success"])
        self.assertEqual(len(self.store.get_record("ERR-REPLAY-1").repair_history), 1)

    def test_save_and_reload(self):
        self.store.load_from_dataset("data_sample/error_dataset_50.json")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            self.store.save_store(tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 100)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
