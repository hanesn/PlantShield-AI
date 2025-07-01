@echo off
echo Building GUI launcher...
pyinstaller --noconfirm --onefile --windowed installer/launcher.py --distpath . --specpath installer --workpath installer/build
echo Done! Executable placed in project root