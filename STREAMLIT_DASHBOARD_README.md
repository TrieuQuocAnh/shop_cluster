# Streamlit Dashboard - Phân tích Cụm Khách Hàng

Để chạy dashboard, sử dụng lệnh:

```bash
cd c:\Code\DataMining\shop_cluster
streamlit run streamlit_dashboard.py
```

## Tính Năng

### 1. 📊 Thống Kê Cụm
- Hiển thị các thông tin chính của cụm: số lượng khách hàng, chi tiêu trung bình, tần suất mua, recency
- Biểu đồ phân phối Monetary (chi tiêu) và Frequency (tần suất mua)
- Bảng thống kê chi tiết các chỉ số RFM
- Tùy chọn so sánh với baseline

### 2. 📋 Top Rules
- Xem top luật kết hợp của từng cụm
- Lựa chọn giữa "Top Rules" (dựa trên Activation Rate) và "Dominant Rules" (dựa trên RFM)
- Biểu đồ so sánh activation rate của các luật
- Phân tích chi tiết từng luật với các sản phẩm liên quan

### 3. 🎁 Bundle & Cross-sell
- Đề xuất bundle sản phẩm (kết hợp nhiều sản phẩm)
- Gợi ý cross-sell (gợi ý sản phẩm bổ sung)
- Chiến lược bán hàng được đề xuất:
  - Discount Bundle: tạo combo giá đặc biệt
  - Recommendation Engine: hiển thị sản phẩm liên quan
  - Email Marketing: gửi thông báo về sản phẩm bổ sung
  - Tối ưu hóa: A/B test và tracking

### 4. 📈 So Sánh Cụm
- Heatmap so sánh metric RFM giữa các cụm
- Bảng so sánh chi tiết các cụm
- Biểu đồ so sánh chi tiêu trung bình và tần suất mua
- Phân loại khách hàng:
  - 💎 High-value (Chi tiêu cao)
  - 🔄 Loyal (Mua thường xuyên)
  - ⭐ Recent (Mua gần đây)
  - 📍 Standard (Bình thường)

## Dữ Liệu Đầu Vào

Dashboard sử dụng các file dữ liệu:
- `data/processed/customer_clusters_from_rules.csv`: Dữ liệu cụm khách hàng
- `data/processed/rules_fpgrowth_filtered.csv`: Tất cả luật kết hợp
- `data/processed/top_rules_rule/cluster_*.csv`: Top rules cho từng cụm
- `data/processed/dominant_rules_rule_rfm/cluster_*.csv`: Dominant rules cho từng cụm
- `data/processed/customer_clusters_from_rules_baseline.csv`: Dữ liệu baseline (tùy chọn)

## Các Tùy Chọn

- **Chọn cụm**: Lựa chọn cụm khách hàng để phân tích
- **Hiển thị so sánh Baseline**: So sánh kết quả hiện tại với baseline
- **Hiển thị metric RFM**: Hiển thị/ẩn các metric RFM (Recency, Frequency, Monetary)
- **Số rules hiển thị**: Tùy chỉnh số lượng rules được hiển thị (5-50)
- **Loại gợi ý**: Chọn loại gợi ý bundle & cross-sell

## Yêu Cầu

```
streamlit>=1.24.0
pandas>=2.0.2
plotly>=5.15.0
numpy>=1.24.3
```

## Ghi Chú

- Dashboard được xây dựng bằng tiếng Việt
- Sử dụng Plotly cho các biểu đồ tương tác
- Streamlit cache data để tăng tốc độ
- Responsive design cho nhiều kích thước màn hình
