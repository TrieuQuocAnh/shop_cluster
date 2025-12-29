# -*- coding: utf-8 -*-
"""
Streamlit Dashboard - Phân tích cụm khách hàng và luật kết hợp
Dashboard để đọc file output, lọc theo cụm, xem top rules, xem gợi ý bundle/cross-sell
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Cấu hình trang
st.set_page_config(
    page_title="📊 Phân tích Cụm Khách hàng",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh cho Vietnamese text
st.markdown("""
    <style>
    * {
        font-family: 'Arial', 'Segoe UI', sans-serif;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# HÀM PHỤ TRỢ
# ============================================

@st.cache_data
def load_cluster_data():
    """Tải dữ liệu cụm khách hàng"""
    data_path = Path("data/processed/customer_clusters_from_rules.csv")
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    return None

@st.cache_data
def load_all_rules():
    """Tải tất cả luật kết hợp"""
    data_path = Path("data/processed/rules_fpgrowth_filtered.csv")
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    return None

@st.cache_data
def load_cluster_rules(cluster_id):
    """Tải luật top cho một cụm"""
    rules_path = Path(f"data/processed/top_rules_rule/cluster_{cluster_id}.csv")
    if rules_path.exists():
        df = pd.read_csv(rules_path)
        return df
    return None

@st.cache_data
def load_dominant_rules(cluster_id):
    """Tải luật dominant cho một cụm"""
    rules_path = Path(f"data/processed/dominant_rules_rule_rfm/cluster_{cluster_id}.csv")
    if rules_path.exists():
        df = pd.read_csv(rules_path)
        # Trả về None nếu dataframe trống
        if len(df) == 0:
            return None
        return df
    return None

@st.cache_data
def load_baseline_clusters():
    """Tải dữ liệu cụm baseline"""
    data_path = Path("data/processed/customer_clusters_from_rules_baseline.csv")
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    return None

def parse_rule_string(rule_str):
    """Phân tích chuỗi luật thành antecedents và consequents"""
    if pd.isna(rule_str):
        return None, None
    
    if "→" in rule_str:
        parts = rule_str.split("→")
        antecedents = parts[0].strip()
        consequents = parts[1].strip() if len(parts) > 1 else ""
        return antecedents, consequents
    return None, None

def extract_products_from_rule(rule_str):
    """Trích xuất sản phẩm từ chuỗi luật"""
    if pd.isna(rule_str):
        return []
    
    # Xóa dấu → nếu có
    rule_str = rule_str.replace("→", ",")
    
    # Tách các sản phẩm
    products = [p.strip() for p in rule_str.split(",") if p.strip()]
    return products

# ============================================
# GIAO DIỆN CHÍNH
# ============================================

st.title("📊 Dashboard Phân Tích Cụm Khách Hàng")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Tùy chọn")
    
    # Load dữ liệu
    cluster_data = load_cluster_data()
    all_rules = load_all_rules()
    baseline_data = load_baseline_clusters()
    
    if cluster_data is None:
        st.error("❌ Không thể tải dữ liệu cụm")
        st.stop()
    
    # Chọn số lượng cụm
    num_clusters = cluster_data['cluster'].nunique()
    selected_cluster = st.selectbox(
        "🔍 Chọn cụm khách hàng:",
        options=sorted(cluster_data['cluster'].unique()),
        format_func=lambda x: f"Cụm {x}"
    )
    
    st.markdown("---")
    
    # Tùy chọn hiển thị
    show_baseline = st.checkbox("Hiển thị so sánh Baseline", value=False)
    show_rfm = st.checkbox("Hiển thị metric RFM", value=True)
    
    st.markdown("---")
    st.info(f"📈 Tổng số cụm: {num_clusters}")
    st.info(f"👥 Tổng số khách hàng: {len(cluster_data):,}")

# ============================================
# TAB 1: THỐNG KÊ CỤM
# ============================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Thống Kê Cụm", 
    "📋 Top Rules", 
    "🎁 Bundle & Cross-sell", 
    "📈 So Sánh Cụm"
])

with tab1:
    st.header(f"Thống Kê Cụm {selected_cluster}")
    
    # Lọc dữ liệu của cụm
    cluster_customers = cluster_data[cluster_data['cluster'] == selected_cluster]
    
    # Hiển thị số liệu chính
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Số khách hàng",
            f"{len(cluster_customers):,}",
            f"{len(cluster_customers)/len(cluster_data)*100:.1f}% tổng"
        )
    
    with col2:
        if show_rfm:
            st.metric(
                "💰 Avg Monetary",
                f"${cluster_customers['Monetary'].mean():,.0f}",
                f"Range: ${cluster_customers['Monetary'].min():,.0f} - ${cluster_customers['Monetary'].max():,.0f}"
            )
    
    with col3:
        if show_rfm:
            st.metric(
                "🔄 Avg Frequency",
                f"{cluster_customers['Frequency'].mean():.1f}",
                f"Median: {cluster_customers['Frequency'].median():.0f}"
            )
    
    with col4:
        if show_rfm:
            st.metric(
                "📅 Avg Recency",
                f"{cluster_customers['Recency'].mean():.0f} ngày",
                f"Median: {cluster_customers['Recency'].median():.0f}"
            )
    
    st.markdown("---")
    
    # Biểu đồ phân phối
    col1, col2 = st.columns(2)
    
    if show_rfm:
        with col1:
            st.subheader("Phân phối Monetary (Chi tiêu)")
            fig = px.histogram(
                cluster_customers,
                x="Monetary",
                nbins=30,
                title="Phân phối chi tiêu",
                labels={"Monetary": "Tổng chi tiêu ($)"}
            )
            fig.update_xaxes(title_text="Tổng chi tiêu ($)")
            fig.update_yaxes(title_text="Số khách hàng")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Phân phối Frequency (Tần suất)")
            fig = px.histogram(
                cluster_customers,
                x="Frequency",
                nbins=20,
                title="Phân phối tần suất mua hàng",
                labels={"Frequency": "Tần suất"}
            )
            fig.update_xaxes(title_text="Tần suất mua")
            fig.update_yaxes(title_text="Số khách hàng")
            st.plotly_chart(fig, use_container_width=True)
    
    # Bảng thống kê chi tiết
    st.subheader("📋 Thống Kê Chi Tiết")
    
    stats_data = {
        "Chỉ số": [
            "Số khách hàng",
            "% tổng",
            "Chi tiêu trung bình (Monetary)",
            "Chi tiêu min/max",
            "Tần suất trung bình (Frequency)",
            "Tần suất min/max",
            "Recency trung bình (ngày)",
            "Recency min/max"
        ],
        "Giá trị": [
            f"{len(cluster_customers):,}",
            f"{len(cluster_customers)/len(cluster_data)*100:.1f}%",
            f"${cluster_customers['Monetary'].mean():,.2f}",
            f"${cluster_customers['Monetary'].min():,.2f} / ${cluster_customers['Monetary'].max():,.2f}",
            f"{cluster_customers['Frequency'].mean():.2f}",
            f"{cluster_customers['Frequency'].min():.0f} / {cluster_customers['Frequency'].max():.0f}",
            f"{cluster_customers['Recency'].mean():.1f}",
            f"{cluster_customers['Recency'].min():.0f} / {cluster_customers['Recency'].max():.0f}"
        ]
    }
    
    st.dataframe(
        pd.DataFrame(stats_data),
        use_container_width=True,
        hide_index=True
    )
    
    # So sánh với baseline nếu chọn
    if show_baseline and baseline_data is not None:
        st.markdown("---")
        st.subheader("🔄 So sánh với Baseline")
        
        baseline_cluster = baseline_data[baseline_data['cluster'] == selected_cluster]
        
        # Kiểm tra xem baseline_cluster có dữ liệu không
        if len(baseline_cluster) > 0:
            # Kiểm tra xem baseline có cột RFM không
            has_rfm = 'Monetary' in baseline_cluster.columns
            
            if has_rfm:
                # Baseline có RFM - so sánh đầy đủ
                comparison_data = {
                    "Chỉ số": ["Số khách hàng", "Avg Monetary", "Avg Frequency", "Avg Recency"],
                    "Cụm hiện tại": [
                        len(cluster_customers),
                        f"${cluster_customers['Monetary'].mean():,.2f}",
                        f"{cluster_customers['Frequency'].mean():.2f}",
                        f"{cluster_customers['Recency'].mean():.1f}"
                    ],
                    "Baseline": [
                        len(baseline_cluster),
                        f"${baseline_cluster['Monetary'].mean():,.2f}",
                        f"{baseline_cluster['Frequency'].mean():.2f}",
                        f"{baseline_cluster['Recency'].mean():.1f}"
                    ]
                }
            else:
                # Baseline không có RFM - chỉ so sánh số lượng
                comparison_data = {
                    "Chỉ số": ["Số khách hàng"],
                    "Cụm hiện tại": [len(cluster_customers)],
                    "Baseline": [len(baseline_cluster)]
                }
                st.info("ℹ️ Baseline không có dữ liệu RFM, chỉ so sánh số lượng khách")
            
            st.dataframe(
                pd.DataFrame(comparison_data),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("⚠️ Không có dữ liệu baseline cho cụm này")

# ============================================
# TAB 2: TOP RULES
# ============================================

with tab2:
    st.header(f"Top Rules Cụm {selected_cluster}")
    
    rules = load_cluster_rules(selected_cluster)
    dominant_rules = load_dominant_rules(selected_cluster)
    
    if rules is not None:
        # Tùy chọn hiển thị
        rule_options = ["Top Rules (Activation Rate)"]
        if dominant_rules is not None:
            rule_options.append("Dominant Rules (RFM)")
        
        rule_type = st.radio(
            "Chọn loại luật:",
            options=rule_options,
            horizontal=True
        )
        
        if rule_type == "Top Rules (Activation Rate)":
            display_rules = rules
            metric_col = "activation_rate"
            metric_label = "Activation Rate"
        else:
            display_rules = dominant_rules if dominant_rules is not None else rules
            metric_col = "activation_rate"
            metric_label = "Activation Rate"
        
        # Lọc số lượng rules
        num_rules = st.slider(
            "📊 Số rules hiển thị:",
            min_value=5,
            max_value=min(50, len(display_rules)),
            value=10,
            step=5
        )
        
        display_rules = display_rules.head(num_rules)
        
        # Biểu đồ activation rate
        st.subheader("📈 Biểu đồ Activation Rate")
        
        # Rút gọn tên rules để hiển thị
        display_rules_plot = display_rules.copy()
        display_rules_plot['rule_short'] = display_rules_plot['rule'].str[:60] + "..."
        
        fig = px.bar(
            display_rules_plot,
            x="activation_rate",
            y="rule_short",
            orientation="h",
            title=f"Top {num_rules} Rules - Activation Rate",
            labels={"activation_rate": "Activation Rate", "rule_short": "Luật"}
        )
        fig.update_layout(height=max(400, num_rules * 20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Bảng chi tiết
        st.subheader("📋 Chi Tiết Các Luật")
        
        # Format lại bảng hiển thị
        display_table = display_rules.copy()
        display_table.columns = [
            "Luật", "Tỷ lệ kích hoạt", "Tỷ lệ toàn cầu", "Tỷ lệ dominant"
        ]
        
        st.dataframe(display_table, use_container_width=True, hide_index=True)
        
        # Phân tích từng luật
        st.subheader("🔍 Phân Tích Chi Tiết Từng Luật")
        
        selected_rule_idx = st.selectbox(
            "Chọn luật để xem chi tiết:",
            options=range(len(display_rules)),
            format_func=lambda i: f"Luật {i+1}: {display_rules.iloc[i]['rule'][:80]}..."
        )
        
        selected_rule = display_rules.iloc[selected_rule_idx]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Activation Rate", f"{selected_rule['activation_rate']:.4f}")
        with col2:
            st.metric("Global Rate", f"{selected_rule['global_rate']:.4f}")
        with col3:
            st.metric("Dominance", f"{selected_rule['dominance']:.4f}")
        
        st.markdown("**Luật:**")
        st.code(selected_rule['rule'], language="text")
        
        # Trích xuất sản phẩm
        products = extract_products_from_rule(selected_rule['rule'])
        if products:
            st.markdown("**Sản phẩm liên quan:**")
            cols = st.columns(len(products))
            for i, product in enumerate(products):
                with cols[i]:
                    st.info(product)
    else:
        st.warning(f"⚠️ Không có dữ liệu rules cho cụm {selected_cluster}")

# ============================================
# TAB 3: BUNDLE & CROSS-SELL
# ============================================

with tab3:
    st.header(f"🎁 Gợi ý Bundle & Cross-sell Cụm {selected_cluster}")
    
    rules = load_cluster_rules(selected_cluster)
    dominant_rules = load_dominant_rules(selected_cluster)
    
    if rules is not None:
        st.markdown("""
        **Bundle & Cross-sell** là chiến lược bán hàng để:
        - **Bundle**: Bán kết hợp nhiều sản phẩm với giá giảm
        - **Cross-sell**: Gợi ý sản phẩm bổ sung khi khách mua
        """)
        
        # Phân loại loại gợi ý
        suggestion_type = st.radio(
            "Loại gợi ý:",
            options=["High Lift Rules (Cross-sell mạnh)", "High Activation (Thực tế)", "Combination (Cả hai)"],
            horizontal=True
        )
        
        if suggestion_type == "High Lift Rules (Cross-sell mạnh)":
            display_rules = rules.nlargest(15, 'activation_rate')
        elif suggestion_type == "High Activation (Thực tế)":
            display_rules = rules.head(15)
        else:
            display_rules = rules.head(20)
        
        # Tạo gợi ý bundle
        st.subheader("📦 Đề xuất Bundle")
        
        bundles = []
        for idx, row in display_rules.iterrows():
            products = extract_products_from_rule(row['rule'])
            if len(products) >= 2:
                bundles.append({
                    'Tên Bundle': f"Bundle #{len(bundles)+1}",
                    'Sản phẩm': " + ".join(products),
                    'Activation Rate': f"{row['activation_rate']:.2%}",
                    'Khuyến khích': "Cao" if row['activation_rate'] > 1.0 else "Trung bình"
                })
        
        if bundles:
            df_bundles = pd.DataFrame(bundles)
            st.dataframe(df_bundles, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Không có bundle nào được tìm thấy cho cụm này")
        
        # Tạo gợi ý cross-sell
        st.subheader("🔄 Đề xuất Cross-sell")
        
        crosssell = []
        for idx, row in display_rules.head(10).iterrows():
            antecedents, consequents = parse_rule_string(row['rule'])
            if antecedents and consequents:
                crosssell.append({
                    'Khi khách mua': antecedents,
                    'Gợi ý thêm': consequents,
                    'Tỷ lệ kích hoạt': f"{row['activation_rate']:.2%}",
                    'Ưu tiên': "🌟 Cao" if row['activation_rate'] > 1.0 else "⭐ Trung bình"
                })
        
        if crosssell:
            df_crosssell = pd.DataFrame(crosssell)
            st.dataframe(df_crosssell, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Không có gợi ý cross-sell")
        
        # Chiến lược bán hàng
        st.subheader("💡 Chiến Lược Bán Hàng Được Đề Xuất")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **1. Discount Bundle:**
            - Bán kết hợp sản phẩm có activation_rate cao
            - Tạo combo giá đặc biệt cho các sản phẩm thường được mua cùng
            
            **2. Recommendation Engine:**
            - Hiển thị "Khách khác cũng mua" trên trang sản phẩm
            - Gợi ý ở checkout: "Thêm sản phẩm này được khuyến khích"
            """)
        
        with col2:
            st.markdown("""
            **3. Email Marketing:**
            - Gửi email về sản phẩm bổ sung theo hành vi mua
            - Tạo campaign "Khám phá combo giá tốt"
            
            **4. Tối ưu hóa:**
            - A/B test các gợi ý bundle
            - Track conversion từ cross-sell
            - Điều chỉnh gợi ý theo mùa vụ
            """)

# ============================================
# TAB 4: SO SÁNH CỤM
# ============================================

with tab4:
    st.header("📈 So Sánh Các Cụm")
    
    # So sánh RFM giữa các cụm
    st.subheader("Heatmap Metric RFM theo Cụm")
    
    # Tính toán trung bình RFM cho mỗi cụm
    cluster_rfm = cluster_data.groupby('cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Normalize để dễ so sánh
    cluster_rfm_norm = (cluster_rfm - cluster_rfm.min()) / (cluster_rfm.max() - cluster_rfm.min())
    
    fig = px.imshow(
        cluster_rfm_norm.T,
        labels=dict(x="Cụm", y="Metric", color="Giá trị chuẩn hóa"),
        x=[f"Cụm {i}" for i in cluster_rfm_norm.index],
        y=["Recency (ngày)", "Frequency (lần)", "Monetary ($)"],
        color_continuous_scale="RdYlGn_r",
        aspect="auto",
        title="So sánh Metric RFM giữa các Cụm (Chuẩn hóa)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Bảng so sánh chi tiết
    st.subheader("Bảng So Sánh Các Cụm")
    
    comparison_table = pd.DataFrame({
        'Cụm': [f"Cụm {i}" for i in cluster_rfm.index],
        'Số khách': [len(cluster_data[cluster_data['cluster'] == i]) for i in cluster_rfm.index],
        'Avg Recency': [f"{cluster_rfm.loc[i, 'Recency']:.1f}" for i in cluster_rfm.index],
        'Avg Frequency': [f"{cluster_rfm.loc[i, 'Frequency']:.2f}" for i in cluster_rfm.index],
        'Avg Monetary': [f"${cluster_rfm.loc[i, 'Monetary']:,.0f}" for i in cluster_rfm.index],
    })
    
    st.dataframe(comparison_table, use_container_width=True, hide_index=True)
    
    # Biểu đồ so sánh
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            cluster_rfm.reset_index().rename(columns={'cluster': 'Cụm', 'Monetary': 'Chi tiêu'}),
            x='Cụm',
            y='Chi tiêu',
            title="So sánh Chi tiêu Trung bình",
            labels={'Cụm': 'Cụm', 'Chi tiêu': 'Avg Monetary ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            cluster_rfm.reset_index().rename(columns={'cluster': 'Cụm', 'Frequency': 'Tần suất'}),
            x='Cụm',
            y='Tần suất',
            title="So sánh Tần suất Mua",
            labels={'Cụm': 'Cụm', 'Tần suất': 'Avg Frequency'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Phân loại cụm
    st.subheader("🏆 Phân Loại Cụm Khách Hàng")
    
    cluster_profiles = []
    for cluster_id in sorted(cluster_data['cluster'].unique()):
        cluster_info = cluster_data[cluster_data['cluster'] == cluster_id]
        
        avg_monetary = cluster_info['Monetary'].mean()
        avg_frequency = cluster_info['Frequency'].mean()
        avg_recency = cluster_info['Recency'].mean()
        
        # Phân loại
        if avg_monetary > cluster_data['Monetary'].quantile(0.75):
            profile = "💎 High-value (Chi tiêu cao)"
        elif avg_frequency > cluster_data['Frequency'].quantile(0.75):
            profile = "🔄 Loyal (Mua thường xuyên)"
        elif avg_recency < cluster_data['Recency'].quantile(0.25):
            profile = "⭐ Recent (Mua gần đây)"
        else:
            profile = "📍 Standard (Bình thường)"
        
        cluster_profiles.append({
            'Cụm': f"Cụm {cluster_id}",
            'Phân loại': profile,
            'Số khách': len(cluster_info),
            'Chi tiêu': f"${avg_monetary:,.0f}",
            'Tần suất': f"{avg_frequency:.2f}",
            'Recency': f"{avg_recency:.0f}"
        })
    
    df_profiles = pd.DataFrame(cluster_profiles)
    st.dataframe(df_profiles, use_container_width=True, hide_index=True)

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
<p style='color: gray; font-size: 12px;'>
📊 Dashboard Phân Tích Cụm Khách Hàng - Online Retail Dataset<br>
Data được xử lý từ: apriori & FP-Growth association rules + KMeans clustering<br>
Last updated: 2025
</p>
</div>
""", unsafe_allow_html=True)
