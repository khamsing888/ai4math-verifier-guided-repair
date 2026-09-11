# ĐỀ CƯƠNG BÀI TẬP LỚN (MỐC TUẦN 1)
### HỌC PHẦN: DỮ LIỆU LỚN (INT4418) - CAO HỌC PTIT (2026)

---

**1. Tên nhóm và đề tài:**  
* **Nhóm:** Nhóm 6 (Quy mô: 06 học viên).  
* **Tên đề tài:** Verifier-Guided Repair: Hệ thống phân loại lỗi và tự động sửa mã chứng minh hình thức Lean 4 dựa trên phản hồi của trình kiểm chứng dưới giới hạn tài nguyên.

**2. Câu hỏi nghiên cứu:**  
* *RQ1:* Việc nạp thông báo lỗi có cấu trúc (Structured Compiler Diagnostics) từ Lean 4 vào bộ định tuyến sửa lỗi (Router) có cải thiện tỷ lệ sửa thành công (Repair Success Rate) vượt trội so với chiến lược thử lại nguyên văn prompt ban đầu (Retry Baseline) không?
* *RQ2:* Dưới một ngân sách cố định về chi phí token LLM và thời gian phản hồi, chính sách retry có chặn (Bounded Retry Loop) kết hợp Rule-based Heuristic và LLM nào tối ưu được tỷ lệ biên dịch thành công (Compile Rate) và giảm thiểu độ trễ đuôi (Tail Latency P95)?

**3. Nút thắt Big Data (Big Data Bottleneck):**  
* **Tải xử lý & Độ trễ:** Khi quy mô bài toán tăng lên hàng nghìn tới hàng chục nghìn ($1.000 ightarrow 10.000$ candidates), hệ thống gặp nút thắt về lập lịch hàng đợi phân tán, tranh chấp tài nguyên giữa nhiều worker kiểm chứng Lean (vốn rất tốn CPU và bộ nhớ), bùng nổ độ trễ đuôi ($P95 / P99$) và chi phí token nếu retry không kiểm soát.
* **Đa dạng lỗi & Trùng lặp:** Sự bùng nổ các biến thể lỗi (lỗi cú pháp, thiếu import, sai kiểu, timeout) đòi hỏi kỹ thuật phân loại theo lô và xử lý song song để tránh lãng phí chi phí suy luận.

**4. Dữ liệu và giấy phép:**  
* **Nguồn dữ liệu:**
  1. Dữ liệu candidate lỗi từ pipeline chuyển đổi tự động (Nhóm 5 Autoformalization) dựa trên `ProofNet` (MIT License) và `NuminaMath-CoT` (Apache-2.0).
  2. Kho định lý và bổ đề toán hình thức `mathlib4` (Apache-2.0).
* **Quản trị dữ liệu:** Dữ liệu mẫu (50 mẫu tuần 1) và manifest được lưu trong `data_sample/`. Tập kiểm thử độc lập (Hold-out set) chiếm 30% được đóng băng hoàn toàn để đánh giá khách quan.

**5. Baseline bắt buộc:**  
* **Phương pháp:** Thử lại (retry) nguyên văn prompt gốc đúng 01 lần duy nhất khi Lean báo lỗi; không bóc tách thông báo lỗi, không phân loại lỗi, không áp dụng heuristic rule.
* **Điều kiện so sánh:** Baseline chạy trên cùng tập dữ liệu, cùng split, cùng timeout (60s) và cùng tài nguyên phần cứng.

**6. Ba mức quy mô / tải thí nghiệm (Scalability Tiers):**  
* **Mức 1 (Small / Smoke test):** 100 error candidates, 1 worker Lean, retry budget = 1.
* **Mức 2 (Medium / Standard scale):** 1.000 error candidates, 2 workers song song, retry budget = 1 và 3.
* **Mức 3 (Large / Stress scale):** 10.000 error candidates, 4–8 workers song song, so sánh FIFO Queue vs. Priority Queue (ưu tiên sửa lỗi nhanh).

**7. Primary Metrics (Chỉ số đánh giá chính):**  
* **Chất lượng:**
  * *Repair Success Rate (%):* Tỷ lệ ứng viên lỗi được sửa thành công và Lean biên dịch thông qua.
  * *Final Compile Rate (%):* Tỷ lệ tổng số mẫu hợp lệ cuối cùng.
  * *Semantic Pass Rate (%):* Tỷ lệ mẫu vượt qua kiểm tra ngữ nghĩa (không cheat, không làm đổi đề).
* **Hiệu năng & Chi phí:**
  * *Queue Latency P95 (ms):* Thời gian chờ trong hàng đợi phân vị 95%.
  * *Throughput (items/sec):* Số lượng candidate được xử lý và kiểm chứng trên một đơn vị thời gian.
  * *Token Cost per Success:* Lượng token tiêu thụ trung bình cho mỗi bài sửa thành công.

**8. Kiến trúc bản nháp (Draft Architecture):**  
* `Input Queue` (Nhận candidate từ Nhóm 5) $ightarrow$ `Lean 4 Verifier` $ightarrow$ `Structured Error Parser` (JSON diagnostics) $ightarrow$ `Error Taxonomy & Router` $ightarrow$
  * Nhánh 1 (Lỗi đơn giản: import, typo, ngoặc): `Rule-based Fixer` (0-token cost).
  * Nhánh 2 (Lỗi logic, sai kiểu): `LLM Repair Engine` (Error context injected).
* $ightarrow$ `Bounded Retry Controller` (Kiểm tra giới hạn ngân sách & số lần thử) $ightarrow$ `Output Store & Replay Log`.

**9. Phân vai thành viên:**  
* **Thành viên 1:** Error Dataset & Hold-out curation (Thu thập, gán nhãn, quản lý tập kiểm thử độc lập).
* **Thành viên 2:** Parser & Error Taxonomy (Bóc tách log JSON từ compiler, chuẩn hóa phân loại lỗi).
* **Thành viên 3:** Rule-based Repair (Cài đặt các bộ luật sửa nhanh cú pháp và namespace).
* **Thành viên 4:** LLM Prompting & Repair Engine (Xây dựng prompt tiêm ngữ cảnh lỗi, gọi mô hình AI).
* **Thành viên 5:** Queue & Distributed Worker System (Hàng đợi, đa tiến trình worker Lean, quản lý timeout & retry).
* **Thành viên 6:** Evaluation, Pareto Analysis & Report (Đo đạc chỉ số P95, chi phí token, viết báo cáo).

**10. Rủi ro và phương án dự phòng:**  
* *Rủi ro 1: Lean 4 biên dịch quá lâu dẫn tới treo worker.* $ightarrow$ **Dự phòng:** Đặt timeout cứng (`maxHeartbeats = 200.000`, process timeout 15s) và kill tiến trình quá hạn.
* *Rủi ro 2: Chi phí gọi API LLM tăng quá cao khi mở rộng 10.000 mẫu.* $ightarrow$ **Dự phòng:** Dùng Rule-based xử lý trước các lỗi phổ biến (chiếm ~40%); sử dụng mô hình mã nguồn mở cục bộ (Qwen2.5-Coder / DeepSeek-Coder qua vLLM/Ollama).
* *Rủi ro 3: Mã sửa biên dịch qua nhưng làm sai ngữ nghĩa bài toán.* $ightarrow$ **Dự phòng:** Thiết kế bộ lọc Semantic Audit kiểm tra AST chữ ký định lý không bị biến đổi so với đề gốc.
