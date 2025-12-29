#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Streamlit Dashboard Startup Script
Chạy dashboard phân tích cụm khách hàng
"""

import subprocess
import sys
import os

def main():
    # Kiểm tra Streamlit đã cài đặt
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit chưa được cài đặt!")
        print("Cài đặt Streamlit: pip install streamlit")
        sys.exit(1)
    
    # Kiểm tra file dashboard tồn tại
    if not os.path.exists("streamlit_dashboard.py"):
        print("❌ File streamlit_dashboard.py không tìm thấy!")
        print(f"Thư mục hiện tại: {os.getcwd()}")
        sys.exit(1)
    
    # Kiểm tra dữ liệu tồn tại
    required_files = [
        "data/processed/customer_clusters_from_rules.csv",
        "data/processed/rules_fpgrowth_filtered.csv",
        "data/processed/top_rules_rule/cluster_0.csv",
        "data/processed/dominant_rules_rule_rfm/cluster_0.csv"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("⚠️  Một số file dữ liệu không tìm thấy:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nDashboard vẫn sẽ chạy nhưng một số tính năng có thể không khả dụng.")
    
    print("\n🚀 Khởi động Streamlit Dashboard...")
    print("📊 URL: http://localhost:8501")
    print("\nNhấn Ctrl+C để dừng server\n")
    
    # Chạy Streamlit
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_dashboard.py"],
        env={**os.environ, "STREAMLIT_LOGGER_LEVEL": "error"}
    )

if __name__ == "__main__":
    main()
