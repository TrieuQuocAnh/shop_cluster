# 📊 Hướng Dẫn Sử Dụng Streamlit Dashboard - Phân tích Cụm Khách Hàng

## 🎯 Giới Thiệu

Dashboard Streamlit này được xây dựng để phân tích kết quả từ dự án:
- **Phân cụm khách hàng dựa trên luật kết hợp** sử dụng FP-Growth
- **Chiến lược bán hàng** dựa trên từng cụm khách hàng
- **Bundle & Cross-sell** recommendations

## 🚀 Cách Chạy

### Cách 1: Chạy bằng Python (Khuyến nghị)
```bash
cd c:\Code\DataMining\shop_cluster
python run_dashboard.py
```

### Cách 2: Chạy Streamlit trực tiếp
```bash
cd c:\Code\DataMining\shop_cluster
streamlit run streamlit_dashboard.py
```

### Cách 3: Chạy bằng Batch file (Windows)
```bash
c:\Code\DataMining\shop_cluster\run_dashboard.bat
```

Dashboard sẽ mở tại: **http://localhost:8501**

## 📋 Các Tính Năng Chính

### 1️⃣ Tab: Thống Kê Cụm (📊 Thống Kê Cụm)

**Mục đích:** Xem tổng quan thông tin cụm khách hàng

**Các thành phần:**

#### Số Liệu Chính (Metrics)
- 👥 **Số khách hàng**: Tổng số khách trong cụm và % so với tổng
- 💰 **Avg Monetary**: Mức chi tiêu trung bình (nếu bật RFM)
- 🔄 **Avg Frequency**: Số lần mua trung bình (nếu bật RFM)
- 📅 **Avg Recency**: Số ngày kể từ lần mua cuối cùng (nếu bật RFM)

#### Biểu Đồ
- **Phân phối Monetary**: Histogram chi tiêu của khách hàng trong cụm
- **Phân phối Frequency**: Histogram tần suất mua hàng

#### Bảng Thống Kê
- Bảng chi tiết các chỉ số RFM của cụm

#### So Sánh Baseline (tùy chọn)
- So sánh các chỉ số với baseline cũ (nếu file tồn tại)

### 2️⃣ Tab: Top Rules (📋 Top Rules)

**Mục đích:** Xem các luật kết hợp sản phẩm trong cụm

**Các thành phần:**

#### Lựa Chọn Loại Luật
- **Top Rules (Activation Rate)**: Luật dựa trên tỷ lệ kích hoạt trong cụm
- **Dominant Rules (RFM)**: Luật đặc biệt cho cụm (nếu tồn tại)

#### Số Lượng Rules
- Slider để chọn số luật hiển thị (5-50)

#### Biểu Đồ Activation Rate
- Biểu đồ thanh ngang hiển thị activation rate của từng luật
- Activation Rate > 1.0 = Luật mạnh trong cụm

#### Bảng Chi Tiết
- Bảng hiển thị từng luật với:
  - **Luật**: Mô tả sản phẩm kết hợp
  - **Tỷ lệ kích hoạt**: Activation rate
  - **Tỷ lệ toàn cầu**: Global rate
  - **Tỷ lệ dominant**: Dominance score

#### Phân Tích Chi Tiết
- Chọn luật để xem chi tiết
- Hiển thị các sản phẩm liên quan

### 3️⃣ Tab: Bundle & Cross-sell (🎁 Bundle & Cross-sell)

**Mục đích:** Đề xuất chiến lược bán hàng (kết hợp sản phẩm)

**Các thành phần:**

#### Loại Gợi Ý
- **High Lift Rules**: Luật có khả năng cross-sell mạnh
- **High Activation**: Luật thực tế thường xảy ra
- **Combination**: Kết hợp cả hai

#### Bundle Recommendations
- Các kết hợp sản phẩm để bán gộp
- Cột "Khuyến khích": Mức độ ưu tiên dựa trên activation rate

#### Cross-sell Recommendations
- Gợi ý sản phẩm bổ sung:
  - **Khi khách mua**: Sản phẩm đầu tiên (antecedent)
  - **Gợi ý thêm**: Sản phẩm bổ sung (consequent)
  - **Tỷ lệ kích hoạt**: Xác suất khách sẽ mua cùng

#### Chiến Lược Bán Hàng
**4 chiến lược được đề xuất:**

1. **Discount Bundle**
   - Tạo combo giá đặc biệt cho sản phẩm thường được mua cùng
   - Áp dụng cho luật có activation rate cao

2. **Recommendation Engine**
   - Hiển thị "Khách khác cũng mua" trên trang sản phẩm
   - Gợi ý ở checkout

3. **Email Marketing**
   - Gửi email về sản phẩm bổ sung theo hành vi
   - Tạo campaign "Khám phá combo giá tốt"

4. **Tối Ưu Hóa**
   - A/B test gợi ý bundle
   - Track conversion từ cross-sell
   - Điều chỉnh theo mùa vụ

### 4️⃣ Tab: So Sánh Cụm (📈 So Sánh Cụm)

**Mục đích:** So sánh các cụm khách hàng với nhau

**Các thành phần:**

#### Heatmap RFM
- Heatmap so sánh metric RFM giữa các cụm
- Màu sắc hiển thị mức độ (xanh = cao, đỏ = thấp)

#### Bảng So Sánh
- So sánh chi tiết:
  - Số khách hàng
  - Avg Recency (ngày)
  - Avg Frequency (lần)
  - Avg Monetary ($)

#### Biểu Đồ So Sánh
- **Chi tiêu Trung bình**: So sánh monetary value
- **Tần suất Mua**: So sánh frequency

#### Phân Loại Cụm
Hệ thống tự động phân loại cụm:
- 💎 **High-value**: Chi tiêu cao (top 25%)
- 🔄 **Loyal**: Mua thường xuyên (top 25%)
- ⭐ **Recent**: Mua gần đây (bottom 25% recency)
- 📍 **Standard**: Khách hàng bình thường

## ⚙️ Các Tùy Chọn Trong Sidebar

### Chọn Cụm Khách Hàng
```
🔍 Chọn cụm khách hàng: [Cụm 0] [Cụm 1] [Cụm 2] [Cụm 3]
```
- Chọn cụm muốn phân tích từ dropdown

### Hiển Thị So Sánh Baseline
```
☑ Hiển thị so sánh Baseline
```
- Bật/tắt so sánh với baseline (nếu file tồn tại)

### Hiển Thị Metric RFM
```
☑ Hiển thị metric RFM
```
- Bật/tắt hiển thị các metric Recency, Frequency, Monetary

## 📊 Giải Thích Các Metric

### RFM Analytics
- **Recency (R)**: Số ngày kể từ lần mua cuối cùng (càng thấp càng tốt)
- **Frequency (F)**: Số lần mua trong khoảng thời gian (càng cao càng tốt)
- **Monetary (M)**: Tổng giá trị mua (càng cao càng tốt)

### Association Rules Metrics
- **Activation Rate**: Tỷ lệ sản phẩm B được mua khi mua A trong cụm
  - > 1.0: Luật mạnh hơn so với toàn bộ
  - = 1.0: Luật trung bình
  - < 1.0: Luật yếu

- **Lift**: Mức độ khuyến khích mối quan hệ giữa hai sản phẩm
  - Được tính từ all_rules

- **Support**: Tỷ lệ giao dịch chứa cả hai sản phẩm

- **Confidence**: Xác suất mua B nếu mua A

- **Dominance**: Tỷ lệ dominant của luật trong cụm

## 📁 Cấu Trúc File

```
shop_cluster/
├── streamlit_dashboard.py          # Dashboard chính
├── run_dashboard.py                # Script chạy Python
├── run_dashboard.bat               # Script chạy Windows
├── STREAMLIT_DASHBOARD_README.md   # Hướng dẫn ngắn
├── STREAMLIT_DASHBOARD_GUIDE.md    # Hướng dẫn chi tiết (file này)
└── data/processed/
    ├── customer_clusters_from_rules.csv
    ├── customer_clusters_from_rules_baseline.csv
    ├── rules_fpgrowth_filtered.csv
    ├── top_rules_rule/
    │   ├── cluster_0.csv
    │   ├── cluster_1.csv
    │   ├── cluster_2.csv
    │   └── cluster_3.csv
    └── dominant_rules_rule_rfm/
        ├── cluster_0.csv
        ├── cluster_1.csv
        ├── cluster_2.csv
        └── cluster_3.csv
```

## 🔧 Yêu Cầu & Cài Đặt

### Yêu Cầu Python
- Python >= 3.7
- pandas >= 2.0.2
- streamlit >= 1.24.0
- plotly >= 5.15.0
- numpy >= 1.24.3

### Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

Hoặc cài thêm Streamlit nếu chưa có:
```bash
pip install streamlit
```

## 💡 Mẹo Sử Dụng

### 1. Lần Đầu Chạy
- Dashboard sẽ mất vài giây để tải dữ liệu lần đầu
- Lần sau sẽ nhanh hơn nhờ cache

### 2. Thay Đổi Giữa Cụm
- Khi chọn cụm khác, tất cả biểu đồ sẽ cập nhật tự động

### 3. Biểu Đồ Tương Tác
- Hover chuột vào biểu đồ để xem thông tin chi tiết
- Click vào legend để ẩn/hiện các yếu tố

### 4. Export Dữ Liệu
- Click nút "⬇️" trên biểu đồ để tải về SVG
- Click nút "📋" trên bảng để copy dữ liệu

### 5. Tối Ưu Hóa Màn Hình
- Sử dụng chế độ toàn màn hình (F11)
- Dashboard tự động căn chỉnh theo kích thước màn hình

## 🐛 Khắc Phục Sự Cố

### Lỗi: "File does not exist"
**Nguyên nhân**: Không tìm thấy file dữ liệu
**Giải pháp**: 
- Chắc chắn chạy từ thư mục `shop_cluster`
- Kiểm tra các file dữ liệu trong `data/processed/`

### Lỗi: "No module named 'streamlit'"
**Nguyên nhân**: Streamlit chưa cài đặt
**Giải pháp**: 
```bash
pip install streamlit
```

### Dashboard chạy chậm
**Nguyên nhân**: Máy tính không đủ RAM hoặc CPU yếu
**Giải pháp**:
- Đóng các chương trình khác
- Giảm số rules hiển thị
- Khởi động lại dashboard

### Lỗi khi chuyển tab
**Nguyên nhân**: Dữ liệu không tải đủ
**Giải pháp**:
- Đợi dashboard tải xong (thường mất 5-10 giây lần đầu)
- Làm mới trang (F5)
- Khởi động lại dashboard

## 📞 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra log ở terminal chạy dashboard
2. Xem phần "Khắc Phục Sự Cố" trên
3. Kiểm tra yêu cầu cài đặt

## 📝 Ghi Chú

- Dashboard được xây dựng bằng **Tiếng Việt** hoàn toàn
- Sử dụng **Plotly** cho biểu đồ tương tác
- Hỗ trợ **Real-time interaction** với dữ liệu
- Responsive design cho nhiều kích thước màn hình
- Tối ưu hiệu suất bằng **Streamlit caching**

---

**Phiên bản**: 1.0  
**Cập nhật**: 2025  
**Dataset**: Online Retail - UCI
