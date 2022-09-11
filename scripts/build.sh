cd `dirname $0`
cd ..
pyinstaller -F --noconfirm --onefile --console --name "monster-siren-downloader" "main.py"