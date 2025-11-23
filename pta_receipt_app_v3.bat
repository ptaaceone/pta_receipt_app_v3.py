

@echo off
REM pta_receipt_app_v3.py をワンクリックで起動するバッチ

REM Pythonがインストールされていることを前提
REM ファイルパスは保存場所に合わせて修正してください

cd /d "C:\Users\rk0008\Desktop\4510\a\b\c"  REM <- pta_receipt_app_v3.py のあるフォルダに変更
streamlit run pta_receipt_app_v3.py

pause
