"""Demo Replay Script for Replayable Error Store (Tuần 2 deliverable).

Usage:
    python3 scripts/replay_error_run.py --candidate ERR-001
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import json
from src.error_store import ReplayableErrorStore
from src.error_parser import LeanErrorParser, ErrorCategory, RepairRoute


def mock_rule_repair_strategy(code: str, diag: dict) -> dict:
    """A sample deterministic rule-based repair function."""
    cat, route = LeanErrorParser.classify_message(diag.get("message", ""))

    # Example 1: Fix missing colon in syntax
    if "expected ':'" in diag.get("message", "") and " n > 0" in code:
        repaired = code.replace(" n > 0", " : n > 0")
        return {"success": True, "repaired_code": repaired, "strategy": "rule_insert_colon"}

    # Example 2: Fix missing import by prepending Mathlib import
    if "Real" in code and cat == ErrorCategory.MISSING_IMPORT:
        repaired = "import Mathlib.Data.Real.Basic\n" + code
        return {"success": True, "repaired_code": repaired, "strategy": "rule_add_mathlib_import"}

    # Fallback: cannot fix with simple rule
    return {"success": False, "repaired_code": None, "strategy": "rule_no_match"}


def main():
    parser = argparse.ArgumentParser(description="Replay Error Candidates")
    parser.add_argument("--data", default="data_sample/error_dataset_50.json", help="Path to error dataset")
    parser.add_argument("--candidate", default=None, help="Specific candidate ID to replay (optional)")
    args = parser.parse_args()

    store = ReplayableErrorStore()
    total_loaded = store.load_from_dataset(args.data)
    print(f"[STORE] Loaded {total_loaded} error records into Replayable Error Store.")

    if args.candidate:
        targets = [args.candidate]
    else:
        # Pick 3 diverse candidates for demonstration
        targets = ["ERR-001", "ERR-009", "ERR-025"]

    print(f"[REPLAY] Executing replay on {len(targets)} candidates...\n")
    for cid in targets:
        rec = store.get_record(cid)
        if not rec:
            print(f"❌ Candidate {cid} not found.")
            continue

        res = store.replay_candidate(cid, mock_rule_repair_strategy)
        print(f"--- Replay Result: {cid} ---")
        print(f"Problem:      {rec.statement_natural}")
        print(f"Input Code:   {rec.candidate_code}")
        print(f"Error Msg:    {rec.compiler_diagnostics[0].get('message')}")
        print(f"Status:       {res['status']}")
        print(f"Success:      {res['replay_entry']['success']}")
        print(f"Strategy:     {res['replay_entry']['strategy']}")
        if res['replay_entry']['repaired_code']:
            print(f"Repaired:     {res['replay_entry']['repaired_code']}")
        print(f"Duration:     {res['replay_entry']['duration_ms']}ms\n")

    # Persist updated store with replay histories
    out_store_path = "results/raw/replayable_store_snapshot_w2.json"
    store.save_store(out_store_path)
    print(f"[OK] Replay session completed. Store snapshot saved to: {out_store_path}")


if __name__ == "__main__":
    main()
