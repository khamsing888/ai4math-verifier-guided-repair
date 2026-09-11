# CONTRIBUTIONS.md - Phân công vai trò & Nhật ký đóng góp

Môn học: **INT4418 - Dữ liệu lớn (Trình độ Thạc sĩ, PTIT)**  
Đề tài: **NHÓM 6 — Verifier-Guided Repair: Sửa bản Lean dựa trên phản hồi kiểm chứng**  
Giảng viên hướng dẫn: **TS. Nguyễn Kiều Linh**

---

## 1. Cơ cấu phân vai chính thức (06 thành viên)

Căn cứ Mục 5 (Trang 18–19) trong *Hướng dẫn Bài tập lớn AI4Math*, cơ cấu 6 vai trò chính và vai trò dự phòng của nhóm được xác định như sau:

| STT | Thành viên & Mã HV | Vai trò (Chính / Dự phòng) | Nhiệm vụ cụ thể (Làm gì) | Tệp & Thư mục làm việc (Ở đâu) | Công cụ & Công nghệ | Sản phẩm bàn giao chính |
|:---:|:---|:---|:---|:---|:---|:---|
| **1** | **Đào Văn Tâm**<br>`B25CHHT112`<br>*(Trưởng nhóm)* | **Evaluation & Cost Analysis (TV6)**<br>*(DP: Queue System)* | • Chủ trì tiến độ, kết nối Nhóm 5 & 7.<br>• Viết module Semantic Safety Audit.<br>• Chạy benchmark 3 mức tải, đo P50/P95, QPS, Token Cost.<br>• Viết script vẽ biểu đồ Pareto.<br>• Chủ trì Báo cáo 12-20 trang & Slide. | • `src/semantic_auditor.py`<br>• `src/baseline_repair.py`<br>• `scripts/run_experiment.py`<br>• `scripts/generate_figures.py`<br>• `reports/report.pdf/docx`<br>• `results/raw/`, `results/figures/` | Python, NumPy, Pandas, Matplotlib, Seaborn, LaTeX/Word, Git Projects | • Báo cáo khoa học 12-20 trang.<br>• Biểu đồ P95 & Pareto curve.<br>• Semantic Safety Auditor. |
| **2** | **Trần Quang Đức Dũng**<br>`B25CHHT088` | **Queue & Worker System (TV5)**<br>*(DP: Evaluation)* | • Cấu hình Redis Queue phân tán.<br>• Lập trình Priority Queue vs FIFO.<br>• Xây dựng Lean 4 Verifier Worker Pool (đa tiến trình song song).<br>• Cài đặt Bounded Retry Controller & timeout 15s. | • `src/worker_queue.py`<br>• `src/verifier_pool.py`<br>• `src/bounded_controller.py`<br>• `docker-compose.yml`<br>• `Dockerfile`<br>• `tests/test_queue.py` | Redis, Python `redis-py`, `multiprocessing`, `asyncio`, `subprocess`, Docker | • Redis Task Dispatcher.<br>• Lean 4 Worker Pool.<br>• Docker Compose cụm Queue.<br>• Báo cáo Queue P95 latency. |
| **3** | **Lâm Thành Trung**<br>`B25CHHT117` | **Rule-based Repair (TV3)**<br>*(DP: LLM Repair)* | • Phát triển các bộ luật sửa heuristic 0-token (< 5ms).<br>• Cân bằng ngoặc `()`, `[]`, `{}`.<br>• Chèn từ khóa thiếu (`by`, `:`).<br>• Tự động thêm `import Mathlib...`.<br>• Đánh giá Rule Coverage. | • `src/rule_repair.py`<br>• `configs/mathlib_import_table.json`<br>• `tests/test_rule_repair.py` | Python, Regex (`re`), Unicode Lean 4 syntax, Pytest/Unittest | • Module `rule_repair.py`.<br>• Bảng tra cứu Mathlib import.<br>• Bộ unit test 100% pass.<br>• Báo cáo Rule Coverage. |
| **4** | **Nguyễn Xuân Tùng**<br>`B25CHHT119` | **LLM Repair Engine (TV4)**<br>*(DP: Rule Repair)* | • Xây dựng module gọi LLM sửa lỗi logic (Type mismatch, Tactic).<br>• Thiết kế Prompt Templates tiêm ngữ cảnh lỗi chẩn đoán (Diagnostic Injection).<br>• Tích hợp API/Local Model (Qwen/DeepSeek qua Ollama/vLLM).<br>• Tối ưu hóa chi phí token/lần sửa. | • `src/llm_repair.py`<br>• `configs/prompts/*.yaml`<br>• `tests/test_llm_repair.py` | Python, `httpx`, `requests`, LLM APIs / Ollama / vLLM, Prompt Engineering | • Module `llm_repair.py`.<br>• Bộ Prompt Templates.<br>• Thống kê Token Cost/bài.<br>• Mock LLM Test Suite. |
| **5** | **Khamsing OUTHAIHUENG**<br>`B25CHHT125` | **Parser & Taxonomy (TV2)**<br>*(DP: Error Dataset)* | • Nâng cấp bộ bóc tách log compiler (`lean --json`).<br>• Chuẩn hóa mã lỗi theo Taxonomy v0.1 (`SYN_01` $\rightarrow$ `SEM_06`).<br>• Cài đặt Error Router định tuyến sang Rule hoặc LLM.<br>• Đo đạc Parser Accuracy. | • `src/error_parser.py`<br>• `src/error_router.py`<br>• `docs/error_taxonomy_v0.1.md`<br>• `tests/test_error_parser.py` | Python, Pydantic, Regular Expressions, Lean 4 Diagnostics JSON | • Module `error_parser.py`.<br>• Bộ định tuyến `error_router.py`.<br>• Báo cáo độ chính xác Parser. |
| **6** | **Mekdala Nounou**<br>`B25CHHT124` | **Error Dataset & Contract (TV1)**<br>*(DP: Parser)* | • Đầu mối kết nối Data Contract với Nhóm 5.<br>• Mở rộng tập lỗi lên 1.000 và 10.000 mẫu.<br>• Quản lý tập Hold-out 30% chống rò rỉ.<br>• Duy trì Replayable Error Store (dedup sha256).<br>• Đóng gói Trace Lake Parquet cho Nhóm 7. | • `src/error_store.py`<br>• `data_sample/error_dataset_50.json`<br>• `data_sample/manifest.json`<br>• `scripts/replay_error_run.py`<br>• `scripts/export_to_group7.py`<br>• `tests/test_error_store.py` | Python, PyArrow, FastParquet, Pandas, HuggingFace Datasets, SHA-256 | • Replayable Error Store.<br>• Dataset 1K & 10K mẫu.<br>• File Parquet xuất cho Nhóm 7.<br>• Script Replay kiểm chứng. |

> **Nguyên tắc bảo vệ:** Mỗi thành viên có vai trò chính và vai trò dự phòng. Khi bảo vệ vấn đáp, từng thành viên phải nắm vững toàn bộ pipeline và giải trình được chi tiết phần việc mình phụ trách.

---

## 2. Nhật ký công việc và Pull Requests (PR Log)

| Tuần | Nhiệm vụ trọng tâm | Người phụ trách chính | PR / Commit | Trạng thái | Minh chứng bàn giao |
|:---:|:---|:---:|:---:|:---:|:---|
| **W1** | Chốt đề cương 1 trang, Taxonomy v0.1, 50 lỗi mẫu & Baseline plan | Cả nhóm (Tâm chủ trì) | `7388923`, `a557797` | ✅ Hoàn thành | [docs/de_cuong_nhom_6_tuan_1.md](file:///Users/daotam/Documents/Workspace/Master/3.DLL/docs/de_cuong_nhom_6_tuan_1.md)<br>[docs/error_taxonomy_v0.1.md](file:///Users/daotam/Documents/Workspace/Master/3.DLL/docs/error_taxonomy_v0.1.md)<br>[data_sample/error_dataset_50.json](file:///Users/daotam/Documents/Workspace/Master/3.DLL/data_sample/error_dataset_50.json)<br>[src/baseline_repair.py](file:///Users/daotam/Documents/Workspace/Master/3.DLL/src/baseline_repair.py) |
| **W2** | Nhận Data Contract từ Nhóm 5, dựng Replayable Error Store | Nounou, Khamsing, Tâm | `c53a5fa` | ✅ Hoàn thành | [docs/data_contract_group5_group6.md](file:///Users/daotam/Documents/Workspace/Master/3.DLL/docs/data_contract_group5_group6.md)<br>[src/error_store.py](file:///Users/daotam/Documents/Workspace/Master/3.DLL/src/error_store.py)<br>[scripts/replay_error_run.py](file:///Users/daotam/Documents/Workspace/Master/3.DLL/scripts/replay_error_run.py) |
| **W3** | Chạy Baseline retry nguyên prompt trên dữ liệu đầy đủ | Trung, Tùng | - | ⏳ Chờ thực hiện | Baseline raw metrics + demo nội bộ |
| **W4** | Hoàn thiện Error Parser & Rule-based fixes cho lỗi đơn giản | Khamsing, Trung | - | ⏳ Chờ thực hiện | Parser accuracy test + Rule coverage report |
| **W5** | Hoàn thiện Router và module LLM Repair nạp ngữ cảnh lỗi | Tùng, Tâm | - | ⏳ Chờ thực hiện | Repair service v0.1 + prompt versions |
| **W6** | Tích hợp Bounded Loop, Timeout, Dedup & Queue workers | Dũng, Tâm | - | ⏳ Chờ thực hiện | End-to-end pipeline service + recovery test |
| **W7** | Thí nghiệm Scalability 3 mức tải (100 $\rightarrow$ 1K $\rightarrow$ 10K) | Dũng, Tâm, Cả nhóm | - | ⏳ Chờ thực hiện | Raw CSV/JSON + Biểu đồ Queue P95 & Throughput |
| **W8** | Ablation study, Taxonomy lỗi thất bại & Semantic audit | Tâm, Cả nhóm | - | ⏳ Chờ thực hiện | Bảng ablation + failure taxonomy + safety note |
| **W9** | Đóng gói Docker Compose, hoàn thiện Báo cáo khoa học | Tâm, Cả nhóm | - | ⏳ Chờ thực hiện | Release candidate + Draft Report 12–20 trang |
| **W10** | Chuẩn bị Slide, Kịch bản Live Demo và Bảo vệ vấn đáp | Cả nhóm | - | ⏳ Chờ thực hiện | Final package + Slide demo + Bảo vệ cá nhân |
