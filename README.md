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
### 4.2 Chọn luật
- TOP_K_RULES = 200 (không dùng toàn bộ luật vì gây nhiễu và làm vector đặc trưng quá thưa)
- SORT_RULES_BY = "lift" (ưu tiên sức mạnh mối quan hệ)
- Lift range: 20.04 - 74.57
- Confidence range: 0.35 - 0.98
- Support range: 0.01 - 0.02

| # | Antecedent | Consequent | Support | Confidence | Lift |
|---|------------|------------|---------|------------|------|
| 0 | HERB MARKER PARSLEY, HERB MARKER ROSEMARY | HERB MARKER THYME | 0.010932 | 0.951691 | 74.5670 |
| 1 | REGENCY TEA PLATE GREEN , REGENCY TEA PLATE ROSES  | REGENCY TEA PLATE PINK | 0.012374 | 0.793594 | 53.7645 |
| 2 | JAM JAR WITH GREEN LID | JAM JAR WITH PINK LID | 0.010488 | 0.718631 | 47.0925 |
| 3 | SET OF 3 WOODEN TREE DECORATIONS | SET OF 3 WOODEN STOCKING DECORATION | 0.011597 | 0.757246 | 46.4161 |
| 4 | HERB MARKER BASIL, HERB MARKER THYME | HERB MARKER ROSEMARY | 0.010710 | 0.950739 | 74.1700 |
| 5 | POPPY'S PLAYHOUSE BEDROOM , POPPY'S PLAYHOUSE KITCHEN | POPPY'S PLAYHOUSE LIVINGROOM  | 0.010432 | 0.709434 | 45.1756 |
| 6 | HERB MARKER MINT, HERB MARKER ROSEMARY | HERB MARKER THYME | 0.010599 | 0.931707 | 73.0013 |
| 7 | CHILDRENS CUTLERY POLKADOT PINK | CHILDRENS CUTLERY POLKADOT BLUE | 0.010155 | 0.535087 | 40.0117 |
| 8 | PINK VINTAGE PAISLEY PICNIC BAG | SCANDINAVIAN PAISLEY PICNIC BAG | 0.014594 | 0.690288 | 29.7600 |
| 9 | HERB MARKER CHIVES | HERB MARKER PARSLEY | 0.010377 | 0.921182 | 72.8098 |
