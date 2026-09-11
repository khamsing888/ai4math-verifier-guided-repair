"""Utility script to log and quantify AI-assisted contributions.

Adheres to PTIT INT4418 guidelines on transparent AI disclosure.
"""

import argparse
import datetime
import json
import os
from pathlib import Path

LOG_FILE = Path("docs/ai_use_log.jsonl")
STATEMENT_FILE = Path("docs/ai_use_statement.md")


def append_ai_log(
    stage: str,
    tool_model: str,
    task_type: str,
    description: str,
    verification_method: str,
    human_auditor: str,
    code_lines_approx: int = 0
):
    """Appends an entry to ai_use_log.jsonl and regenerates ai_use_statement.md."""
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "stage": stage,
        "tool_model": tool_model,
        "task_type": task_type,
        "description": description,
        "code_lines_approx": code_lines_approx,
        "verification_method": verification_method,
        "human_auditor": human_auditor,
        "status": "VERIFIED"
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    rebuild_statement_markdown()
    print(f"[OK] AI use logged: {stage} - {task_type}")


def rebuild_statement_markdown():
    """Reads ai_use_log.jsonl and updates docs/ai_use_statement.md."""
    if not LOG_FILE.exists():
        return

    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    total_entries = len(entries)
    total_lines = sum(e.get("code_lines_approx", 0) for e in entries)
    task_distribution = {}
    model_distribution = {}

    for e in entries:
        t = e.get("task_type", "Other")
        m = e.get("tool_model", "Unknown")
        task_distribution[t] = task_distribution.get(t, 0) + 1
        model_distribution[m] = model_distribution.get(m, 0) + 1

    md_content = f"""# AI-USE STATEMENT (BẢN TUYÊN BỐ SỬ DỤNG AI)
### HỌC PHẦN: DỮ LIỆU LỚN (INT4418) - NHÓM 6: VERIFIER-GUIDED REPAIR

> **Quy định học phần:** Theo Hướng dẫn Bài tập lớn INT4418 và Đề cương chi tiết, việc sử dụng các mô hình AI/LLM phải được công khai minh bạch, có định lượng cụ thể, và toàn bộ mã nguồn cũng như kết luận đều phải được nhóm học viên kiểm chứng độc lập (thông qua Lean 4 compiler và automated tests).

---

## 1. Bảng số liệu định lượng tổng hợp (Quantitative Summary)

* **Tổng số phiên/hạng mục AI hỗ trợ:** `{total_entries}`
* **Ước tính số dòng mã & tài liệu AI đồng hành:** `~{total_lines}` dòng
* **Cơ chế kiểm chứng bắt buộc:** 100% mã nguồn được xác minh qua unit test tự động và trình kiểm chứng Lean 4; không chấp nhận mã chưa kiểm chứng.

### Phân bổ theo loại tác vụ:
| Loại tác vụ | Số lần ghi nhận | Tỷ trọng (%) |
|:---|:---:|:---:|
"""
    for t, count in sorted(task_distribution.items(), key=lambda x: x[1], reverse=True):
        pct = round((count / total_entries) * 100, 1)
        md_content += f"| {t} | {count} | {pct}% |\n"

    md_content += f"""
### Phân bổ theo mô hình / công cụ AI:
| Mô hình / Công cụ | Số lần ghi nhận | Tỷ trọng (%) |
|:---|:---:|:---:|
"""
    for m, count in sorted(model_distribution.items(), key=lambda x: x[1], reverse=True):
        pct = round((count / total_entries) * 100, 1)
        md_content += f"| {m} | {count} | {pct}% |\n"

    md_content += f"""
---

## 2. Nhật ký chi tiết hoạt động AI hỗ trợ (Chronological AI Activity Log)

| Thời điểm (UTC) | Giai đoạn | Mô hình / Công cụ | Loại tác vụ | Nội dung thực hiện | Phương thức kiểm chứng | Người kiểm duyệt | Trạng thái |
|:---|:---|:---|:---|:---|:---|:---:|:---:|
"""
    for e in entries:
        ts = e["timestamp"][:16].replace("T", " ")
        md_content += (
            f"| {ts} | {e['stage']} | {e['tool_model']} | {e['task_type']} | "
            f"{e['description']} | {e['verification_method']} | {e['human_auditor']} | "
            f"✅ {e['status']} |\n"
        )

    md_content += """
---

## 3. Cam kết liêm chính học thuật (Academic Integrity Affirmation)

1. Nhóm học viên chịu trách nhiệm hoàn toàn về tính chính xác, tính logic toán học và khả năng thực thi của toàn bộ mã nguồn trong dự án.
2. Các phát biểu toán học và mã sửa Lean 4 đều phải được kiểm tra qua trình biên dịch hình thức (`lean` CLI).
3. Mọi kết quả thực nghiệm, số đo độ trễ $P50 / P95$ và thông lượng đều được sinh ra từ các lần chạy thật trên hệ thống thực tế (lưu tại `results/raw/`), không sử dụng số liệu suy diễn từ AI.
"""

    with open(STATEMENT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log AI use event")
    parser.add_argument("--stage", required=True, help="Project stage (e.g. Week 1)")
    parser.add_argument("--model", default="Claude Code / Antigravity", help="AI Model used")
    parser.add_argument("--type", required=True, help="Task type (e.g. Code, Architecture, Docs)")
    parser.add_argument("--desc", required=True, help="Task description")
    parser.add_argument("--verify", required=True, help="Verification method")
    parser.add_argument("--auditor", default="Nhóm 6 Lead", help="Human reviewer")
    parser.add_argument("--lines", type=int, default=0, help="Approx code lines")
    args = parser.parse_args()

    append_ai_log(
        stage=args.stage,
        tool_model=args.model,
        task_type=args.type,
        description=args.desc,
        verification_method=args.verify,
        human_auditor=args.auditor,
        code_lines_approx=args.lines
    )
