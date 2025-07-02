import zipfile
import os
from pathlib import Path
from datetime import datetime

# Config
ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
DIST_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
OUTPUT_ZIP = DIST_DIR / f"tomato_classifier_{timestamp}.zip"

# Directories and files to skip entirely
EXCLUDED_DIRS = {
    ".git", "__pycache__", ".idea", "node_modules", ".venv",
    "dist", "installer/build", "installer/__pycache__",
    ".pytest_cache", ".mypy_cache", ".ipynb_checkpoints", "build",
}

EXCLUDED_FILES = {
    ".env", "app.log", "launcher.exe", "launcher.spec"
}

def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True
    if path.name in EXCLUDED_FILES:
        return True
    return False

# Zip it!
with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
    for filepath in ROOT_DIR.rglob("*"):
        if filepath.is_file() and not is_excluded(filepath.relative_to(ROOT_DIR)):
            try:
                zipf.write(filepath, filepath.relative_to(ROOT_DIR))
            except Exception as e:
                print(f"[SKIP] {filepath}: {e}")

print(f"\nProject zipped successfully: {OUTPUT_ZIP}")