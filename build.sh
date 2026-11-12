python3 -m venv .venv
source .venv/Scripts/activate

pip install nuitka zstandard pygame
python -m nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=res/tomato.ico --include-data-dir=res=res --assume-yes-for-downloads main.py

for d in main.build main.onefile-build main.dist; do rm -rf "$d"; done
mv main Pomodoro