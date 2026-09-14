"""Replayable Error Store for Verifier-Guided Repair.

Features:
- Ingestion conforming to Data Contract v0.1
- Error persistence & indexing
- Deterministic replay execution mechanism
"""

import datetime
import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional
from src.error_parser import LeanErrorParser, ErrorCategory, RepairRoute


@dataclass
class DiagnosticItem:
    severity: str
    line: int
    column: int
    message: str


@dataclass
class CandidateErrorRecord:
    candidate_id: str
    problem_id: str
    statement_natural: str
    candidate_code: str
    compiler_diagnostics: List[Dict[str, Any]]
    split: str = "train"
    source_dataset: str = "ProofNet"
    checksum_sha256: str = ""
    created_at: str = ""
    status: str = "PENDING"  # PENDING | REPAIRED | UNREPAIRABLE
    repaired_code: Optional[str] = None
    repair_attempts: int = 0
    repair_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.checksum_sha256:
            self.checksum_sha256 = hashlib.sha256(self.candidate_code.encode("utf-8")).hexdigest()
        if not self.created_at:
            self.created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()


class ReplayableErrorStore:
    """In-memory and file-backed replayable store for candidate Lean errors."""

    def __init__(self, store_path: Optional[str] = None):
        self.store_path = store_path
        self._records: Dict[str, CandidateErrorRecord] = {}
        self._checksum_index: Dict[str, str] = {}  # checksum -> candidate_id

    def add_record(self, record: CandidateErrorRecord) -> bool:
        """Adds record to store. Returns False if duplicate checksum exists."""
        if record.checksum_sha256 in self._checksum_index:
            return False  # Deduplicated

        self._records[record.candidate_id] = record
        self._checksum_index[record.checksum_sha256] = record.candidate_id
        return True

    def get_record(self, candidate_id: str) -> Optional[CandidateErrorRecord]:
        return self._records.get(candidate_id)

    def list_records(self, split: Optional[str] = None, status: Optional[str] = None) -> List[CandidateErrorRecord]:
        res = list(self._records.values())
        if split:
            res = [r for r in res if r.split == split]
        if status:
            res = [r for r in res if r.status == status]
        return res

    def load_from_dataset(self, json_path: str) -> int:
        """Loads dataset from JSON format (e.g. data_sample/error_dataset_50.json)."""
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        loaded = 0
        for item in raw_data:
            diagnostics = [item.get("compiler_log", {})]
            rec = CandidateErrorRecord(
                candidate_id=item.get("error_id", f"ERR-{loaded:03d}"),
                problem_id=f"PROB-{item.get('error_id', loaded)}",
                statement_natural=item.get("title", "Math problem statement"),
                candidate_code=item.get("code_snippet", ""),
                compiler_diagnostics=diagnostics,
                split=item.get("split", "train"),
                source_dataset="AI4Math-Sample"
            )
            if self.add_record(rec):
                loaded += 1
        return loaded

    def save_store(self, output_path: str):
        """Saves current store state to JSON format."""
        data = [asdict(r) for r in self._records.values()]
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def replay_candidate(
        self,
        candidate_id: str,
        repair_fn: Callable[[str, Dict[str, Any]], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Replays repair action deterministically for a single candidate.

        Args:
            candidate_id: Identifier of the candidate to replay.
            repair_fn: Callable taking (code, diagnostics) and returning repair outcome.

        Returns:
            Dictionary containing replay execution logs and outcome.
        """
        record = self.get_record(candidate_id)
        if not record:
            raise KeyError(f"Candidate {candidate_id} not found in store.")

        start_time = datetime.datetime.now(datetime.timezone.utc)
        outcome = repair_fn(record.candidate_code, record.compiler_diagnostics[0] if record.compiler_diagnostics else {})
        duration_ms = (datetime.datetime.now(datetime.timezone.utc) - start_time).total_seconds() * 1000.0

        # Record replay outcome in candidate history
        replay_entry = {
            "replayed_at": start_time.isoformat(),
            "duration_ms": round(duration_ms, 2),
            "success": outcome.get("success", False),
            "repaired_code": outcome.get("repaired_code"),
            "strategy": outcome.get("strategy", "unknown")
        }
        record.repair_history.append(replay_entry)
        record.repair_attempts += 1
        if outcome.get("success"):
            record.status = "REPAIRED"
            record.repaired_code = outcome.get("repaired_code")

        return {
            "candidate_id": candidate_id,
            "status": record.status,
            "replay_entry": replay_entry
        }
