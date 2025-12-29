#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup & Validation Script for Streamlit Dashboard
Kiểm tra cấu hình và chuẩn bị chạy dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """In tiêu đề"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python():
    """Kiểm tra phiên bản Python"""
    print_header("1. Kiểm Tra Python")
    
    version_info = sys.version_info
    version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    print(f"✓ Python {version}")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 7):
        print("✗ Cần Python 3.7 hoặc cao hơn")
        return False
    return True

def check_packages():
    """Kiểm tra các package cần thiết"""
    print_header("2. Kiểm Tra Packages")
    
    required_packages = {
        'streamlit': '1.24.0',
        'pandas': '2.0.0',
        'plotly': '5.0.0',
        'numpy': '1.20.0',
    }
    
    missing_packages = []
    
    for package, min_version in required_packages.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {package} ({version})")
        except ImportError:
            print(f"✗ {package} - CHƯA CÀI ĐẶT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Các package bị thiếu: {', '.join(missing_packages)}")
        print("\n💡 Cài đặt lệnh:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_data_files():
    """Kiểm tra file dữ liệu"""
    print_header("3. Kiểm Tra File Dữ Liệu")
    
    required_files = {
        'data/processed/customer_clusters_from_rules.csv': 'Dữ liệu cụm chính',
        'data/processed/rules_fpgrowth_filtered.csv': 'Tất cả luật kết hợp',
        'data/processed/top_rules_rule/cluster_0.csv': 'Top rules cụm 0',
        'data/processed/top_rules_rule/cluster_1.csv': 'Top rules cụm 1',
        'data/processed/top_rules_rule/cluster_2.csv': 'Top rules cụm 2',
        'data/processed/top_rules_rule/cluster_3.csv': 'Top rules cụm 3',
    }
    
    optional_files = {
        'data/processed/customer_clusters_from_rules_baseline.csv': 'Dữ liệu baseline',
        'data/processed/dominant_rules_rule_rfm/cluster_0.csv': 'Dominant rules cụm 0',
        'data/processed/dominant_rules_rule_rfm/cluster_1.csv': 'Dominant rules cụm 1',
        'data/processed/dominant_rules_rule_rfm/cluster_2.csv': 'Dominant rules cụm 2',
        'data/processed/dominant_rules_rule_rfm/cluster_3.csv': 'Dominant rules cụm 3',
    }
    
    missing_required = []
    missing_optional = []
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / 1024 / 1024  # MB
            print(f"✓ {file_path} ({size:.1f} MB) - {description}")
        else:
            print(f"✗ {file_path} - {description}")
            missing_required.append(file_path)
    
    print("\nFile tùy chọn:")
    for file_path, description in optional_files.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / 1024  # KB
            if size > 0:
                print(f"✓ {file_path} ({size:.1f} KB) - {description}")
            else:
                print(f"⚠️  {file_path} (TRỐNG) - {description}")
        else:
            missing_optional.append(file_path)
    
    if missing_required:
        print(f"\n✗ LỖI: Thiếu file bắt buộc:")
        for f in missing_required:
            print(f"   - {f}")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Không có các file tùy chọn:")
        for f in missing_optional:
            print(f"   - {f}")
        print("   (Dashboard vẫn chạy nhưng một số tính năng bị hạn chế)")
    
    return True

def check_dashboard_file():
    """Kiểm tra file dashboard"""
    print_header("4. Kiểm Tra File Dashboard")
    
    if not os.path.exists('streamlit_dashboard.py'):
        print("✗ streamlit_dashboard.py - KHÔNG TÌM THẤY")
        return False
    
    print("✓ streamlit_dashboard.py tồn tại")
    
    # Kiểm tra syntax
    try:
        import py_compile
        py_compile.compile('streamlit_dashboard.py', doraise=True)
        print("✓ Syntax của streamlit_dashboard.py hợp lệ")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Lỗi syntax trong streamlit_dashboard.py:")
        print(f"   {e}")
        return False

def main():
    """Chạy tất cả các kiểm tra"""
    print("\n" + "🔧 SETUP & VALIDATION - STREAMLIT DASHBOARD".center(60))
    
    os.chdir(Path(__file__).parent)
    print(f"Thư mục làm việc: {os.getcwd()}\n")
    
    all_ok = True
    
    # Chạy các kiểm tra
    all_ok = check_python() and all_ok
    all_ok = check_packages() and all_ok
    all_ok = check_data_files() and all_ok
    all_ok = check_dashboard_file() and all_ok
    
    # Tóm tắt
    print_header("✓ KẾT LUẬN")
    
    if all_ok:
        print("✓ Tất cả kiểm tra đã vượt qua!")
        print("\n💡 Để chạy dashboard, sử dụng:")
        print("   python run_dashboard.py")
        print("   hoặc")
        print("   streamlit run streamlit_dashboard.py")
        print("\n📊 Dashboard sẽ mở tại: http://localhost:8501")
        return 0
    else:
        print("✗ Có một số vấn đề cần được sửa chữa.")
        print("\n💡 Vui lòng:")
        print("   1. Cài đặt các package bị thiếu")
        print("   2. Đảm bảo tất cả file dữ liệu tồn tại")
        print("   3. Chạy lại script này để kiểm tra")
        return 1

if __name__ == "__main__":
    sys.exit(main())
