1. So sánh Binary vs Weighted
Binary rules WEIGHTING = "none"
Weighted rules WEIGHTING = "lift"
2. So sánh Rule-only vs Rule + RFM
Rule-only	USE_RFM = False
Rule + RFM	USE_RFM = True
3. Top-K nhỏ vs Top-K lớn

# So sánh kết luận
1️⃣ Binary rules vs Weighted rules (WEIGHTING = none vs lift)
So sánh TH1 vs TH2
Thiết lập	            Silhouette tốt nhất (k=2)	Silhouette k>2
Binary (TH1)	        0.704	                    ~0.47–0.48
Weighted – lift (TH2)	0.855	                    ~0.48–0.58

Nhận xét

Weighted rules vượt trội rõ rệt

k=2: +0.15 silhouette

k=3: 0.583 vs 0.483

Lift giữ lại thông tin độ mạnh của luật, giúp:

Khoảng cách giữa khách hàng phản ánh mức độ liên kết mua hàng, không chỉ có/không

Giảm nhiễu từ các luật phổ biến nhưng yếu

Kết luận 1

Weighted rules (lift) tốt hơn Binary rules cả về chất lượng phân cụm lẫn ý nghĩa hành vi mua hàng.

2️⃣ Rule-only vs Rule + RFM
So sánh TH2 vs TH3
Thiết lập	        Silhouette k=2	Silhouette k=3–7
Rule-only (TH2)	    0.8546	        ~0.48–0.58
Rule + RFM (TH3)	0.8541	        ~0.49–0.58 (ổn định hơn)

Nhận xét

k=2 gần như không đổi → luật chi phối mạnh

Nhưng khi k ≥ 5, Rule+RFM:

Silhouette cao hơn nhẹ

Thứ hạng k ổn định hơn

RFM giúp:

Phân biệt khách hàng có luật giống nhau nhưng giá trị khác nhau

Tạo persona rõ ràng hơn (VIP, mua thường xuyên, mua rải rác…)

Kết luận 2

Rule + RFM không làm giảm silhouette nhưng tăng khả năng diễn giải & giá trị kinh doanh → nên dùng.

3️⃣ Top-K nhỏ vs Top-K lớn
Tổng hợp nhanh
TH	TOP_K	    Silhouette cao nhất	Nhận định
TH6	50	~0.99	❌ Quá tốt → nghi over-separation
TH4	100	0.92	⭐ Rất tốt
TH3	200	0.85	Tốt
TH5	400	0.82	Bắt đầu nhiễu
TH7	800	0.79	❌ Nhiễu, giảm mạnh

Phân tích sâu

Top-K quá nhỏ (50):

Silhouette ~1 → cụm cách ly cực mạnh

Nhưng:

Cụm dễ bị chi phối bởi vài luật rất mạnh

Thiếu đa dạng hành vi

Top-K quá lớn (400–800):

Nhiều luật yếu, trùng lặp

Khoảng cách khách hàng bị “làm loãng”

Khoảng tối ưu: 100–200 luật

Kết luận 3

TOP_K_RULES ∈ [100, 200] là cân bằng tốt nhất giữa chất lượng & khả năng diễn giải.

4️⃣ Đánh giá cấu hình FINAL
FINAL CONFIG
TOP_K_RULES = 200
WEIGHTING = lift
USE_RFM = True
MIN_ANTECEDENT_LEN = 2

Kết quả
k	Silhouette
2	0.954
3–6	~0.94
≥7	giảm dần
Đánh giá

MIN_ANTECEDENT_LEN = 2:

Loại luật đơn giản → luật giàu ngữ nghĩa hơn

Silhouette:

Cao nhưng không cực đoan như TH6

Giảm hợp lý khi tăng k → mô hình ổn định

Rất phù hợp cho:

Phân tích hành vi mua

Gắn nhãn persona

Trình bày học thuật

Kết luận FINAL

Cấu hình final là lựa chọn tốt nhất tổng thể: chất lượng cao, ổn định, dễ diễn giải và có ý nghĩa kinh doanh.

5️⃣ Tổng kết ngắn gọn 

Weighted rules (lift) cải thiện đáng kể chất lượng phân cụm so với binary rules.

Việc kết hợp RFM không làm giảm silhouette nhưng giúp cụm có ý nghĩa kinh doanh rõ ràng hơn.

Số lượng luật Top-K ảnh hưởng mạnh đến chất lượng: quá ít gây over-separation, quá nhiều gây nhiễu.

Cấu hình TOP_K = 200, WEIGHTING = lift, USE_RFM = True, antecedent ≥ 2 đạt cân bằng tối ưu giữa hiệu năng và khả năng diễn giải.

# Chi tiết trường hợp
## TH1: baseline
notebooks\runs\clustering_from_rules_baseline_run.ipynb

TOP_K_RULES = 200
SORT_RULES_BY = "lift"
WEIGHTING = "None"
MIN_ANTECEDENT_LEN = 1
USE_RFM = False
RFM_SCALE = False
RULE_SCALE = False

    k	silhouette
0	2	0.703935
1	8	0.483309
2	3	0.483107
3	6	0.478620
4	7	0.477378
5	5	0.476875
6	4	0.466701
7	10	0.440233
8	9	0.438168

## TH2: WEIGHTING = "lift"
notebooks\runs\clustering_from_rules_th2_run.ipynb

TOP_K_RULES = 200
SORT_RULES_BY = "lift"
WEIGHTING = "lift"
MIN_ANTECEDENT_LEN = 1
USE_RFM = False
RFM_SCALE = False
RULE_SCALE = False

	k	silhouette
0	2	0.854603
1	3	0.583132
2	9	0.488141
3	8	0.487427
4	10	0.485141
5	4	0.481887
6	6	0.479825
7	7	0.478548
8	5	0.470463

## TH3: USE_RFM
notebooks\runs\clustering_from_rules_th3_run.ipynb

        TOP_K_RULES=200,
        SORT_RULES_BY="lift",
        WEIGHTING="lift",
        MIN_ANTECEDENT_LEN=1,
        USE_RFM=True,
        RFM_SCALE=True,
        RULE_SCALE=False,


k	silhouette
0	2	0.854095
1	3	0.581274
2	7	0.494725
3	6	0.492822
4	5	0.487540
5	9	0.486536
6	10	0.484775
7	8	0.484119
8	4	0.480065

## TH4: USE_RFM TOP_K_RULES=100
notebooks\runs\clustering_from_rules_th4_run.ipynb

        TOP_K_RULES=100,
        SORT_RULES_BY="lift",
        WEIGHTING="lift",
        MIN_ANTECEDENT_LEN=1,
        USE_RFM=True,
        RFM_SCALE=True,
        RULE_SCALE=False,

k	silhouette
0	2	0.922280
1	7	0.716587
2	6	0.713215
3	10	0.693925
4	9	0.690932
5	8	0.688024
6	5	0.683287
7	3	0.682213
8	4	0.681243

## TH5: TOP_K_RULES=400
notebooks\runs\clustering_from_rules_th5_run.ipynb

        TOP_K_RULES=400,
        SORT_RULES_BY="lift",
        WEIGHTING="lift",
        MIN_ANTECEDENT_LEN=1,
        USE_RFM=True,
        RFM_SCALE=True,
        RULE_SCALE=False,

	k	silhouette
0	2	0.824354
1	3	0.513197
2	4	0.502503
3	8	0.421360
4	9	0.421301
5	5	0.412590
6	6	0.411091
7	10	0.408336
8	7	0.406779

## TH6: USE_RFM TOP_K_RULES=50
notebooks\runs\clustering_from_rules_th6_run.ipynb

        TOP_K_RULES=50,
        SORT_RULES_BY="lift",
        WEIGHTING="lift",
        MIN_ANTECEDENT_LEN=1,
        USE_RFM=True,
        RFM_SCALE=True,
        RULE_SCALE=False,

	k	silhouette
0	10	0.993279
1	9	0.993144
2	8	0.992677
3	7	0.992546
4	6	0.991636
5	5	0.989398
6	4	0.986798
7	2	0.986423
8	3	0.985536

## TH7:  TOP_K_RULES=800
notebooks\runs\clustering_from_rules_th7_run.ipynb

        TOP_K_RULES=800,
        SORT_RULES_BY="lift",
        WEIGHTING="lift",
        MIN_ANTECEDENT_LEN=1,
        USE_RFM=True,
        RFM_SCALE=True,
        RULE_SCALE=False,

	k	silhouette
0	2	0.795389
1	3	0.789636
2	4	0.573694
3	5	0.446427
4	6	0.445945
5	7	0.440599
6	8	0.364970
7	9	0.321391
8	10	0.301525

## TH: final
notebooks\runs\clustering_from_rules_run.ipynb
data\processed\dominant_rules_rule_rfm
data\processed\top_rules_rule
    TOP_K_RULES=200,
    SORT_RULES_BY="lift",
    WEIGHTING="lift",
    MIN_ANTECEDENT_LEN=2,
    USE_RFM=True,
    RFM_SCALE=True,
    RULE_SCALE=False,

	k	silhouette
0	2	0.953706
1	6	0.942228
2	5	0.938557
3	3	0.938463
4	4	0.936962
5	9	0.838164
6	8	0.837387
7	7	0.834601
8	10	0.775505
