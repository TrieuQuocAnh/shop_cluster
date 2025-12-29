@echo off
REM -*- coding: utf-8 -*-
REM Streamlit Dashboard Startup Batch File
REM Khởi động dashboard phân tích cụm khách hàng

echo.
echo ====================================================
echo   STREAMLIT DASHBOARD - PHAN TICH CUM KHACH HANG
echo ====================================================
echo.

REM Kiểm tra Python đã cài đặt
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo [ERROR] Vui long cai dat Python tren may tinh
    pause
    exit /b 1
)

REM Kiểm tra Streamlit đã cài đặt
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Streamlit chua duoc cai dat!
    echo [INFO] Dang cai dat Streamlit...
    pip install streamlit
)

REM Chạy dashboard
echo [INFO] Khoi dong Streamlit Dashboard...
echo [INFO] URL: http://localhost:8501
echo.
echo Nhan Ctrl+C de dung server
echo.

python -m streamlit run streamlit_dashboard.py

pause
