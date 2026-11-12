python -m venv .venv
call .venv/Scripts/activate.bat

pip install nuitka zstandard
python -m nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=res/tomato.ico --assume-yes-for-downloads main.py

for %%D in (main.build main.onefile-build main.dist) do rmdir /s /q "%%D"
move /y main.exe pomodoro.exe