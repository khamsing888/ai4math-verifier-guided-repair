"""Rule-based Repair Engine for Lean 4 formal mathematical theorems.

Provides heuristic fixes for:
- SYN_01: Bracket balancing and keyword insertion
- IMP_02: Mathlib import injection using lookup table
- ID_03: Common identifier alias & typo resolution
"""

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "mathlib_import_table.json"

# Common identifier aliases and typo corrections for Lean 4
IDENTIFIER_REPLACEMENTS = {
    r"\.len\b": ".length",
    r"\bNat\.suc\b": "Nat.succ",
    r"\bsqrt\b": "Real.sqrt",
    r"\bNat\.add_com\b": "Nat.add_comm",
    r"\.size\b": ".length",
    r"\bsemip\b": "simp",
    r"\bClassical\.some\b": "Classical.choose",
    r"\.cardinal\b": ".card",
}


@dataclass
class RuleRepairResult:
    """Represents the output of a rule-based repair operation."""
    repaired_code: str
    rule_applied: str
    category_code: str
    latency_ms: float
    token_cost: int = 0
    confidence: float = 1.0


class RuleRepairEngine:
    """Heuristic rule-based repair engine running at zero token cost."""

    def __init__(self, table_path: Path | None = None) -> None:
        """Initializes the engine with Mathlib import table."""
        path = table_path or DEFAULT_CONFIG_PATH
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.import_table: dict[str, str] = json.load(f)
        else:
            self.import_table = {}

    def fix_brackets(self, code: str, error_message: str) -> str | None:
        """R1: Bracket Balancer for (), [], {}."""
        msg_lower = error_message.lower()

        # Handle unmatched square bracket: expected ']'
        if "expected ']'" in msg_lower or "[" in code and "]" not in code:
            open_sq = code.count("[")
            close_sq = code.count("]")
            if open_sq > close_sq:
                return code + ("]" * (open_sq - close_sq))

        # Handle unexpected token ')' (extra closing bracket)
        if "unexpected token ')'" in msg_lower:
            # Remove redundant closing parenthesis if present at end or before ':='
            if "))" in code:
                return code.replace("))", ")", 1)
            # Remove trailing ')' before ':=' or end of statement
            fixed = re.sub(r"\)\s*:=\s*", " := ", code)
            if fixed != code:
                return fixed

        # Handle unclosed parenthesis or unexpected token ':' expecting ')'
        if "expected ')'" in msg_lower or "unclosed" in msg_lower:
            open_paren = code.count("(")
            close_paren = code.count(")")
            if open_paren > close_paren:
                # Common pattern: (h : (a + b = 2 : a = 2 - b -> (h : a + b = 2) : a = 2 - b
                if re.search(r"\(\s*h\s*:\s*\(\s*([^:]+?)\s*:\s*", code):
                    return re.sub(r"\(\s*h\s*:\s*\(\s*([^:]+?)\s*:\s*", r"(h : \1) : ", code)
                # If there's a colon separating hypothesis and conclusion
                if " : " in code:
                    parts = code.rsplit(" : ", 1)
                    missing = parts[0].count("(") - parts[0].count(")")
                    if missing > 0:
                        return f"{parts[0]}{')' * missing} : {parts[1]}"
                return code + (")" * (open_paren - close_paren))

        # General bracket counts check
        for open_ch, close_ch in [("(", ")"), ("[", "]"), ("{", "}")]:
            diff = code.count(open_ch) - code.count(close_ch)
            if diff > 0:
                return code + (close_ch * diff)

        return None

    def fix_keywords(self, code: str, error_message: str) -> str | None:
        """R2: Keyword Inserter for missing keywords (':', ':=', 'by', etc.)."""
        msg_lower = error_message.lower()

        # Unexpected token ';'
        if "unexpected token ';'" in msg_lower or ";" in code:
            fixed = code.replace(";", "")
            return fixed

        # Expected command (missing 'theorem ' or 'def ')
        if "expected command" in msg_lower and not code.strip().startswith(("theorem ", "def ", "lemma ", "example ")):
            return f"theorem {code.strip()}"

        # Missing colon: expected ':'
        if "expected ':'" in msg_lower:
            # Pattern: theorem foo (n : Nat) n > 0 -> theorem foo (n : Nat) : n > 0
            match = re.search(r"(theorem|lemma|def)\s+([^\(:]+)(\([^\)]+\))\s+([^\s:]+.*)", code)
            if match:
                decl, name, params, body = match.groups()
                return f"{decl} {name}{params} : {body}"
            # Another pattern: simple name and type/body
            if " : " not in code and ("theorem" in code or "def" in code):
                parts = code.split(maxsplit=2)
                if len(parts) == 3:
                    return f"{parts[0]} {parts[1]} : {parts[2]}"

        # Expected ':=' or '|' before tactic block or missing 'by'
        if "expected ':='" in msg_lower or "expected 'by'" in msg_lower:
            lines = code.splitlines()
            if len(lines) >= 2:
                # Theorem on first line, proof tactic on second line
                header = lines[0].rstrip()
                body = "\n".join(lines[1:])
                if not header.endswith(":="):
                    if ":=" in header:
                        header = header.replace(":=", ":= by")
                    else:
                        header = f"{header} := by"
                elif header.endswith(":=") and "by" not in header:
                    header = f"{header} by"
                return f"{header}\n  {body.strip()}"

        # Expected '→' or ':=' (e.g. using ASCII '->' instead of Lean unicode '→')
        if ("expected '→'" in msg_lower or "->" in code) and "->" in code:
            return code.replace("->", "→")

        return None

    def fix_missing_import(self, code: str, error_message: str) -> str | None:
        """R3: Mathlib Import Injector using lookup table."""
        # Extract package/identifier name from message
        # e.g., unknown identifier 'Real', failed to import 'Mathlib.Data.Real.Basic'
        match = re.search(r"'(?P<pkg>[A-Za-z0-9_\.]+)'", error_message)
        pkg_name = match.group("pkg") if match else ""

        import_statement = None
        if pkg_name and pkg_name in self.import_table:
            import_statement = self.import_table[pkg_name]
        else:
            # Check if any identifier in import table appears in error message or code
            for id_key, stmt in self.import_table.items():
                if id_key in error_message or (re.search(rf"\b{re.escape(id_key)}\b", code) and stmt not in code):
                    import_statement = stmt
                    break

        if import_statement:
            if import_statement in code:
                return code
            return f"{import_statement}\n\n{code.strip()}"

        return None

    def fix_identifier(self, code: str, error_message: str) -> str | None:
        """R4: Simple Identifier Resolver for known aliases & typos."""
        repaired = code
        applied = False

        for pattern, replacement in IDENTIFIER_REPLACEMENTS.items():
            if re.search(pattern, repaired):
                repaired = re.sub(pattern, replacement, repaired)
                applied = True

        if applied:
            return repaired
        return None

    def repair_candidate(
        self,
        code: str,
        category_code: str,
        error_message: str,
        line: int = 1,
        column: int = 1
    ) -> RuleRepairResult | None:
        """Runs the rule pipeline on an error candidate.

        Returns RuleRepairResult on match, or None for LLM fail-over.
        """
        start_time = time.perf_counter()
        repaired: str | None = None
        rule_applied: str = ""

        # Route according to taxonomy category
        if category_code == "SYN_01":
            repaired = self.fix_brackets(code, error_message)
            if repaired and repaired != code:
                rule_applied = "R1_bracket_balancer"
            else:
                repaired = self.fix_keywords(code, error_message)
                if repaired and repaired != code:
                    rule_applied = "R2_keyword_inserter"

        elif category_code == "IMP_02":
            repaired = self.fix_missing_import(code, error_message)
            if repaired and repaired != code:
                rule_applied = "R3_mathlib_import_injector"

        elif category_code == "ID_03":
            repaired = self.fix_identifier(code, error_message)
            if repaired and repaired != code:
                rule_applied = "R4_identifier_resolver"
            else:
                # Could be an unknown identifier due to missing import
                repaired = self.fix_missing_import(code, error_message)
                if repaired and repaired != code:
                    rule_applied = "R3_mathlib_import_injector"

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

        if repaired and repaired != code:
            return RuleRepairResult(
                repaired_code=repaired,
                rule_applied=rule_applied,
                category_code=category_code,
                latency_ms=elapsed_ms,
                token_cost=0,
                confidence=1.0
            )

        return None


# Module-level convenience singleton & function
_default_engine = RuleRepairEngine()


def apply_rules(
    lean_code: str,
    category_code: str,
    error_message: str,
    line: int = 1,
    column: int = 1
) -> str | None:
    """Applies rule-based heuristic fixes to Lean 4 code snippet.

    Returns the repaired code string if a rule matched, or None to fall back to LLM.
    """
    res = _default_engine.repair_candidate(lean_code, category_code, error_message, line, column)
    return res.repaired_code if res else None


def evaluate_dataset(dataset_path: str) -> dict[str, Any]:
    """Evaluates rule coverage and token savings on an error dataset."""
    engine = RuleRepairEngine()
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    rule_handled = 0
    per_category: dict[str, int] = {}
    latencies = []

    for item in data:
        cat = item.get("category_code", "UNKNOWN")
        msg = item.get("compiler_log", {}).get("message", "")
        code = item.get("code_snippet", "")
        line = item.get("compiler_log", {}).get("line", 1)
        col = item.get("compiler_log", {}).get("column", 1)

        res = engine.repair_candidate(code, cat, msg, line, col)
        if res:
            rule_handled += 1
            per_category[cat] = per_category.get(cat, 0) + 1
            latencies.append(res.latency_ms)

    hit_rate = round(rule_handled / total, 4) if total > 0 else 0.0
    avg_latency = round(sum(latencies) / len(latencies), 3) if latencies else 0.0
    tokens_saved = rule_handled * 550  # average baseline tokens per sample

    return {
        "total_samples": total,
        "rule_repaired_samples": rule_handled,
        "rule_hit_rate": hit_rate,
        "per_category_coverage": per_category,
        "avg_latency_ms": avg_latency,
        "tokens_saved_approx": tokens_saved
    }
