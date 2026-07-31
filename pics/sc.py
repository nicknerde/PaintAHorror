from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

for file in sorted(SCRIPT_DIR.iterdir()):
    if file.is_file():
        print(file.name)