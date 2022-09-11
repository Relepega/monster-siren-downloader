@ECHO off
cd %~dp0
cd ..
pyinstaller -F --noconfirm --onefile --console --name "monster-siren-downloader" "main.py"