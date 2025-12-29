# Experiments Summary — Clustering from Rules

Đây là báo cáo tóm tắt kết quả thử nghiệm so sánh các biến thể đặc trưng cho phân cụm khách hàng dựa trên luật kết hợp (association rules).

Files chính
- Kịch bản chạy: `src/evaluate_configurations.py`
- Kết quả thô: `data/processed/experiments_results.csv`

Mục tiêu
- So sánh 4 chiều cấu hình:
  - rule-only vs rule + RFM
  - binary (presence) vs weighted (normalized counts)
  - Top-K nhỏ (50) vs Top-K lớn (200)
  - Độ lệch/độ ổn định cluster (sử dụng KMeans với `n_clusters=3` trong thử nghiệm này)

Tóm tắt kết quả (trích `data/processed/experiments_results.csv`)

| Config | n_customers | silhouette | davies_bouldin | calinski_harabasz | cluster_sizes |
|---|---:|---:|---:|---:|---|
| K=50 | enc=binary | rfm=False | 138 | 0.6997 | 0.9261 | 83.30 | {0:116,1:12,2:10} |
| K=50 | enc=binary | rfm=True  | 3921 | 0.9596 | 0.1891 | 15647.94 | {0:3794,1:126,2:1} |
| K=50 | enc=weighted | rfm=False | 138 | 0.5517 | 0.6398 | 260.72 | {0:81,1:41,2:16} |
| K=50 | enc=weighted | rfm=True  | 3921 | 0.9433 | 0.4889 | 8585.79 | {0:3844,1:16,2:61} |
| K=200 | enc=binary | rfm=False | 2028 | 0.4642 | 1.2217 | 832.50 | {0:88,1:1808,2:132} |
| K=200 | enc=binary | rfm=True  | 3921 | 0.6582 | 1.0651 | 1602.31 | {0:132,1:3700,2:89} |
| K=200 | enc=weighted | rfm=False | 2028 | 0.6168 | 0.7321 | 607.36 | {0:1952,1:16,2:60} |
| K=200 | enc=weighted | rfm=True  | 3921 | 0.7588 | 0.6624 | 1153.01 | {0:3843,1:16,2:62} |

Ghi chú: `n_customers` là số khách hàng sau khi lọc khách hàng có đặc trưng không toàn 0; các số cho `cluster_sizes` là kích thước mỗi nhãn phân cụm (label 0/1/2).

Những phát hiện chính
- Thêm RFM cải thiện chất lượng phân cụm rõ rệt: so sánh cặp cùng `encoding` và `K` thấy `use_rfm=True` cho silhouette cao hơn và Davis–Bouldin thấp hơn.
- `Binary (presence)` với Top-K nhỏ (50) + RFM đạt điểm silhouette tốt nhất (0.9596) — nghĩa là ma trận nhị phân các luật quan trọng cộng với RFM tách nhóm rất rõ ràng.
- `Weighted` làm giảm một phần tín hiệu phân biệt khi so với `binary` trên Top-K nhỏ ở thử nghiệm này (binary tốt hơn weighted).
- Top-K lớn (200) thường làm giảm hiệu năng phân cụm — nhiều luật yếu làm tăng chiều không gian và nhiễu.

Giải thích ngắn gọn tại sao
- RFM đem vào các đặc trưng liên tục về hành vi khách hàng (recency/frequency/monetary) giúp tách những khách hàng có hành vi mua tương tự nhưng khác giá trị/độ thường xuyên. Đây là tín hiệu hữu ích bổ trợ cho luật kết hợp.
- Vector luật nhị phân (presence) tạo ma trận thưa nhưng phân biệt; khi bình thường hóa (weighted) theo tổng hóa đơn, một số khác biệt bị làm mờ, nhất là với khách hàng ít giao dịch.
- Khi lấy quá nhiều luật (Top-K lớn), nhiều luật có lift/importance thấp sẽ được thêm vào, làm tăng noise và có thể làm phân cụm kém hơn.

Khuyến nghị (nên áp dụng)
- Sử dụng kết hợp `rule presence (binary)` + `RFM` với bộ luật chọn lọc (Top-K nhỏ, ví dụ K=50) cho bước phân đoạn ban đầu.
- Nếu cần nhiều rule hơn để khám phá hành vi vi mô, cân nhắc tiền xử lý chọn luật bằng threshold về `lift` hoặc `confidence` thay vì chỉ lấy Top-K lớn.

Reproducibility — cách chạy lại
1. Chạy script đánh giá (từ thư mục project gốc):

```bash
python -u src/evaluate_configurations.py
```

2. Kết quả sẽ được lưu tại: `data/processed/experiments_results.csv`.

Tiếp theo (đề xuất công việc nâng cao)
- Sinh bảng pivot chi tiết: silhouette/davies_bouldin/CH theo từng chiều cấu hình (có thể làm trong notebook `notebooks/clustering_from_rules.ipynb`).
- Tạo các biểu đồ: silhouette per config, phân bố kích thước cluster, heatmap trung bình RFM theo cluster.
- Thử thêm thuật toán phân cụm khác (GaussianMixture, Agglomerative) và kiểm tra tính ổn định (nhiều lần chạy, seed khác nhau).

Nếu bạn muốn, tôi sẽ tiếp tục tạo:
- `reports/experiments_plots.png` và một notebook chạy phân tích trực quan;
- hoặc cập nhật `README.md` chính để đưa phần này vào phần Documentation.

---
Report generated: summary of `data/processed/experiments_results.csv` — mở file để xem chi tiết từng cấu hình.
