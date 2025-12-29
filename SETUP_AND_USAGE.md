# 📊 Streamlit Dashboard - Phân Tích Cụm Khách Hàng

> **Tạo ngày**: 2025  
> **Trạng thái**: ✅ Hoàn thành và sẵn sàng sử dụng

## 📌 Giới Thiệu Nhanh

Đây là một **dashboard tương tác** xây dựng bằng **Streamlit** để phân tích kết quả từ dự án:
- 🎯 Phân cụm khách hàng dựa trên luật kết hợp (FP-Growth)
- 📊 Thống kê RFM chi tiết cho từng cụm
- 💼 Gợi ý chiến lược bán hàng (Bundle & Cross-sell)
- 📈 So sánh phân tích giữa các cụm

## 🚀 Cách Sử Dụng Nhanh

### Bước 1: Kiểm Tra Cấu Hình
```bash
cd c:\Code\DataMining\shop_cluster
python setup_dashboard.py
```

### Bước 2: Chạy Dashboard
```bash
python run_dashboard.py
```

Hoặc trực tiếp:
```bash
streamlit run streamlit_dashboard.py
```

### Bước 3: Mở Trong Trình Duyệt
Dashboard tự động mở tại: **http://localhost:8501**

## 📂 Cấu Trúc File

```
📁 shop_cluster/
├── 📄 streamlit_dashboard.py          ⭐ Dashboard chính
├── 📄 setup_dashboard.py              🔧 Script kiểm tra cấu hình
├── 📄 run_dashboard.py                ▶️  Script chạy Python
├── 📄 run_dashboard.bat               ⚙️  Script chạy Windows
├── 📄 README.md                       📖 README dự án gốc
├── 📄 STREAMLIT_DASHBOARD_README.md   📖 Hướng dẫn ngắn
├── 📄 STREAMLIT_DASHBOARD_GUIDE.md    📚 Hướng dẫn chi tiết
├── 📄 SETUP_AND_USAGE.md              📋 File này
└── 📁 data/processed/
    ├── customer_clusters_from_rules.csv
    ├── rules_fpgrowth_filtered.csv
    ├── 📁 top_rules_rule/
    │   ├── cluster_0.csv
    │   ├── cluster_1.csv
    │   ├── cluster_2.csv
    │   └── cluster_3.csv
    └── 📁 dominant_rules_rule_rfm/
        ├── cluster_0.csv
        ├── cluster_1.csv
        ├── cluster_2.csv
        └── cluster_3.csv
```

## 🎨 Các Tab Chính

### 1️⃣ **📊 Thống Kê Cụm**
- Hiển thị thông tin chi tiết của cụm
- Số lượng khách hàng, chi tiêu, tần suất mua
- Biểu đồ phân phối dữ liệu
- So sánh với baseline (tùy chọn)

### 2️⃣ **📋 Top Rules**
- Xem các luật kết hợp sản phẩm
- Phân loại theo Activation Rate hoặc Dominant Rules
- Phân tích chi tiết từng luật
- Cảy sản phẩm liên quan

### 3️⃣ **🎁 Bundle & Cross-sell**
- Đề xuất kết hợp sản phẩm (Bundle)
- Gợi ý sản phẩm bổ sung (Cross-sell)
- Chiến lược bán hàng:
  - Discount Bundle
  - Recommendation Engine
  - Email Marketing
  - Tối ưu hóa A/B Test

### 4️⃣ **📈 So Sánh Cụm**
- Heatmap RFM giữa các cụm
- Bảng so sánh chi tiết
- Biểu đồ so sánh
- Phân loại cụm (High-value, Loyal, Recent, Standard)

## 🔧 Cài Đặt Dependencies

Tất cả dependencies đã được bao gồm trong `requirements.txt`:

```bash
pip install -r requirements.txt
```

Hoặc cài thêm Streamlit:
```bash
pip install streamlit>=1.24.0
```

## ⚙️ Tùy Chọn Sidebar

| Tùy Chọn | Mô Tả |
|---------|-------|
| 🔍 Chọn cụm | Lựa chọn cụm khách hàng (0-3) |
| ☑ Baseline | Bật/tắt so sánh với baseline |
| ☑ Metric RFM | Bật/tắt hiển thị RFM metrics |

## 📊 Giải Thích Metrics

### RFM Analysis
- **R (Recency)**: Số ngày từ lần mua cuối (↓ tốt)
- **F (Frequency)**: Số lần mua (↑ tốt)
- **M (Monetary)**: Tổng chi tiêu (↑ tốt)

### Association Rules
- **Activation Rate**: Tỷ lệ kích hoạt trong cụm
  - > 1.0 = Luật mạnh
  - = 1.0 = Luật trung bình
  - < 1.0 = Luật yếu

## 💡 Mẹo Sử Dụng

✨ **Lần đầu chạy sẽ mất vài giây** để tải dữ liệu - điều này bình thường

🎨 **Hover chuột** lên biểu đồ để xem thông tin chi tiết

📥 **Tải dữ liệu** bằng nút trên biểu đồ hoặc bảng

🔄 **Chuyển giữa cụm** - mọi thứ sẽ cập nhật tự động

## 🐛 Khắc Phục Sự Cố

### "File does not exist"
✅ Chạy từ thư mục `shop_cluster`

### "No module named 'streamlit'"
✅ Cài đặt: `pip install streamlit`

### Dashboard chạy chậm
✅ Đóng các chương trình khác, hoặc khởi động lại

### Lỗi khi chuyển tab
✅ Đợi tải xong (5-10 giây) hoặc làm mới trang (F5)

## 📝 Yêu Cầu Hệ Thống

| Yêu Cầu | Phiên Bản Tối Thiểu |
|---------|-------------------|
| Python | 3.7+ |
| Streamlit | 1.24.0+ |
| Pandas | 2.0.0+ |
| Plotly | 5.0.0+ |
| Numpy | 1.20.0+ |

## 📞 Thông Tin Thêm

📖 **Hướng dẫn chi tiết**: Xem file `STREAMLIT_DASHBOARD_GUIDE.md`

❓ **Câu hỏi**: Kiểm tra phần "Khắc Phục Sự Cố" trong hướng dẫn chi tiết

🎯 **Cách tối ưu**: Tham khảo phần "Mẹo Sử Dụng" trong hướng dẫn

## ✅ Trạng Thái

- ✅ Tất cả kiểm tra đã vượt qua
- ✅ Dashboard sẵn sàng sử dụng
- ✅ Tất cả dữ liệu đã được tải
- ✅ Tiếng Việt được hỗ trợ đầy đủ

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: 2025  
**Trạng thái**: 🟢 Hoạt động bình thường
