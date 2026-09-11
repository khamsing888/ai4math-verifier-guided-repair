# CONTRIBUTIONS.md - Phân công vai trò & Nhật ký đóng góp

Môn học: **INT4418 - Dữ liệu lớn (Trình độ Thạc sĩ, PTIT)**  
Đề tài: **NHÓM 6 — Verifier-Guided Repair: Sửa bản Lean dựa trên phản hồi kiểm chứng**  
Giảng viên hướng dẫn: **TS. Nguyễn Kiều Linh**

---

## 1. Cơ cấu phân vai chính thức (06 thành viên)

Căn cứ Mục 5 (Trang 18–19) trong *Hướng dẫn Bài tập lớn AI4Math*, cơ cấu 6 vai trò chính và vai trò dự phòng của nhóm được xác định như sau:

| STT | Họ và tên | Mã học viên | Vai trò chính | Vai trò dự phòng | Nhiệm vụ phụ trách chính |
|:---:|:---|:---:|:---|:---|:---|
| 1 | **Đào Văn Tâm** *(Trưởng nhóm)* | **B25CHHT112** | **Evaluation & Cost Analysis** (TV6) | Queue / Worker System | • Chủ trì điều phối nhóm, chốt đề cương & kiến trúc hệ thống.<br>• Đo đạc chỉ số chất lượng vs chi phí (Latency P50/P95, QPS, Token Cost).<br>• Phân tích đường cong Pareto, Ablation study và tổng hợp Báo cáo học phần. |
| 2 | **Trần Quang Đức Dũng** | **B25CHHT088** | **Queue & Worker System** (TV5) | Evaluation & Cost Analysis | • Xây dựng kiến trúc hàng đợi phân tán (Queue) và quản lý worker pools.<br>• Thiết kế vòng lặp sửa có chặn (Bounded retry loop), cơ chế timeout.<br>• Đo lường và tối ưu hóa độ trễ đuôi Queue P95. |
| 3 | **Lâm Thành Trung** | **B25CHHT117** | **Rule-based Repair** (TV3) | LLM Repair Engine | • Phát triển các bộ luật heuristic sửa nhanh (0-Token cost fixes): cân bằng ngoặc, sửa lỗi gõ cú pháp.<br>• Tự động bổ sung namespace và tra cứu thư viện Mathlib import.<br>• Đánh giá tỷ lệ bao phủ của luật (Rule coverage). |
| 4 | **Nguyễn Xuân Tùng** | **B25CHHT119** | **LLM Repair Engine** (TV4) | Rule-based Repair | • Thiết kế Prompt Templates tiêm ngữ cảnh lỗi có cấu trúc (Diagnostic Injection).<br>• Tích hợp API/Model mã nguồn mở sửa các lỗi logic phức tạp (Type mismatch, Unsolved goals).<br>• Tối ưu hóa số lượng token tiêu thụ trên mỗi lần sửa. |
| 5 | **Khamsing OUTHAIHUENG** | **B25CHHT125** | **Parser & Taxonomy** (TV2) | Error Dataset | • Xây dựng bộ Parser bóc tách compiler diagnostics của Lean 4 sang JSON có cấu trúc.<br>• Chuẩn hóa mã lỗi theo bảng Taxonomy v0.1 (`SYN_01` $\rightarrow$ `SEM_06`).<br>• Cài đặt logic định tuyến (Router) phân luồng Rule vs LLM. |
| 6 | **Mekdala Nounou** | **B25CHHT124** | **Error Dataset & Contract** (TV1) | Parser & Taxonomy | • Tiếp nhận Data Contract từ Nhóm 5 (Autoformalization).<br>• Thu thập, làm sạch và gán nhãn tập dữ liệu lỗi thực tế.<br>• Quản lý và đóng băng tập kiểm thử độc lập (Hold-out test set 30%) chống rò rỉ dữ liệu. |

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
