"""Structured Lean 4 Compiler Error Parser & Taxonomy Classifier."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ErrorCategory(str, Enum):
    """Normalized Lean 4 error categories."""
    SYNTAX_ERROR = "SYN_01"
    MISSING_IMPORT = "IMP_02"
    UNKNOWN_IDENTIFIER = "ID_03"
    TYPE_MISMATCH = "TYP_04"
    TIMEOUT_EXCEEDED = "TMO_05"
    SEMANTIC_MISMATCH = "SEM_06"
    UNKNOWN = "UNK_99"


class RepairRoute(str, Enum):
    """Routing destinations based on error characteristics."""
    RULE_REPAIR = "rule_repair"
    LLM_REPAIR = "llm_repair"
    HYBRID_REPAIR = "hybrid_repair"
    SYSTEM_CONTROL = "system_control"
    SEMANTIC_AUDIT = "semantic_audit"


@dataclass
class DiagnosticRecord:
    """Structured diagnostic representation."""
    line: int
    column: int
    severity: str
    message: str
    category: ErrorCategory
    route: RepairRoute
    raw_payload: Optional[dict[str, Any]] = None


class LeanErrorParser:
    """Parses raw Lean compiler diagnostics into structured categories and routes."""

    @staticmethod
    def classify_message(message: str) -> tuple[ErrorCategory, RepairRoute]:
        """Maps raw text message to standard Taxonomy and repair route."""
        msg_lower = message.lower()

        # 1. Missing Imports
        if any(w in msg_lower for w in ["unknown package", "module not found", "failed to import"]):
            return ErrorCategory.MISSING_IMPORT, RepairRoute.RULE_REPAIR

        # 2. Syntax Errors
        if any(w in msg_lower for w in ["expected '", "unexpected token", "unclosed", "expected ':='", "expected command"]):
            return ErrorCategory.SYNTAX_ERROR, RepairRoute.RULE_REPAIR

        # 3. Timeout Exceeded
        if any(w in msg_lower for w in ["timeout at", "heartbeats exceeded", "deep recursion detected", "timed out"]):
            return ErrorCategory.TIMEOUT_EXCEEDED, RepairRoute.SYSTEM_CONTROL

        # 4. Type Mismatch
        if any(w in msg_lower for w in ["type mismatch", "cannot be unified with", "dimension mismatch", "subtype violation"]):
            return ErrorCategory.TYPE_MISMATCH, RepairRoute.LLM_REPAIR

        # 5. Unknown Identifier
        if any(w in msg_lower for w in ["unknown identifier", "unknown constant", "unknown theorem", "unknown tactic"]):
            # If it might be a mathlib module, could be rule, otherwise hybrid
            return ErrorCategory.UNKNOWN_IDENTIFIER, RepairRoute.HYBRID_REPAIR

        # 6. Semantic Warnings
        if any(w in msg_lower for w in ["uses sorry", "altered quantifier", "dubious assumption"]):
            return ErrorCategory.SEMANTIC_MISMATCH, RepairRoute.SEMANTIC_AUDIT

        return ErrorCategory.UNKNOWN, RepairRoute.LLM_REPAIR

    @classmethod
    def parse_diagnostic(cls, diag_dict: dict[str, Any]) -> DiagnosticRecord:
        """Parses a dictionary diagnostic message."""
        line = diag_dict.get("line", 1)
        col = diag_dict.get("column", 1)
        severity = diag_dict.get("severity", "error")
        message = diag_dict.get("message", "")

        cat, route = cls.classify_message(message)
        return DiagnosticRecord(
            line=line,
            column=col,
            severity=severity,
            message=message,
            category=cat,
            route=route,
            raw_payload=diag_dict
        )
