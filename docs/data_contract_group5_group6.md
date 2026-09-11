# DATA CONTRACT SPECIFICATION: NHÓM 5 ➔ NHÓM 6
### HỌC PHẦN: DỮ LIỆU LỚN (INT4418) - HỆ SINH THÁI AI4MATH (PTIT 2026)

* **Bên phát hành dữ liệu (Upstream Producer):** Nhóm 5 (Autoformalization Pipeline).
* **Bên tiêu thụ dữ liệu (Downstream Consumer):** Nhóm 6 (Verifier-Guided Repair).
* **Phiên bản Contract:** `v0.1.0` (Mốc Tuần 2).
* **Trạng thái:** Đề xuất kỹ thuật (Ready for review).

---

## 1. Mục đích & Phạm vi

Bản hợp đồng dữ liệu (Data Contract) này quy định cấu trúc dữ liệu chuẩn mực, giao thức bàn giao và các ràng buộc toàn vẹn giữa **Nhóm 5** (sinh mã Lean từ đề toán tự nhiên nhưng gặp lỗi biên dịch) và **Nhóm 6** (tiếp nhận lỗi, phân loại và sửa lỗi tự động).

```
┌─────────────────────────────────┐
│     Nhóm 5: Autoformalization   │
│ (Sinh mã Lean 4 hàng loạt/Batch)│
└────────────────┬────────────────┘
                 │
                 │ Bàn giao Candidate Lỗi + Compiler Logs
                 ▼ [DATA CONTRACT v0.1]
┌─────────────────────────────────┐
│  Nhóm 6: Verifier-Guided Repair │
│    (Replayable Error Store)     │
└─────────────────────────────────┘
```

---

## 2. Định dạng & Giao thức Bàn giao (Payload Format)

* **Định dạng file:** `JSONL` (JSON Lines) hoặc `Parquet` (đối với batch lớn $\ge 1.000$ mẫu).
* **Quy ước đặt tên tệp:** `autoformalization_errors_<split>_<timestamp>_<git_commit>.jsonl`
* **Mã hóa ký tự:** Bắt buộc `UTF-8` (hỗ trợ toàn bộ ký tự toán học Unicode của Lean 4: `∀`, `∃`, `→`, `↔`, `∧`, `∨`, `ℝ`, `ℕ`, `ℤ`, `⟨`, `⟩`).

---

## 3. Lược đồ Dữ liệu Chi tiết (Data Schema)

Mỗi bản ghi đại diện cho một candidate mã Lean 4 biên dịch không thành công:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "candidate_id": "string (UUID v4 hoặc ID duy nhất)",
  "problem_id": "string (Mã bài toán gốc, vd: ProofNet_012, Numina_5421)",
  "source_dataset": "string (ProofNet | NuminaMath | Custom)",
  "split": "string (train | validation | test | holdout)",
  "statement_natural": "string (Đề bài bằng ngôn ngữ tự nhiên/LaTeX)",
  "candidate_code": "string (Toàn bộ mã nguồn Lean 4 được sinh ra)",
  "generator_metadata": {
    "model_name": "string (vd: Qwen2.5-Coder-7B, DeepSeek-Coder-V2)",
    "prompt_version": "string (vd: v1.2-fewshot)",
    "temperature": "number (0.0 - 1.0)",
    "generation_time_ms": "number"
  },
  "compiler_diagnostics": [
    {
      "severity": "string (error | warning | information)",
      "line": "integer (1-indexed)",
      "column": "integer (1-indexed)",
      "message": "string (Thông báo lỗi nguyên bản từ lean --json)"
    }
  ],
  "checksum_sha256": "string (SHA256 của candidate_code)",
  "created_at": "string (ISO 8601 UTC timestamp)"
}
```

### Chi tiết các trường dữ liệu:

| Tên trường | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Ý nghĩa |
|:---|:---:|:---:|:---|
| `candidate_id` | `string` | **Có** | Khóa chính duy nhất, định danh cho mỗi lần sinh mã. |
| `problem_id` | `string` | **Có** | ID bài toán gốc để đối chiếu khi đánh giá ngữ nghĩa. |
| `source_dataset` | `string` | **Có** | Nguồn gốc dữ liệu (`ProofNet`, `NuminaMath-CoT`). |
| `split` | `string` | **Có** | Phân tập dữ liệu: `train`, `validation`, hoặc `holdout`. |
| `statement_natural`| `string` | **Có** | Đề bài gốc bằng ngôn ngữ tự nhiên. Không được rỗng. |
| `candidate_code` | `string` | **Có** | Đoạn mã Lean 4 bị lỗi cần đưa vào sửa chữa. |
| `generator_metadata`| `object` | **Có** | Thông tin mô hình và tham số suy luận từ Nhóm 5. |
| `compiler_diagnostics`| `array` | **Có** | Danh sách lỗi do trình biên dịch Lean 4 trả về (`lean --json`). Ít nhất 1 lỗi `severity: error`. |
| `checksum_sha256`| `string` | **Có** | Checksum để khử trùng lặp (Deduplication) và chống biến đổi mã. |
| `created_at` | `string` | **Có** | Thời gian xuất bản dữ liệu chuẩn ISO 8601. |

---

## 4. Cam kết Chất lượng Dữ liệu (Service Level Agreements - SLA)

1. **Tính hợp lệ biên dịch (Compilation Failure Guarantee):** Nhóm 5 chỉ chuyển giao các candidate đã được kiểm chứng thực tế là **bị lỗi** (exit code $
eq 0$ hoặc có ít nhất một thông điệp lỗi). Không gửi mã đã hợp lệ vào luồng sửa.
2. **Không rò rỉ tập Hold-out (Zero Leakage):** Nhóm 5 phải tôn trọng phân vùng `holdout` để Nhóm 6 dùng độc lập đánh giá thuật toán sửa lỗi.
3. **Tính toàn vẹn đề bài (Faithfulness):** `statement_natural` phải giữ nguyên vẹn đề gốc từ benchmark, không bị cắt tỉa làm mất giả thiết toán học.

---

## 5. Kịch bản Phản hồi & Xử lý Ngoại lệ (Feedback Loop)

Sau khi Nhóm 6 xử lý xong mỗi batch lỗi, Nhóm 6 sẽ xuất bản báo cáo hoàn trả:
* `repaired_code`: Đoạn mã Lean 4 đã sửa thành công.
* `repair_strategy`: Chiến lược đã dùng (`rule_repair` hoặc `llm_repair`).
* `attempts_used`: Số lần thử trước khi thành công.
* `final_status`: `SUCCESS` (biên dịch qua) hoặc `FAILED` (hết ngân sách retry).
