# Third part of case study: Shopping Cart Analysis
## 1. Thông tin Nhóm
- **Nhóm: 1**  
- **Thành viên:** 
  - Triệu Quốc Anh
  - Nguyễn Trung Thành
  - Lê Thị Ngọc Bích
- **Chủ đề:** PHÂN CỤM KHÁCH HÀNG DỰA TRÊN LUẬT KẾT HỢP
- **Dataset:** Online Retail (UCI) - Dữ liệu bán lẻ trực tuyến UK

## 2. Mục tiêu 
- Áp dụng thuật toán phân cụm KMeans để phân cụm khách hàng
- Trực quan hóa và diễn giải các cụm
- Đề xuất chiến lược hành động từ từng cụm

## 3. Quy trình 
Tiền xử lý và khai phá luật

   ↓
   
Trích xuất đặc trưng từ luật

   ↓
   
Phân cụm

   ↓
   
Diễn giải và trực quan hóa

## 4. Lựa chọn luật kết hợp
### 4.1 Danh sách luật đầu vào
Với thuật toán FP-Growth và tham số:
- MIN_SUPPORT=0.01,
- MAX_LEN=3,
- METRIC="lift",
- MIN_THRESHOLD=1.0,
- MIN_CONF=0.3,
- MIN_LIFT=1.2,
- MAX_ANTECEDENTS=2,
- MAX_CONSEQUENTS=1,
thu được 1,794 luật kết hợp
