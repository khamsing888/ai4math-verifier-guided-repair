# ERROR TAXONOMY v0.1 - PHÂN LOẠI LỖI LEAN 4 & CHIẾN LƯỢC SỬA
### DỰ ÁN AI4MATH - NHÓM 6: VERIFIER-GUIDED REPAIR

---

## 1. Mục tiêu
Tài liệu này chuẩn hóa bảng mã lỗi (Taxonomy) gặp phải khi biên dịch các đoạn mã phát biểu định lý và chứng minh hình thức bằng Lean 4, phân định rõ ràng giữa các lỗi có thể sửa tự động bằng luật (Rule-based) và các lỗi cần tới mô hình ngôn ngữ lớn (LLM-based).

---

## 2. Bảng phân loại 6 nhóm lỗi (Taxonomy Specification)

| Mã danh mục | Tên danh mục | Dấu hiệu nhận biết trong Lean 4 Log | Chiến lược xử lý gợi ý | Độ ưu tiên / Chi phí |
|:---|:---|:---|:---:|:---:|
| `SYN_01` | **SYNTAX_ERROR** | `expected ...`, `unexpected token`, `unclosed bracket/parenthesis` | **Rule-based** (sửa ngoặc, chuẩn hóa cú pháp) | Rất cao / 0 Token |
| `IMP_02` | **MISSING_IMPORT** | `unknown package`, `module not found`, `failed to import` | **Rule-based** (tra cứu bảng Mathlib import) | Rất cao / 0 Token |
| `ID_03` | **UNKNOWN_IDENTIFIER** | `unknown identifier 'foo'`, `unknown constant 'bar'` | **Hybrid** (tra cứu namespace hoặc LLM gợi ý) | Trung bình / Thấp |
| `TYP_04` | **TYPE_MISMATCH** | `type mismatch at term ... has type A but expected B` | **LLM Repair** (truyền ngữ cảnh kiểu lỗi) | Trung bình / Cao |
| `TMO_05` | **TIMEOUT_EXCEEDED** | `(deterministic) timeout at ...`, `maximum heartbeats exceeded` | **System Control** (tăng ngân sách hoặc loại bỏ) | Thấp / Rất cao |
| `SEM_06` | **SEMANTIC_MISMATCH** | Mã compile qua nhưng phát biểu sai khác đề gốc | **Semantic Auditor** (so khớp AST và đối chiếu) | Nghiêm ngặt / Audit |

---

## 3. Chiến lược định tuyến sửa lỗi (Repair Routing Policy)

```
[Mã Lean lỗi từ Nhóm 5]
           │
           ▼
 [Structured Error Parser]  <── Trích xuất: Dòng, Cột, Severity, Thông báo lỗi
           │
           ▼
    [Error Classifier]
           │
     ┌─────┴───────────────────────────┐
     ▼                                 ▼
[Lỗi SYN_01, IMP_02, ID_03]     [Lỗi TYP_04, ID_03 phức tạp]
     │                                 │
     ▼                                 ▼
[Rule-based Fixer]              [LLM Context-Injected Fixer]
(Zero Token Cost, < 5ms)        (Bounded Token Budget, < 3000ms)
     │                                 │
     └──────────────┬──────────────────┘
                    ▼
           [Lean 4 Re-Verifier]
                    │
           ┌────────┴────────┐
        (Thành công)      (Thất bại)
           │                 │
           ▼                 ▼
   [Semantic Safety]    [Kiểm tra Retry Budget]
   (Kiểm tra đổi đề)         ├── Còn ngân sách: Thử vòng tiếp theo
           │                 └── Hết ngân sách: Ghi log thất bại
           ▼
    [Hoàn thành / Lưu Log]
```

---

## 4. Tiêu chí an toàn ngữ nghĩa (Semantic Safety Criteria)

Hệ thống bắt buộc phải kiểm tra tính toàn vẹn ngữ nghĩa sau khi sửa lỗi:
1. **Không triệt tiêu giả thiết:** Không được phép chèn giả thiết mâu thuẫn (như `h : False`) để chứng minh mục tiêu một cách tầm thường.
2. **Không tầm thường hóa mục tiêu:** Không được thay thế kết luận định lý thành các hằng số hiển nhiên như `True` hoặc `0 = 0`.
3. **Bảo tồn chữ ký:** Tên định lý và danh sách biến đầu vào của bài toán phải giữ nguyên vẹn so với đề bài ngôn ngữ tự nhiên ban đầu.
